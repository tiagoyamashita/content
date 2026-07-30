---
label: "IIa"
subtitle: "Exemplos de artefatos"
group: "AI Applied"
order: 3
---
Exemplos de artefatos

Amostras concretas para cada tipo de artefato em [Artefatos e por que se preocupar](ii-artifacts-why-and-what.md). Copie, corte e adapte – mantenha apenas o que é específico do seu repositório.

## Bom versus ruim (padrões recorrentes)

| Padrão | Ruim | Bom |
|--------|-----|------|
| Habilidade`description`| “Git ajudante” | Tarefa + gatilhos: “mensagem de commit… quando o usuário pede para commitar ou menciona arquivos preparados” |
|`AGENTS.md`tamanho | Documento de arquitetura inteiro colado | Tabela de pilha + comandos + links para`docs/`|
| Escopo da regra |`alwaysApply: true`para nicho estilo SQL |`globs: **/*.sql`então ele carrega apenas quando relevante |
| Corpo de habilidade | Tutorial sobre o que é um PR | Checklist + formato de saída + suas convenções |

###

## 1. Habilidade (`SKILL.md`)

**Onde:**`.cursor/skills/commit-messages/SKILL.md`,`.claude/skills/commit-messages/SKILL.md`ou configuração de habilidade do Codex.

```markdown
---
name: commit-messages
description: Write conventional commit messages for staged changes. Use when the user asks to commit, write a commit message, or mentions staged files.
---

# Conventional commits

## Format

`<type>(<scope>): <summary>`

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.

## Checklist

- [ ] Summary is imperative, under 72 characters
- [ ] Body explains *why*, not *what* (the diff shows what)
- [ ] Breaking changes noted with `BREAKING CHANGE:` in body

## Example

    fix(auth): reject expired refresh tokens

    Tokens past TTL were still accepted when clock skew was under 5s.
    Now enforce server-side expiry regardless of client clock.
```

### PR habilidade de revisão (segundo exemplo)

**Onde:**`.cursor/skills/pr-review/SKILL.md`— pares com [nota Cursor](iv-cursor-skills-rules-agents-md.md).

```markdown
---
name: pr-review
description: Review pull requests for security, tests, and team conventions. Use when reviewing PRs, diffs, pull requests, or when the user asks for a code review.
---

# PR review

## Output format

1. **Verdict** — ship / ship with nits / needs changes
2. **Blockers** — must fix
3. **Suggestions** — optional
4. **Test coverage** — what was added; gaps

## Checklist

- [ ] Scope matches PR description; flag drive-by changes
- [ ] No secrets, tokens, or PII in diff
- [ ] Behaviour changes have tests (`npm test` per AGENTS.md)
- [ ] Public API changes update OpenAPI in `docs/api/`
```

###

## 2. Regras (`.mdc`)

**Onde:**`.cursor/rules/typescript-errors.mdc`(Cursor apenas).

```markdown
---
description: TypeScript error handling conventions
globs: **/*.{ts,tsx}
alwaysApply: false
---

# TypeScript errors

- Never use empty `catch` blocks
- Wrap external API calls with typed errors from `lib/errors.ts`
- Prefer `Result<T, E>` from `lib/result.ts` over throwing in domain code
- Log unexpected errors with `requestId` when available
```

**Regra sempre ativa** (estilo para toda a equipe) — use com moderação:

```markdown
---
description: Core project conventions for every task
alwaysApply: true
---

# Project conventions

- Match existing naming in the file you edit
- Do not add dependencies without asking
- Run `npm test` after behaviour changes when feasible
```

###

## 3.`AGENTS.md`

**Onde:** repo root (lido por Cursor, Codex, Claude Code, Copilot e outros).

```markdown
# AGENTS.md

## Stack

- Node 22, TypeScript, Next.js 15 (App Router)
- Postgres via Prisma; Redis for sessions

## Layout

| Path | Purpose |
|------|---------|
| `app/` | Routes and server components |
| `lib/` | Shared utilities, DB client |
| `prisma/` | Schema and migrations |
| `tests/` | Vitest unit + Playwright e2e |

## Commands

    npm install
    npm run dev          # local app on :3000
    npm test             # unit tests
    npm run test:e2e     # Playwright (needs .env.test)
    npx prisma migrate dev

## Do not

- Edit `node_modules/`, `.next/`, or generated Prisma client
- Commit `.env` or API keys

## PR / commit

Follow `.cursor/skills/commit-messages/SKILL.md`. PRs need tests for behavior changes.

## Skills

| Workflow | Path |
|----------|------|
| PR review | `.cursor/skills/pr-review/SKILL.md` |
```

###

## 4.`CLAUDE.md`

