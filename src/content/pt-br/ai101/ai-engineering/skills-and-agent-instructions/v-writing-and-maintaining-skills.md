---
label: "V"
subtitle: "Escrita e manutenção de habilidades"
group: "AI Applied"
order: 6
---
Escrita e manutenção de habilidades

Como escrever instruções que os agentes realmente seguem — e mantê-las precisas à medida que o seu processo muda.

## 7. Escrevendo instruções que os agentes realmente seguem

### Seja conciso

O agente já conhece programação genérica. Adicione apenas **o que é específico para você**.

| Pular | Incluir |
|------|---------|
| “JSON é um formato de dados…” | “Nosso API retorna`{ data, error }`envelope” |
| Tutoriais longos | Listas de verificação, comandos, modelos |
| Repetindo`AGENTS.md`em todas as habilidades | “Veja AGENTS.md para comando de teste” |

Segmentar **abaixo de aproximadamente 500 linhas** no principal`SKILL.md`; mover profundidade para`reference.md`.

### Escreva descrições que acionem

O`description`campo é como o agente decide carregar a habilidade. Inclua **o que ele faz** e **quando usá-lo** com as palavras que os usuários realmente dizem.

| Fraco | Forte |
|------|--------|
| “Ajuda com o git.” | "Escreva mensagens de commit convencionais para alterações preparadas. Use quando o usuário solicitar uma confirmação, escreva uma mensagem de confirmação ou mencione arquivos preparados." |
| “Habilidade de revisão de código.” | "Revise solicitações pull para segurança, testes e convenções de equipe. Use ao revisar PRs, diferenças ou quando o usuário solicitar uma revisão de código." |
| “Ajudante de documentos.” | “Editar notas de remarcação swe101: frontmatter,`_meta.json`, nomes de arquivos kebab. Use quando o usuário menciona repositório de conteúdo, estrutura de notas ou`_meta.json`.” |

Adicione **sinônimos** que sua equipe usa: “PR”, “pull request”, “diff”, “merge request”.

### Divulgação progressiva

Estruture a habilidade para que o agente leia primeiro o mínimo:

```markdown
# Deploy to staging

## Quick path (most runs)

1. `npm run build`
2. `npm run deploy:staging`
3. Confirm health: `curl https://staging.example.com/health`

## Pre-deploy checklist

- [ ] Migrations applied on staging DB
- [ ] Feature flag `new-checkout` documented in PR

## Rollback

    npm run deploy:staging -- --rollback <previous-tag>

## Full runbook

