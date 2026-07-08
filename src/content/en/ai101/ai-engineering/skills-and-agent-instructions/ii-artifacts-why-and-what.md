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
| Long chat preamble every session | Short prompt + loaded context |

Think of skills as **onboarding docs for the agent** — short, actionable, trigger-aware.

```text
You (once)  →  write SKILL.md / rules / AGENTS.md
Agent (each task)  →  loads matching instructions  →  fewer retries
```

**Promotion rule:** if you have typed the same instruction **three times**, move it to a skill, rule, or `AGENTS.md`. See [Persistent instructions](../loop-prompting/iii-persistent-instructions.md).

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

See [Artifact examples](iia-artifact-examples.md) for copy-paste samples of each row above.

## 3. Which artifact? (decision guide)

```text
Need a multi-step workflow (review, deploy, incident writeup)?
  → SKILL.md

Need code to always look a certain way in .ts files?
  → Cursor rule (.mdc) with globs

Need every agent to know stack, tests, and folder map?
  → AGENTS.md (repo root)

Claude Code only — stable prefs and gotchas, not a procedure?
  → CLAUDE.md

Web assistant with uploaded policies / no repo?
  → Claude Project instructions or Custom GPT

Deep domain doc (one feature area) linked from AGENTS.md?
  → docs/.../context.md
```

| Question | Answer |
|----------|--------|
| “Always use Prettier defaults” | **Rule** (`alwaysApply` or `globs`) |
| “How we run smoke tests and read output” | **Skill** |
| “We use Next.js 15; tests are `npm test`” | **`AGENTS.md`** |
| “Never invent dates in status reports” | **Project instructions** or Custom GPT |
| Same workflow in Cursor and Claude Code | **`SKILL.md`** in both `.cursor/skills/` and `.claude/skills/` |

## 4. Layering (use together)

```text
AGENTS.md          ← baseline: stack, commands, layout (always relevant)
  ├── rules/*.mdc  ← style when editing matching files
  ├── SKILL.md     ← heavy workflows on demand
  └── docs/*.md    ← optional deep context, linked not pasted
```

Do **not** paste the entire skill into `AGENTS.md` — link to it. Keep `AGENTS.md` under ~2–3 screens; Codex enforces a size cap by default.

## 5. Common mistakes

| Mistake | Fix |
|---------|-----|
| One giant instructions blob | Split: `AGENTS.md` + skills + `reference.md` |
| Vague skill `description` (“helps with code”) | Name task + trigger words: “PR, diff, code review” |
| Duplicating the same rule in 5 files | Single source; link from `AGENTS.md` |
| Secrets or live API keys in skills | Redacted examples; env vars only |
| Skills never updated after process change | Owner + quarterly review |

**Next:** [Artifact examples](iia-artifact-examples.md) → [Cross-tool portable setup](iii-cross-tool-portable-setup.md).
