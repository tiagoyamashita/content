---
label: "V"
subtitle: "Teste e conecte em Cursor"
group: "How to create your custom MCP"
order: 5
---
Teste e conecte em Cursor

## 1. MCP Inspetor (feedback mais rápido)

O **MCP Inspector** oficial fala com seu servidor via stdio sem Cursor:

```bash
npx @modelcontextprotocol/inspector node /absolute/path/to/my-mcp-server/dist/index.js
# Python:
npx @modelcontextprotocol/inspector python /absolute/path/to/my-mcp-server/server.py
```

| Inspetor UI | O que verificar |
|--------------|----------------|
| Guia **Ferramentas** | Todas as ferramentas listadas com esquemas |
| **Ferramenta de chamada** | Correr`echo`com argumentos de amostra - verifique a resposta |
| **Registros** | Erros JSON-RPC, rastreamentos de pilha |

Corrija erros de esquema e manipulador aqui antes de abrir Cursor.

```mermaid
flowchart LR
  Code[Your server] --> Inspector[MCP Inspector]
  Inspector --> Fix[Fix schema / handler]
  Fix --> Cursor[Wire mcp.json]
  Cursor --> Agent[Verify in agent]
```

## 2. Dicas de registro local

| Dica | Por que |
|-----|-----|
| **Nunca`console.log`para stdout** em servidores stdio | stdout é o fio JSON-RPC - corrompe o protocolo |
| Faça logon em **stderr** |`console.error(...)`-&#09;o`logging`para stderr é seguro |
| Nome da ferramenta de registro + duração | Depurar chamadas API lentas |

```typescript
console.error(`[get_issue] id=${issue_id} duration_ms=${Date.now() - t0}`);
```

## 3. Cursor`mcp.json`

Nível do projeto (comprometido com a equipe) -`.cursor/mcp.json`TÉCNICO.:

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

Python exemplo:

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

| Campo | Notas |
|-------|-------|
|`command`| Executável – use caminhos absolutos para venv`python`|
|`args`| Caminho do script como primeiro argumento |
|`env`| Segredos — prefira substituições no nível do usuário para chaves reais |

**A configuração global do usuário** também funciona: Cursor Configurações → MCP → adicionar servidor (mesmo formato).

Após salvar, **reinicie MCP** ou recarregue Cursor — então verifique o status de MCP em IDE.

## 4. Servidor TypeScript vinculado a npm

Durante o desenvolvimento:

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

Ou publique localmente:`npm link`e`"command": "my-mcp-server"`.

## 5. Verifique em Cursor

1. Abra o modo chat/agente.
2. Pergunte: *“Use a ferramenta de eco para dizer olá”* — ou uma ferramenta real como`search_issues`.
3. Confirme se o agente invoca seu servidor (chamada de ferramenta MCP em UI).
4. Se faltarem ferramentas: verifique se há erros de conexão no painel MCP.

| Sintoma | Correção |
|--------|-----|
| Servidor desconectado | Caminho errado; reconstruir`dist/`; faltando shebang`#!/usr/bin/env node`|
| Nenhuma ferramenta listada | Falha do servidor na inicialização – execute via Inspector |
| A chamada da ferramenta falha | registros stderr; retornar`isError`com mensagem |
| Ambiente não definido | Adicionar`env`bloquear; reiniciar MCP |

## 6. Claude Desktop (opcional)

`claude_desktop_config.json`(o caminho do macOS/Linux varia):

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

Mesmo binário de servidor — uma implementação, vários hosts.

## 7. Transporte HTTP (servidor de equipe)

Para MCP compartilhado remotamente, implante com Streamable HTTP de acordo com as especificações — fora do escopo da primeira versão; inicie o stdio localmente, extraia HTTP quando precisar de uma instância compartilhada. Consulte [JSON-RPC e transportes](../ii-json-rpc-and-transports.md).

## Próximo

[Segurança e distribuição](vi-security-and-distribution.md) — envie para sua equipe com segurança.
