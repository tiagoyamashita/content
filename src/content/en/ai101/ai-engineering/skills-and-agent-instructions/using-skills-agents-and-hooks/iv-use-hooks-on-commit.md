---
label: "IV"
subtitle: "Hooks on commit"
group: "Using skills, agents & hooks"
order: 4
---
Hooks on commit

**Hooks** run on **events** — before the agent or user runs `git commit`, after a file edit, on session start, etc. The user does **not** need to ask. The product invokes your script or prompt hook.

## What a hook is not

| Hook is not… | Why |
|--------------|-----|
| A skill | Skills need user intent; hooks are automatic |
| `AGENTS.md` | Briefing is passive; hooks **gate or modify** actions |
| A replacement for CI | Hooks are local/dev-time; CI still runs on push |

## Commit hook flow

```text
User or agent types: git commit -m "..."
  → beforeShellExecution hook fires
  → secrets_scan.py reads stdin JSON
  → scans staged files
  → writes log to .cursor/hooks/logs/
  → stdout: { "permission": "allow" | "deny" }
  → exit 2 → commit blocked (if failClosed)
```

**Agent is not in the loop** unless the commit is blocked and the user asks why.

## Live files

| Piece | Path |
|-------|------|
| Hook config | [Examples: `.cursor/hooks.json`](../examples/.cursor/hooks.json) |
| Hook script | [Examples: `.cursor/hooks/secrets_scan.py`](../examples/.cursor/hooks/secrets_scan.py) |
| Scan logic | [Examples: `.cursor/hooks/lib/`](../examples/.cursor/hooks/lib/) |
| Sample config (minimal) | [sample/.cursor/hooks.json](sample/.cursor/hooks.json) |

Copy the full [examples/.cursor/](../examples/.cursor/README.md) tree for a working secrets gate.

### `hooks.json` (commit gate)

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "python3 .cursor/hooks/secrets_scan.py",
        "matcher": "git\\s+commit",
        "timeout": 30,
        "failClosed": true
      }
    ]
  }
}
```

| Field | Meaning |
|-------|---------|
| `beforeShellExecution` | Run before terminal runs the command |
| `matcher` | JS regex on full shell string |
| `failClosed` | Block commit if hook crashes or times out |

## Hook without skill

```text
git commit
  → hook runs
  → pass → commit proceeds (agent may never know hook ran)
  → fail → shell blocked; user sees user_message from hook JSON
```

## Hook + companion skill (recommended)

Hooks should stay **small and deterministic**. Put **explanation and remediation** in a skill:

| Layer | Job |
|-------|-----|
| Hook | Block + write log |
| Skill `secrets-scan-help` | Explain log, suggest `git reset`, rotation |

See [Examples: secrets-scan-help](../examples/.cursor/skills/secrets-scan-help/SKILL.md).

## git pre-commit (outside Cursor)

Same scan logic can run in `.git/hooks/pre-commit` for teammates without Cursor — see [Examples: hook doc](../examples/iv-hook-secrets-env-scan.md).

## Test hook manually

```bash
echo '{"command":"git commit -m test"}' | python3 .cursor/hooks/secrets_scan.py
```

Stage a `.env` file first to see `permission: deny`.

## Next

[Combine all three](v-combine-skills-agents-hooks.md) — how `AGENTS.md`, skills, and hooks work together on a real commit.
