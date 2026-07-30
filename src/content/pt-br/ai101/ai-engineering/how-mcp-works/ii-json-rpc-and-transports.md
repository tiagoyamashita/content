---
label: "II"
subtitle: "JSON-RPC e transportes"
group: "AI Applied"
order: 2
---
JSON-RPC e transportes

## 1. Modelo de uma frase

**MCP não é gRPC.** As mensagens são **JSON-RPC 2.0** (solicitações/respostas JSON estruturadas) enviadas por **stdio** (local) ou **HTTP** (remoto). O servidor MCP então se comunica com o sistema real - geralmente um **REST/HTTPS API** normal.

```mermaid
flowchart LR
  You --> Host[AI host]
  Host <-->|JSON-RPC| Client[MCP client]
  Client <-->|stdio / HTTP| Server[MCP server]
  Server -->|HTTPS| API[Linear / Postgres / Slack]
```

## 2. Três funções

| Função | O que é | Exemplo |
|------|------------|--------|
| **Anfitrião** | Aplicativo que você usa | Cursor, Claude Desktop, VS Código + extensão |
| **MCP cliente** | Integrado ao host; fala MCP | Camada MCP de Cursor |
| **MCP servidor** | Conector que você instala/configura |`github`,`postgres`,`@modelcontextprotocol/server-*`|

Você só configura **servidores** nas configurações. O host executa o **cliente** para você.

## 3. Protocolo de transmissão: JSON-RPC, não gRPC

### O que é JSON-RPC?

**JSON-RPC** é uma maneira pequena e padrão de dizer **“execute esta função remotamente, aqui estão os argumentos, devolva-me um resultado”** — com tudo codificado como texto **JSON**.

| Palavra | Significado |
|------|---------|
| **JSON** | O corpo da mensagem é simples JSON você pode ler em um log |
| **RPC** | **Chamada de procedimento remoto** — o chamador invoca um **método nomeado** em outro processo, como chamar uma função através de um canal ou HTTP |

Pense nisso como um **envelope fino**, não como um design REST API completo:

```text
Request:  "Please run method X with params Y"  (one JSON object)
Response: "Here is result Z" or "Error: …"       (one JSON object)
```

**não** é o mesmo que:

| | JSON-RPC (fio MCP) | REST API (Linear, GitHub) |
|---|---------------------|--------------------------|
| **Estilo** | **métodos** nomeados (`tools/call`) | **URLs** + verbos HTTP (`GET /issues`) |
| **Quem usa** | MCP **cliente ↔ MCP servidor** | MCP **servidor ↔ SaaS externo** |
| **Você configura** | Raramente – o host cuida disso | Tokens, URLs base na configuração do servidor |

MCP escolheu JSON-RPC porque é **simples**, **legível por humanos** e funciona em **tubos stdio** (uma entrada de linha JSON, uma saída de linha JSON) sem inventar um protocolo binário personalizado.

### Formulário de solicitação e resposta

Cada mensagem é um objeto JSON com alguns campos fixos:

**Solicitação** (cliente → servidor):

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

| Campo | Função |
|-------|------|
|`jsonrpc`| Sempre`"2.0"`— versão do protocolo |
|`id`| Correlaciona solicitação com resposta (como uma solicitação ID) |
|`method`| **Qual função remota** executar (MCP define nomes como`tools/call`,`tools/list`) |
|`params`| Argumentos para esse método |

**Resposta** (servidor → cliente) — sucesso:

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

**Resposta** — falha:

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

| Campo | Função |
|-------|------|
|`result`| Carga útil em caso de sucesso — para ferramentas MCP, geralmente **texto ou conteúdo estruturado** |
|`error`| Carga útil em caso de falha — código + mensagem (não`result`) |

O **host** envia JSON-RPC para o servidor MCP; o **LLM nunca analisa JSON-RPC**. Ele vê apenas o **resultado da ferramenta** do qual o host extrai`result`e entra no chat.

### JSON-RPC vs gRPC (por que MCP não escolheu gRPC)

| | MCP (JSON-RPC) | gRPC (para comparação) |
|---|----------------|---------|
| **Formato da mensagem** | **JSON texto** | Protobuf (binário) |
| **Transporte típico** | tubos stdio ou **HTTP POST** | HTTP/2 |
| **Legível por humanos** | Sim — fácil de depurar em logs | Não — binário codificado |
| **Padrão na especificação MCP** | Sim | **Não usado** por MCP |

O modelo não envia HTTP bruto para Linear. Ele pede ao **host** para executar uma MCP **ferramenta**; o host envia **JSON-RPC** para o servidor MCP; o servidor implementa essa ferramenta e pode chamar **HTTPS REST API** da Linear com seu token.

## 4. Dois transportes padrão

A [especificação MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) define como JSON-RPC se move entre cliente e servidor.

### stdio (local — mais comum em IDEs)

```text
Host spawns MCP server as subprocess
  Client writes JSON-RPC → server's stdin
  Server writes JSON-RPC → server's stdout
```

| Usado quando | Exemplos |
|-----------|----------|
| O servidor é executado **na sua máquina** | Cursor, configuração local do Claude Desktop |
| O servidor é um **script ou binário** |`npx @modelcontextprotocol/server-filesystem`|

| Prós | Contras |
|------|------|
| Simples; sem portas abertas | O servidor deve ser instalado localmente |
| Bom para segredos no laptop | Um processo de servidor por entrada de configuração |

**Cursor`mcp.json`(conceptual):**

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

O host **inicia** o processo; a comunicação é **pipes**, e não você clicar em URL.

### Streamable HTTP (remoto)

Para servidores executados como um **serviço web** (conector hospedado em equipe, SaaS MCP):

```text
Client → HTTP POST (JSON-RPC body) → https://your-company.com/mcp
Server → JSON response OR SSE stream (Server-Sent Events)
```

| Peça | Detalhe |
|-------|--------|
| **POST** | Cada mensagem do cliente pode ser um POST para um endpoint **MCP** (por exemplo`/mcp`) |
| **GET** | Opcional - abra o fluxo **SSE** para que o servidor possa enviar notificações |
| **Cabeçalhos** |`Mcp-Protocol-Version`,`Mcp-Session-Id`para versionamento/sessões |
| **Autorização** | Normalmente token portador ou OAuth em HTTPS — igual a qualquer API |

Isso é **simples HTTP(S)** — balanceadores de carga, gateways API e proxies corporativos geralmente funcionam sem suporte gRPC.

**Transporte mais antigo:** MCP inicial usado **HTTP + SSE** (dois pontos de extremidade). Novas implementações devem usar **Streamable HTTP**; algumas pilhas suportam ambos para compatibilidade.