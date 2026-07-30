---
label: "III"
subtitle: "Exemplos de artefatos"
group: "AI Applied"
order: 4
---
Configuração portátil entre ferramentas

## 3. Ferramenta cruzada: Cursor, Claude Code, Codex

**Resposta curta:** sim — a **mesma ideia** funciona em todas as ferramentas, mas **os caminhos das pastas são diferentes**. O **`SKILL.md`formato** é um padrão aberto ([Habilidades do agente](https://agentskills.io)); **`AGENTS.md`** é a ferramenta cruzada “README para agentes”.

| Ferramenta | Pasta de habilidades | Contexto do projeto | Notas |
|------|---------------|-----------------|-------|
| **Cursor** |`.cursor/skills/name/SKILL.md`ou`~/.cursor/skills/`|`AGENTS.md`,`.cursor/rules/*.mdc`| Regras (`.mdc`) são apenas Cursor |
| **Código Claude** |`.claude/skills/name/SKILL.md`ou`~/.claude/skills/`|`CLAUDE.md`,`AGENTS.md`| Invocar com`/skill-name`; mesmo frontmatter YAML |
| **Códice OpenAI** | Habilidades via configuração/descoberta do Codex |`AGENTS.md`(raiz + aninhado),`~/.codex/AGENTS.md`| Cargas`AGENTS.md`cadeia automaticamente; Limite padrão de 32 KiB |
| **GitHub Copiloto** | Habilidades do agente (em evolução) |`AGENTS.md`,`.github/copilot-instructions.md`| Prefiro`AGENTS.md`para portabilidade |
| **Windsurf, Aider, outros** | Varia | Lê frequentemente **`AGENTS.md`** | Verifique a documentação da ferramenta |

### Quais portas versus o que não funciona

| Portos em todos os lugares | Específico da ferramenta |
|------------------|---------------|
|`AGENTS.md`corpo |`.cursor/rules/*.mdc`|
|`SKILL.md`nome, descrição, corpo de redução | Cursor`@`mencionar sintaxe |
| Listas de verificação, comandos, modelos |`disable-model-invocation`manipulação |
|`docs/`arquivos de contexto | Caminhos de habilidades pessoais (`~/.cursor/`contra`~/.claude/`) |

Cole regras somente Cursor em **`AGENTS.md`** ou **`CLAUDE.md`** quando companheiros de equipe usam outros agentes.

## Configuração portátil (um repositório, muitos agentes)

```text
repo/
  AGENTS.md                      ← everyone reads this
  CLAUDE.md                      ← Claude Code standing prefs (optional)
  docs/skills/pr-review/         ← optional single source (see below)
    SKILL.md
  .cursor/skills/
    pr-review/SKILL.md           ← Cursor
  .claude/skills/
    pr-review/SKILL.md           ← Claude Code
```

### Estratégias de sincronização

| Estratégia | Detalhe | Melhor quando |
|----------|--------|-----------|
| **Duplicado** | Mesmo`SKILL.md`em`.cursor/`e`.claude/`| Equipe pequena; poucas habilidades |
| **Link simbólico** | Um arquivo, dois caminhos (se OS permitir) | Desenvolvedor local no macOS/Linux |
| **`docs/skills/`fonte** | Cópia canônica; cópias de script em mudança | CI ou sincronização pré-commit |
| **`AGENTS.md`apenas** | Sem habilidades por ferramenta; fluxos de trabalho em documentos vinculados | Uso de agente leve |

Exemplo de script de sincronização (manual ou CI):

```bash
#!/bin/sh
# sync-skills.sh — run from repo root
for skill in docs/skills/*/; do
  name=$(basename "$skill")
  cp "$skill/SKILL.md" ".cursor/skills/$name/SKILL.md"
  cp "$skill/SKILL.md" ".claude/skills/$name/SKILL.md"
done
```

Documento “executar`./sync-skills.sh`após habilidades de edição” em README.

Conteúdo em`SKILL.md`(nome, descrição, lista de verificação, modelos) transfere bem - apenas o **diretório pai** muda.

### O que *não* é portado diretamente

| Cursor-somente | Use em outro lugar como |
|------------|------------------|
|`.cursor/rules/*.mdc`| Lista com marcadores em`AGENTS.md`ou`CLAUDE.md`|
|`disable-model-invocation`em frontmatter | Código Claude: bandeiras semelhantes; Codex: configuração de habilidade manual |
|`@file`Cursor menciona | Código Claude`@`importações; Codex: caminhos em`AGENTS.md`|

## Especificidades do Codex

- **`AGENTS.md`** na raiz do repositório (e diretórios aninhados) é carregado **automaticamente** a cada execução - mais próximo do contexto “sempre ativo”.
- **Habilidades** no Codex são uma camada separada (metadados + instruções); configurar de acordo com [documentos do Codex](https://developers.openai.com/codex/guides/agents-md).
- Correr`codex /init`para andaime`AGENTS.md`; manter abaixo do limite de tamanho ou aumentar`project_doc_max_bytes`.
- **Monorepos:** adiciona nível de pacote`AGENTS.md`com comandos de teste locais; Codex sobe e desce na árvore.

```text
monorepo/
  AGENTS.md                 # global: node version, CI entry
  apps/web/AGENTS.md        # npm run dev, Playwright paths
  apps/api/AGENTS.md        # go test ./..., OpenAPI location
```

## Especificidades do Código Claude

- Mesmo **`SKILL.md`** forma como Cursor:`name`,`description`, corpo de marcação.
- **`/skill-name`** executa uma habilidade manualmente; bom`description`→ carregamento automático quando relevante.
- Procedimentos longos pertencem a **habilidades**; fatos estáveis ​​​​em **`CLAUDE.md`** ou **`AGENTS.md`**.
- **`CLAUDE.md`** não substitui habilidades — mantenha os runbooks de implantação/revisão em`.claude/skills/`.

## Copiloto e`.github/copilot-instructions.md`

O copiloto pode ler **`.github/copilot-instructions.md`**. Para portabilidade, mantenha **`AGENTS.md`** como fonte da verdade e:

- Duplicar um breve resumo em`copilot-instructions.md`, ou
- Apontar usuários do Copilot para`AGENTS.md`nos documentos da equipe.

Prefira um arquivo mantido a três cópias divergentes.

## Manutenção quando as ferramentas são atualizadas

| Evento | Ação |
|-------|--------|
| Novo membro da equipe em diferentes IDE | Verificar`AGENTS.md`+ pasta de habilidades da ferramenta |
| Habilidade`description`para de disparar | Teste novamente em uma nova sessão; adicionar sinônimos de gatilho |
| Codex “contexto muito grande” | Aparar`AGENTS.md`; link para`docs/`|
| Alteração de processo (novo comando de teste) | Atualizar`AGENTS.md`primeiro, depois as habilidades que o referenciam |

**Próximo:** [Cursor habilidades, regras e AGENTS.md](iv-cursor-skills-rules-agents-md.md) para detalhes somente de Cursor.
