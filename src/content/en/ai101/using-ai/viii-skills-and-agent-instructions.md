---
label: "VIII"
subtitle: "Skills & agent instructions"
group: "Using AI"
order: 8
---
Skills and agent instructions
**Skills** and **instruction `.md` files** teach an AI agent **your** workflows — commit format, review checklist, API conventions, doc style — so you stop re-explaining the same rules every chat.

This is for **people who use agents** (especially **Cursor**, Claude Projects, Custom GPTs). You write markdown; the product loads it when relevant.

## 1. Why bother?

| Without persistent instructions | With skills / rules / project docs |
|--------------------------------|----------------------------------|
| Repeat “use conventional commits” daily | Agent reads skill once per task |
| Agent guesses stack and folder layout | Points at `SKILL.md` or `AGENTS.md` |
| Inconsistent PR and doc format | Same template every time |

Think of skills as **onboarding docs for the agent** — short, actionable, trigger-aware.

## 2. What to create (pick by product)

| Artifact | Product | Scope |
|----------|---------|--------|
| **Skill (`SKILL.md`)** | Cursor | Task-specific workflows (review, deploy, SQL) |
| **Rules (`.mdc`)** | Cursor | Always-on or file-pattern coding standards |
| **`AGENTS.md`** | Cursor / many repos | Repo-wide agent briefing at root |
| **Project instructions** | Claude Projects | Tone, format, attached knowledge |
| **Custom GPT instructions** | ChatGPT | Persona + process for one assistant |
| **Context `.md` in repo** | Any IDE agent | `docs/agent-context.md`, architecture notes |

Same content idea everywhere: **when to use this + what to do + examples**.

```text
You (once)  →  write SKILL.md / rules / AGENTS.md
Agent (each task)  →  loads matching instructions  →  fewer retries
```

## 3. Cursor skills — layout

Skills live in a **folder** with a required **`SKILL.md`**:

```text
.cursor/skills/                    # project — shared in git
  my-skill-name/
    SKILL.md                       # required
    reference.md                   # optional deep detail
    examples.md                    # optional

~/.cursor/skills/                  # personal — all your projects
  my-skill-name/
    SKILL.md
```

Do **not** put custom skills in `~/.cursor/skills-cursor/` — that is for Cursor built-ins.

### SKILL.md template

```markdown
---
name: pr-review-team-standards
description: Review pull requests for security, tests, and team conventions. Use when reviewing PRs, diffs, or when the user asks for a code review.
---

# PR review (team standards)

## When to use
- User asks for review or mentions PR / diff.

## Checklist
1. Tests added or justified
2. No secrets in diff
3. Public API changes documented

## Output format
- **Summary** (2 sentences)
- **Must fix** / **Should fix** / **Nice to have**
```

| Field | Rule |
|-------|------|
| **`name`** | Lowercase, hyphens, ≤64 chars |
| **`description`** | **What** + **when** — agent uses this to decide relevance; include trigger words |

**Description example (good):**

```yaml
description: Generate commit messages from staged diffs using conventional commits. Use when the user asks to commit, write a commit message, or review staged changes.
```

**Description example (weak):**

```yaml
description: Helps with git.
```

## 4. Cursor rules vs skills

| | **Rules** (`.cursor/rules/*.mdc`) | **Skills** (`SKILL.md`) |
|---|-----------------------------------|-------------------------|
| **Purpose** | Coding standards, conventions | Multi-step workflows |
| **When loaded** | Always, or when file pattern matches | When task matches description |
| **Example** | “Use `async/await` in `**/*.ts`” | “How to run and interpret our smoke tests” |

```markdown
---
description: TypeScript error handling conventions
globs: **/*.ts
alwaysApply: false
---

# TypeScript errors

- Never empty catch blocks
- Wrap external API calls with typed errors from `lib/errors.ts`
```

Use **rules** for “how code should look”; use **skills** for “how to run a process.”

## 5. AGENTS.md and project context files

