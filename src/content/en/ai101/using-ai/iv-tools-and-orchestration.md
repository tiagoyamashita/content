---
label: "IV"
subtitle: "Tools & orchestration"
group: "Using AI"
order: 4
---
Tools and orchestration
**Orchestration** means connecting AI to **where you already work** — chat apps, IDEs, browsers, docs, Slack — so tasks flow without copy-pasting between ten tabs.

This is for **users** choosing and wiring tools, not building ML pipelines.

## 1. Tool map

| Category | Examples | Best for |
|----------|----------|----------|
| **General chat** | ChatGPT, Claude, Gemini | Writing, analysis, brainstorming |
| **IDE / code** | Cursor, GitHub Copilot, Cody | Implementation, refactors, tests — use [Skills](viii-skills-and-agent-instructions.md) |
| **Office / enterprise** | Microsoft Copilot, Google Duet | Email, slides, sheets in tenant |
| **Search + AI** | Perplexity, Gemini with search | Cited quick research |
| **Automation** | Zapier, Make, n8n | Trigger → AI step → action |
| **Meeting / voice** | Otter, Fireflies, native transcribe | Notes, follow-ups |
| **Design / image** | Midjourney, DALL·E, Ideogram | Visuals from prompts |

Pick **one primary chat** and **one primary coding assistant** to avoid context sprawl.

## 2. Orchestration patterns

### Copy-paste bridge (lowest friction)

```text
Source doc → chat → paste result → destination
```

Fine for occasional tasks; does not scale.

### Connected apps (connectors)

ChatGPT / Claude / Copilot **connectors** read Google Drive, Slack, GitHub, etc.

| Benefit | Watch out |
|---------|-----------|
| Less manual upload | Permissions — only connect what you’re allowed to share |
| Fresher context | Model may still misread or summarise wrong |

### IDE + repo context

**Cursor:** codebase index, rules, terminal, multi-file agent.

| Practice | Why |
|----------|-----|
| Keep `README` / rules accurate | Agent follows wrong patterns otherwise |
| Small, scoped tasks | Easier review |
| Use `@file` / mentions | Pin exact context |

### MCP (Model Context Protocol)

**MCP** plugs the agent into **live systems** (GitHub, Postgres, Sentry) via **MCP servers**. Wire format is **JSON-RPC** over **stdio** (local) or **HTTP** (remote) — **not gRPC**. The server then calls each product’s normal **REST/HTTPS API**.

| You see | Under the hood |
|---------|----------------|
| “Search our Linear tickets” in Cursor | Host → MCP server → Linear HTTPS API |
| MCP settings / `mcp.json` | Spawns or connects to connector process |

**Deep dive:** [How MCP works](ix-how-mcp-works.md) — transports, roles, security, vs skills.

### Automation chains

```text
Form submit → AI summarise → create Notion page → Slack notify
```

| Platform | Strength |
|----------|----------|
| **Zapier / Make** | No-code; many SaaS integrations |
| **n8n** | Self-host; technical teams |

Put **human approval** steps before external sends (email to customers, public posts).

## 3. Choosing models in the UI

| Situation | Typical choice |
|-----------|----------------|
| Fast drafts, simple edits | Smaller / “mini” model |
| Long docs, nuance, coding | Flagship model |
| Huge context (whole codebase) | Long-context or “project” mode |
| Privacy / compliance | Enterprise workspace, no training on data |

**Model switching:** draft cheap → polish with flagship on final pass.

## 4. Team orchestration

| Practice | Purpose |
|----------|---------|
| **Shared prompt library** | Consistent quality across team |
| **Approved connectors only** | Reduce data leakage |
| **Naming conventions for Projects** | Find customer / product context |
| **Review before client-facing** | Quality and liability |

## 5. Anti-patterns

| Anti-pattern | Problem |
|--------------|---------|
| Same sensitive doc in 5 different free-tier chats | Spread of data; inconsistent answers |
| Agent with full repo write, no review | Broken builds |
| Automation posting AI text without review | Embarrassment, compliance |
| Chasing every new tool weekly | No accumulated prompt/context library |

## 6. Rehearsal questions

- Name two orchestration patterns besides copy-paste.
- When is a “mini” model enough?
- Is MCP gRPC or HTTP? ([How MCP works](ix-how-mcp-works.md))

**Related:** [How MCP works](ix-how-mcp-works.md), [Agents](iii-agents-and-agentic-workflows.md), [Custom assistants](v-custom-assistants-and-knowledge.md).
