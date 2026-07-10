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
    lib/
      run_log.py          ← shared helper (see overview)
    deploy_check.py
  logs/                    ← gitignore; created at runtime
    run-20260710T120301Z.json
```

## Script — `scripts/deploy_check.py`

```python
#!/usr/bin/env python3
"""Deploy preflight checks — writes JSON log under ../logs/."""
from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from lib.run_log import Timer, log_path, write_log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy preflight checks")
    parser.add_argument(
        "--environment",
        required=True,
        choices=("staging", "production"),
        help="Target environment",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deploy (recommended for production)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    timer = Timer()
    messages: list[str] = []
    failures = 0

    if args.environment == "production" and not args.dry_run:
        messages.append("WARN: production deploy without dry-run")

    url = os.environ.get("STAGING_URL", "https://staging.example.com/health")
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if 200 <= resp.status < 300:
                messages.append("Health OK")
            else:
                messages.append(f"Health FAILED: HTTP {resp.status}")
                failures += 1
    except (urllib.error.URLError, TimeoutError) as exc:
        messages.append(f"Health FAILED: {exc}")
        failures += 1

    log_file = log_path(log_dir)
    write_log(
        log_file,
        script="deploy_check.py",
        started_at=timer.started_at,
        duration_ms=timer.duration_ms,
        exit_code=failures,
        parameters={"environment": args.environment, "dry_run": args.dry_run},
        results={"checks_failed": failures},
        messages=messages,
    )
    return failures


if __name__ == "__main__":
    sys.exit(main())
```

```bash
chmod +x .cursor/skills/deploy-check/scripts/deploy_check.py
```

Copy `run_log.py` from [Examples overview](i-overview.md#shared-logging-helper-optional).

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
> `python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run`
> Proceed? (yes/no)

Only run after **yes** or an unambiguous command ("run it", "go ahead").

## Run

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py \
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