See [reference.md](reference.md) for DB failover and on-call escalation.
```

| Camada | Arquivo | Conteúdo |
|-------|------|--------|
| Gatilho + resumo |`SKILL.md`topo | O que, quando, etapas rápidas |
| Lista de verificação repetível |`SKILL.md`corpo | Caixas de seleção, comandos |
| Casos extremos raros |`reference.md`| Prosa longa, links, história |
| Amostras boas/ruins |`examples.md`| Opcional; reduz desvio de formato |
| Comandos fixos |`scripts/*.sh`| **Arquivo separado** ao lado de`SKILL.md`— o agente é executado via Shell quando a habilidade diz isso; código **não** está dentro do`.md`— veja [vinculando scripts](iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script) |

### Teste antes de confiar

1. Inicie um **novo bate-papo** (sem contexto anterior).
2. Use um **prompt curto** que deve acionar a habilidade — por exemplo, “revisar esta diferença”.
3. Verifique: seguiu seu formato de saída? Execute o comando correto de`AGENTS.md`?
4. Caso contrário: aperte`description`palavras de gatilho ou adicione um item ausente da lista de verificação.
5. Repita após atualizações principais do modelo ou Cursor.

## 8. Exemplos de habilidades (ideias iniciais)

| Nome da habilidade | Gatilhos na descrição |
|------------|------------------------|
|`commit-messages`| commit, commits preparados e convencionais |
|`pr-review`| PR, diff, revisão de código, solicitação pull |
|`api-design-notes`| REST, OpenAPI, novo terminal |
|`incident-writeup`| post-mortem, incidente, interrupção, RCA |
|`weekly-status`| relatório de status, resumo standup, atualização de liderança |
|`deploy-staging`| implantar, preparar, liberar |
|`content-notes`| swe101, frontmatter,`_meta.json`(este repositório) |

Copie os iniciadores de [Exemplos de artefatos](iia-artifact-examples.md); adicione seus comandos e listas de verificação.

## 9. Equivalentes ChatGPT / Claude (web)

| Habilidade Cursor | Não-Cursor |
|-------------|------------|
|`SKILL.md`corpo | GPT personalizado **Instruções** |
|`description`gatilhos | Primeiras linhas: “Use isto quando usuário…” |
|`reference.md`| Carregado arquivo PDF / conhecimento do projeto |
| Regras`alwaysApply`| “Siga sempre estas regras:” em Instruções do projeto |
|`AGENTS.md`| Bloco “Contexto do projeto” colado ou resumo do repositório carregado |

Você pode **manter uma fonte de redução** no git (`docs/skills/weekly-status.md`) e copie seções em cada produto quando eles mudarem.

## 10. Fluxo de trabalho da equipe

| Prática | Por que |
|----------|-----|
| **Habilidades de projeto em git** | Toda a equipe obtém o mesmo comportamento do agente |
| **Proprietário por habilidade** | Alguém atualiza quando o processo muda |
| **Registro de alterações na habilidade** | “v2: lista de verificação de segurança adicionada 2026-06” na parte inferior`SKILL.md`|
| **Analise habilidades como código** | Erros de escala de instruções incorretas |
| **PR toca habilidade → teste no agente** | Igual ao código: verifique antes de mesclar |

Comece com **um** fluxo de trabalho de alto atrito (revisão ou confirmação de PR); expandir quando funcionar.

### Sincronize entre ferramentas

Quando você oferece suporte a Cursor e Claude Code:

```text
docs/skills/pr-review/SKILL.md   # optional single source
  → copy or symlink to .cursor/skills/pr-review/
  → copy or symlink to .claude/skills/pr-review/
```

Documente a etapa de sincronização em README ou em um script de uma linha – evite desvios silenciosos.

## 11. Lista de verificação de manutenção

- [ ]`description`diz **o que** e **quando** com termos de gatilho
- [] Arquivo principal escaneável (títulos, listas de verificação)
- [] Comandos que podem ser copiados e colados e **testados** no branch atual
- [] Sem segredos ou URLs internos que expiram sem aviso prévio
- [] Conteúdo longo dividido em`reference.md`- [] Vinculado de`AGENTS.md`ou README se for para todo o repositório
- [] Proprietário nomeado no rodapé da habilidade ou no runbook da equipe
- [ ] Revisado após mudança de processo ou ferramental (mínimo trimestral)

## 12. Antipadrões

| Erro | Correção |
|--------|-----|
| Habilidade duplicada inteira`AGENTS.md`| Link para`AGENTS.md`; habilidade = somente fluxo de trabalho |
| 200 linhas`description`| Mova o detalhe para o corpo; descrição ≤ ~1–3 frases |
| Itens da lista de verificação nunca verificados na prática | Remover ou rebaixar para`reference.md`|
| Habilidade para “sempre formatar as importações desta forma” | Use uma **regra** com`globs`em vez disso |
| Nunca invocado — pasta de produto errada |`.cursor/skills/`contra`.claude/skills/`por ferramenta |

## 13. Perguntas de ensaio

- Habilidade versus regra — qual é “sempre usar padrões mais bonitos”?
- Quais são as duas coisas que pertencem a uma habilidade`description`?
- Por que manter`SKILL.md`curta e coloque detalhes`reference.md`?
- Mesma habilidade em Cursor e Claude Code — o que muda, o que permanece igual?
- Como você verifica se uma habilidade funciona antes de mesclá-la com a principal?

**Relacionado:** [Como MCP funciona](../how-mcp-works/i-overview.md) (ferramentas ativas versus habilidades estáticas), [Agentes e fluxos de trabalho de agente](../agents-and-agentic-workflows/i-overview.md), [Ferramentas e orquestração](../tools-and-orchestration/i-overview.md), [Assistentes personalizados](../custom-assistants-and-knowledge/i-overview.md), [Solicitação eficaz](../effective-prompting/i-overview.md), [Instruções persistentes](../loop-prompting/iii-persistent-instructions.md).
