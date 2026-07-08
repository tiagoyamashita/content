---
label: "III"
subtitle: "Persistent instructions"
group: "AI Applied"
order: 3
---
Persistent instructions
**Persistent instructions** are the “prompt you don’t repeat” — loaded automatically when the product thinks they apply. Build this layer once; your daily loop becomes short commands.

## 1. Stack (pick what your tool supports)

```text
Assistant / Project instructions     →  who you are, tone, always-do rules
Skills / saved workflows             →  how to run a process
Rules / repo conventions             →  code style, file patterns
Knowledge files / RAG                →  docs the model can retrieve
Personal prompt library              →  templates you paste rarely
```

| Layer | ChatGPT / Claude | Cursor / IDE |
|-------|------------------|--------------|
| **Project / Custom GPT** | Instructions + uploaded files | Rules, `AGENTS.md`, index |
| **Workflows** | Custom GPT actions, projects | `SKILL.md` |
| **Knowledge** | Project knowledge, RAG | `@` mentions, codebase index |

Deep dives: [Custom assistants](../custom-assistants-and-knowledge/i-overview.md), [Skills & agent instructions](../skills-and-agent-instructions/i-overview.md).

## 2. What belongs in persistent layer

| Store persistently | Keep per-message |
|--------------------|------------------|
| Role, tone, audience | Today’s data, one-off facts |
| Output format defaults | “Use Tuesday’s numbers only” |
| Team naming, stack, test commands | “Stop after step 2” |
| Verification habits (“cite sources”) | Specific file paths this turn |
| Things you say every week | Novel constraints for this draft |

**Rule:** if you have sent it **three times**, externalize it.

## 3. Claude Projects / ChatGPT Custom GPTs

| Field | Loop prompting use |
|-------|-------------------|
| **Instructions** | Stable persona + quality bar |
| **Knowledge files** | Policies, glossaries, past examples |
| **Conversation** | Short deltas inside the project |

```text
Project: “Acme PM assistant”
  Instructions: bullet memos, flag risks, never invent dates
  Files: roadmap.pdf, style-guide.md
  Loop message: “Summarise this Slack export for exec standup.”
```

Same project next week — only swap the export.

## 4. Cursor: rules, skills, AGENTS.md

| Artifact | Loads when | Example content |
|----------|------------|-----------------|
| **`.cursor/rules/*.mdc`** | File patterns or always | TypeScript error handling |
| **`SKILL.md`** | Task matches description | “How we run smoke tests” |
| **`AGENTS.md`** | Agent opens repo | Test command, folder map |

You say **“review this PR”** — rules enforce style, skills define the checklist, `AGENTS.md` says how to run tests. No essay in the chat box.

See [Cursor skills, rules & AGENTS.md](../skills-and-agent-instructions/iv-cursor-skills-rules-agents-md.md).

## 5. Prompt library (lightweight persistence)

Not everything needs a Custom GPT. A **personal library** works:

```text
prompts/
  weekly-status.md      # role + format + “paste updates below”
  client-email.md
  code-review-delta.md  # “checklist already in SKILL; paste diff”
```

Loop = open template in a **project that already has instructions**, paste only the variable part.

## 6. Promotion workflow

When a one-shot chat went well:

```text
1. Highlight reusable blocks (role, format, checks)
2. Move to project instructions or SKILL.md
3. Replace long text with a name: “Use weekly-status template”
4. Delete duplicate paragraphs from old chats
5. Test one short prompt — does quality hold?
```

## 7. Anti-patterns

| Mistake | Fix |
|---------|-----|
| Dump entire wiki into instructions | Link or RAG; keep instructions scannable |
| Duplicate rules in 5 places | One source of truth; link from `AGENTS.md` |
| Never update after process change | Review skills quarterly |
| Secrets in instructions | Never — use env vars and redacted examples |

## 8. Rehearsal questions

- Name three artifacts that store persistent instructions in Cursor.
- What should stay in the message vs move to project instructions?
- What is the “three times” promotion rule?

**Next:** [Session & recurring loops](iv-session-and-recurring-loops.md).