**Onde:** repo root (memória do projeto Claude Code — instruções permanentes, não fluxos de trabalho passo a passo).

```markdown
# CLAUDE.md

## Project

B2B billing dashboard. Customers manage subscriptions and invoices.

## Preferences

- Prefer small, focused diffs; ask before large refactors
- Use existing `Button` and `DataTable` from `components/ui/`
- Match existing error copy tone: short, actionable, no blame

## Gotchas

- Invoice PDFs are generated async — check job status, not immediate download
- `STRIPE_WEBHOOK_SECRET` must match the environment; test mode keys only in dev

## Skills

Heavy workflows live in `.claude/skills/` — e.g. `/pr-review` for code review.
```

**Divisão:** procedimentos → habilidades; fatos e preferências estáveis ​​→`CLAUDE.md`+`AGENTS.md`.

###

## 5. Instruções do projeto Claude (web)

**Onde:** Claude.ai → Projeto → **Instruções personalizadas** (não é um arquivo no git).

```markdown
You help write weekly engineering status updates for the Platform team.

## When to use

User mentions standup, status report, weekly update, or leadership summary.

## Output format

1. **Shipped** — bullets, past tense, link PRs when given
2. **In progress** — owner + ETA or blocker
3. **Risks** — only if material; include mitigation
4. **Asks** — decisions or help needed from leadership

## Tone

Concise, factual, no hype. Max ~300 words unless user asks for detail.

## Do not

Invent metrics or claim work shipped without evidence in the chat or attached files.
```

Anexe **arquivos de conhecimento** (guia de estilo PDF, roteiro) para fatos; mantenha instruções para formato e comportamento.

###

## 6. Instruções GPT personalizadas (ChatGPT)

**Onde:** ChatGPT → **Explorar GPTs** → Criar → **Instruções**.

```markdown
You are a SQL reviewer for a Postgres analytics warehouse.

## Role

Review queries for correctness, performance, and team style. Do not run queries — user pastes SQL.

## Check every review

- [ ] `JOIN` keys and filters use indexed columns where possible
- [ ] No `SELECT *` in production-bound queries
- [ ] CTEs named clearly; final `SELECT` states grain (per user, per day, etc.)
- [ ] `NULL` handling explicit in aggregations

## Response format

**Summary** (one line) → **Issues** (severity: high/medium/low) → **Suggested rewrite** (only if needed)

## Style reference

We use `snake_case` identifiers and schema `analytics.*`. Date columns are `timestamptz`.
```

Carregue um arquivo de **conhecimento** com lista de colunas indexadas ou guia de estilo se as revisões continuarem faltando detalhes do esquema.

###

## 7. Contexto`.md`no repositório

**Onde:**`docs/agent-context.md`,`docs/architecture/overview.md`, ou qualquer caminho que você faça referência`AGENTS.md`.

```markdown
# Agent context — checkout flow

Last updated: 2026-06. For repo map and commands, see root `AGENTS.md`.

## Business rules

- Guest checkout allowed; account created after payment succeeds
- Promo codes stack with team discounts only when `allow_stack=true` on the code
- Carts expire after 24h; do not persist payment methods on expired carts

## Key files

| File | Role |
|------|------|
| `app/checkout/page.tsx` | UI entry |
| `lib/checkout/cart.ts` | Cart state and expiry |
| `lib/checkout/charge.ts` | Stripe PaymentIntent creation |

## Testing notes

E2E checkout uses test card `4242…` — see `tests/e2e/checkout.spec.ts`.
```

Link de`AGENTS.md`(“Fluxo de checkout →`docs/agent-context/checkout.md`”) em vez de duplicar regras de negócios na raiz.

###

## Mapa rápido

| Artefato | Exemplo acima | Carregado quando |
|----------|---------------|------------|
|`SKILL.md`| §1 confirma, §1b PR revisão | A tarefa corresponde à habilidade`description`|
| Regras`.mdc`| §2 TypeScript (+ variante sempre ativa) | O padrão de arquivo corresponde ou`alwaysApply`|
|`AGENTS.md`| §3 briefing do repositório | Agente abre repositório/carregamento automático do Codex |
|`CLAUDE.md`| §4 preferências permanentes | Início da sessão do Claude Code |
| Instruções do projeto | §5 relatórios de situação | Bate-papos de usuários nesse Projeto Claude |
| GPT personalizado | §6 SQL revisor | O usuário conversa com aquele GPT |
| Contexto`.md`| §7 Fluxo de checkout | Vinculado ou`@`mencionado |

**Próximo:** [Configuração portátil entre ferramentas](iii-cross-tool-portable-setup.md) — mesmo conteúdo, pastas diferentes por produto.
