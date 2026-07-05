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

## Map of this submenu

| Note | Focus |
|------|--------|
| [Artifacts & why bother](ii-artifacts-why-and-what.md) | What to create, which product uses which artifact |
| [Artifact examples](iia-artifact-examples.md) | Copy-paste samples for every artifact type |
| [Cross-tool portable setup](iii-cross-tool-portable-setup.md) | One repo, Cursor + Claude Code + Codex |
| [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) | Cursor layout, rules vs skills, `AGENTS.md` sections |
| [Writing & maintaining skills](v-writing-and-maintaining-skills.md) | Descriptions, progressive disclosure, team workflow |

**Related loop:** [Persistent instructions](../loop-prompting/iii-persistent-instructions.md) — when to promote chat text into skills.

## Study order

[Artifacts & why bother](ii-artifacts-why-and-what.md) → [Artifact examples](iia-artifact-examples.md) → [Cross-tool portable setup](iii-cross-tool-portable-setup.md) → [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) → [Writing & maintaining skills](v-writing-and-maintaining-skills.md)

## Start here (15 minutes)

1. Add a minimal **`AGENTS.md`** at repo root (stack, test command, layout) — see [Artifact examples](iia-artifact-examples.md) §3.
2. Pick **one** repeated workflow (commits or PR review) and add a **`SKILL.md`** — see §1 or §8 in [Writing & maintaining skills](v-writing-and-maintaining-skills.md).
3. Try a short prompt that should trigger the skill; refine the `description` if it does not load.
