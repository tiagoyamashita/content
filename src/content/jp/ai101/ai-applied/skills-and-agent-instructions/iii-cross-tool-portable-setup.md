---
label: "III"
subtitle: "Cross-tool portable setup"
group: "AI Applied"
order: 3
---
Cross-tool portable setup

## 3. Cross-tool: Cursor, Claude Code, Codex

**Short answer:** yes — the **same idea** works across tools, but **folder paths differ**. The **`SKILL.md` format** is an open pattern ([Agent Skills](https://agentskills.io)); **`AGENTS.md`** is the cross-tool “README for agents.”

| Tool | Skills folder | Project context | Notes |
|------|---------------|-----------------|-------|
| **Cursor** | `.cursor/skills/name/SKILL.md` or `~/.cursor/skills/` | `AGENTS.md`, `.cursor/rules/*.mdc` | Rules (`.mdc`) are Cursor-only |
| **Claude Code** | `.claude/skills/name/SKILL.md` or `~/.claude/skills/` | `CLAUDE.md`, `AGENTS.md` | Invoke with `/skill-name`; same YAML frontmatter |
| **OpenAI Codex** | Skills via Codex config / discovery | `AGENTS.md` (root + nested), `~/.codex/AGENTS.md` | Loads `AGENTS.md` chain automatically; 32 KiB default cap |
| **GitHub Copilot** | Agent Skills (evolving) | `AGENTS.md`, `.github/copilot-instructions.md` | Prefer `AGENTS.md` for portability |
| **Windsurf, Aider, others** | Varies | Often reads **`AGENTS.md`** | Check tool docs |

### Portable setup (one repo, many agents)

```text
repo/
  AGENTS.md                 ← everyone reads this (stack, commands, layout)
  .cursor/skills/           ← Cursor
    pr-review/SKILL.md
  .claude/skills/           ← Claude Code (can symlink or duplicate)
    pr-review/SKILL.md
```

| Strategy | Detail |
|----------|--------|
| **Same body, two folders** | Copy or symlink `SKILL.md` into `.cursor/skills/` and `.claude/skills/` |
| **AGENTS.md only** | One file for baseline; tool-specific skills for heavy workflows |
| **Single source in `docs/skills/`** | Copy into each tool folder in CI or manually when updating |

Content in `SKILL.md` (name, description, checklist, templates) transfers well — only the **parent directory** changes.

### What does *not* port directly

| Cursor-only | Use elsewhere as |
|-------------|------------------|
| `.cursor/rules/*.mdc` | Paste into `AGENTS.md` or `CLAUDE.md` |
| `disable-model-invocation` in frontmatter | Claude Code: similar flags; Codex: manual skill config |
| `@file` Cursor mentions | Claude Code `@` imports; Codex: paths in `AGENTS.md` |

### Codex specifics

- **`AGENTS.md`** at repo root (and nested dirs) is loaded **automatically** each run — closest to “always-on” context.
- **Skills** in Codex are a separate layer (metadata + instructions); configure per [Codex docs](https://developers.openai.com/codex/guides/agents-md).
- Run `codex /init` to scaffold `AGENTS.md`; keep under the size limit or raise `project_doc_max_bytes`.

### Claude Code specifics

- Same **`SKILL.md`** shape as Cursor: `name`, `description`, markdown body.
- **`/skill-name`** runs a skill manually; good description → auto-load when relevant.
- Long procedures belong in skills; stable facts in **`CLAUDE.md`** or **`AGENTS.md`**.