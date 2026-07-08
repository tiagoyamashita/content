---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
Loop prompting — overview
**Loop prompting** is working with AI in **cycles** instead of **restarting from zero every time**. You invest once in durable instructions and context, then each turn is a small correction or trigger — not another full brief.

This sits between [Effective prompting](../effective-prompting/i-overview.md) (how to write a good prompt) and [Agents](../agents-and-agentic-workflows/i-overview.md) (multi-step tool use). Loop prompting is the **habit layer**: stop re-explaining what the model should already know.

## Map of this submenu

| Note | Focus |
|------|--------|
| [One-shot vs loop](ii-one-shot-vs-loop.md) | Old chat habit vs set-up-once, iterate-many |
| [Persistent instructions](iii-persistent-instructions.md) | Projects, skills, rules, saved system context |
| [Session & recurring loops](iv-session-and-recurring-loops.md) | Same-thread refinement, `/loop`, automations |
| [Hygiene & when to reset](v-hygiene-and-when-to-reset.md) | Context rot, stale skills, trust boundaries |

## 1. Two kinds of loop

| Loop type | You do | Example |
|-----------|--------|---------|
| **Human-in-the-loop** | Keep one session or project; send short deltas | “Shorter intro.” “Fix table 2.” “Run tests again.” |
| **Time / event loop** | Arm a recurring or watcher trigger | Cursor `/loop 5m check CI`, deploy watcher, weekly digest automation |

Both reuse **stored context** instead of pasting the same preamble into a new chat.

## 2. Mental model

```text
OLD (one-shot every time)
  New chat → full role + task + constraints + paste docs → answer → discard

NEW (loop prompting)
  Set up once (project / skill / rule / assistant)
    → loop: small prompt + optional new file
    → loop: verify / refine
    → loop: (optional) scheduled or event-driven rerun
```

| Layer | What persists | Where (examples) |
|-------|---------------|------------------|
| **Identity & standards** | Tone, format, team rules | Custom GPT, Claude Project, `.cursor/rules` |
| **Workflows** | Multi-step how-to | `SKILL.md`, saved prompt library |
| **Repo / knowledge** | Files the model should see | Project files, RAG, `@folder` in Cursor |
| **Session state** | Current deliverable in progress | Same chat thread, agent transcript |

## 3. Who should read this

| You… | Start with |
|------|------------|
| Re-type the same instructions daily | [Persistent instructions](iii-persistent-instructions.md) |
| Refine drafts across many “try again” messages | [One-shot vs loop](ii-one-shot-vs-loop.md) |
| Want CI or deploy checked without asking each time | [Session & recurring loops](iv-session-and-recurring-loops.md) |
| Use Cursor or IDE agents heavily | This track → [Skills & agent instructions](../skills-and-agent-instructions/i-overview.md) |

## 4. Study order

[One-shot vs loop](ii-one-shot-vs-loop.md) → [Persistent instructions](iii-persistent-instructions.md) → [Session & recurring loops](iv-session-and-recurring-loops.md) → [Hygiene & when to reset](v-hygiene-and-when-to-reset.md)

## 5. Rehearsal questions

- What is the difference between a human-in-the-loop and a time/event loop?
- Name two places persistent instructions can live.
- When is a new chat still the right choice?

**Next:** [One-shot vs loop](ii-one-shot-vs-loop.md).
