---
label: "I"
subtitle: "Overview"
group: "Using AI"
order: 1
---
Using AI — overview
**Practical AI for people who use it** — ChatGPT, Claude, Gemini, Copilot, Cursor, and similar tools — not for training models or reading research papers.

If you want how models work under the hood, see [Machine learning](../machine-learning/i-overview.md) → [Deep learning](../deep-learning/i-overview.md) → [LLMs](../llms/i-overview.md). **Start here** if your goal is better **outputs**, **workflows**, and **trust** in daily work.

## Map of this submenu

| Part | Topic |
|------|--------|
| **I — Overview** | Who this is for, mental model, pick your path |
| **II — Effective prompting** | Prompts that work for writing, analysis, coding help |
| **III — Agents & agentic workflows** | Multi-step AI that plans, uses tools, and executes |
| **IV — Tools & orchestration** | Chat apps, IDE agents, automations, MCP |
| **V — Custom assistants & knowledge** | Projects, custom GPTs, doc uploads, team libraries |
| **VI — Multimodal & files** | PDFs, images, spreadsheets, voice |
| **VII — Trust, privacy & verify** | Hallucinations, sensitive data, fact-checking |
| **VIII — Skills & agent instructions** | `SKILL.md`, rules, `AGENTS.md` for Cursor and agents |
| **IX — How MCP works** | JSON-RPC, stdio vs HTTP — not gRPC; how connectors reach APIs |

## Mental model (user view)

```text
You  →  prompt + context  →  AI model  →  answer / action
              ↑                    ↑
        instructions          may use tools
        examples              (search, code, files)
        attached files
```

| You control | AI controls |
|-------------|-------------|
| Goal, tone, format, examples | Wording and reasoning (within limits) |
| What files/context to attach | Which tool to call (in agent mode) |
| When to stop or redirect | Step order in multi-step tasks |

## Who should read what

| Your job | Start with |
|----------|------------|
| Knowledge worker (PM, analyst, writer) | [Effective prompting](ii-effective-prompting.md) → [Custom assistants](v-custom-assistants-and-knowledge.md) |
| Developer using Cursor/Copilot | [Agents](iii-agents-and-agentic-workflows.md) → [Skills & instructions](viii-skills-and-agent-instructions.md) |
| Manager rolling out AI to a team | [Trust & privacy](vii-trust-privacy-and-verify.md) → [Custom assistants](v-custom-assistants-and-knowledge.md) |
| Power user chaining tools | [Orchestration](iv-tools-and-orchestration.md) → [Agents](iii-agents-and-agentic-workflows.md) |

## 2024–2026 shift: from chat to agents

| Era | Interaction | Example |
|-----|-------------|---------|
| **Chat** | One question → one answer | “Summarise this email” |
| **Assistants** | Saved instructions + files | Claude Project, Custom GPT |
| **Agents** | Goal → many steps + tools | “Research competitors and draft a table” |
| **Orchestration** | Several AIs or automations wired together | CRM → AI summary → Slack |

You do not need to build any of this — products expose it in the UI. You **do** need clear goals, good context, and verification habits.

## Next

Continue with [Effective prompting](ii-effective-prompting.md).

**Related:** [LLM prompt engineering (technical)](../llms/iv-prompt-engineering.md), [RAG for users](v-custom-assistants-and-knowledge.md).
