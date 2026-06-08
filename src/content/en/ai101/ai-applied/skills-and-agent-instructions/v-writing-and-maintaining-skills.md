---
label: "V"
subtitle: "Writing & maintaining skills"
group: "AI Applied"
order: 5
---
Writing & maintaining skills

## 7. Writing instructions agents actually follow

### Be concise

The agent already knows generic programming. Add only **what is specific to you**.

| Skip | Include |
|------|---------|
| “JSON is a data format…” | “Our API returns `{ data, error }` envelope” |
| Long tutorials | Checklists, commands, templates |

Target **under ~500 lines** in main `SKILL.md`; move depth to `reference.md`.

### Progressive disclosure

```markdown

## 8. Example skills (starter ideas)

| Skill name | Triggers in description |
|------------|-------------------------|
| `commit-messages` | commit, staged, conventional commits |
| `pr-review` | PR, diff, code review |
| `api-design-notes` | REST, OpenAPI, new endpoint |
| `incident-writeup` | postmortem, incident, outage |
| `weekly-status` | status report, standup summary |
| `content-notes` | swe101, frontmatter, `_meta.json` (this repo) |

## 9. ChatGPT / Claude (web) equivalents

| Cursor skill | Non-Cursor |
|--------------|------------|
| `SKILL.md` body | Custom GPT **Instructions** |
| `description` triggers | First lines: “Use this when user …” |
| `reference.md` | Uploaded PDF / project file |
| Rules alwaysApply | “Always follow these rules:” in Project instructions |

You can **maintain one markdown source** and copy sections into each product.

## 10. Team workflow

| Practice | Why |
|----------|-----|
| **Project skills in git** | Whole team gets same agent behaviour |
| **Owner per skill** | Someone updates when process changes |
| **Changelog in skill** | “v2: added security checklist 2026-06” |
| **Review skills like code** | Bad instructions scale mistakes |

Start with **one** high-friction workflow (PR review or commits); expand when it works.

## 11. Maintenance checklist

- [ ] Description says **what** and **when** with trigger terms
- [ ] Main file scannable (headings, checklists)
- [ ] Commands copy-pasteable and tested
- [ ] No secrets or internal URLs that expire without notice
- [ ] Long content split into `reference.md`
- [ ] Linked from `AGENTS.md` or README if repo-wide

## 12. Rehearsal questions

- Skill vs rule — which for “always use Prettier defaults”?
- What two things belong in a skill `description`?
- Why keep `SKILL.md` short and put details elsewhere?
- Same skill in Cursor and Claude Code — what changes, what stays the same?

**Related:** [How MCP works](../how-mcp-works/i-overview.md) (live tools vs static skills), [Agents & agentic workflows](../agents-and-agentic-workflows/i-overview.md), [Tools & orchestration](../tools-and-orchestration/i-overview.md), [Custom assistants](../custom-assistants-and-knowledge/i-overview.md), [Effective prompting](../effective-prompting/i-overview.md).