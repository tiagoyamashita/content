---
label: "I"
subtitle: "Overview"
group: "Obsidian"
order: 1
---
Obsidian — overview
**Obsidian** is a **local-first** note app built on **plain Markdown files**. Your notes live in a **vault** — a folder on disk — so you own the data, can sync with [Git](../git/essentials/i-overview.md), and open files in any editor. Engineers use it for **personal knowledge bases**, **RFC drafts**, **on-call runbooks**, **learning logs**, and **project wikis** that stay close to the repo without requiring a hosted wiki.

For diagram syntax inside notes, see [Mermaid](../languages&frameworks/mermaid/i-overview.md) and [PlantUML](../languages&frameworks/plantuml/i-overview.md). For version control when the vault is a repo, see [Git essentials](../git/essentials/i-overview.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Vault model, when Obsidian fits, vs other tools |
| **II — Install & vault setup** | Download, create a vault, folder layout |
| **III — Markdown & editing** | Syntax, callouts, frontmatter, live preview |
| **IV — Links, graph & tags** | Wikilinks, backlinks, graph view, MOCs |
| **V — Plugins & customization** | Core plugins, community plugins, themes |
| **VI — Git sync & team workflows** | obsidian-git, `.gitignore`, shared vaults |
| **VII — Engineering workflows** | Daily notes, ADRs, runbooks, PARA/CODE |

## Mental model

```text
Vault (folder on disk)
  └── .obsidian/          ← app settings (often committed selectively)
  └── notes/*.md          ← your content (plain Markdown)
        └── [[wikilinks]] connect notes
        └── #tags         classify without folders
```

| Piece | Role |
|-------|------|
| **Vault** | Root folder Obsidian opens — one knowledge base |
| **Note** | A `.md` file; filename becomes default link target |
| **Wikilink** | `[[Note title]]` — internal link between notes |
| **Plugin** | Extends sync, templates, linting, publishing |
| **Graph** | Visual map of links — useful for discovery, not navigation |

## Why engineers use Obsidian

| Strength | What it means in practice |
|----------|---------------------------|
| **Plain files** | Notes survive app changes; diff in Git; grep from terminal |
| **Fast linking** | `[[` autocomplete builds a web of concepts and runbooks |
| **Offline** | No account required; works on a plane or in a locked-down network |
| **Extensible** | Community plugins for Git, Dataview, Excalidraw, linting |
| **Low ceremony** | Start with one folder and a daily note — no database setup |

## Obsidian vs other options

| Tool | Strength | Trade-off |
|------|----------|-----------|
| **Obsidian** | Local Markdown + graph + plugins | Sync and mobile need setup (Git, Obsidian Sync, etc.) |
| **Notion** | Rich databases, sharing, comments | Hosted; export and offline weaker |
| **Confluence / wiki** | Team permissions, enterprise search | Heavy; not ideal for personal scratch notes |
| **VS Code + folder** | Already in the editor | No backlinks graph or note-centric UX out of the box |
| **Logseq** | Outliner-first, also local Markdown | Different mental model (blocks vs pages) |

**Rule of thumb:** use **Obsidian** when you want **your own** Markdown corpus with **links and plugins**, especially if you already sync docs with **Git**. Use a **hosted wiki** when non-technical stakeholders need permissions and search without cloning a repo.

## When Obsidian fits

| Good fit | Poor default |
|----------|--------------|
| Personal engineering notebook | Company-wide source of truth with strict ACLs alone |
| ADRs, design notes, learning logs | Real-time collaborative doc editing (Google Docs style) |
| Vault synced via Git next to code | Replacing production monitoring or ticket systems |
| Offline or air-gapped documentation | Notes that must only live in a SaaS with no local copy |

## Next

Continue with [Install & vault setup](ii-install-and-vault-setup.md) to create your first vault and a sensible folder layout.
