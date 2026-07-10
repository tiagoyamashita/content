---
label: "I"
subtitle: "Overview"
group: "Using skills, agents & hooks"
order: 1
---
Using skills, agents & hooks — overview

Three different layers — **do not merge them into one file**. Each has its own trigger and job.

| Layer | File(s) | When it runs | Who starts it |
|-------|---------|--------------|---------------|
| **Agent briefing** | `AGENTS.md` (repo root) | Every agent session in this repo | Cursor / Claude Code automatically |
| **Skill** | `.cursor/skills/<name>/SKILL.md` | When user prompt matches `description` | **User** (or explicit skill invoke) |
| **Hook** | `.cursor/hooks.json` + `.cursor/hooks/*` | On events: shell, commit, edit, stop | **Product** — no user prompt |

```text
                    ┌─────────────────────────────────────┐
                    │  AGENTS.md — always-on briefing      │
                    │  stack, tests, folder map, skill index │
                    └─────────────────┬───────────────────┘
                                      │ every chat
                                      ▼
User: "review this PR" ──────► SKILL loads ──────► agent follows workflow
                                      │
User: "git commit" ────────────► HOOK runs first ──► allow / deny shell
                                      │ blocked?
                                      ▼
User: "why did commit fail?" ► SKILL (hook-failure-help) explains log
```

## Map of this submenu

| Note | Focus |
|------|--------|
| [Skills alone](ii-use-skills-alone.md) | On-demand workflows — user asks, skill loads |
| [AGENTS.md alone](iii-use-agents-md-alone.md) | Standing repo context — no trigger phrase needed |
| [Hooks on commit](iv-use-hooks-on-commit.md) | Automatic gates before `git commit` |
| [Combine all three](v-combine-skills-agents-hooks.md) | End-to-end commit flow + when to use which |

**Runnable scripts + full hook implementation:** [Examples](../examples/i-overview.md) (copy `examples/.cursor/` to your project).

**Sample files to copy:** [sample/.cursor/](sample/.cursor/README.md) — minimal `AGENTS.md`, skills, and `hooks.json` layout.

## Quick picker

| You want… | Use | Not |
|-----------|-----|-----|
| “Always know our test command” | `AGENTS.md` | Skill |
| “Run PR review when I ask” | Skill | Hook |
| “Block commit if `.env` staged” | Hook | Skill alone |
| “Explain hook failure in chat” | Skill (companion) | Hook (hooks don’t chat) |

## Study order

[Skills alone](ii-use-skills-alone.md) → [AGENTS.md alone](iii-use-agents-md-alone.md) → [Hooks on commit](iv-use-hooks-on-commit.md) → [Combine all three](v-combine-skills-agents-hooks.md).

## Related

- [Artifacts & why bother](../ii-artifacts-why-and-what.md)
- [Cursor skills, rules & AGENTS.md](../iv-cursor-skills-rules-agents-md.md)
- [Examples — parameterized scripts & logs](../examples/i-overview.md)
