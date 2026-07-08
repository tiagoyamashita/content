---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
AI Applied — 概要
**Practical AI for people who use it** — ChatGPT, Claude, Gemini, Copilot, Cursor, and similar tools — not for training models or reading research papers.

If you want how models work under the hood, see [Machine learning](../machine-learning/i-overview.md) → [Deep learning](../deep-learning/i-overview.md) → [LLMs](../llms/i-overview.md). **Start here** if your goal is better **outputs**, **workflows**, and **trust** in daily work.

## このサブメニューのマップ

| Part | Topic |
|------|--------|
| **I — Overview** | 対象者、メンタルモデル、学習パス |
| **[Effective prompting](effective-prompting/i-overview.md)** | プロンプト構造、技法、テンプレート |
| **[Agents & agentic workflows](agents-and-agentic-workflows/i-overview.md)** | マルチステップ AI、ツール、ガードレール |
| **[Tools & orchestration](tools-and-orchestration/i-overview.md)** | チャット、IDE、自動化、MCP 入門 |
| **[Custom assistants & knowledge](custom-assistants-and-knowledge/i-overview.md)** | Projects、カスタム GPT、ユーザー向け RAG |
| **[Multimodal & files](multimodal-and-files/i-overview.md)** | PDF、画像、スプレッドシート、音声 |
| **[Trust, privacy & verify](trust-privacy-and-verify/i-overview.md)** | ハルシネーション、機密データ、検証 |
| **[Skills & agent instructions](skills-and-agent-instructions/i-overview.md)** | `SKILL.md`、ルール、`AGENTS.md` |
| **[How MCP works](how-mcp-works/i-overview.md)** | JSON-RPC、stdio vs HTTP、ベクトル DB と MCP |

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
| Knowledge worker (PM, analyst, writer) | [Effective prompting](effective-prompting/i-overview.md) → [Custom assistants](custom-assistants-and-knowledge/i-overview.md) |
| Developer using Cursor/Copilot | [Agents](agents-and-agentic-workflows/i-overview.md) → [Skills & instructions](skills-and-agent-instructions/i-overview.md) |
| Manager rolling out AI to a team | [Trust & privacy](trust-privacy-and-verify/i-overview.md) → [Custom assistants](custom-assistants-and-knowledge/i-overview.md) |
| Power user chaining tools | [Orchestration](tools-and-orchestration/i-overview.md) → [Agents](agents-and-agentic-workflows/i-overview.md) |

## 2024–2026 shift: from chat to agents

| Era | Interaction | Example |
|-----|-------------|---------|
| **Chat** | One question → one answer | “Summarise this email” |
| **Assistants** | Saved instructions + files | Claude Project, Custom GPT |
| **Agents** | Goal → many steps + tools | “Research competitors and draft a table” |
| **Orchestration** | Several AIs or automations wired together | CRM → AI summary → Slack |

You do not need to build any of this — products expose it in the UI. You **do** need clear goals, good context, and verification habits.

## Next

Continue with [Effective prompting](effective-prompting/i-overview.md).

**Related:** [LLM prompt engineering (technical)](../llms/iv-prompt-engineering.md), [RAG for users](custom-assistants-and-knowledge/i-overview.md).
