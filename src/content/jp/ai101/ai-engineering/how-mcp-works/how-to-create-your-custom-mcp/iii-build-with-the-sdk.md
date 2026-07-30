---
label: "III"
subtitle: "Build with the SDK"
group: "How to create your custom MCP"
order: 3
---
Build with the SDK

Official SDKs wrap JSON-RPC and stdio so you register **tools** instead of parsing raw messages. Pick **TypeScript** (most examples in the wild) or **Python** (FastMCP — fastest for scripts).

## 1. TypeScript — project scaffold

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init --module NodeNext --moduleResolution NodeNext --target ES2022 --outDir dist
```

`package.json` — add bin entry for the host to run:

```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": { "my-mcp-server": "./dist/index.js" },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  }
}
```

`src/index.ts` — minimal server:

```typescript
#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0",
});

server.tool(
  "echo",
  "Echo text back — smoke test for wiring.",
  { message: z.string().describe("Text to echo") },
  async ({ message }) => ({
    content: [{ type: "text", text: message }],
  }),
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

```bash
npm run build
node dist/index.js
# Blocks with no output — waiting for JSON-RPC on stdin (correct for stdio)
```

## 2. Python — FastMCP scaffold

```bash
mkdir my-mcp-server && cd my-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]"
```

`server.py`:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-mcp-server")


@mcp.tool()
def echo(message: str) -> str:
    """Echo text back — smoke test for wiring."""
    return message


if __name__ == "__main__":
    mcp.run()
```

```bash
python server.py
# Blocks — stdio transport active
```

## 3. Project layout (either language)

```text
my-mcp-server/
  README.md          # env vars, tools list, Cursor snippet
  package.json / pyproject.toml
  src/ or server.py
  .gitignore         # .env, node_modules, .venv
```

Keep **business logic** in separate modules (`crm_client.ts`, `queries.py`) so handlers stay thin.

## 4. Calling an external API from a tool

TypeScript pattern:

```typescript
server.tool(
  "get_weather",
  "Get current weather for a city. Read-only.",
  { city: z.string() },
  async ({ city }) => {
    const key = process.env.WEATHER_API_KEY;
    if (!key) {
      return {
        content: [{ type: "text", text: "Error: WEATHER_API_KEY not set" }],
        isError: true,
      };
    }
    const res = await fetch(
      `https://api.example.com/weather?city=${encodeURIComponent(city)}`,
      { headers: { Authorization: `Bearer ${key}` } },
    );
    if (!res.ok) {
      return {
        content: [{ type: "text", text: `API error: ${res.status} ${await res.text()}` }],
        isError: true,
      };
    }
    const data = await res.json();
    return {
      content: [{ type: "text", text: JSON.stringify(data, null, 2) }],
    };
  },
);
```

Python FastMCP — use `httpx` or `requests` the same way; return strings or raise for errors.

## 5. SDK choice

| Pick | When |
|------|------|
| **TypeScript** | Team already on Node; publishing to npm; mirroring MCP official examples |
| **Python** | Data/ops scripts, FastAPI shops, quickest prototype |
| **Other** | Go/Rust SDKs exist — use when binary size or performance matters |

## Next

[Tools, resources & prompts](iv-tools-resources-and-prompts.md) — schemas, resources, and response shapes.
