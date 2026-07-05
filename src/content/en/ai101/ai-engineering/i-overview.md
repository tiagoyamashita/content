---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
AI Applied — overview
**Practical AI for people who use it** — ChatGPT, Claude, Gemini, Copilot, Cursor, and similar tools — not for training models or reading research papers.

If you want how models work under the hood, see [Machine learning](../machine-learning/i-overview.md) → [Deep learning](../deep-learning/i-overview.md) → [LLMs](../llms/i-overview.md). **Start here** if your goal is better **outputs**, **workflows**, and **trust** in daily work.

## Map of this submenu

| Part | Topic |
|------|--------|
| **I — Overview** | Who this is for, mental model, pick your path |
| **[Effective prompting](effective-prompting/i-overview.md)** | Prompt structure, techniques, templates |
| **[Loop prompting](loop-prompting/i-overview.md)** | Set up once, iterate in loops — not re-prompt every time |
| **[Agents & agentic workflows](agents-and-agentic-workflows/i-overview.md)** | Multi-step AI, tools, guardrails |
| **[Tools & orchestration](tools-and-orchestration/i-overview.md)** | Chat apps, IDE agents, automations, MCP intro |
| **[Custom assistants & knowledge](custom-assistants-and-knowledge/i-overview.md)** | Projects, custom GPTs, RAG for users |
| **[Multimodal & files](multimodal-and-files/i-overview.md)** | PDFs, images, spreadsheets, voice |
| **[Trust, privacy & verify](trust-privacy-and-verify/i-overview.md)** | Hallucinations, sensitive data, fact-checking |
| **[Skills & agent instructions](skills-and-agent-instructions/i-overview.md)** | `SKILL.md`, rules, `AGENTS.md` |
| **[How MCP works](how-mcp-works/i-overview.md)** | JSON-RPC, stdio vs HTTP, vector DB vs MCP |


## Mental model (user view)

```text
You  →  prompt + context  →  AI model  →  answer / action
              ↑                    ↑
        instructions          may use tools
        examples              (search, code, files)
        attached files
        (persistent: projects, skills, rules)
```

**Loop prompting:** store instructions once, then send **short deltas** in the same session or on a schedule — see [Loop prompting](loop-prompting/i-overview.md).

| You control | AI controls |
|-------------|-------------|
| Goal, tone, format, examples | Wording and reasoning (within limits) |
| What files/context to attach | Which tool to call (in agent mode) |
| When to stop or redirect | Step order in multi-step tasks |

## Who should read what

| Your job | Start with |
|----------|------------|
| Knowledge worker (PM, analyst, writer) | [Effective prompting](effective-prompting/i-overview.md) → [Loop prompting](loop-prompting/i-overview.md) → [Custom assistants](custom-assistants-and-knowledge/i-overview.md) |
| Developer using Cursor/Copilot | [Loop prompting](loop-prompting/i-overview.md) → [Agents](agents-and-agentic-workflows/i-overview.md) → [Skills & instructions](skills-and-agent-instructions/i-overview.md) |
| Manager rolling out AI to a team | [Trust & privacy](trust-privacy-and-verify/i-overview.md) → [Custom assistants](custom-assistants-and-knowledge/i-overview.md) |
| Power user chaining tools | [Orchestration](tools-and-orchestration/i-overview.md) → [Agents](agents-and-agentic-workflows/i-overview.md) |

## 2024–2026 shift: from chat to loops and agents

| Era | Interaction | Example |
|-----|-------------|---------|
| **Chat** | One question → one answer | “Summarise this email” |
| **Loop prompting** | Stored instructions + short deltas | Project rules + “fix table 2” / `/loop 5m check CI` |
| **Assistants** | Saved instructions + files | Claude Project, Custom GPT |
| **Agents** | Goal → many steps + tools | “Research competitors and draft a table” |
| **Orchestration** | Several AIs or automations wired together | CRM → AI summary → Slack |

You do not need to build any of this — products expose it in the UI. You **do** need clear goals, good context, and verification habits.

## Next

Continue with [Effective prompting](effective-prompting/i-overview.md), then [Loop prompting](loop-prompting/i-overview.md).

**Related:** [LLM prompt engineering (technical)](../llms/iv-prompt-engineering.md), [RAG for users](custom-assistants-and-knowledge/i-overview.md).
