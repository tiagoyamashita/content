---
label: "III"
subtitle: "Orchestration patterns"
group: "AI Applied"
order: 3
---
Orchestration patterns

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

### MCP (Model Context Protocol) — user view

**MCP** lets an AI client plug into **tools and data sources** (databases, issue trackers, custom APIs) through standard connectors — like USB for AI tools.

| You see | Under the hood |
|---------|----------------|
| “Search our Linear tickets” in Cursor/Claude Desktop | MCP server talks to Linear |
| One-time admin setup | IT or power user enables servers |

You **use** MCP through products that support it; you rarely “write MCP” unless you’re automating at work.

### Automation chains

```text
Form submit → AI summarise → create Notion page → Slack notify
```

| Platform | Strength |
|----------|----------|
| **Zapier / Make** | No-code; many SaaS integrations |
| **n8n** | Self-host; technical teams |

Put **human approval** steps before external sends (email to customers, public posts).