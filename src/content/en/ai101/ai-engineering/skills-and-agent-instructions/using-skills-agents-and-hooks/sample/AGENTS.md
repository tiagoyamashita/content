# Agent briefing — this repo

Short facts every agent session should know. Procedures live in `.cursor/skills/`.

## Stack

- Content / markdown repo (educational notes)
- Python 3.10+ for example scripts under `.cursor/skills/`

## Commands

| Task | Command |
|------|---------|
| Smoke test deploy skill | `python3 .cursor/skills/deploy-check/scripts/deploy_check.py --environment staging --dry-run` |
| Run tests (if package exists) | `npm test` |

## Layout

```text
src/content/en/     ← English notes
.cursor/skills/     ← on-demand workflows (user asks)
.cursor/hooks/      ← automatic commit gates
AGENTS.md           ← this file (always loaded)
```

## Skills (on demand)

| Skill | When |
|-------|------|
| `pr-review-lite` | User asks for PR / code review |
| `deploy-check` | User asks about deploy readiness |
| `secrets-scan-help` | Commit blocked by secrets hook |
| `hook-failure-help` | User asks why a hook blocked an action |

## Hooks (automatic)

- **`beforeShellExecution`** on `git commit` → `.cursor/hooks/secrets_scan.py` blocks staged `.env` and obvious secrets.
- Hooks run **without** user prompt. Use `secrets-scan-help` skill to explain failures.

## Conventions

- Do not commit `.cursor/skills/*/logs/` or `.cursor/hooks/logs/`
- Do not put real API keys in markdown — use placeholders
