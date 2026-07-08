---
label: "II"
subtitle: "Artifacts & why bother"
group: "AI Applied"
order: 2
---
Artifacts & why bother

## 1. Why bother?

| Without persistent instructions | With skills / rules / project docs |
|--------------------------------|----------------------------------|
| Repeat “use conventional commits” daily | Agent reads skill once per task |
| Agent guesses stack and folder layout | Points at `SKILL.md` or `AGENTS.md` |
| Inconsistent PR and doc format | Same template every time |

Think of skills as **onboarding docs for the agent** — short, actionable, trigger-aware.

## 2. What to create (pick by product)

| Artifact | Product | Scope |
|----------|---------|--------|
| **Skill (`SKILL.md`)** | Cursor, **Claude Code**, Codex (configured) | Task-specific workflows (review, deploy, SQL) |
| **Rules (`.mdc`)** | Cursor | Always-on or file-pattern coding standards |
| **`AGENTS.md`** | Cursor, **Codex**, Claude Code, Copilot, many others | Repo-wide agent briefing at root |
| **`CLAUDE.md`** | Claude Code | Project memory / standing instructions |
| **Project instructions** | Claude Projects (web) | Tone, format, attached knowledge |
| **Custom GPT instructions** | ChatGPT | Persona + process for one assistant |
| **Context `.md` in repo** | Any IDE agent | `docs/agent-context.md`, architecture notes |

Same content idea everywhere: **when to use this + what to do + examples**.

```text
You (once)  →  write SKILL.md / rules / AGENTS.md
Agent (each task)  →  loads matching instructions  →  fewer retries
```