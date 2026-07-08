---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
How MCP works — overview
Deep dive on **how mcp works** — split into focused notes below.

## Map of this submenu

| Note | Focus |
|------|--------|
| [JSON-RPC & transports](ii-json-rpc-and-transports.md) | Part of how mcp works track |
| [End-to-end flow & LLM](iii-end-to-end-flow-and-llm.md) | Part of how mcp works track |
| [MCP vs connectors & security](iv-mcp-vs-connectors-and-security.md) | Part of how mcp works track |
| [Vector DB, skills & reference](v-vector-db-skills-and-reference.md) | Part of how mcp works track |
| **[How to create your custom MCP](how-to-create-your-custom-mcp/i-overview.md)** | Plan, build, test, and ship your own MCP server |

How MCP works
**MCP (Model Context Protocol)** is how tools like **Cursor**, **Claude Desktop**, and **Claude Code** plug into **external systems** — databases, GitHub, Linear, Sentry — through small **connector programs** called **MCP servers**.

You configure them once; the agent **calls tools** the server exposes. This note explains **how that connection works** — API, gRPC, or something else.

## Study order

[JSON-RPC & transports](ii-json-rpc-and-transports.md) → [End-to-end flow & LLM](iii-end-to-end-flow-and-llm.md) → [MCP vs connectors & security](iv-mcp-vs-connectors-and-security.md) → [Vector DB, skills & reference](v-vector-db-skills-and-reference.md)

**Build your own:** [How to create your custom MCP](how-to-create-your-custom-mcp/i-overview.md) — after you understand transports and the end-to-end flow.
