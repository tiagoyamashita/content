---
label: "III"
subtitle: "Cross-tool portable setup"
group: "AI Applied"
order: 4
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

### What ports vs what does not

| Ports everywhere | Tool-specific |
|------------------|---------------|
| `AGENTS.md` body | `.cursor/rules/*.mdc` |
| `SKILL.md` name, description, markdown body | Cursor `@` mention syntax |
| Checklists, commands, templates | `disable-model-invocation` handling |
| `docs/` context files | Personal skill paths (`~/.cursor/` vs `~/.claude/`) |

Paste Cursor-only rules into **`AGENTS.md`** or **`CLAUDE.md`** when teammates use other agents.

## Portable setup (one repo, many agents)

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

### Sync strategies

| Strategy | Detail | Best when |
|----------|--------|-----------|
| **Duplicate** | Same `SKILL.md` in `.cursor/` and `.claude/` | Small team; few skills |
| **Symlink** | One file, two paths (OS permitting) | Local dev on macOS/Linux |
| **`docs/skills/` source** | Canonical copy; script copies on change | CI or pre-commit sync |
| **`AGENTS.md` only** | No per-tool skills; workflows in linked docs | Light agent use |

Example sync script (manual or CI):

```bash
#!/bin/sh
# sync-skills.sh — run from repo root
for skill in docs/skills/*/; do
  name=$(basename "$skill")
  cp "$skill/SKILL.md" ".cursor/skills/$name/SKILL.md"
  cp "$skill/SKILL.md" ".claude/skills/$name/SKILL.md"
done
```

Document “run `./sync-skills.sh` after editing skills” in README.

Content in `SKILL.md` (name, description, checklist, templates) transfers well — only the **parent directory** changes.

### What does *not* port directly

| Cursor-only | Use elsewhere as |
|-------------|------------------|
| `.cursor/rules/*.mdc` | Bullet list in `AGENTS.md` or `CLAUDE.md` |
| `disable-model-invocation` in frontmatter | Claude Code: similar flags; Codex: manual skill config |
| `@file` Cursor mentions | Claude Code `@` imports; Codex: paths in `AGENTS.md` |

## Codex specifics

- **`AGENTS.md`** at repo root (and nested dirs) is loaded **automatically** each run — closest to “always-on” context.
- **Skills** in Codex are a separate layer (metadata + instructions); configure per [Codex docs](https://developers.openai.com/codex/guides/agents-md).
- Run `codex /init` to scaffold `AGENTS.md`; keep under the size limit or raise `project_doc_max_bytes`.
- **Monorepos:** add package-level `AGENTS.md` with local test commands; Codex walks up/down the tree.

```text
monorepo/
  AGENTS.md                 # global: node version, CI entry
  apps/web/AGENTS.md        # npm run dev, Playwright paths
  apps/api/AGENTS.md        # go test ./..., OpenAPI location
```

## Claude Code specifics

- Same **`SKILL.md`** shape as Cursor: `name`, `description`, markdown body.
- **`/skill-name`** runs a skill manually; good `description` → auto-load when relevant.
- Long procedures belong in **skills**; stable facts in **`CLAUDE.md`** or **`AGENTS.md`**.
- **`CLAUDE.md`** is not a substitute for skills — keep deploy/review runbooks in `.claude/skills/`.

## Copilot and `.github/copilot-instructions.md`

Copilot may read **`.github/copilot-instructions.md`**. For portability, keep **`AGENTS.md`** as source of truth and either:

- Duplicate a short summary into `copilot-instructions.md`, or
- Point Copilot users to `AGENTS.md` in team docs.

Prefer one maintained file over three diverging copies.

## Maintenance when tools update

| Event | Action |
|-------|--------|
| New team member on different IDE | Verify `AGENTS.md` + their tool’s skill folder |
| Skill `description` stops triggering | Re-test in fresh session; add trigger synonyms |
| Codex “context too large” | Trim `AGENTS.md`; link to `docs/` |
| Process change (new test command) | Update `AGENTS.md` first, then skills that reference it |

**Next:** [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) for Cursor-only details.
