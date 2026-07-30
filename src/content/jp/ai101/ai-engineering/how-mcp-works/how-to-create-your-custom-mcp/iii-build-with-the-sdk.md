---
label: "III"
subtitle: "SDK を使用して構築する"
group: "How to create your custom MCP"
order: 3
---
SDK を使用して構築する

公式 SDK は JSON-RPC と stdio をラップするため、生のメッセージを解析する代わりに **ツール** を登録します。 **TypeScript** (実際に存在するほとんどの例) または **Python** (FastMCP — スクリプトとしては最速) を選択します。

## 1. TypeScript — プロジェクトの足場

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init --module NodeNext --moduleResolution NodeNext --target ES2022 --outDir dist
```

`package.json`— 実行するホストの bin エントリを追加します。

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

`src/index.ts`— 最小限のサーバー:

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

## 2. Python — FastMCP スキャフォールド

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

## 3. プロジェクトのレイアウト (いずれかの言語)

```text
my-mcp-server/
  README.md          # env vars, tools list, Cursor snippet
  package.json / pyproject.toml
  src/ or server.py
  .gitignore         # .env, node_modules, .venv
```

**ビジネス ロジック**を別のモジュールに保持します (`crm_client.ts`、`queries.py`) そのためハンドラーは薄いままになります。

## 4. ツールから外部 API を呼び出す

TypeScript パターン:

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

Python FastMCP — 使用する`httpx`または`requests`同じように;文字列を返すか、エラーが発生した場合に発生します。

## 5. SDK の選択

|選択 |いつ |
|------|------|
| **TypeScript** |チームはすでにノード上にあります。 npm に公開する。ミラーリング MCP 公式例 |
| **Python** |データ/運用スクリプト、FastAPI ショップ、最速のプロトタイプ |
| **その他** | Go/Rust SDK が存在します - バイナリ サイズやパフォーマンスが重要な場合に使用します |

＃＃ 次

[ツール、リソース、プロンプト](iv-tools-resources-and-prompts.md) - スキーマ、リソース、および応答形状。
