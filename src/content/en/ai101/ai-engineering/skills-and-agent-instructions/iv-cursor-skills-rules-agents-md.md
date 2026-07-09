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

### Linking a fixed script

Skills do **not** auto-run scripts. You **bundle** the script in the skill folder and tell the agent in **`SKILL.md`** to **execute** it via the Shell tool when the workflow runs.

```text
.cursor/skills/deploy-staging/
  SKILL.md
  scripts/
    smoke-test.sh          ← fixed script (committed to git)
    validate-release.py
```

| Piece | Role |
|-------|------|
| **`scripts/`** | Canonical copy of the script the team maintains |
| **`SKILL.md`** | When to run, exact command, how to read output |
| **Agent Shell** | Runs the command you specified — not magic wiring |

**1. Add the script** (executable, repo-relative paths inside):

```bash
chmod +x .cursor/skills/deploy-staging/scripts/smoke-test.sh
```

```bash
#!/usr/bin/env bash
# .cursor/skills/deploy-staging/scripts/smoke-test.sh
set -euo pipefail
curl -fsS "${STAGING_URL:-https://staging.example.com}/health"
```

**2. Link it in `SKILL.md`** — use imperative language and the path from **repo root**:

```markdown
---
name: deploy-staging
description: Deploy to staging and run smoke checks. Use when the user asks to deploy staging, release to staging, or verify a staging deploy.
---

# Deploy to staging

## Required steps (in order)

1. `npm run build`
2. `npm run deploy:staging`
3. **Always run the smoke script before reporting success:**
   ```bash
   .cursor/skills/deploy-staging/scripts/smoke-test.sh
   ```
4. Paste the script output in your reply. If non-zero exit, stop — do not claim deploy succeeded.

## Do not

- Reimplement the health check inline — use the script above
- Skip the script unless the user explicitly says to skip verification
```

**3. Test** — fresh chat, prompt “deploy to staging”, confirm the agent runs your script path.

#### Path rules

| Do | Avoid |
|----|-------|
| Paths from **repo root** in `SKILL.md` | Paths relative to the skill folder only (agent cwd is usually project root) |
| One clear command per script | “Run something like curl …” (agent may improvise) |
| `scripts/` under the skill folder | Scattered one-off scripts with no owner |
| Forward slashes in paths | Backslashes |

#### Alternatives (same idea, different anchor)

| Approach | When |
|----------|------|
| **`scripts/` in skill folder** | Team-owned workflow script; versioned with the skill |
| **`npm run smoke:staging`** in `package.json` | Script already part of app toolchain; skill says `npm run …` |
| **`AGENTS.md` Commands** | One-liner used across many skills (“tests = `npm test`”) |
| **MCP tool** | Script wraps a **live API** or DB the agent must call repeatedly — see [How MCP works](../how-mcp-works/i-overview.md) |
| **Cursor hook** (`.cursor/hooks.json`) | Run **automatically** on events (after edit, before shell) — not skill-triggered |

```text
Skill + script     → agent runs YOUR file when the TASK matches (deploy, review, …)
Hook               → Cursor runs YOUR file on EVENTS (afterFileEdit, beforeShellExecution, …)
MCP server         → agent calls a TOOL (search, create ticket, query API)
```

Use a **skill-linked script** for repeatable **procedures** (“always run this check”). Use a **hook** when it must fire **without** the user asking. Use **MCP** when the agent needs **live data**, not a fixed local command.

#### Safety

- No secrets in scripts — read from env (`STAGING_URL`, `API_KEY`)
- Keep scripts short and reviewable; avoid `rm -rf` or broad `git` commands unless intentional
- For destructive ops, add `disable-model-invocation: true` and require explicit `/deploy-staging` or user confirmation in the skill body

See [Writing & maintaining skills](v-writing-and-maintaining-skills.md) for testing and team ownership.

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
