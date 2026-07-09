---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
How MCP works — overview
Deep dive on **how mcp works** — split into focused notes below.

## Map of this submenu

```mermaid
flowchart TD
  Root["📁 How MCP works"]
  II["📄 JSON-RPC & transports"]
  III["📄 End-to-end flow & LLM"]
  IV["📄 MCP vs connectors & security"]
  V["📄 Vector DB, skills & reference"]
  Nested["📁 How to create your custom MCP"]
  Root --> II
  Root --> III
  Root --> IV
  Root --> V
  Root --> Nested
  Nested --> N1["📄 Plan your server"]
  Nested --> N2["📄 Build with the SDK"]
  Nested --> N3["📄 Tools, resources & prompts"]
  Nested --> N4["📄 Test & wire into Cursor"]
  Nested --> N5["📄 Security & distribution"]
  click II "ii-json-rpc-and-transports.md" "Open note"
  click III "iii-end-to-end-flow-and-llm.md" "Open note"
  click IV "iv-mcp-vs-connectors-and-security.md" "Open note"
  click V "v-vector-db-skills-and-reference.md" "Open note"
  click Nested "how-to-create-your-custom-mcp/i-overview.md" "Open folder overview"
  click N1 "how-to-create-your-custom-mcp/ii-plan-your-server.md" "Open note"
  click N2 "how-to-create-your-custom-mcp/iii-build-with-the-sdk.md" "Open note"
  click N3 "how-to-create-your-custom-mcp/iv-tools-resources-and-prompts.md" "Open note"
  click N4 "how-to-create-your-custom-mcp/v-test-and-wire-cursor.md" "Open note"
  click N5 "how-to-create-your-custom-mcp/vi-security-and-distribution.md" "Open note"
```

Click a node to open that note (GitHub / Mermaid Live). If clicks are disabled in your viewer, use the sidebar or search.

How MCP works
**MCP (Model Context Protocol)** is how tools like **Cursor**, **Claude Desktop**, and **Claude Code** plug into **external systems** — databases, GitHub, Linear, Sentry — through small **connector programs** called **MCP servers**.

You configure them once; the agent **calls tools** the server exposes. This note explains **how that connection works** — API, gRPC, or something else.

## Study order

[JSON-RPC & transports](ii-json-rpc-and-transports.md) → [End-to-end flow & LLM](iii-end-to-end-flow-and-llm.md) → [MCP vs connectors & security](iv-mcp-vs-connectors-and-security.md) → [Vector DB, skills & reference](v-vector-db-skills-and-reference.md)

**Build your own:** [How to create your custom MCP](how-to-create-your-custom-mcp/i-overview.md) — after you understand transports and the end-to-end flow.
