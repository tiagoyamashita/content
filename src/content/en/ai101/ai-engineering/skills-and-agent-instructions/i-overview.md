---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
Skills & agent instructions — overview

Deep dive on **skills & agent instructions** — how to teach an agent your workflows once, so you stop re-explaining them every chat.

## What this track covers

**Skills** and **instruction `.md` files** encode *your* rules: commit format, PR checklist, API envelope shape, doc frontmatter, deploy steps. The product loads them when the task matches — you write markdown; the agent follows it.

| You get | Without this layer |
|---------|-------------------|
| Same PR review every time | “Remember to check tests…” each diff |
| Agent knows `npm test` and folder layout | Guesses commands; edits wrong dirs |
| Team shares behaviour via git | Everyone’s agent behaves differently |

This is for **people who use agents daily** — especially **Cursor**, **Claude Code**, **Codex**, Claude Projects, and Custom GPTs. Not for training models.

## Skills vs live tools (MCP)

| | **Skills / rules / `AGENTS.md`** | **MCP / connectors** |
|---|----------------------------------|----------------------|
| **What** | Static markdown instructions | Live APIs (DB, Slack, browser, etc.) |
| **When** | “How *we* do X” | “Fetch / act on *current* data” |
| **Example** | PR review checklist skill | Query production logs via MCP |

Use both: skills tell the agent *your process*; MCP gives it *live access*. See [How MCP works](../how-mcp-works/i-overview.md).

## Project skills vs personal (user) skills

Cursor (and Claude Code) load skills from **two different places**. The rule is simple: **team process → repo**; **your habits → home folder**.

| | **Project skills** | **Personal (user) skills** |
|---|-------------------|---------------------------|
| **Cursor path** | `.cursor/skills/<skill-name>/SKILL.md` | `~/.cursor/skills/<skill-name>/SKILL.md` |
| **Claude Code path** | `.claude/skills/<skill-name>/SKILL.md` | `~/.claude/skills/<skill-name>/SKILL.md` |
| **Who sees it** | Everyone who clones the repo | Only you, on every repo you open |
| **Git** | **Commit and PR** like code | **Never commit** — lives outside the repo |
| **Good for** | PR review standards, deploy steps, repo frontmatter rules | Private runbooks, your commit tone, experiments |
| **Example** | `.cursor/skills/pr-review/SKILL.md` | `~/.cursor/skills/my-weekly-status/SKILL.md` |

```text
/home/you/
  ~/.cursor/skills/              ← YOUR machine only (not in any git repo)
    my-commit-style/SKILL.md

/path/to/your-project/           ← THIS repo (git tracks it)
  .cursor/skills/
    pr-review/SKILL.md
  AGENTS.md
```

**Do not** put custom skills in `~/.cursor/skills-cursor/` — that directory is for Cursor built-ins only.

### What else lives in the repo (git-managed)

| File / folder | Purpose | Commit? |
|---------------|---------|---------|
| **`AGENTS.md`** (repo root) | Stack, test commands, folder map — every agent reads this | Yes |
| **`.cursor/skills/`** | Team workflows | Yes |
| **`.cursor/rules/*.mdc`** | Always-on or glob-matched coding rules (Cursor-only) | Yes |
| **`docs/skills/`** | Optional **canonical** copy before syncing to `.cursor/` / `.claude/` | Yes |
| **`.claude/skills/`** | Same skills for Claude Code teammates | Yes (if team uses Claude Code) |
| **`CLAUDE.md`** | Claude Code standing prefs | Yes (optional) |

Personal skills never go in the repo — if you need a team workflow, move it from `~/.cursor/skills/` into `.cursor/skills/` and open a PR.

## Managing skills with git

Treat project skills as **source code**: versioned, reviewed, owned.

### What to commit

```bash
git add AGENTS.md
git add .cursor/skills/pr-review/SKILL.md
git add .cursor/skills/pr-review/scripts/smoke-test.sh   # if the skill ships a script
git add .cursor/rules/typescript-errors.mdc              # rules, not skills — still team config
```

**Include in git:** all of `.cursor/skills/`, `AGENTS.md`, optional `docs/skills/`, scripts under skill folders.

**Exclude from git:** nothing under `~/.cursor/` or `~/.claude/` (those paths are outside the repo anyway).

### Typical git workflow

