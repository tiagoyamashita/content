---
label: "V"
subtitle: "Higiene e quando reiniciar"
group: "AI Applied"
order: 5
---
Higiene e quando reiniciar
A solicitação de loop falha quando **contexto armazenado reside** ou **threads apodrecem**. Mantenha camadas persistentes como código: revise, versione e redefina deliberadamente.

## 1. Sintomas de podridão de contexto

| Sintoma | Causa provável |
|--------|-------------|
| Modelo “esquece” regras no meio da discussão | Janela de contexto repleta de curvas antigas |
| Respostas contraditórias | Tópico poluído + habilidade desatualizada |
| Padrões de arquivo errados | Incompatibilidade global de regras após refatoração |
| Loop continua reportando status obsoleto | Observador não redefinido após implantação |

## 2. Quando redefinir

| Redefinir **tópico** | Redefinir **instruções/habilidade** |
|------------------|--------------------------------|
| Modelo travou repetindo erro | Processo ou pilha alterada |
| Pivô do tópico | As instruções contêm fatos errados |
| Sangramento confidencial | Habilidade copiada de emprego antigo |
| Linha longa > ~20 voltas pesadas | Revisão trimestral de qualquer maneira |

**Novo bate-papo + mesmo projeto** geralmente corrige problemas de thread sem perder instruções persistentes.

## 3. Cadência de manutenção

| Artefato | Revisão |
|----------|--------|
| GPT personalizado / instruções do projeto | Quando a qualidade da saída diminui |
|`SKILL.md`| Após alterações no fluxo de trabalho ou CLI |
|`.cursor/rules`| Após grande refatoração |
|`AGENTS.md`| Quando comandos de teste ou alteração de layout |
| Loops de automação | Após a renomeação do repositório, alteração da política da ramificação |

Adicione a data da **última revisão** no rodapé da habilidade caso sua equipe esqueça.

## 4. Confiança e verificação em loops

Loops amplificam erros – a mesma verificação errada é executada a cada 5 minutos.

| Hábito | Inscreva-se em |
|-------|----------|
| **Verifique as fontes** | Ciclos de pesquisa, resumos de dados |
| **Diferença antes de aceitar** | Loops de código, edições de agente |
| **Portão humano** | Envios externos, mesclagens, gastos |
| **Saída do loop de registro** | Audite o que foi executado automaticamente |

Consulte [Confiança, privacidade e verificação](../trust-privacy-and-verify/i-overview.md).

## 5. Limites de segurança

| Nunca faça loop sem supervisão… | Sem… |
|------------------------|----------|
| Enviar email/Slack para clientes | Etapa de aprovação |
| Mesclar para principal | CI + revisão humana |
| Use credenciais de produção | Tokens somente leitura com escopo definido |
| Cole segredos nas instruções | Redação e env vars |

Solicitações recorrentes em terminais ou logs compartilhados podem **vazar** detalhes da tarefa — loops de escopo para ambientes confiáveis.

## 6. Lançamento da equipe

| Etapa | Ação |
|------|--------|
| 1 | Identifique os 3 principais prompts repetidos → habilidades ou projeto |
| 2 | Documento no repositório (`AGENTS.md`, equipe wiki) |
| 3 | Pequenos exemplos internos de mensagens **delta** |
| 4 | Revisão compartilhada de habilidades como código |
| 5 | Meça o tempo economizado; descartar loops não utilizados |

## 7. Lista de verificação de decisão

Antes de iniciar um fluxo de trabalho de loop:

```text
[ ] Persistent layer holds stable rules (not retyped each time)
[ ] Each turn / tick prompt is a clear delta or self-contained check
[ ] I know when to start a fresh chat
[ ] Instructions updated for current stack
[ ] Verification step for high-stakes output
[ ] Stop condition defined for recurring loops
```

## 8. Perguntas de ensaio

- O que é a podridão do contexto e uma correção?
- Quando você deve atualizar uma habilidade em vez de iniciar um novo chat?
- Por que os loops autônomos são arriscados para o e-mail do cliente?

**Próximo:** [Agentes e fluxos de trabalho de agente](../agents-and-agentic-workflows/i-overview.md) ou [Habilidades e instruções do agente](../skills-and-agent-instructions/i-overview.md).
