---
label: "II"
subtitle: "One-shot vs loop"
group: "AI Applied"
order: 2
---
One-shot vs loop
**One-shot prompting** treats every chat like a blank slate. **Loop prompting** assumes most of the briefing already lives somewhere durable — your job each turn is to **steer**, not **rebrief**.

## 1. One-shot habit (still common)

```text
Open new chat
  → paste role paragraph
  → paste constraints
  → attach files
  → ask task
  → get answer
  → tomorrow: repeat everything
```

| Cost | Detail |
|------|--------|
| **Time** | Minutes of setup per session |
| **Quality drift** | Yesterday’s wording ≠ today’s |
| **Lost iteration** | Good refinements trapped in old threads |
| **Token waste** | Same context re-sent every message |

One-shot is fine for **truly novel** tasks. It is expensive for **recurring** work (weekly reports, PR reviews, support replies, doc edits).

## 2. Loop habit

```text
Set up once (project / skill / assistant / rules)
  → turn 1: “Draft Q3 summary from @data/”
  → turn 2: “Cut section 2; keep all numbers.”
  → turn 3: “Export as bullet email for execs.”
  → next week: “Same format; new file @data/q4.csv”
```

Each turn is a **delta** — a correction, a new attachment, or a changed input — not a rebuilt system prompt.

## 3. Side-by-side

| Dimension | One-shot | Loop |
|-----------|----------|------|
| **Setup per session** | Full prompt | Mostly already stored |
| **Typical message length** | Long | Short |
| **Context location** | Chat only | Project + chat |
| **Best for** | One-off, sensitive isolation | Repeat workflows, same standards |
| **Failure mode** | Inconsistent outputs | Stale or wrong stored context |

## 4. The iteration loop (human)

From [Effective prompting — iteration](../effective-prompting/iii-iteration-and-templates.md), upgraded:

```text
1. Rough ask (context already loaded)
2. Specific fix (“table 2 wrong source”)
3. One constraint per turn
4. Save what worked → skill or template (not just chat history)
```

**Loop rule:** if you typed the same paragraph twice this week, **promote it** to persistent instructions — see [Persistent instructions](iii-persistent-instructions.md).

## 5. Loop is not “never start fresh”

| Start a **new** chat when… | **Continue** the loop when… |
|----------------------------|-----------------------------|
| Topic or audience changed completely | Same deliverable or workflow |
| Context is polluted with wrong assumptions | Refining output quality |
| You need isolation (confidential mix-up) | Agent already read the right files |
| Model stuck in a bad pattern | Small directed fixes work |

## 6. Relation to agents

| | Loop prompting | Agents |
|---|----------------|--------|
| **Focus** | Don’t rebrief; iterate cheaply | Many steps + tools toward a goal |
| **Your input** | Short steering | Goal + boundaries + checkpoints |
| **Overlap** | Agent sessions *are* loops when context persists | Agents benefit from stored skills/rules |

Read [Agents — overview](../agents-and-agentic-workflows/i-overview.md) for tool-heavy multi-step work. Use loop prompting for **everyday** repeat steering.

## 7. Rehearsal questions

- Why does one-shot prompting waste tokens?
- What makes a good “delta” message in a loop?
- When should you still open a new chat?

**Next:** [Persistent instructions](iii-persistent-instructions.md).
