---
label: "II"
subtitle: "One-shot vs loop"
group: "AI Applied"
order: 2
---
One-shot vs loop
**Avisos únicos** tratam cada bate-papo como uma folha em branco. **Avisos de loop** pressupõem que a maior parte do briefing já está em algum lugar durável — sua função em cada turno é **dirigir**, não **rebrief**.

## 1. Hábito único (ainda comum)

```text
Open new chat
  → paste role paragraph
  → paste constraints
  → attach files
  → ask task
  → get answer
  → tomorrow: repeat everything
```

| Custo | Detalhe |
|------|--------|
| **Tempo** | Minutos de configuração por sessão |
| **Desvio de qualidade** | Redação de ontem ≠ de hoje |
| **Iteração perdida** | Bons refinamentos presos em fios antigos |
| **Desperdício de tokens** | O mesmo contexto reenvia todas as mensagens |

One-shot é adequado para tarefas **verdadeiramente novas**. É caro para trabalhos **recorrentes** (relatórios semanais, revisões PR, respostas de suporte, edições de documentos).

## 2. Hábito de loop

```mermaid
flowchart LR
  Setup[Set up once] --> T1[Turn 1: draft]
  T1 --> T2[Turn 2: fix section]
  T2 --> T3[Turn 3: change format]
  T3 --> T4[Next week: new file]
```

Cada turno é um **delta** — uma correção, um novo anexo ou uma entrada alterada — e não um prompt do sistema reconstruído.

## 3. Lado a lado

| Dimensão | Um tiro | Laço |
|-----------|----------|------|
| **Configuração por sessão** | Prompt completo | A maior parte já está armazenada |
| **Tamanho típico da mensagem** | Longo | Curto |
| **Localização de contexto** | Somente bate-papo | Projeto + bate-papo |
| **Melhor para** | Isolamento único e sensível | Fluxos de trabalho repetidos, mesmos padrões |
| **Modo de falha** | Resultados inconsistentes | Contexto armazenado obsoleto ou errado |

## 4. O loop de iteração (humano)

De [Solicitação efetiva - iteração](../effective-prompting/iii-iteration-and-templates.md), atualizado:

```text
1. Rough ask (context already loaded)
2. Specific fix (“table 2 wrong source”)
3. One constraint per turn
4. Save what worked → skill or template (not just chat history)
```

**Regra de loop:** se você digitou o mesmo parágrafo duas vezes esta semana, **promova-o** para instruções persistentes — consulte [Instruções persistentes](iii-persistent-instructions.md).

## 5. Loop não é “nunca começar do zero”

| Inicie um **novo** bate-papo quando… | **Continue** o loop quando… |
|----------------------------|------------------------------------------|
| Tópico ou público mudou completamente | Mesma entrega ou fluxo de trabalho |
| O contexto está poluído com suposições erradas | Refinando a qualidade da saída |
| Você precisa de isolamento (confusão confidencial) | Agente já leu os arquivos corretos |
| Modelo preso em um padrão ruim | Pequenas correções direcionadas funcionam |

## 6. Relação com agentes

| | Solicitação de loop | Agentes |
|---|----------------|--------|
| **Foco** | Não reflita; iterar barato | Muitos passos + ferramentas em direção a um objetivo |
| **Sua opinião** | Direção curta | Meta + limites + pontos de verificação |
| **Sobreposição** | Sessões de agente *são* loops quando o contexto persiste | Os agentes se beneficiam de habilidades/regras armazenadas |

Leia [Agentes — visão geral](../agents-and-agentic-workflows/i-overview.md) para trabalhos em várias etapas com uso pesado de ferramentas. Use a solicitação de loop para repetir a direção **todos os dias**.

## 7. Perguntas de ensaio

- Por que a solicitação única desperdiça tokens?
- O que constitui uma boa mensagem “delta” em loop?
- Quando você ainda deve abrir um novo chat?

**Próximo:** [Instruções persistentes](iii-persistent-instructions.md).
