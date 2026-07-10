---
label: "II"
subtitle: "Parameterized script + clarify"
group: "Skills examples"
order: 2
---
Parameterized script + clarify

**Goal:** Run a script with **parameters** (`environment`, `dry_run`, etc.). If the user did not supply enough info, the agent **asks** for missing values and **confirms intent** before executing. The script **logs** runtime and results to JSON.

## Folder layout

```text
.cursor/skills/deploy-check/
  SKILL.md
  scripts/
    deploy-check.sh
  logs/                    ← gitignore; created at runtime
    run-20260710T120301Z.json
```

## Script — `scripts/deploy-check.sh`

Accepts CLI flags; always writes a log file.

```bash
#!/usr/bin/env bash
# .cursor/skills/deploy-check/scripts/deploy-check.sh
set -euo pipefail

ENVIRONMENT=""
DRY_RUN="false"
LOG_DIR="$(dirname "$0")/../logs"
mkdir -p "$LOG_DIR"

usage() {
  echo "Usage: $0 --environment staging|production [--dry-run]"
  exit 2
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --environment) ENVIRONMENT="$2"; shift 2 ;;
    --dry-run) DRY_RUN="true"; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown arg: $1"; usage ;;
  esac
done

[[ -z "$ENVIRONMENT" ]] && usage

STARTED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
START_MS="$(date +%s%3N)"

# --- checks (replace with your real logic) ---
MESSAGES=()
FAILURES=0
if [[ "$ENVIRONMENT" == "production" && "$DRY_RUN" != "true" ]]; then
  MESSAGES+=("WARN: production deploy without dry-run")
fi
curl -fsS "${STAGING_URL:-https://staging.example.com}/health" >/dev/null \
  && MESSAGES+=("Health OK") || { MESSAGES+=("Health FAILED"); FAILURES=$((FAILURES+1)); }
# --- end checks ---

END_MS="$(date +%s%3N)"
FINISHED_AT="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DURATION_MS=$((END_MS - START_MS))
EXIT_CODE=$FAILURES

LOG_FILE="$LOG_DIR/run-$(date -u +%Y%m%dT%H%M%SZ).json"
cat >"$LOG_FILE" <<EOF
{
  "script": "deploy-check.sh",
  "started_at": "$STARTED_AT",
  "finished_at": "$FINISHED_AT",
  "duration_ms": $DURATION_MS,
  "exit_code": $EXIT_CODE,
  "parameters": { "environment": "$ENVIRONMENT", "dry_run": $DRY_RUN },
  "results": { "checks_failed": $FAILURES },
  "messages": $(printf '%s\n' "${MESSAGES[@]}" | jq -R . | jq -s .),
  "log_file": "$LOG_FILE"
}
EOF

echo "Log written: $LOG_FILE"
cat "$LOG_FILE"
exit $EXIT_CODE
```

```bash
chmod +x .cursor/skills/deploy-check/scripts/deploy-check.sh
```

Requires `jq` for JSON array formatting (or simplify `messages` to a plain string).

## SKILL.md — parameters, clarify, then run

```markdown
---
name: deploy-check
description: Run deploy preflight checks for staging or production. Use when user asks to verify deploy readiness, run deploy-check, or check staging before release.
---

# Deploy check

## Before running the script

1. **Required parameter:** `environment` — `staging` or `production`.
2. **Optional:** `dry_run` — default `true` for production unless user explicitly wants live deploy.

### If parameters are missing

Do **not** guess. Ask the user:

- "Which environment — **staging** or **production**?"
- "Dry run only (**yes**/no)? Production defaults to dry-run unless you confirm otherwise."

### Confirm intent (required)

Restate what you will run and wait for confirmation:

> I will run:
> `.cursor/skills/deploy-check/scripts/deploy-check.sh --environment staging --dry-run`
> Proceed? (yes/no)

Only run after **yes** or an unambiguous command ("run it", "go ahead").

## Run

```bash
.cursor/skills/deploy-check/scripts/deploy-check.sh \
  --environment <staging|production> \
  [--dry-run]
```

## After run

1. Read the **JSON log** path printed by the script (under `logs/`).
2. Summarize: `duration_ms`, `exit_code`, `messages`.
3. If `exit_code` != 0, list failures and **do not** claim deploy is ready.

## Do not

- Run without `environment`
- Skip intent confirmation on **production**
- Invent health-check logic inline — use the script only
```

## Agent flow

```text
User: "check if we're ready to deploy"
  → Skill loads
  → Agent: missing environment → asks user
  → Agent: restates command → user confirms
  → Agent runs script via Shell
  → Script writes logs/run-….json
  → Agent reads log → reports results
```

## Test

Fresh chat: *"run deploy check"* — agent should ask for environment before running.

## Next

[Loop on script results](iii-loop-on-script-results.md) — reuse log data across iterations.
