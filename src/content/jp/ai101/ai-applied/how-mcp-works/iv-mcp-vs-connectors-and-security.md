---
label: "IV"
subtitle: "MCP vs connectors & security"
group: "AI Applied"
order: 4
---
MCP vs connectors & security

## 8. MCP vs “built-in connector” vs REST

| Approach | Who builds it | Wire to AI host |
|----------|---------------|-----------------|
| **MCP server** | Community or vendor | JSON-RPC (stdio/HTTP) |
| **Native integration** | ChatGPT/Anthropic/Microsoft | Vendor-specific API |
| **Custom REST in your app** | Your backend | Your code — not MCP unless you wrap it |

MCP’s value is **one connector format** many hosts can reuse — same GitHub server for Cursor and Claude Desktop.

## 9. Security (user checklist)

| Risk | Mitigation |
|------|------------|
| MCP server has **API keys** | Env vars; never commit tokens; rotate |
| **Over-broad tools** | Enable only servers you need |
| **Remote MCP URL** | HTTPS only; trust the provider |
| **stdio server runs locally** | It can read files/shell per its design — read server docs |
| **Prompt injection → tool abuse** | Limit scopes; review agent actions ([Trust & verify](../trust-privacy-and-verify/i-overview.md)) |

MCP does not replace **permission models** of underlying APIs — your GitHub token still only does what GitHub allows.