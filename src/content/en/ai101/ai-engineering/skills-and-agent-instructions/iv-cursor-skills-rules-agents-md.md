---
label: "IV"
subtitle: "Cursor skills, rules & AGENTS.md"
group: "AI Applied"
order: 5
---
Cursor skills, rules & AGENTS.md

Cursor-specific layout for skills, rules, and repo briefing files. For portable setup across Claude Code and Codex, see [Cross-tool portable setup](iii-cross-tool-portable-setup.md).

## 4. Cursor skills — layout

Skills live in a **folder** with a required **`SKILL.md`**:

```text
.cursor/skills/                    # project — shared in git
  pr-review/
    SKILL.md                       # required
    reference.md                   # optional deep detail
    examples.md                    # optional

~/.cursor/skills/                  # personal — all your projects
  my-private-skill/
    SKILL.md
```

Do **not** put custom skills in `~/.cursor/skills-cursor/` — that is for Cursor built-ins.

| Location | Use for |
|----------|---------|
| `.cursor/skills/` (project) | Team workflows in git |
| `~/.cursor/skills/` (user) | Personal habits across repos |
| `reference.md` in skill folder | Long checklists, API details |
| `examples.md` in skill folder | Good/bad output samples |

### SKILL.md template (PR review)

```markdown
---
name: pr-review-team-standards
description: Review pull requests for security, tests, and team conventions. Use when reviewing PRs, diffs, or when the user asks for a code review.
---

# PR review (team standards)

## Before you comment

- [ ] Read the full diff; note files outside the stated scope
- [ ] Run `npm test` if behaviour changed (see AGENTS.md)
- [ ] Check for secrets, PII, or debug logging left in

## Review output format

1. **Summary** — one line: ship / ship with nits / needs changes
2. **Blockers** — must fix before merge
3. **Suggestions** — optional improvements
4. **Tests** — what is covered; what is missing

## Team conventions

- New API routes need OpenAPI update in `docs/api/`
- Auth changes need test in `tests/auth/`
- No new `any` in `lib/` without comment explaining why

## Deep detail

See [reference.md](reference.md) for security checklist and past incident patterns.
```

Frontmatter fields:

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | Yes | Stable id; lowercase, hyphens |
| `description` | Yes | **What** + **when** — drives auto-load |
| `disable-model-invocation` | No | If `true`, only runs when user invokes explicitly |

## 5. Cursor rules vs skills

| | **Rules** (`.cursor/rules/*.mdc`) | **Skills** (`SKILL.md`) |
|---|-----------------------------------|-------------------------|
| **Purpose** | Coding standards, conventions | Multi-step workflows |
| **When loaded** | Always, or when file pattern matches | When task matches `description` |
| **Size** | Keep short — applied often | Can be longer; loaded on demand |
| **Example** | “Use `async/await` in `**/*.ts`” | “How to run and interpret our smoke tests” |

Use **rules** for “how code should look”; use **skills** for “how to run a process.”

### Rule template

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
```

| `alwaysApply` | `globs` | Effect |
|---------------|---------|--------|
| `true` | ignored | Rule in every chat in this project |
| `false` | `**/*.ts` | Rule when agent touches matching files |
| `false` | omitted | Rule available; agent decides relevance |

**User rules** (Cursor Settings → Rules) apply across all projects. Prefer **project rules** in `.cursor/rules/` for team standards in git.

### Quick picker

| You want… | Use |
|-----------|-----|
| “Always use conventional commits when I ask to commit” | **Skill** (triggered by task) |
| “Never empty catch in TypeScript” | **Rule** with `globs` |
| “Our whole team uses the same tab width” | **Rule** with `alwaysApply: true` |
| “How to triage production alerts” | **Skill** |

## 6. AGENTS.md and project context files

**`AGENTS.md`** at repo root gives agents a **map of the repo**. Cursor, Codex, Claude Code, and Copilot read it; keep it the **portable baseline**.

| Section | Content |
|---------|---------|
| **Stack** | Language, framework, test runner |
| **Layout** | Where routes, models, tests live |
| **Commands** | Install, dev, test, lint, migrate |
| **Do not** | Generated folders, secrets, vendored trees |
| **PR / commit** | Link to skill or one-paragraph standard |
| **Skills** | Optional list: “PR review → `.cursor/skills/pr-review/`” |

Keep it **short** — link to longer docs instead of pasting them.

```markdown
# AGENTS.md

## Stack

Node 22, TypeScript, Next.js 15 (App Router), Prisma, Vitest, Playwright.

## Layout

| Path | Purpose |
|------|---------|
| `app/` | Routes and server components |
| `lib/` | Shared utilities, DB client |
| `prisma/` | Schema and migrations |
| `tests/` | Unit (`*.test.ts`) and e2e (`e2e/`) |

## Commands

    npm install
    npm run dev
    npm test
    npm run test:e2e
    npx prisma migrate dev

## Do not

- Edit `node_modules/`, `.next/`, or generated Prisma client
- Commit `.env` or credentials

## PR / commit

Use skill `.cursor/skills/commit-messages/SKILL.md`. Behaviour changes need tests.

## Skills

| Workflow | Path |
|----------|------|
| PR review | `.cursor/skills/pr-review/SKILL.md` |
| Commits | `.cursor/skills/commit-messages/SKILL.md` |

## More context

Checkout flow: `docs/agent-context/checkout.md`
```

### Nested `AGENTS.md`

Some tools (especially Codex) load **`AGENTS.md` in subfolders** when work happens there. Use nested files for monorepo packages:

```text
repo/
  AGENTS.md                 # global
  services/billing/
    AGENTS.md               # billing-specific commands and layout
```

## 7. Wiring it together

```text
User: "Review this PR"

  AGENTS.md     → how to run tests, where tests live
  rules/*.mdc   → style while reading .ts files
  pr-review/    → checklist, output format, blockers vs nits
    SKILL.md
```

You type a short prompt; the stack supplies the rest.

**Next:** [Writing & maintaining skills](v-writing-and-maintaining-skills.md) — descriptions, testing, team ownership.
