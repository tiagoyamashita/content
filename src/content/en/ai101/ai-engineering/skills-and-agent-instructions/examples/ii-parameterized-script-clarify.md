---
label: "II"
subtitle: "Parameterized script + clarify"
group: "Skills examples"
order: 2
---
Parameterized script + clarify

**Goal:** Run a script with **parameters** (`environment`, `dry_run`, etc.). If the user did not supply enough info, the agent **asks** for missing values and **confirms intent** before executing. The script **logs** runtime and results to JSON.

## Live files (copy-ready)

| File | Path |
|------|------|
| Skill instructions | [`.cursor/skills/deploy-check/SKILL.md`](.cursor/skills/deploy-check/SKILL.md) |
| Script | [`.cursor/skills/deploy-check/scripts/deploy_check.py`](.cursor/skills/deploy-check/scripts/deploy_check.py) |
| Logging helper | [`.cursor/skills/deploy-check/scripts/lib/run_log.py`](.cursor/skills/deploy-check/scripts/lib/run_log.py) |

Copy all of [`.cursor/`](.cursor/README.md) to your project — paths already use `.cursor/skills/...`.

## Folder layout

```text
.cursor/skills/deploy-check/
  SKILL.md
  scripts/
    lib/run_log.py
    deploy_check.py
  logs/                    ← gitignore; created at runtime
```

## What the skill teaches the agent

From [`SKILL.md`](.cursor/skills/deploy-check/SKILL.md):

1. **Ask** if `environment` is missing (`staging` | `production`).
2. **Confirm** before run — especially for production.
3. **Run** `python3 .cursor/skills/deploy-check/scripts/deploy_check.py …`
4. **Read** the JSON log under `logs/` and summarize `duration_ms`, `exit_code`, `messages`.

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

After copy to your project:

```bash
python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run
```

Fresh agent chat: *"run deploy check"* — agent should ask for environment before running.

## Next

[Loop on script results](iii-loop-on-script-results.md) — reuse log data across iterations.
