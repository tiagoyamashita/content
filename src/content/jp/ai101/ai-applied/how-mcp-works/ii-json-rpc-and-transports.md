---
label: "II"
subtitle: "JSON-RPC & transports"
group: "AI Applied"
order: 2
---
JSON-RPC & transports

## 1. One-sentence model

**MCP is not gRPC.** Messages are **JSON-RPC 2.0** (structured JSON requests/responses) sent over **stdio** (local) or **HTTP** (remote). The MCP server then talks to the real system — often a normal **REST/HTTPS API**.

```text
You → AI host (Cursor) → MCP client → MCP server → Linear/Postgres/Slack API
                         JSON-RPC          HTTPS
```

## 2. Three roles

| Role | What it is | Example |
|------|------------|---------|
| **Host** | App you use | Cursor, Claude Desktop, VS Code + extension |
| **MCP client** | Built into the host; speaks MCP | Cursor’s MCP layer |
| **MCP server** | Connector you install/configure | `github`, `postgres`, `@modelcontextprotocol/server-*` |

You only configure **servers** in settings. The host runs the **client** for you.

## 3. Wire protocol: JSON-RPC, not gRPC

### What is JSON-RPC?

**JSON-RPC** is a small, standard way to say **“run this function remotely, here are the arguments, give me back a result”** — with everything encoded as **JSON text**.

| Word | Meaning |
|------|---------|
| **JSON** | The message body is plain JSON you can read in a log |
| **RPC** | **Remote procedure call** — caller invokes a **named method** on another process, like calling a function over a pipe or HTTP |

Think of it as a **thin envelope**, not a full REST API design:

```text
Request:  "Please run method X with params Y"  (one JSON object)
Response: "Here is result Z" or "Error: …"       (one JSON object)
```

It is **not** the same as:

| | JSON-RPC (MCP wire) | REST API (Linear, GitHub) |
|---|---------------------|---------------------------|
| **Style** | Named **methods** (`tools/call`) | **URLs** + HTTP verbs (`GET /issues`) |
| **Who uses it** | MCP **client ↔ MCP server** | MCP **server ↔ external SaaS** |
| **You configure** | Rarely — host handles it | Tokens, base URLs in server config |

MCP picked JSON-RPC because it is **simple**, **human-readable**, and works over **stdio pipes** (one JSON line in, one JSON line out) without inventing a custom binary protocol.

### Request and response shape

Every message is a JSON object with a few fixed fields:

**Request** (client → server):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_issues",
    "arguments": { "query": "checkout bug" }
  }
}
```

| Field | Role |
|-------|------|
| `jsonrpc` | Always `"2.0"` — protocol version |
| `id` | Correlates request with response (like a request ID) |
| `method` | **Which remote function** to run (MCP defines names like `tools/call`, `tools/list`) |
| `params` | Arguments for that method |

**Response** (server → client) — success:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "[{\"id\": 42, \"title\": \"Checkout timeout\"}]" }
    ]
  }
}
```

**Response** — failure:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Linear API rate limited"
  }
}
```

| Field | Role |
|-------|------|
| `result` | Payload on success — for MCP tools, often **text or structured content** |
| `error` | Payload on failure — code + message (no `result`) |

The **host** sends JSON-RPC to the MCP server; the **LLM never parses JSON-RPC**. It only sees the **tool result** the host extracts from `result` and drops into the chat.

### JSON-RPC vs gRPC (why MCP did not pick gRPC)

| | MCP (JSON-RPC) | gRPC (for comparison) |
|---|----------------|------------------------|
| **Message format** | **JSON text** | Protobuf (binary) |
| **Typical transport** | stdio pipes or **HTTP POST** | HTTP/2 |
| **Human readable** | Yes — easy to debug in logs | No — encoded binary |
| **Standard in MCP spec** | Yes | **Not used** by MCP |

The model does not send raw HTTP to Linear. It asks the **host** to run an MCP **tool**; the host sends **JSON-RPC** to the MCP server; the server implements that tool and may call Linear’s **HTTPS REST API** with your token.

## 4. Two standard transports

The [MCP specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) defines how JSON-RPC moves between client and server.

### stdio (local — most common in IDEs)

```text
Host spawns MCP server as subprocess
  Client writes JSON-RPC → server's stdin
  Server writes JSON-RPC → server's stdout
```

| Used when | Examples |
|-----------|----------|
| Server runs **on your machine** | Cursor, Claude Desktop local config |
| Server is a **script or binary** | `npx @modelcontextprotocol/server-filesystem` |

| Pros | Cons |
|------|------|
| Simple; no open ports | Server must be installed locally |
| Good for secrets on laptop | One server process per config entry |

**Cursor `mcp.json` (conceptual):**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "..." }
    }
  }
}
```

Host **starts** the process; communication is **pipes**, not you clicking a URL.

### Streamable HTTP (remote)

For servers running as a **web service** (team-hosted connector, SaaS MCP):

```text
Client → HTTP POST (JSON-RPC body) → https://your-company.com/mcp
Server → JSON response OR SSE stream (Server-Sent Events)
```

| Piece | Detail |
|-------|--------|
| **POST** | Each client message can be a POST to one **MCP endpoint** (e.g. `/mcp`) |
| **GET** | Optional — open **SSE** stream so server can push notifications |
| **Headers** | `Mcp-Protocol-Version`, `Mcp-Session-Id` for versioning/sessions |
| **Auth** | Usually Bearer token or OAuth on HTTPS — same as any API |

This is **plain HTTP(S)** — load balancers, API gateways, and corporate proxies often work without gRPC support.

**Older transport:** early MCP used **HTTP + SSE** (two endpoints). New implementations should use **Streamable HTTP**; some stacks support both for compatibility.