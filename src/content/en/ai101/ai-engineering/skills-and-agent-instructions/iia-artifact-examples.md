---
label: "IIa"
subtitle: "Artifact examples"
group: "AI Applied"
order: 3
---
Artifact examples

Concrete samples for each artifact type from [Artifacts & why bother](ii-artifacts-why-and-what.md). Copy, trim, and adapt — keep only what is specific to your repo.

## Good vs bad (patterns that recur)

| Pattern | Bad | Good |
|---------|-----|------|
| Skill `description` | “Git helper” | Task + triggers: “commit message… when user asks to commit or mentions staged files” |
| `AGENTS.md` size | Entire architecture doc pasted | Stack table + commands + links to `docs/` |
| Rule scope | `alwaysApply: true` for niche SQL style | `globs: **/*.sql` so it loads only when relevant |
| Skill body | Tutorial on what a PR is | Checklist + output format + your conventions |

---

## 1. Skill (`SKILL.md`)

**Where:** `.cursor/skills/commit-messages/SKILL.md`, `.claude/skills/commit-messages/SKILL.md`, or Codex skill config.

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

### PR review skill (second example)

**Where:** `.cursor/skills/pr-review/SKILL.md` — pairs with [Cursor note](iv-cursor-skills-rules-agents-md.md).

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

---

## 2. Rules (`.mdc`)

**Where:** `.cursor/rules/typescript-errors.mdc` (Cursor only).

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

**Always-on rule** (team-wide style) — use sparingly:

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

---

## 3. `AGENTS.md`

**Where:** repo root (read by Cursor, Codex, Claude Code, Copilot, and others).

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

---

## 4. `CLAUDE.md`

**Where:** repo root (Claude Code project memory — standing instructions, not step-by-step workflows).

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

**Split:** procedures → skills; stable facts and prefs → `CLAUDE.md` + `AGENTS.md`.

---

## 5. Claude Project instructions (web)

**Where:** Claude.ai → Project → **Custom instructions** (not a file in git).

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

Attach **knowledge files** (style guide PDF, roadmap) for facts; keep instructions for format and behaviour.

---

## 6. Custom GPT instructions (ChatGPT)

**Where:** ChatGPT → **Explore GPTs** → Create → **Instructions**.

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

Upload a **knowledge** file with indexed column list or style guide if reviews keep missing schema details.

---

## 7. Context `.md` in repo

**Where:** `docs/agent-context.md`, `docs/architecture/overview.md`, or any path you reference from `AGENTS.md`.

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

Link from `AGENTS.md` (“Checkout flow → `docs/agent-context/checkout.md`”) instead of duplicating business rules at root.

---

## Quick map

| Artifact | Example above | Loaded when |
|----------|---------------|-------------|
| `SKILL.md` | §1 commits, §1b PR review | Task matches skill `description` |
| Rules `.mdc` | §2 TypeScript (+ always-on variant) | File pattern matches or `alwaysApply` |
| `AGENTS.md` | §3 repo briefing | Agent opens repo / Codex auto-load |
| `CLAUDE.md` | §4 standing prefs | Claude Code session start |
| Project instructions | §5 status reports | User chats in that Claude Project |
| Custom GPT | §6 SQL reviewer | User chats with that GPT |
| Context `.md` | §7 checkout flow | Linked or `@`-mentioned |

**Next:** [Cross-tool portable setup](iii-cross-tool-portable-setup.md) — same content, different folders per product.
