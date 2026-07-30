---
label: "III"
subtitle: "Construa com o SDK"
group: "How to create your custom MCP"
order: 3
---
Construa com o SDK

Os SDKs oficiais agrupam JSON-RPC e stdio para que você registre **ferramentas** em vez de analisar mensagens brutas. Escolha **TypeScript** (a maioria dos exemplos disponíveis) ou **Python** (FastMCP — mais rápido para scripts).

## 1. TypeScript – estrutura do projeto

```bash
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init --module NodeNext --moduleResolution NodeNext --target ES2022 --outDir dist
```

`package.json`— adicione entrada bin para o host executar:

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

`src/index.ts`— servidor mínimo:

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

## 2. Python — Andaime rápidoMCP

```bash
mkdir my-mcp-server && cd my-mcp-server
python3 -m venv .venv
source .venv/bin/activate
pip install "mcp[cli]"
```

`server.py`TÉCNICO.:

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

## 3. Layout do projeto (qualquer idioma)

```text
my-mcp-server/
  README.md          # env vars, tools list, Cursor snippet
  package.json / pyproject.toml
  src/ or server.py
  .gitignore         # .env, node_modules, .venv
```

Mantenha a **lógica de negócios** em módulos separados (`crm_client.ts`,`queries.py`) para que os manipuladores permaneçam magros.

## 4. Chamando um API externo de uma ferramenta

Padrão TypeScript:

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

Python RápidoMCP - usar`httpx`ou`requests`da mesma forma; retornar strings ou aumentar em caso de erros.

## 5. SDK escolha

| Escolha | Quando |
|------|------|
| **TypeScript** | Equipe já no Node; publicação no npm; espelhando exemplos oficiais de MCP |
| **Python** | Scripts de dados/operações, lojas FastAPI, protótipo mais rápido |
| **Outros** | Existem SDKs Go/Rust — use quando o tamanho binário ou o desempenho são importantes |

## Próximo

[Ferramentas, recursos e instruções](iv-tools-resources-and-prompts.md) — esquemas, recursos e formas de resposta.
