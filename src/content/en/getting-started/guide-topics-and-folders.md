---
label: "Guide"
subtitle: "Topics and folders"
group: "Getting started"
order: 10
---
Using this notes repo
How the folders and metadata fit together, and how to add a new topic.

## 1. Layout

All notes live under **`src/content/`**:

- **`src/content/_meta.json`** — root metadata for the whole library (required by GitHub-backed viewers such as Cursor Notes).
- **`src/content/<topic-folder>/`** — one folder per sidebar section (e.g. `python`, `sysdesign`).
- **`src/content/<topic-folder>/_meta.json`** — defines the section title and sort order among sections.
- **`src/content/<topic-folder>/*.md`** — individual notes (Markdown plus YAML frontmatter).
- **`src/content/<topic-folder>/<subfolder>/`** — optional nested folder for a **collapsible submenu** under that topic (each subfolder gets its own **`_meta.json`** and its own **`.md`** files).

Keep folder names short, lowercase, and hyphenated (`machine-learning`, not `Machine Learning`).

### Example in this repo

Under **`getting-started/`**, the **`intro/`** subfolder groups **Installation** and **Setup** as separate files—see **`getting-started/intro/_meta.json`** plus **`i-installation.md`** and **`ii-setup.md`**. Use the same pattern anywhere you want a submenu (`advanced/`, `labs/`, etc.).

## 2. Section metadata (`_meta.json`)

Each **topic** folder needs **`_meta.json`** next to its notes (and next to any subfolders):

```json
{
  "label": "Human-readable section title",
  "order": 3
}
```

Each **nested subfolder** (submenu) also has its own **`_meta.json`** with the same shape—the **`label`** becomes the submenu title in clients that support collapsible groups.

**`order`** controls placement among siblings (sections at the content root, or notes/subfolders inside one topic). Lower numbers appear earlier.

## 3. Note frontmatter

Every **`.md`** file starts with YAML between **`---`** lines:

```yaml
---
label: "I"
subtitle: "Basics & syntax"
group: "Python"
order: 1
---
```

| Field | Purpose |
|--------|---------|
| **`label`** | Short marker for ordering or numbering (Roman numerals, “Guide”, etc.). Used at the start of the filename (see below). |
| **`subtitle`** | Distinguishes the piece inside the section; becomes part of the filename. Omit only if the note is a single special page (see memory estimator example). |
| **`group`** | Display grouping / curriculum name; usually matches the topic’s theme (same string across notes in that topic is fine). |
| **`order`** | Sort order of this note **within** its folder (or within that group, depending on how your viewer sorts). |

Optional keys (only if you already use them elsewhere): e.g. **`groupOrder`**.

After the closing **`---`**, write a title line and the body in Markdown as usual.

## 4. File naming

Filenames follow:

**`{label}-{subtitle-slug}.md`** in **kebab-case** (lowercase; spaces and punctuation → hyphens; **`&`** → **`and`**).

Examples:

- label **`I`**, subtitle **`Overview`** → **`i-overview.md`** (e.g. **`ai101/machine-learning/i-overview.md`**)
- label **`III`**, subtitle **`Beans & dependency injection`** → **`iii-beans-and-dependency-injection.md`**

If there is **no** `subtitle`, use **`{label-slug}.md`** only (e.g. **`memory-estimator.md`**).

Avoid renaming files casually if bookmarks or external links point at GitHub paths; prefer **`git mv`** when you change names.

## 5. Adding a new topic (checklist)

1. Create **`src/content/<your-topic>/`**.
2. Add **`src/content/<your-topic>/_meta.json`** with **`label`** and **`order`**.
3. Add one or more **`.md`** files with frontmatter **`label`**, **`subtitle`** (unless the single-label exception applies), **`group`**, **`order`**, and a filename built from the rule above.
4. Optional: add **`src/content/<your-topic>/<subfolder>/`** with its own **`_meta.json`**, then put related **`.md`** files inside that subfolder (same frontmatter and naming rules).
5. Commit and push **`main`** (this repo uses **`main`**, not **`master`**).

## 6. Cursor Notes / GitHub settings

To load these notes from GitHub in Cursor:

1. Open **GitHub** settings from the Notes UI (menu).
2. Set **owner/repo** to your GitHub repository.
3. Set **branch** to **`main`** (or whatever branch you push to).
4. Set **content path** to **`src/content`** so the root **`_meta.json`** and all topic folders resolve correctly.
5. Use a token with repo access if the repository is private.

After changing folder or file names, refresh or sync so the client refetches the tree.

## 7. Quick template (topic + nested intro submenu)

**`_meta.json`** for a new topic **`robotics`**:

```json
{
  "label": "Robotics",
  "order": 10
}
```

**`src/content/robotics/i-overview.md`**:

```yaml
---
label: "I"
subtitle: "Overview"
group: "Robotics"
order: 1
---
Robotics — Part I: Overview

Your intro paragraph and sections follow here.
```

**Nested submenu** under robotics:

```text
src/content/robotics/intro/_meta.json
src/content/robotics/intro/i-installation.md
src/content/robotics/intro/ii-setup.md
```

**`intro/_meta.json`**:

```json
{
  "label": "Intro",
  "order": 1
}
```

That matches how **`getting-started/intro/`** is laid out in this repository.

## 8. Cross-links between notes

When pointing readers to another note in this repo, use **markdown links** with **relative paths** (not bare backtick filenames).

| Do | Don't |
|----|--------|
| `[Networking, VPC & LB](../foundations/vi-networking-vpc-and-lb.md)` | `` `vi-networking-vpc-and-lb.md` `` |
| `[Secrets & OIDC](../security-and-best-practices/iii-secrets-and-oidc.md)` | `` `../security-and-best-practices/iii-secrets-and-oidc.md` `` |

**Link text:** use the target note’s **`subtitle`** from frontmatter (e.g. “Networking, VPC & LB”). If there is no subtitle, use a short human title from the filename.

**Same submenu** — filename only is fine:

```markdown
**Related:** [HA & disaster recovery](vii-ha-and-disaster-recovery.md)
```

**Another submenu or topic** — include the path:

```markdown
See [Docker in CI](../../cicd/tools-and-platforms/v-docker-in-ci.md).
```

**Submenu name in prose** — keep bold for the sidebar label; link the overview or a specific note:

```markdown
**Patterns & design** submenu — start at [Overview](../patterns-and-design/i-overview.md).
```

**External URLs** — normal markdown links (`[Rust Book](https://doc.rust-lang.org/book/)`).

**Do not link** meta examples in this guide (filenames shown as naming rules), external repos’ `README.md`, or notes that do not exist yet.

To re-apply links after bulk edits, run:

```text
python scripts/linkify-content-refs.py
```
