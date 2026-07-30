---
label: "VI"
subtitle: "Security & distribution"
group: "How to create your custom MCP"
order: 6
---
Security & distribution

Custom MCP servers run **on the user’s machine** with whatever credentials you put in `env`. Treat them like small services with production hygiene.

## 1. Security checklist

| Risk | Mitigation |
|------|------------|
| **Leaked API keys** in `mcp.json` | Use env from OS secret store; `.gitignore` local overrides; document placeholders only in committed config |
| **Overpowered token** | Scoped API keys (read-only CRM, single GitHub repo) |
| **Prompt injection → tool abuse** | Narrow tools; no arbitrary code execution; confirm writes in UI ([Trust & verify](../../trust-privacy-and-verify/i-overview.md)) |
| **Path traversal** | If reading files, canonicalize paths and jail to allowlisted roots |
| **SSRF** | Do not pass user URLs straight to server-side `fetch` without allowlist |
| **Logging secrets** | Redact tokens in stderr logs |

MCP does not add permissions — your API token still only does what the upstream API allows.

## 2. Least-privilege tools

| Pattern | Example |
|---------|---------|
| Separate read vs write tools | `get_order` vs `cancel_order` — disable write server in low-trust contexts |
| Allowlisted actions | `rerun_job` only for job ids matching `^ci-\d+$` |
| Rate limiting | Throttle expensive API calls server-side |

## 3. README template for your repo

```markdown
# my-mcp-server

MCP server for [system]. Exposes tools: `list_x`, `get_x`, `create_x`.

## Env vars

| Variable | Required | Description |
|----------|----------|-------------|
| CRM_API_KEY | yes | Read-only CRM token |

## Cursor

Add to `.cursor/mcp.json` (see docs).

## Development

npm run build && npx @modelcontextprotocol/inspector node dist/index.js
```

## 4. Distribution options

| Method | Audience |
|--------|----------|
| **Git repo + `mcp.json` snippet** | Internal team |
| **npm** `npx -y @yourorg/my-mcp-server` | TS servers — same pattern as official MCP packages |
| **pip** + `uvx` | Python FastMCP packages |
| **Single binary** (Go/Rust) | Air-gapped or no Node/Python on host |

Published package example in `mcp.json`:

```json
{
  "mcpServers": {
    "crm": {
      "command": "npx",
      "args": ["-y", "@yourorg/crm-mcp-server"],
      "env": { "CRM_API_KEY": "..." }
    }
  }
}
```

## 5. Versioning and breaking changes

| Change | Practice |
|--------|----------|
| Rename tool | Major version bump; document migration |
| Add optional field | Minor — backward compatible |
| Remove tool | Major; warn in server startup log |

## 6. MCP vs Skills — when to add which

| Layer | Holds |
|-------|-------|
| **MCP server** | Live data, authenticated APIs, mutations |
| **Skill** | How your team wants the agent to use those tools ([Skills](../../skills-and-agent-instructions/i-overview.md)) |

Example: MCP exposes `search_logs`; a Skill says “always filter `env=prod` and last 1h unless user specifies otherwise.”

## 7. Operational monitoring

| Signal | Action |
|--------|--------|
| Tool latency | Log duration to stderr; alert on p95 |
| API 401/403 | Clear error text — “rotate CRM_API_KEY” |
| Crash on startup | CI job that runs Inspector headless against mock env |

## Related

- [How MCP works](../i-overview.md)
- [JSON-RPC & transports](../ii-json-rpc-and-transports.md)
- [MCP vs connectors & security](../iv-mcp-vs-connectors-and-security.md)
- [Agents & MCP wiring](../../agents-and-agentic-workflows/ii-chat-assistant-agent.md)