| Step | Action |
|------|--------|
| **1. Branch** | `git checkout -b skills/add-pr-review` |
| **2. Add skill** | Create `.cursor/skills/pr-review/SKILL.md` (+ `reference.md`, `scripts/` if needed) |
| **3. Link in `AGENTS.md`** | Add a row under `## Skills` pointing to the skill path |
| **4. Test locally** | Fresh agent chat → prompt that should trigger the skill → verify behaviour |
| **5. PR** | Reviewers check instructions like code (wrong command = broken deploy) |
| **6. Merge** | Teammates get skills on `git pull` — no manual install |

### Keep skills in sync across tools

If some teammates use **Cursor** and others **Claude Code**, duplicate or sync the same `SKILL.md`:

| Strategy | How | Git note |
|----------|-----|----------|
| **Duplicate** | Copy to `.cursor/skills/` and `.claude/skills/` | Commit **both** folders |
| **Canonical `docs/skills/`** | Edit once in `docs/skills/pr-review/`, run sync script | Commit `docs/skills/` + synced copies |
| **Symlink** (local only) | `ln -s ../../docs/skills/pr-review .cursor/skills/pr-review` | Symlinks often **don’t** port well — document duplicate or script for CI |

Example sync script (commit to repo, run after editing `docs/skills/`):

```bash
#!/bin/sh
# scripts/sync-skills.sh — from repo root
set -e
for skill in docs/skills/*/; do
  name=$(basename "$skill")
  mkdir -p ".cursor/skills/$name" ".claude/skills/$name"
  cp "$skill/SKILL.md" ".cursor/skills/$name/SKILL.md"
  cp "$skill/SKILL.md" ".claude/skills/$name/SKILL.md"
done
echo "Synced skills to .cursor/ and .claude/"
```

Add to README: *“After changing `docs/skills/`, run `./scripts/sync-skills.sh`.”*

### PR and ownership practices

| Practice | Why |
|----------|-----|
| **One skill = one folder = one PR theme** | Easier review (“adds deploy-staging skill”) |
| **Name an owner** in skill footer or team doc | Someone updates when process changes |
| **Test in agent before merge** | Same bar as changing a runbook |
| **Changelog line in `SKILL.md`** | `<!-- v2: added staging smoke script 2026-07 -->` |
| **Don’t commit secrets** | Use env vars in scripts; reference in skill text only |

When `AGENTS.md` changes (new test command), update skills that say `npm test` in the **same PR** or immediately after — avoid drift.

### Clone / new teammate checklist

After `git clone` and opening the repo in Cursor:

1. **`AGENTS.md`** loads automatically (repo root).
2. **`.cursor/skills/`** is available — no extra install step.
3. **Personal skills** in `~/.cursor/skills/` still apply **in addition** to project skills (don’t duplicate conflicting instructions).
4. Optional: run `./scripts/sync-skills.sh` only if your team uses `docs/skills/` as source.

## Skills folder tree

How a typical **project** skills directory is organized. Each skill is a **folder** with a required **`SKILL.md`**; optional files hold detail the agent reads only when needed.

```text
repo/
├── AGENTS.md                          ← repo briefing (stack, tests, layout) — not a skill
├── .cursor/
│   ├── rules/                         ← always-on / glob rules (Cursor-only)
│   │   ├── typescript-errors.mdc
│   │   └── api-conventions.mdc
│   └── skills/                        ← project skills (commit to git)
│       ├── pr-review/
│       │   ├── SKILL.md               ← required — name, description, workflow
│       │   ├── reference.md           ← optional — long checklist, security notes
│       │   └── examples.md            ← optional — good/bad review samples
│       ├── conventional-commits/
│       │   └── SKILL.md
│       ├── deploy-staging/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── smoke-test.sh      ← optional — runnable helpers
│       └── incident-writeup/
│           ├── SKILL.md
│           └── reference.md
│
└── docs/skills/                       ← optional canonical copy (sync to .cursor/)
    └── pr-review/
        └── SKILL.md

~/.cursor/skills/                        ← personal skills (all your repos)
  ├── my-commit-style/
  │   └── SKILL.md
  └── private-runbook/
      ├── SKILL.md
      └── reference.md
```

### Where scripts live (not inside the `.md`)

Scripts are **real files on disk** in a `scripts/` subfolder next to `SKILL.md`. They are **not** embedded inside the markdown.

```text
.cursor/skills/deploy-staging/
  SKILL.md              ← instructions only: WHEN to run, WHICH command
  scripts/
    smoke-test.sh       ← the actual bash script (separate file)
    validate.py         ← optional second script
```

| File | Contains |
|------|----------|
| **`SKILL.md`** | Text: “Run this command: `.cursor/skills/deploy-staging/scripts/smoke-test.sh`” |
| **`scripts/*.sh`** | Executable code the agent runs via **Shell** |
| **`reference.md`** | Extra prose — not executed |

