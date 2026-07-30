---
label: "II"
subtitle: "Install & vault setup"
group: "Obsidian"
order: 2
---
Obsidian — Part II
How to **install** Obsidian, **create a vault**, pick a **folder layout**, and configure basics so notes stay portable and Git-friendly.

## 1. Install

Download from [obsidian.md](https://obsidian.md) for **Windows**, **macOS**, or **Linux**. Mobile apps exist for iOS and Android (often paired with Obsidian Sync or a Git-based workflow).

| Platform | Tip |
|----------|-----|
| **Windows** | Installer or portable; vault path can live under `Documents` or next to repos |
| **macOS** | Drag to Applications; grant folder access when prompted |
| **Linux** | AppImage, Snap, or Flatpak — same vault format everywhere |

Obsidian is **free for personal use**; commercial use and Sync/Publish are separate paid products — check current licensing on the official site.

## 2. Create a vault

On first launch:

1. **Create new vault** — choose an empty folder (e.g. `~/notes/engineering-vault`).
2. Or **Open folder as vault** — point at an existing Markdown tree (e.g. a repo `docs/` folder).

```text
engineering-vault/
  .obsidian/              ← created by Obsidian (settings, plugins)
  README.md               ← optional landing note
  inbox/
  projects/
  reference/
  templates/
```

| Choice | Guidance |
|--------|----------|
| **One vault vs many** | One vault for linked personal knowledge; separate vaults for unrelated contexts (work vs personal) |
| **Vault inside a Git repo** | Common — entire repo or subfolder `notes/` is the vault |
| **Vault = monorepo `docs/`** | Works if you want notes versioned with the product |

## 3. Suggested folder layout (engineers)

No single standard — pick one and stay consistent:

```text
inbox/           ← quick captures, process weekly
daily/           ← YYYY-MM-DD.md (Daily notes plugin)
projects/        ← per-repo or per-initiative notes
reference/       ← stable facts: APIs, commands, cheatsheets
meetings/        ← optional
templates/       ← Templater / core Templates snippets
attachments/     ← images, PDFs (or per-note subfolders)
```

**PARA** (Projects, Areas, Resources, Archives) and **CODE** (Capture, Organize, Distill, Express) are popular frameworks — see [Engineering workflows](vii-engineering-workflows.md).

## 4. Essential settings

Open **Settings** (gear icon):

| Setting | Suggestion |
|---------|------------|
| **Files & links → New link format** | `Shortest path when possible` — readable wikilinks |
| **Files & links → Default location for new notes** | `In folder specified below` → `inbox/` or `daily/` |
| **Files & links → Attachment folder path** | `attachments/` — keeps images out of note root |
| **Editor → Strict line breaks** | Off unless you want GitHub-flavored single newlines |
| **Appearance → Theme** | Default is fine; community themes later |

## 5. `.obsidian` and Git

The `.obsidian/` folder holds workspace state, hotkeys, and plugin config.

| Commit to Git? | Files |
|----------------|-------|
| **Often yes** | `appearance.json`, `core-plugins.json`, `community-plugins.json`, `plugins/`, shared `snippets/` |
| **Often no** | `workspace.json`, `workspace-mobile.json` (machine-specific layout) |

Example `.gitignore` inside the vault:

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
```

Teams that share a vault usually commit **plugin list and settings** so everyone gets the same tooling.

## 6. Open vault from the command line (optional)

```bash
# macOS (after installing Obsidian.app)
open -a Obsidian ~/notes/engineering-vault

# Windows (typical install path)
"C:\Program Files\Obsidian\Obsidian.exe" "C:\Users\you\notes\engineering-vault"
```

Useful for scripts or pinning a dev vault next to a repo checkout.

## Rehearsal

- What is a **vault** in one sentence?
- Why put new notes in **`inbox/`** instead of the vault root?

## Next

Continue with [Markdown & editing](iii-markdown-and-editing.md) for syntax, callouts, and frontmatter.
