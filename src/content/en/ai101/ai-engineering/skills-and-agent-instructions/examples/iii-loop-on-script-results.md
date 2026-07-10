---
label: "III"
subtitle: "Loop on script results"
group: "Skills examples"
order: 3
---
Loop on script results

**Goal:** Run a script, read its **log file**, and **iterate** on the same data — refine fixes or analysis without re-fetching from scratch each time. Keeps `last_log_file` in the conversation as the source of truth.

## Folder layout

```text
.cursor/skills/test-flake-hunt/
  SKILL.md
  scripts/
    run-flaky-tests.sh
  logs/
    run-20260710T143022Z.json
```

## Script — `scripts/run-flaky-tests.sh`

Runs tests (or a subset); logs structured output for the agent to loop on.

```bash
#!/usr/bin/env bash
# .cursor/skills/test-flake-hunt/scripts/run-flaky-tests.sh
set -euo pipefail

PATTERN="${1:-}"
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
START_MS="$(date +%s%3N)"

# Example: run tests matching pattern (adjust to your runner)
if [[ -n "$PATTERN" ]]; then
  TEST_CMD=(npm test -- --testPathPattern="$PATTERN")
else
  TEST_CMD=(npm test)
fi

set +e
OUTPUT="$("${TEST_CMD[@]}" 2>&1)"
EXIT_CODE=$?
set -e

END_MS="$(date +%s%3N)"
FINISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DURATION_MS=$((END_MS - START_MS))

LOG_FILE="$LOG_DIR/run-$(date -u +%Y%m%dT%H%M%SZ).json"
# Escape output for JSON (minimal — use jq -Rs for production)
OUTPUT_JSON=$(printf '%s' "$OUTPUT" | jq -Rs .)

cat >"$LOG_FILE" <<EOF
{
  "script": "run-flaky-tests.sh",
  "started_at": "$STARTED_AT",
  "finished_at": "$FINISHED_AT",
  "duration_ms": $DURATION_MS,
  "exit_code": $EXIT_CODE,
  "parameters": { "pattern": "$PATTERN" },
  "results": {
    "command": "${TEST_CMD[*]}",
    "output_excerpt": $OUTPUT_JSON
  },
  "log_file": "$LOG_FILE"
}
EOF

echo "Log written: $LOG_FILE"
echo "exit_code=$EXIT_CODE"
tail -n 40 <<<"$OUTPUT"
exit $EXIT_CODE
```

## SKILL.md — loop on the same log

```markdown
---
name: test-flake-hunt
description: Run tests, analyze failures from log files, and iterate fixes. Use when user mentions flaky tests, failing CI, or re-run tests after a fix.
---

# Test flake hunt (loop on results)

## Iteration loop (max 5 rounds)

Keep **`current_log_file`** — path from the latest script run. Do not discard prior log content until the user starts a new hunt.

### Round 1 — run

```bash
.cursor/skills/test-flake-hunt/scripts/run-flaky-tests.sh "[optional-test-pattern]"
```

Record `current_log_file` from script output (e.g. `logs/run-20260710T143022Z.json`).

### Round 2+ — refine (same data)

1. **Read** `current_log_file` (do not re-run tests yet if analyzing the same failure).
2. Parse `exit_code`, `results.output_excerpt`, `duration_ms`.
3. Propose a **specific fix** (file + line if visible in output).
4. After user approves edit OR you apply a fix, ask: **"Re-run tests?"**
5. Only re-run script when verifying a fix → new log becomes `current_log_file`.

### Stop when

- `exit_code` is 0, or
- User says stop, or
- 5 iterations without progress → summarize blockers from **last log**

## Output format each round

```markdown
## Iteration N
- **Log:** `logs/run-….json`
- **Duration:** … ms | **Exit:** …
- **Finding:** …
- **Next:** fix X / re-run / ask user
```

## Do not

- Re-run full suite every message without reading the existing log
- Lose the log path between turns — cite `current_log_file` in each reply
```

## Optional: Cursor `stop` hook for follow-up

For **automatic** “keep going” loops (agent continues after stop), use a `stop` hook with `loop_limit` in `.cursor/hooks.json` — see [Hook — secrets scan](iv-hook-secrets-env-scan.md) for hook layout. Skills alone rely on the **agent following the loop** in `SKILL.md`; hooks enforce automation.

## Tie-in: loop prompting

Store this skill once; each chat turn is a **short delta** (“iteration 3: read last log, fix `auth.test.ts`”) — see [Loop prompting](../../loop-prompting/i-overview.md).

## Next

[Hook — secrets & `.env` scan](iv-hook-secrets-env-scan.md) — automatic checks without user asking.
