---
label: "IV"
subtitle: "Cursor skills, rules & AGENTS.md"
group: "AI Applied"
order: 4
---
Cursor skills, rules & AGENTS.md

## 4. Cursor skills — layout

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

## 5. Cursor rules vs skills

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

## 6. AGENTS.md and project context files

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