**`AGENTS.md`** at repo root (or paths your team documents) gives agents a **map of the repo**:

| Section | Content |
|---------|---------|
| **Stack** | Language, framework, test command |
| **Layout** | Where routes, models, tests live |
| **Commands** | `npm test`, `make lint`, migrate DB |
| **Do not** | Generated folders, secrets, huge vendored trees |
| **PR / commit** | Link to skill or one-paragraph standard |

Keep it **short** — link to longer docs instead of pasting them.

```markdown
# AGENTS.md

## Stack
Node 20, Next.js 14, Postgres via Prisma.

## Commands
- Test: `npm test`
- Lint: `npm run lint`

## Conventions
See `.cursor/skills/pr-review-team-standards/SKILL.md` for reviews.
```

Any **`docs/*.md`** can play the same role if you `@`-mention or index it in Cursor.

## 6. Writing instructions agents actually follow

### Be concise

The agent already knows generic programming. Add only **what is specific to you**.

| Skip | Include |
|------|---------|
| “JSON is a data format…” | “Our API returns `{ data, error }` envelope” |
| Long tutorials | Checklists, commands, templates |

Target **under ~500 lines** in main `SKILL.md`; move depth to `reference.md`.

### Progressive disclosure

```markdown
## Quick steps
1. Run `./scripts/deploy-staging.sh`
2. Verify health at `/health`

## More detail
- Full runbook: [reference.md](reference.md)
```

### Set freedom level

| Task | Style |
|------|--------|
| Code review | High — principles + checklist |
| Release notes | Medium — fixed markdown template |
| DB migration | Low — exact command sequence |

### Include triggers in description

Mention filenames, tools, and user phrases: “PR”, “`.xlsx`”, “conventional commits”, “Supabase”, “deploy staging”.

### Verbatim user wording

If you care about exact phrasing (legal disclaimer, brand voice), paste it **verbatim** in the skill — do not let the agent paraphrase.

## 7. Example skills (starter ideas)

| Skill name | Triggers in description |
|------------|-------------------------|
| `commit-messages` | commit, staged, conventional commits |
| `pr-review` | PR, diff, code review |
| `api-design-notes` | REST, OpenAPI, new endpoint |
| `incident-writeup` | postmortem, incident, outage |
| `weekly-status` | status report, standup summary |
| `content-notes` | swe101, frontmatter, `_meta.json` (this repo) |

## 8. ChatGPT / Claude equivalents

| Cursor skill | Non-Cursor |
|--------------|------------|
| `SKILL.md` body | Custom GPT **Instructions** |
| `description` triggers | First lines: “Use this when user …” |
| `reference.md` | Uploaded PDF / project file |
| Rules alwaysApply | “Always follow these rules:” in Project instructions |

You can **maintain one markdown source** and copy sections into each product.

## 9. Team workflow

| Practice | Why |
|----------|-----|
| **Project skills in git** | Whole team gets same agent behaviour |
| **Owner per skill** | Someone updates when process changes |
| **Changelog in skill** | “v2: added security checklist 2026-06” |
| **Review skills like code** | Bad instructions scale mistakes |

Start with **one** high-friction workflow (PR review or commits); expand when it works.

## 10. Maintenance checklist

- [ ] Description says **what** and **when** with trigger terms
- [ ] Main file scannable (headings, checklists)
- [ ] Commands copy-pasteable and tested
- [ ] No secrets or internal URLs that expire without notice
- [ ] Long content split into `reference.md`
- [ ] Linked from `AGENTS.md` or README if repo-wide

## 11. Rehearsal questions

- Skill vs rule — which for “always use Prettier defaults”?
- What two things belong in a skill `description`?
- Why keep `SKILL.md` short and put details elsewhere?

**Related:** [Agents & agentic workflows](iii-agents-and-agentic-workflows.md), [Tools & orchestration](iv-tools-and-orchestration.md), [Custom assistants](v-custom-assistants-and-knowledge.md), [Effective prompting](ii-effective-prompting.md).
