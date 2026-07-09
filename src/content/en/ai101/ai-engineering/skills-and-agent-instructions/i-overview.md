---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
Skills & agent instructions — overview

Deep dive on **skills & agent instructions** — how to teach an agent your workflows once, so you stop re-explaining them every chat.

## What this track covers

**Skills** and **instruction `.md` files** encode *your* rules: commit format, PR checklist, API envelope shape, doc frontmatter, deploy steps. The product loads them when the task matches — you write markdown; the agent follows it.

| You get | Without this layer |
|---------|-------------------|
| Same PR review every time | “Remember to check tests…” each diff |
| Agent knows `npm test` and folder layout | Guesses commands; edits wrong dirs |
| Team shares behaviour via git | Everyone’s agent behaves differently |

This is for **people who use agents daily** — especially **Cursor**, **Claude Code**, **Codex**, Claude Projects, and Custom GPTs. Not for training models.

## Skills vs live tools (MCP)

| | **Skills / rules / `AGENTS.md`** | **MCP / connectors** |
|---|----------------------------------|----------------------|
| **What** | Static markdown instructions | Live APIs (DB, Slack, browser, etc.) |
| **When** | “How *we* do X” | “Fetch / act on *current* data” |
| **Example** | PR review checklist skill | Query production logs via MCP |

Use both: skills tell the agent *your process*; MCP gives it *live access*. See [How MCP works](../how-mcp-works/i-overview.md).

## Skills folder tree

How a typical **project** skills directory is organized. Each skill is a **folder** with a required **`SKILL.md`**; optional files hold detail the agent reads only when needed.

```text
repo/
├── AGENTS.md                          ← repo briefing (stack, tests, layout) — not a skill
├── .cursor/
│   ├── rules/                         ← always-on / glob rules (Cursor-only)
│   │   ├── typescript-errors.mdc
│   │   └── api-conventions.mdc
│   └── skills/                        ← project skills (commit to git)
│       ├── pr-review/
│       │   ├── SKILL.md               ← required — name, description, workflow
│       │   ├── reference.md           ← optional — long checklist, security notes
│       │   └── examples.md            ← optional — good/bad review samples
│       ├── conventional-commits/
│       │   └── SKILL.md
│       ├── deploy-staging/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── smoke-test.sh      ← optional — runnable helpers
│       └── incident-writeup/
│           ├── SKILL.md
│           └── reference.md
│
└── docs/skills/                       ← optional canonical copy (sync to .cursor/)
    └── pr-review/
        └── SKILL.md

~/.cursor/skills/                        ← personal skills (all your repos)
  ├── my-commit-style/
  │   └── SKILL.md
  └── private-runbook/
      ├── SKILL.md
      └── reference.md
```

| Path | Scope | Commit to git? |
|------|-------|----------------|
| `.cursor/skills/<name>/` | Team workflows in this repo | Yes |
| `~/.cursor/skills/<name>/` | Personal habits everywhere | No (your machine) |
| `docs/skills/<name>/` | Single source for multi-tool sync | Yes |
| `.cursor/rules/*.mdc` | Coding standards (not skills) | Yes |

**Do not** put custom skills in `~/.cursor/skills-cursor/` — reserved for Cursor built-ins.

One skill folder = one workflow. Split large topics (e.g. `pr-review` vs `deploy-staging`) instead of one mega-skill. Put fixed commands in **`scripts/`** and reference them from `SKILL.md` — see [Linking a fixed script](iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script) in the Cursor layout note.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Artifacts & why bother](ii-artifacts-why-and-what.md) | What to create, which product uses which artifact |
| [Artifact examples](iia-artifact-examples.md) | Copy-paste samples for every artifact type |
| [Cross-tool portable setup](iii-cross-tool-portable-setup.md) | One repo, Cursor + Claude Code + Codex |
| [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) | Cursor layout, rules vs skills, `AGENTS.md`, **linking scripts** |
| [Writing & maintaining skills](v-writing-and-maintaining-skills.md) | Descriptions, progressive disclosure, team workflow |

**Related loop:** [Persistent instructions](../loop-prompting/iii-persistent-instructions.md) — when to promote chat text into skills.

## Study order

[Artifacts & why bother](ii-artifacts-why-and-what.md) → [Artifact examples](iia-artifact-examples.md) → [Cross-tool portable setup](iii-cross-tool-portable-setup.md) → [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) → [Writing & maintaining skills](v-writing-and-maintaining-skills.md)

## Start here (15 minutes)

1. Add a minimal **`AGENTS.md`** at repo root (stack, test command, layout) — see [Artifact examples](iia-artifact-examples.md) §3.
2. Pick **one** repeated workflow (commits or PR review) and add a **`SKILL.md`** — see §1 or §8 in [Writing & maintaining skills](v-writing-and-maintaining-skills.md).
3. Try a short prompt that should trigger the skill; refine the `description` if it does not load.
