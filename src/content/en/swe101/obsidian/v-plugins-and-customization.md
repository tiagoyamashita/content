---
label: "V"
subtitle: "Plugins & customization"
group: "Obsidian"
order: 5
---
Obsidian — Part V
**Core plugins** ship with the app; **community plugins** extend Git sync, templates, queries, and linting. Enable only what you need — fewer plugins means fewer upgrades and security surfaces.

## 1. Core plugins (commonly enabled)

Open **Settings → Core plugins**:

| Plugin | Purpose |
|--------|---------|
| **Daily notes** | `YYYY-MM-DD.md` in a configured folder — journaling, standup log |
| **Templates** | Insert snippets from `templates/` with hotkey |
| **Backlinks** | Incoming / outgoing link panels |
| **Graph view** | Local and global graph |
| **Outline** | Table of contents for long notes |
| **Tag pane** | Browse `#tags` |
| **Search** | Full-text search |
| **Mermaid** | Render ` ```mermaid ` blocks |
| **Properties** | UI for YAML frontmatter |

Disable **Publish**, **Sync**, etc. if you use Git instead.

## 2. Community plugins — engineer favorites

Install via **Settings → Community plugins → Browse** (requires Restricted mode off for third-party plugins).

| Plugin | Use case |
|--------|----------|
| **Obsidian Git** | Commit, pull, push vault from inside the app — see [Git sync](vi-git-sync-and-team-workflows.md) |
| **Templater** | Dynamic templates (`<% tp.date.now() %>`) — ADRs, meeting notes |
| **Dataview** | Query notes like a table: `TABLE status FROM #adr` |
| **Calendar** | UI for daily notes |
| **Linter** | Format Markdown on save — consistent headings, lists |
| **Excalidraw** | Sketches and architecture whiteboards |
| **Advanced Tables** | Spreadsheet-like table editing |
| **Style Settings** | Tune theme CSS variables |

Pin plugin versions in team vaults: commit `.obsidian/plugins/<id>/manifest.json` after upgrades and test on one machine first.

## 3. Templates example (ADR)

`templates/adr.md`:

```markdown
---
title: ADR-<%= tp.file.title %>
date: <% tp.date.now("YYYY-MM-DD") %>
status: proposed
tags:
  - adr
---

# <% tp.file.title %>

## Context

## Decision

## Consequences

## Links
- 
```

Create note from template → filename `adr-004-event-sourcing` → filled dates and tags.

## 4. Dataview example

Index all ADRs by status:

````markdown
```dataview
TABLE status, date
FROM #adr
SORT date DESC
```
````

Requires **Dataview** plugin and consistent frontmatter (`status`, `date`).

## 5. Themes and CSS snippets

| Layer | Location |
|-------|----------|
| **Community theme** | Settings → Appearance → Themes |
| **CSS snippets** | `.obsidian/snippets/*.css` — enable in Appearance |

Keep snippets small — dark-mode contrast for code blocks is a common tweak.

## 6. Security and trust

Community plugins run with access to your vault files.

| Practice | Reason |
|----------|--------|
| Prefer **popular, maintained** plugins | Reduces abandoned-code risk |
| Review plugin **GitHub repo** for work vaults | Supply-chain awareness |
| Separate **work / personal** vaults | Limits blast radius |
| Do not store **secrets** in notes | Use a password manager; see [Secrets in Git history](../git/essentials/viii-secrets-and-sensitive-files-in-history.md) |

## Rehearsal

- Name one **core** and one **community** plugin you would enable for a daily engineering journal.
- What does **Dataview** add that folders alone do not?

## Next

Continue with [Git sync & team workflows](vi-git-sync-and-team-workflows.md) to version the vault with Git.
