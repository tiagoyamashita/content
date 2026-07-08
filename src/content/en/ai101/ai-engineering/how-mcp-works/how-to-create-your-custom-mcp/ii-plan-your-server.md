---
label: "II"
subtitle: "Plan your server"
group: "How to create your custom MCP"
order: 2
---
Plan your server

Before writing code, decide **what the agent may do** and **what it must never do**. MCP servers are small connectors — not full applications.

## 1. One server, one integration

| Good | Avoid |
|------|-------|
| `company-crm-mcp` — CRM search + create lead | One mega-server for CRM + GitHub + email + shell |
| `team-runbooks-mcp` — read internal wiki pages | Exposing every database table as a separate tool |
| `deploy-status-mcp` — query CI / release API | Passing raw SQL from the model with no guardrails |

Hosts list **all tools** from enabled servers. Fewer, clearer tools → better tool choice by the LLM.

## 2. Tools vs resources vs prompts

| MCP primitive | What it is | Example |
|---------------|------------|---------|
| **Tool** | Function the model **calls** with arguments | `search_issues`, `run_health_check` |
| **Resource** | **Readable** URI the user or model can fetch | `runbook://oncall/checkout` |
| **Prompt** | Pre-built **template** the host can insert | `summarize-incident` with slots |

**Start with tools only** — they cover 90% of custom integrations. Add resources when the agent should **read** stable documents; add prompts when you want reusable slash-command style templates.

## 3. Design each tool

For every tool, write a one-line spec before coding:

| Field | Question |
|-------|----------|
| **Name** | snake_case verb phrase — `get_order`, not `order` |
| **Description** | What it does **and when** the model should use it (hosts show this to the LLM) |
| **Inputs** | Minimal JSON schema — required vs optional |
| **Output** | Text summary for the model, or structured JSON as text |
| **Side effects** | Read-only vs writes — mark destructive tools clearly in the description |
| **Auth** | Which env var or config file supplies the API token |

```text
Tool: search_customers
Description: Search CRM by email or company name. Read-only. Use when user asks about a customer record.
Inputs: { "query": string, "limit"?: number }
Output: JSON array of { id, name, email } (max 10)
Auth: CRM_API_KEY from environment
```

## 4. Configuration and secrets

| Pattern | Use |
|---------|-----|
| **Environment variables** | API keys, base URLs — injected by host `mcp.json` |
| **Config file path** | `CONFIG_PATH` pointing at YAML the server reads at startup |
| **No secrets in repo** | Never commit tokens; document required env vars in README |

```json
"env": {
  "CRM_API_KEY": "from-your-secret-store",
  "CRM_BASE_URL": "https://crm.internal.example"
}
```

## 5. Transport choice

| Transport | When |
|-----------|------|
| **stdio** (default) | Local dev, Cursor, Claude Desktop — host spawns your process |
| **Streamable HTTP** | Team-hosted connector, shared service, remote agents |

This track focuses on **stdio** — fastest path to a working custom server. See [JSON-RPC & transports](../ii-json-rpc-and-transports.md) for HTTP deployment.

## 6. Checklist before coding

- [ ] Server name and version (`my-team-crm`, `1.0.0`)
- [ ] List of 1–8 tools with descriptions
- [ ] Env vars documented
- [ ] Read vs write tools identified; writes need human-in-the-loop in product UX where possible
- [ ] Error messages return **actionable text** (rate limit, 404, invalid id) — the model will read them

## Next

[Build with the SDK](iii-build-with-the-sdk.md) — scaffold TypeScript or Python.
