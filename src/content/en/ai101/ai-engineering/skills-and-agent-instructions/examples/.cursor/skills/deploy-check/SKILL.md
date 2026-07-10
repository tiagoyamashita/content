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
> `python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run`
> Proceed? (yes/no)

Only run after **yes** or an unambiguous command ("run it", "go ahead").

## Run

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py \
  --environment <staging|production> \
  [--dry-run]
```

Set `STAGING_URL` to your health-check endpoint for a **live** check. With `--dry-run` and no `STAGING_URL`, the script skips the HTTP call and exits 0.

## After run

1. Read the **JSON log** path printed by the script (under `.cursor/skills/deploy-check/logs/`).
2. Summarize: `duration_ms`, `exit_code`, `messages`.
3. If `exit_code` != 0, list failures and **do not** claim deploy is ready.

## Do not

- Run without `environment`
- Skip intent confirmation on **production**
- Invent health-check logic inline — use the script only
