---
label: "V"
subtitle: "Writing & maintaining skills"
group: "AI Applied"
order: 6
---
Writing & maintaining skills

How to write instructions agents actually follow — and keep them accurate as your process changes.

## 7. Writing instructions agents actually follow

### Be concise

The agent already knows generic programming. Add only **what is specific to you**.

| Skip | Include |
|------|---------|
| “JSON is a data format…” | “Our API returns `{ data, error }` envelope” |
| Long tutorials | Checklists, commands, templates |
| Repeating `AGENTS.md` in every skill | “See AGENTS.md for test command” |

Target **under ~500 lines** in main `SKILL.md`; move depth to `reference.md`.

### Write descriptions that trigger

The `description` field is how the agent decides to load the skill. Include **what it does** and **when to use it** with words users actually say.

| Weak | Strong |
|------|--------|
| “Helps with git.” | “Write conventional commit messages for staged changes. Use when the user asks to commit, write a commit message, or mentions staged files.” |
| “Code review skill.” | “Review pull requests for security, tests, and team conventions. Use when reviewing PRs, diffs, or when the user asks for a code review.” |
| “Docs helper.” | “Edit swe101 markdown notes: frontmatter, `_meta.json`, kebab filenames. Use when user mentions content repo, note structure, or `_meta.json`.” |

Add **synonyms** your team uses: “PR”, “pull request”, “diff”, “merge request”.

### Progressive disclosure

Structure the skill so the agent reads the minimum first:

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

| Layer | File | Content |
|-------|------|---------|
| Trigger + summary | `SKILL.md` top | What, when, quick steps |
| Repeatable checklist | `SKILL.md` body | Checkboxes, commands |
| Rare edge cases | `reference.md` | Long prose, links, history |
| Good/bad samples | `examples.md` | Optional; reduces format drift |
| Fixed commands | `scripts/*.sh` | **Separate file** next to `SKILL.md` — agent runs via Shell when skill says so; code is **not** inside the `.md` — see [linking scripts](iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script) |

### Test before you trust it

1. Start a **fresh chat** (no prior context).
2. Use a **short prompt** that should trigger the skill — e.g. “review this diff”.
3. Check: Did it follow your output format? Run the right command from `AGENTS.md`?
4. If not: tighten `description` trigger words or add a missing checklist item.
5. Repeat after major model or Cursor updates.

## 8. Example skills (starter ideas)

| Skill name | Triggers in description |
|------------|-------------------------|
| `commit-messages` | commit, staged, conventional commits |
| `pr-review` | PR, diff, code review, pull request |
| `api-design-notes` | REST, OpenAPI, new endpoint |
| `incident-writeup` | postmortem, incident, outage, RCA |
| `weekly-status` | status report, standup summary, leadership update |
| `deploy-staging` | deploy, staging, release |
| `content-notes` | swe101, frontmatter, `_meta.json` (this repo) |

Copy starters from [Artifact examples](iia-artifact-examples.md); add your commands and checklists.

## 9. ChatGPT / Claude (web) equivalents

| Cursor skill | Non-Cursor |
|--------------|------------|
| `SKILL.md` body | Custom GPT **Instructions** |
| `description` triggers | First lines: “Use this when user …” |
| `reference.md` | Uploaded PDF / project knowledge file |
| Rules `alwaysApply` | “Always follow these rules:” in Project instructions |
| `AGENTS.md` | Pasted “Project context” block or uploaded repo summary |

You can **maintain one markdown source** in git (`docs/skills/weekly-status.md`) and copy sections into each product when they change.

## 10. Team workflow

| Practice | Why |
|----------|-----|
| **Project skills in git** | Whole team gets same agent behaviour |
| **Owner per skill** | Someone updates when process changes |
| **Changelog in skill** | “v2: added security checklist 2026-06” at bottom of `SKILL.md` |
| **Review skills like code** | Bad instructions scale mistakes |
| **PR touches skill → test in agent** | Same as code: verify before merge |

Start with **one** high-friction workflow (PR review or commits); expand when it works.

### Sync across tools

When you support Cursor and Claude Code:

```text
docs/skills/pr-review/SKILL.md   # optional single source
  → copy or symlink to .cursor/skills/pr-review/
  → copy or symlink to .claude/skills/pr-review/
```

Document the sync step in README or a one-line script — avoid silent drift.

## 11. Maintenance checklist

- [ ] `description` says **what** and **when** with trigger terms
- [ ] Main file scannable (headings, checklists)
- [ ] Commands copy-pasteable and **tested** on current branch
- [ ] No secrets or internal URLs that expire without notice
- [ ] Long content split into `reference.md`
- [ ] Linked from `AGENTS.md` or README if repo-wide
- [ ] Owner named in skill footer or team runbook
- [ ] Reviewed after process or tooling change (quarterly minimum)

## 12. Anti-patterns

| Mistake | Fix |
|---------|-----|
| Skill duplicates entire `AGENTS.md` | Link to `AGENTS.md`; skill = workflow only |
| 200-line `description` | Move detail to body; description ≤ ~1–3 sentences |
| Checklist items never checked in practice | Remove or demote to `reference.md` |
| Skill for “always format imports this way” | Use a **rule** with `globs` instead |
| Never invoked — wrong product folder | `.cursor/skills/` vs `.claude/skills/` per tool |

## 13. Rehearsal questions

- Skill vs rule — which for “always use Prettier defaults”?
- What two things belong in a skill `description`?
- Why keep `SKILL.md` short and put details in `reference.md`?
- Same skill in Cursor and Claude Code — what changes, what stays the same?
- How do you verify a skill works before merging it to main?

**Related:** [How MCP works](../how-mcp-works/i-overview.md) (live tools vs static skills), [Agents & agentic workflows](../agents-and-agentic-workflows/i-overview.md), [Tools & orchestration](../tools-and-orchestration/i-overview.md), [Custom assistants](../custom-assistants-and-knowledge/i-overview.md), [Effective prompting](../effective-prompting/i-overview.md), [Persistent instructions](../loop-prompting/iii-persistent-instructions.md).
