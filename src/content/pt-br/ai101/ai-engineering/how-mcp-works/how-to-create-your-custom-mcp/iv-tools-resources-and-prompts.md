---
label: "IV"
subtitle: "Ferramentas, recursos e prompts"
group: "How to create your custom MCP"
order: 4
---
Ferramentas, recursos e prompts

## 1. Regras de design de ferramentas

| Regra | Por que |
|------|-----|
| **Nomes dos verbos** |`create_ticket`,`list_deployments`— intenção clara para LLM |
| **Descrições ricas** | O host mostra o nome + a descrição ao escolher as ferramentas – inclua “usar quando…” |
| **Pequenos insumos** | Prefiro`id`+`limit`sobre enormes bolhas aninhadas |
| **Saída limitada** | Listas truncadas (10–50 principais); resumir grandes cargas úteis |
| **Leitura/gravação explícita** | Descrição: “Somente leitura” ou “Cria um registro — requer confirmação do usuário em UI” |

### Validação de entrada

Use **Zod** (TypeScript) ou dicas de tipo (FastMCP) para que argumentos ruins falhem **antes** de sua chamada API:

```typescript
{
  issue_id: z.string().uuid(),
  comment: z.string().max(4000),
  dry_run: z.boolean().optional().default(false),
}
```

Retornar erros de validação como resultados da ferramenta com`isError: true`para que o modelo possa tentar novamente.

## 2. Forma do resultado da ferramenta

As ferramentas MCP retornam blocos de **conteúdo** — geralmente texto:

```typescript
return {
  content: [
    { type: "text", text: "Found 3 open incidents:\n1. ..." },
  ],
};
```

| Tipo de conteúdo | Usar |
|--------------|-----|
|`text`| JSON como string formatada, resumos humanos, logs |
|`image`| Base64 ou URL (quando o host suporta) |
|`resource`| Referência a um recurso URI |

Para dados estruturados, **JSON.stringify** em texto é adequado – o modelo os analisa no próximo turno.

### Erros que o modelo pode corrigir

```typescript
return {
  content: [{ type: "text", text: "Error: Project 'foo' not found. Use list_projects first." }],
  isError: true,
};
```

Evite rastreamentos de pilha na produção – registre no lado do servidor e retorne mensagens curtas.

## 3. Recursos (opcional)

Os recursos expõem conteúdo **legível** por URI — bom para runbooks, snippets de configuração e exportações em cache.

TypeScript (conceitual):

```typescript
server.resource(
  "runbook://checkout-failures",
  "Runbook for checkout payment failures",
  async (uri) => ({
    contents: [
      {
        uri: uri.href,
        mimeType: "text/markdown",
        text: await loadRunbook("checkout-failures"),
      },
    ],
  }),
);
```

| Ferramentas | Recursos |
|-------|-----------|
| Modelo **invoca** com parâmetros | Modelo ou usuário **lê** por URI |
| Pesquise, crie, altere | Documentos estáticos ou que mudam lentamente |

## 4. Solicitações (opcional)

Os prompts são **modelos nomeados** com argumentos — como comandos de barra:

```typescript
server.prompt(
  "incident-summary",
  { incident_id: z.string() },
  async ({ incident_id }) => ({
    messages: [
      {
        role: "user",
        content: {
          type: "text",
          text: `Summarize incident ${incident_id} using get_incident and list_timeline events.`,
        },
      },
    ],
  }),
);
```

A maioria dos servidores personalizados ignora os prompts até que as ferramentas estejam estáveis.

## 5. Múltiplas ferramentas relacionadas - conjunto de exemplos

| Ferramenta | Tipo | Trecho de descrição |
|------|------|---------------------|
|`list_projects`| Leia | Listar projetos que o usuário pode acessar. Ligue antes de outras ferramentas de projeto. |
|`get_issue`| Leia | Busque um problema por ID. |
|`search_issues`| Leia | Pesquise por string de consulta; máximo de 20 resultados. |
|`add_comment`| Escreva | Adicionar comentário ao problema – destrutivo. |

Dicas de pedido nas descrições (`Call list_projects first`) melhoram as execuções do agente em várias etapas.

## 6. Antipadrões

| Antipadrão | Correção |
|--------------|-----|
| Uma ferramenta que executa SQL arbitrariamente | Consultas parametrizadas ou IDs de relatório fixos |
|`run_shell`com festa completa | Nunca — ou comandos estritamente permitidos em uma sandbox |
| Retornando 10 MB JSON | Paginar, resumir o lado do servidor |
| Nomes de ferramentas que diferem apenas por caso | Atenha-se a Snake_case |

Consulte [Segurança e distribuição](vi-security-and-distribution.md) e [MCP vs conectores e segurança](../iv-mcp-vs-connectors-and-security.md).

## Próximo

[Teste e conecte em Cursor](v-test-and-wire-cursor.md) — execute o servidor em um IDE.