The skill does **not** auto-run anything. The agent reads `SKILL.md`, then runs the path you wrote using the terminal tool — same as if you typed the command yourself.

**Alternative:** point `SKILL.md` at an existing repo script (e.g. `npm run smoke:staging` in `package.json`) instead of a file under `scripts/`. Full walkthrough: [Linking a fixed script](iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script).

| Path | Scope | Commit to git? |
|------|-------|----------------|
| `.cursor/skills/<name>/` | **Project** — team workflows in this repo | **Yes** |
| `.claude/skills/<name>/` | **Project** — Claude Code teammates | **Yes** (if used) |
| `docs/skills/<name>/` | **Project** — canonical copy for sync | **Yes** |
| `AGENTS.md`, `.cursor/rules/*.mdc` | **Project** — briefing + rules | **Yes** |
| `~/.cursor/skills/<name>/` | **Personal** — all your repos | **No** (outside repo) |
| `~/.claude/skills/<name>/` | **Personal** — Claude Code | **No** (outside repo) |

### Quick picker: where should this live?

| You want… | Put it here |
|-----------|-------------|
| Whole team uses same PR review checklist | `.cursor/skills/pr-review/` → **git commit** |
| Only you want a custom weekly-status format | `~/.cursor/skills/weekly-status/` → **not in git** |
| Every agent knows `npm test` and folder layout | `AGENTS.md` at repo root → **git commit** |
| TypeScript files always use our error types | `.cursor/rules/*.mdc` → **git commit** |
| Same skill for Cursor + Claude Code | `.cursor/skills/` + `.claude/skills/` or `docs/skills/` + sync script |
| Fixed bash/Python script for a workflow | `.cursor/skills/<name>/scripts/*.sh` — **not** pasted into `SKILL.md` |
| Promoted from chat — now team policy | Move from personal folder to `.cursor/skills/`, open PR |

One skill folder = one workflow. Split large topics (e.g. `pr-review` vs `deploy-staging`) instead of one mega-skill. Put fixed commands in **`scripts/`** and reference them from `SKILL.md` — see [Linking a fixed script](iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script). Multi-tool details: [Cross-tool portable setup](iii-cross-tool-portable-setup.md).

## Map of this submenu

| Note | Focus |
|------|--------|
| [Artifacts & why bother](ii-artifacts-why-and-what.md) | What to create, which product uses which artifact |
| [Artifact examples](iia-artifact-examples.md) | Copy-paste samples for every artifact type |
| [Cross-tool portable setup](iii-cross-tool-portable-setup.md) | One repo, Cursor + Claude Code + Codex |
| [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) | Cursor layout, rules vs skills, `AGENTS.md`, **linking scripts** |
| [Writing & maintaining skills](v-writing-and-maintaining-skills.md) | Descriptions, progressive disclosure, team workflow |
| **[Using skills, agents & hooks](using-skills-agents-and-hooks/i-overview.md)** | Skills vs `AGENTS.md` vs hooks; [agent orchestration](using-skills-agents-and-hooks/vi-agent-orchestration.md) |
| **[Examples](examples/i-overview.md)** | Parameterized scripts, loop on logs, commit hooks, perf scans — all with runtime JSON logs |

**Related loop:** [Persistent instructions](../loop-prompting/iii-persistent-instructions.md) — when to promote chat text into skills.

## Study order

[Artifacts & why bother](ii-artifacts-why-and-what.md) → [Artifact examples](iia-artifact-examples.md) → [Cross-tool portable setup](iii-cross-tool-portable-setup.md) → [Cursor skills, rules & AGENTS.md](iv-cursor-skills-rules-agents-md.md) → [Writing & maintaining skills](v-writing-and-maintaining-skills.md) → **[Using skills, agents & hooks](using-skills-agents-and-hooks/i-overview.md)** → **[Examples](examples/i-overview.md)** when you want copy-paste scripts with logging

## Start here (15 minutes)

1. **`AGENTS.md`** at repo root — stack, `npm test`, folder map → **commit to git**. See [Artifact examples](iia-artifact-examples.md) §3.
2. **One project skill** — `.cursor/skills/commit-messages/SKILL.md` (or `pr-review`) → **commit to git**. Not `~/.cursor/skills/` unless it stays personal.
3. Fresh chat → short prompt → refine `description` if the skill does not load.
4. Optional personal skill in `~/.cursor/skills/` only for habits you do **not** want the team to inherit.
