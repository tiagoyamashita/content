---
label: "IV"
subtitle: "Hook — secrets & env scan"
group: "Skills examples"
order: 4
---
Hook — secrets & `.env` scan

**Goal:** A **bot** that runs on **hooks** — before `git commit` or before shell runs `git commit` — and scans for exposed secrets, `.env` files staged, API keys in diffs. Writes a **log**; can **block** the action when `failClosed` is set.

Hooks run **automatically**; skills run when the user asks. See [Linking a fixed script](../../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script).

## Folder layout

```text
.cursor/
  hooks.json
  hooks/
    secrets-scan.sh
    logs/
      secrets-scan-20260710T150001Z.json
```

Add to `.gitignore`:

```gitignore
.cursor/hooks/logs/
.cursor/skills/*/logs/
```

## Hook config — `.cursor/hooks.json`

Run before shell executes `git commit` (and optionally after edits):

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": ".cursor/hooks/secrets-scan.sh",
        "matcher": "git\\s+commit",
        "timeout": 30,
        "failClosed": true
      }
    ]
  }
}
```

| Event | When it fires |
|-------|----------------|
| `beforeShellExecution` + matcher `git\s+commit` | User/agent tries to commit (JS regex — escape backslashes in JSON) |

The script also filters on `git commit` internally so you can omit the matcher while testing.

## Script — `.cursor/hooks/secrets-scan.sh`

`beforeShellExecution` hooks receive JSON on **stdin** and return JSON on **stdout** (`permission`: `allow` | `deny`). This wrapper runs the scan, writes a log, and blocks commits when findings exist.

```bash
#!/usr/bin/env bash
# .cursor/hooks/secrets-scan.sh
set -euo pipefail

INPUT="$(cat)"
COMMAND="$(printf '%s' "$INPUT" | jq -r '.command // empty')"
LOG_DIR="$(dirname "$0")/logs"
mkdir -p "$LOG_DIR"

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
START_MS="$(date +%s%3N)"
FINDINGS=()
BLOCK=0

add_finding() {
  FINDINGS+=("$1")
  BLOCK=1
}

# Only scan on git commit (script-side filter — matcher optional)
if [[ ! "$COMMAND" =~ git[[:space:]]+commit ]]; then
  echo '{ "permission": "allow" }'
  exit 0
fi

# 1) Staged .env files
while IFS= read -r -d '' f; do
  add_finding "STAGED_ENV_FILE: $f"
done < <(git diff --cached --name-only -z 2>/dev/null | grep -zE '\.env$|\.env\.' || true)

# 2) Obvious secret patterns in staged diff
if git diff --cached -U0 2>/dev/null | grep -qiE \
  '(api[_-]?key|secret|password|private[_-]?key)\s*[:=]\s*['\''"][a-zA-Z0-9_\-]{8,}'; then
  add_finding "POSSIBLE_SECRET_IN_STAGED_DIFF"
fi

# 3) .env committed in this commit
if git diff --cached --name-only 2>/dev/null | grep -qE '^\.env$'; then
  add_finding "DOT_ENV_IN_COMMIT"
fi

END_MS="$(date +%s%3N)"
FINISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DURATION_MS=$((END_MS - START_MS))

LOG_FILE="$LOG_DIR/secrets-scan-$(date -u +%Y%m%dT%H%M%SZ).json"
FINDINGS_JSON=$(printf '%s\n' "${FINDINGS[@]:-}" | sed '/^$/d' | jq -R . | jq -s .)

cat >"$LOG_FILE" <<EOF
{
  "script": "secrets-scan.sh",
  "command": $(printf '%s' "$COMMAND" | jq -Rs .),
  "started_at": "$STARTED_AT",
  "finished_at": "$FINISHED_AT",
  "duration_ms": $DURATION_MS,
  "exit_code": $BLOCK,
  "results": { "findings_count": ${#FINDINGS[@]}, "blocked": $([[ $BLOCK -eq 1 ]] && echo true || echo false) },
  "messages": $FINDINGS_JSON,
  "log_file": "$LOG_FILE"
}
EOF

if [[ $BLOCK -eq 1 ]]; then
  MSG=$(printf '%s; ' "${FINDINGS[@]}" | sed 's/; $//')
  jq -n \
    --arg msg "$MSG" \
    --arg log "$LOG_FILE" \
    '{
      "permission": "deny",
      "user_message": ("Commit blocked — secrets scan failed. See " + $log),
      "agent_message": ("Fix before commit: " + $msg)
    }'
  exit 2
fi

echo '{ "permission": "allow", "agent_message": "Secrets scan passed." }'
exit 0
```

```bash
chmod +x .cursor/hooks/secrets-scan.sh
```

## Optional: git pre-commit (runs outside Cursor too)

Extract scan logic to `.cursor/hooks/lib/scan-staged-secrets.sh` and call it from both the hook and git:

```bash
# .git/hooks/pre-commit (or use pre-commit framework)
#!/bin/sh
exec .cursor/hooks/lib/scan-staged-secrets.sh
```

Team members get the gate even without Cursor.

## SKILL.md companion (optional)

For when the agent should **explain** a blocked commit:

```markdown
---
name: secrets-scan-help
description: Explain secrets-scan hook failures and how to fix staged .env or leaked keys. Use when commit blocked, secrets scan failed, or .env staged.
---

# Secrets scan failures

1. Read latest log in `.cursor/hooks/logs/secrets-scan-*.json`.
2. For `STAGED_ENV_FILE`: unstage with `git reset HEAD -- <file>`; ensure `.env` is in `.gitignore`.
3. For `POSSIBLE_SECRET_IN_STAGED_DIFF`: rotate the secret; remove from code; use env vars.
4. Never tell the user to commit secrets to "fix" the hook.
```

## Agent / user flow

```text
User or agent: git commit -m "…"
  → beforeShellExecution fires
  → secrets-scan.sh runs → writes log
  → exit 1 → commit blocked (if failClosed)
  → Agent reads log → suggests fixes
```

## Next

[Performance & bottlenecks](v-performance-bottleneck-scan.md) — on-demand profiling skill.
