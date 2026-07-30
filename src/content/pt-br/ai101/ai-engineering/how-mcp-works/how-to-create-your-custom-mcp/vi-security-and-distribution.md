---
label: "VI"
subtitle: "Segurança e distribuição"
group: "How to create your custom MCP"
order: 6
---
Segurança e distribuição

Servidores MCP personalizados são executados **na máquina do usuário** com quaisquer credenciais que você inserir`env`. Trate-os como pequenos serviços com higiene de produção.

## 1. Lista de verificação de segurança

| Risco | Mitigação |
|------|------------|
| **Chaves API vazadas** em`mcp.json`| Use env do armazenamento secreto OS;`.gitignore`substituições locais; espaços reservados para documentos apenas na configuração confirmada |
| **Token sobrecarregado** | Chaves API com escopo (CRM somente leitura, repositório GitHub único) |
| **Injeção imediata → abuso de ferramenta** | Ferramentas estreitas; nenhuma execução arbitrária de código; confirmar gravações em UI ([Confiar e verificar](../../trust-privacy-and-verify/i-overview.md)) |
| **Travessia de caminho** | Se estiver lendo arquivos, canonize os caminhos e prenda nas raízes da lista de permissões |
| **SSRF** | Não passe URLs de usuários diretamente para o lado do servidor`fetch`sem lista de permissões |
| **Segredos de registro** | Editar tokens em logs stderr |

MCP não adiciona permissões — seu token API ainda faz apenas o que o API upstream permite.

## 2. Ferramentas com menos privilégios

| Padrão | Exemplo |
|--------|---------|
| Ferramentas separadas de leitura e gravação |`get_order`contra`cancel_order`— desabilitar servidor de gravação em contextos de baixa confiança |
| Ações permitidas |`rerun_job`apenas para correspondência de IDs de trabalho`^ci-\d+$`|
| Limitação de taxa | Acelerar chamadas API caras do lado do servidor |

## 3. Modelo README para seu repositório

```markdown
# my-mcp-server

MCP server for [system]. Exposes tools: `list_x`, `get_x`, `create_x`.

## Env vars

| Variable | Required | Description |
|----------|----------|-------------|
| CRM_API_KEY | yes | Read-only CRM token |

## Cursor

Add to `.cursor/mcp.json` (see docs).

## Development

npm run build && npx @modelcontextprotocol/inspector node dist/index.js
```

## 4. Opções de distribuição

| Método | Público |
|--------|----------|
| **Git repositório +`mcp.json`trecho** | Equipe interna |
| **npm**`npx -y @yourorg/my-mcp-server`| Servidores TS — mesmo padrão dos pacotes MCP oficiais |
| ** pip ** +`uvx`| Pacotes Python RápidoMCP |
| **Binário único** (Go/Rust) | Air gap ou nenhum nó/Python no host |

Exemplo de pacote publicado em`mcp.json`TÉCNICO.:

```json
{
  "mcpServers": {
    "crm": {
      "command": "npx",
      "args": ["-y", "@yourorg/crm-mcp-server"],
      "env": { "CRM_API_KEY": "..." }
    }
  }
}
```

## 5. Controle de versão e alterações significativas

| Alterar | Prática |
|--------|----------|
| Ferramenta renomear | Aumento da versão principal; migração de documentos |
| Adicionar campo opcional | Menor — compatível com versões anteriores |
| Remover ferramenta | Principal; avisa no log de inicialização do servidor |

## 6. MCP vs Habilidades — quando adicionar quais

| Camada | Detém |
|-------|-------|
| **MCP servidor** | Dados ativos, APIs autenticados, mutações |
| **Habilidade** | Como sua equipe deseja que o agente use essas ferramentas ([Habilidades](../../skills-and-agent-instructions/i-overview.md)) |

Exemplo: MCP expõe`search_logs`; uma Skill diz “sempre filtrar`env=prod`e dura 1h, a menos que o usuário especifique o contrário.”

## 7. Monitoramento operacional

| Sinal | Ação |
|--------|--------|
| Latência da ferramenta | Duração do registro em stderr; alerta na p95 |
| API 401/403 | Limpar texto de erro – “girar CRM_API_KEY” |
| Falha na inicialização | CI trabalho que executa o Inspector headless em um ambiente simulado |

## Relacionado

- [Como MCP funciona](../i-overview.md)
- [JSON-RPC & transportes](../ii-json-rpc-and-transports.md)
- [MCP vs conectores e segurança](../iv-mcp-vs-connectors-and-security.md)
- [Agentes e fiação MCP](../../agents-and-agentic-workflows/ii-chat-assistant-agent.md)
