---
label: "V"
subtitle: "Performance & bottlenecks"
group: "Skills examples"
order: 5
---
Performance & bottlenecks

**Goal:** A **skill-triggered** bot that scans for **performance issues** — slow tests, large bundles, N+1 patterns (heuristic), hot paths — and logs **runtime + findings** for the agent to summarize and suggest fixes.

## Folder layout

```text
.cursor/skills/perf-scan/
  SKILL.md
  scripts/
    perf-scan.sh
  logs/
    run-20260710T160512Z.json
```

## Script — `scripts/perf-scan.sh`

```bash
#!/usr/bin/env bash
# .cursor/skills/perf-scan/scripts/perf-scan.sh
set -euo pipefail

TARGET_PATH="${1:-.}"
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
START_MS="$(date +%s%3N)"
FINDINGS=()

add() { FINDINGS+=("$1"); }

# --- 1) Slow test files (if jest/vitest report exists) ---
if [[ -f coverage/coverage-summary.json ]] || [[ -d .vitest ]]; then
  : # plug in: parse last test timing report
fi

# --- 2) Large JS/TS files (>500 lines) — quick smell ---
while IFS= read -r f; do
  lines=$(wc -l <"$f")
  [[ "$lines" -gt 500 ]] && add "LARGE_FILE: $f ($lines lines)"
done < <(find "$TARGET_PATH" -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.js' \) \
  ! -path '*/node_modules/*' ! -path '*/.next/*' ! -path '*/dist/*' 2>/dev/null | head -200)

# --- 3) Obvious sync blocking in hot paths (heuristic grep) ---
while IFS= read -r hit; do
  [[ -n "$hit" ]] && add "SYNC_IO_CANDIDATE: $hit"
done < <(grep -rnE 'readFileSync|writeFileSync|execSync' \
  --include='*.ts' --include='*.js' "$TARGET_PATH" 2>/dev/null \
  | grep -v node_modules | head -20 || true)

# --- 4) Optional: run bundler analyze if script exists ---
if npm run -s analyze 2>/dev/null; then
  add "BUNDLE_ANALYZE: npm run analyze completed — check report"
fi

# --- 5) Optional: timing a smoke endpoint ---
if [[ -n "${PERF_URL:-}" ]]; then
  CURL_MS=$(curl -o /dev/null -s -w '%{time_total}' "$PERF_URL" || echo "fail")
  add "HTTP_TIMING: $PERF_URL total=${CURL_MS}s"
fi

END_MS="$(date +%s%3N)"
FINISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DURATION_MS=$((END_MS - START_MS))

LOG_FILE="$LOG_DIR/run-$(date -u +%Y%m%dT%H%M%SZ).json"
FINDINGS_JSON=$(printf '%s\n' "${FINDINGS[@]:-}" | sed '/^$/d' | jq -R . | jq -s .)
COUNT=${#FINDINGS[@]}

cat >"$LOG_FILE" <<EOF
{
  "script": "perf-scan.sh",
  "started_at": "$STARTED_AT",
  "finished_at": "$FINISHED_AT",
  "duration_ms": $DURATION_MS,
  "exit_code": 0,
  "parameters": { "target_path": "$TARGET_PATH", "perf_url": "${PERF_URL:-}" },
  "results": {
    "findings_count": $COUNT,
    "severity_hint": "$([[ $COUNT -gt 10 ]] && echo high || echo medium)"
  },
  "messages": $FINDINGS_JSON,
  "log_file": "$LOG_FILE"
}
EOF

echo "Log written: $LOG_FILE"
cat "$LOG_FILE"
```

```bash
chmod +x .cursor/skills/perf-scan/scripts/perf-scan.sh
```

Extend with your stack: Lighthouse CI, `clinic doctor`, Python `cProfile`, DB slow-query logs.

## SKILL.md

```markdown
---
name: perf-scan
description: Scan codebase for performance smells, large files, sync I/O, and bottlenecks. Use when user asks about performance, slow app, optimization, or profiling.
---

# Performance scan

## Before running

Ask if missing:

- **Scope:** whole repo `.` or path (e.g. `src/api/`)?
- **Runtime check:** optional URL for `PERF_URL` smoke timing?

Confirm:

> I will run perf-scan on `<path>` and summarize findings from the JSON log. Proceed?

## Run

```bash
PERF_URL="${PERF_URL:-}" .cursor/skills/perf-scan/scripts/perf-scan.sh "<path>"
```

## After run

1. Open the log file path from script output.
2. Group findings: **large files**, **sync I/O**, **HTTP timing**, **bundle**.
3. Prioritize top 3 by likely user impact — not every grep hit needs a fix.
4. For each: suggest **one** concrete change (async I/O, split module, cache, index).

## Loop (optional)

After user applies a fix, re-run the **same path** and compare `findings_count` and `duration_ms` to the previous log. Keep both log paths in the reply.

## Do not

- Claim production metrics without data — this is a **static/heuristic** scan
- Run load tests against prod URLs without explicit user approval
```

## Combine with loop example

Use [Loop on script results](iii-loop-on-script-results.md): first log = baseline, re-run after fixes, compare `messages` arrays.

## Related

- [Parameterized script + clarify](ii-parameterized-script-clarify.md)
- [Implementation examples — Ollama](../../ollama/i-overview.md) — not perf, but local tooling pattern
