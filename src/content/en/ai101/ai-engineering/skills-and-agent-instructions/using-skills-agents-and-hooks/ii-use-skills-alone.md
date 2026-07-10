---
label: "II"
subtitle: "Skills alone"
group: "Using skills, agents & hooks"
order: 2
---
Skills alone

A **skill** runs when the **user’s task** matches the skill `description`. Nothing happens until the user (or an explicit skill command) invokes that workflow.

## What a skill is not

| Skill is not… | Why |
|---------------|-----|
| A hook | Hooks fire on events; skills wait for intent |
| `AGENTS.md` | Briefing loads every chat; skills load on match |
| A script | Scripts live in `scripts/`; skill text tells the agent **when** to run them |

## Sample skill (copy-ready)

Live file: [sample/.cursor/skills/pr-review-lite/SKILL.md](sample/.cursor/skills/pr-review-lite/SKILL.md)

```text
.cursor/skills/pr-review-lite/
  SKILL.md
```

### Trigger

User says any of:

- “review this PR”
- “code review”
- “check my diff before merge”

Cursor matches `description` in frontmatter → skill loads.

### What the agent does

1. Read the diff (tool)
2. Follow checklist in `SKILL.md`
3. Output: Summary / Blockers / Suggestions / Tests

**No hook involved.** User could commit without running this skill — it is advisory unless you also add a hook.

## Skill + script (optional)

For workflows that must run the **same command** every time, point the skill at a script — see [Examples: deploy-check](../examples/ii-parameterized-script-clarify.md).

```text
Skill says WHEN + HOW to ask user
Script does the deterministic work + JSON log
Agent reads log and summarizes
```

## User-only flow

```text
User opens chat
  → AGENTS.md loads (background briefing)
  → User: "review my PR"
  → pr-review-lite skill loads
  → Agent reviews per SKILL.md
  → (no hook, no commit gate)
```

## When to use skills alone

| Good for | Example |
|----------|---------|
| Optional expert workflows | PR review, perf scan, deploy check |
| Needs user parameters | environment, path, dry-run |
| Iteration loops | Read log → fix → re-run ([loop example](../examples/iii-loop-on-script-results.md)) |

## Test

1. Copy [sample/.cursor/skills/pr-review-lite/](sample/.cursor/skills/pr-review-lite/) → your `.cursor/skills/`
2. Fresh chat: *“review this PR”*
3. Agent should use the skill checklist format

## Next

[AGENTS.md alone](iii-use-agents-md-alone.md) — context that loads **every** session without a trigger phrase.
