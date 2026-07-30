---
label: "III"
subtitle: "AGENTS.md sozinho"
group: "Using skills, agents & hooks"
order: 3
---
AGENTS.md sozinho

(R)`AGENTS.md`** na **raiz do repositório** está o briefing permanente do agente. Ele carrega **automaticamente** no início da sessão — sem frase de gatilho, sem gancho, sem pasta de habilidades.

## O que AGENTS.md não é

| AGENTS.md não é… | Use em vez disso |
|-------------------|-------------|
| Um longo fluxo de trabalho | Habilidade em`.cursor/skills/`|
| Uma porta de confirmação | Enganchar`.cursor/hooks.json`|
| Valores secretos ou ambientais | Variáveis ​​ambientais; apenas nomes de referência |

Mantenha-o **curto** (uma tela). Vincule-se a habilidades para fluxos de trabalho profundos.

## Arquivo de amostra (pronto para cópia)

Arquivo ativo: [sample/AGENTS.md](sample/AGENTS.md)

Copie para **sua raiz do repositório** como`AGENTS.md`(não dentro`.cursor/`).

### Seções típicas

| Seção | Finalidade |
|--------|---------|
| **Pilha** | Linguagem, framework, gerenciador de pacotes |
| **Comandos** |`npm test`,`npm run lint`, construir |
| **Layout** | Onde residem a fonte, os testes e os documentos |
| **Índice de competências** | Tabela vinculada a`.cursor/skills/*/SKILL.md`|
| **Nota de ganchos** | Uma linha: “Commits bloqueados por varredura de segredos” |

## Fluxo somente de agente (sem habilidade, sem gancho)

```text
User opens repo in Cursor
  → AGENTS.md injected into context
  → User: "add a unit test for auth"
  → Agent uses npm test path from AGENTS.md
  → (no skill unless user asks for PR review, etc.)
```

O agente **não** executa ganchos ou habilidades até que a tarefa do usuário ou um evento os acione.

## AGENTS.md vs habilidade`description`

| | AGENTS.md | Habilidade |
|---|-----------|-------|
| **Cargas** | Cada bate-papo | Na partida |
| **Conteúdo** | Fatos sobre repositório | Procedimento para um trabalho |
| **Exemplo** | “Testes:`npm test`” | “Como revisar um PR passo a passo” |

Coloque **fatos**`AGENTS.md`. Coloque **procedimentos** nas habilidades.

## Teste

1. Copie [sample/AGENTS.md](sample/AGENTS.md) → raiz do repositório
2. Novo bate-papo: *“como faço para executar testes?”*
3. O agente deverá responder com o comando de`AGENTS.md`sem você colar

## Próximo

[Ganchos no commit](iv-use-hooks-on-commit.md) — comportamento automático **sem** solicitação do usuário.
