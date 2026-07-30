---
label: "I"
subtitle: "Visão geral"
group: "AI Applied"
order: 1
---
Solicitação eficaz – visão geral
Aprofunde-se em **solicitações eficazes** — divida em notas específicas abaixo.

## Mapa deste submenu

| Nota | Foco |
|------|--------|
| [Prompt mínimo e técnicas](ii-minimum-prompt-and-techniques.md) | Parte do caminho de estímulo eficaz |
| [Iteração e modelos](iii-iteration-and-templates.md) | Parte do caminho de estímulo eficaz |
| [Instruções e erros do sistema](iv-system-instructions-and-mistakes.md) | Parte do caminho de estímulo eficaz |

Solicitação eficaz
**Avisar** é como você orienta ChatGPT, Claude, Gemini e ferramentas semelhantes. Você não está “programando” o modelo – você está **especificando a tarefa** para que o modelo tenha contexto suficiente para ajudar uma vez, e não após cinco tentativas.

Para detalhes de nível API (funções, modo JSON), consulte [engenharia de prompt LLM](../../llms/iv-prompt-engineering.md). Esta nota é para **uso diário**.

```mermaid
flowchart LR
  Role[Role] --> Task --> Constraints --> Format[Output format]
  Format --> Model[Model reply]
```

Quando um prompt funcionar repetidamente, promova-o para instruções persistentes — consulte [Solicitação de loop](../loop-prompting/i-overview.md).

## Ordem de estudo

[Prompt mínimo e técnicas](ii-minimum-prompt-and-techniques.md) → [Iteração e modelos](iii-iteration-and-templates.md) → [Instruções e erros do sistema](iv-system-instructions-and-mistakes.md) → [Solicitação de loop](../loop-prompting/i-overview.md)
