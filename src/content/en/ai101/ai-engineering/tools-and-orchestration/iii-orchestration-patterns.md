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

### MCP (Model Context Protocol)

**MCP** plugs the agent into **live systems** (GitHub, Postgres, Sentry) via **MCP servers**. Wire format is **JSON-RPC** over **stdio** (local) or **HTTP** (remote) — **not gRPC**. The server then calls each product’s normal **REST/HTTPS API**.

| You see | Under the hood |
|---------|----------------|
| “Search our Linear tickets” in Cursor | Host → MCP server → Linear HTTPS API |
| MCP settings / `mcp.json` | Spawns or connects to connector process |

**Deep dive:** [How MCP works](../how-mcp-works/i-overview.md) — transports, roles, security, vs skills.

### Automation chains

```text
Form submit → AI summarise → create Notion page → Slack notify
```

| Platform | Strength |
|----------|----------|
| **Zapier / Make** | No-code; many SaaS integrations |
| **n8n** | Self-host; technical teams |

Put **human approval** steps before external sends (email to customers, public posts).