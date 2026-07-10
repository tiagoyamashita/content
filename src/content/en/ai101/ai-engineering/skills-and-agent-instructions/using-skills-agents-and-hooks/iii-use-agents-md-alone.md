---
label: "III"
subtitle: "AGENTS.md alone"
group: "Using skills, agents & hooks"
order: 3
---
AGENTS.md alone

**`AGENTS.md`** at the **repo root** is the agent’s standing briefing. It loads **automatically** at session start — no trigger phrase, no hook, no skill folder.

## What AGENTS.md is not

| AGENTS.md is not… | Use instead |
|-------------------|-------------|
| A long workflow | Skill in `.cursor/skills/` |
| A commit gate | Hook in `.cursor/hooks.json` |
| Secret or env values | Env vars; reference names only |

Keep it **short** (one screen). Link out to skills for deep workflows.

## Sample file (copy-ready)

Live file: [sample/AGENTS.md](sample/AGENTS.md)

Copy to **your repo root** as `AGENTS.md` (not inside `.cursor/`).

### Typical sections

| Section | Purpose |
|---------|---------|
| **Stack** | Language, framework, package manager |
| **Commands** | `npm test`, `npm run lint`, build |
| **Layout** | Where source, tests, docs live |
| **Skills index** | Table linking to `.cursor/skills/*/SKILL.md` |
| **Hooks note** | One line: “Commits gated by secrets scan” |

## Agent-only flow (no skill, no hook)

```text
User opens repo in Cursor
  → AGENTS.md injected into context
  → User: "add a unit test for auth"
  → Agent uses npm test path from AGENTS.md
  → (no skill unless user asks for PR review, etc.)
```

The agent **does not** run hooks or skills until the user’s task or an event triggers them.

## AGENTS.md vs skill `description`

| | AGENTS.md | Skill |
|---|-----------|-------|
| **Loads** | Every chat | On match |
| **Content** | Facts about repo | Procedure for one job |
| **Example** | “Tests: `npm test`” | “How to review a PR step by step” |

Put **facts** in `AGENTS.md`. Put **procedures** in skills.

## Test

1. Copy [sample/AGENTS.md](sample/AGENTS.md) → repo root
2. Fresh chat: *“how do I run tests?”*
3. Agent should answer with the command from `AGENTS.md` without you pasting it

## Next

[Hooks on commit](iv-use-hooks-on-commit.md) — automatic behavior **without** user asking.
