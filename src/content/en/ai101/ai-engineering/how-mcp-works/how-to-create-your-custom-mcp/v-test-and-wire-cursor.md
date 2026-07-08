---
label: "V"
subtitle: "Test & wire into Cursor"
group: "How to create your custom MCP"
order: 5
---
Test & wire into Cursor

## 1. MCP Inspector (fastest feedback)

The official **MCP Inspector** talks to your server over stdio without Cursor:

```bash
npx @modelcontextprotocol/inspector node /absolute/path/to/my-mcp-server/dist/index.js
# Python:
npx @modelcontextprotocol/inspector python /absolute/path/to/my-mcp-server/server.py
```

| Inspector UI | What to verify |
|--------------|----------------|
| **Tools** tab | All tools listed with schemas |
| **Call tool** | Run `echo` with sample args — check response |
| **Logs** | JSON-RPC errors, stack traces |

Fix schema and handler bugs here before opening Cursor.

## 2. Local logging tips

| Tip | Why |
|-----|-----|
| **Never `console.log` to stdout** in stdio servers | stdout is the JSON-RPC wire — corrupts protocol |
| Log to **stderr** | `console.error(...)` / `logging` to stderr is safe |
| Log tool name + duration | Debug slow API calls |

```typescript
console.error(`[get_issue] id=${issue_id} duration_ms=${Date.now() - t0}`);
```

## 3. Cursor `mcp.json`

Project-level (committed for team) — `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["/absolute/path/to/my-mcp-server/dist/index.js"],
      "env": {
        "CRM_API_KEY": "your-key-here"
      }
    }
  }
}
```

Python example:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "/absolute/path/to/my-mcp-server/.venv/bin/python",
      "args": ["/absolute/path/to/my-mcp-server/server.py"],
      "env": {
        "CRM_API_KEY": "your-key-here"
      }
    }
  }
}
```

| Field | Notes |
|-------|-------|
| `command` | Executable — use absolute paths for venv `python` |
| `args` | Script path as first arg |
| `env` | Secrets — prefer user-level overrides for real keys |

**User-global** config also works: Cursor Settings → MCP → add server (same shape).

After saving, **restart MCP** or reload Cursor — then check MCP status in the IDE.

## 4. npm-linked TypeScript server

During development:

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "npx",
      "args": ["-y", "tsx", "/path/to/my-mcp-server/src/index.ts"],
      "env": { "CRM_API_KEY": "..." }
    }
  }
}
```

Or publish locally: `npm link` and `"command": "my-mcp-server"`.

## 5. Verify in Cursor

1. Open chat / agent mode.
2. Ask: *“Use the echo tool to say hello”* — or a real tool like `search_issues`.
3. Confirm the agent invokes your server (MCP tool call in UI).
4. If tools missing: check MCP panel for connection errors.

| Symptom | Fix |
|---------|-----|
| Server disconnected | Wrong path; rebuild `dist/`; missing shebang `#!/usr/bin/env node` |
| No tools listed | Server crash on startup — run via Inspector |
| Tool call fails | stderr logs; return `isError` with message |
| Env not set | Add `env` block; restart MCP |

## 6. Claude Desktop (optional)

`claude_desktop_config.json` (macOS/Linux path varies):

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["/path/to/dist/index.js"]
    }
  }
}
```

Same server binary — one implementation, multiple hosts.

## 7. HTTP transport (team server)

For remote shared MCP, deploy with Streamable HTTP per spec — out of scope for first version; start stdio locally, extract HTTP when you need a shared instance. See [JSON-RPC & transports](../ii-json-rpc-and-transports.md).

## Next

[Security & distribution](vi-security-and-distribution.md) — ship to your team safely.
