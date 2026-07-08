# content

Personal curriculum notes in Markdown — software engineering, AI, SRE, CS fundamentals, and related topics. Notes are version-controlled here and designed to load in **Cursor Notes** (or any editor with Markdown preview) from GitHub.

**Repository:** [github.com/tiagoyamashita/content](https://github.com/tiagoyamashita/content)

## What's inside

Notes live under **`src/content/`**, split by locale:

| Locale | Path | Description |
|--------|------|-------------|
| **English** | `src/content/en/` | Primary curriculum |
| **Japanese** | `src/content/jp/` | Translated / localized notes (partial coverage) |

Each locale has top-level **tracks** (sidebar sections), for example:

| Track | Topics |
|-------|--------|
| **Getting started** | How this repo is organized |
| **CS101** | Algorithms, data structures, databases, networking |
| **SWE101** | Languages, Git, system design, databases, Kafka, CDN, … |
| **SRE101** | CI/CD, cloud architecture, Kubernetes, Terraform, observability |
| **AI101** | LLMs, ML, deep learning, AI engineering |
| **Digital marketing** | SEO, content strategy, analytics, email, paid ads |
| **Cryptocurrency101** | Blockchain concepts and network examples |
| **Startups** | Free services and practical tooling |
| **Languages** | Japanese language notes |
| **Food** | Baking and related notes |

Tracks can nest submenus (e.g. `swe101/languages&frameworks/mermaid/`). Section order and titles come from **`_meta.json`** files; each note is a **`.md`** file with YAML frontmatter.

## English content map

One **Mermaid mindmap per top-level track** under **`src/content/en/`** (less cluttered than a single repo-wide diagram). Full index: **[`scripts/output/en-mindmaps/index.md`](scripts/output/en-mindmaps/index.md)**.

Regenerate after adding or renaming sections:

```bash
python scripts/generate-en-mindmap.py
```

Folders can be omitted via **`scripts/en-mindmap-exclude.json`** or **`"mindmapExclude": true`** in a folder’s `_meta.json`.

<!-- EN-MINDMAP-INDEX-START -->

| Track | Mindmap |
|-------|---------|
| Getting started | [Getting started](scripts/output/en-mindmaps/getting-started.md) |
| CS101 | [CS101](scripts/output/en-mindmaps/cs101.md) |
| SWE101 | [SWE101](scripts/output/en-mindmaps/swe101.md) |
| SRE101 | [SRE101](scripts/output/en-mindmaps/sre101.md) |
| Cybersecurity | [Cybersecurity](scripts/output/en-mindmaps/cybersecurity.md) |
| Food | [Food](scripts/output/en-mindmaps/food.md) |
| Languages | [Languages](scripts/output/en-mindmaps/languages.md) |
| Digital marketing | [Digital marketing](scripts/output/en-mindmaps/digital-marketing.md) |
| AI101 | [AI101](scripts/output/en-mindmaps/ai101.md) |
| Cryptocurrency101 | [Cryptocurrency101](scripts/output/en-mindmaps/cryptocurrency101.md) |
| Startups | [Startups](scripts/output/en-mindmaps/startups.md) |

<!-- EN-MINDMAP-INDEX-END -->

## Repository layout

```text
content/
├── README.md                 ← this file
├── scripts/                  ← maintenance utilities (Python)
│   └── output/               ← generated graph JSON, mindmaps
└── src/
    └── content/
        ├── en/               ← English notes
        │   ├── _meta.json
        │   ├── getting-started/
        │   ├── swe101/
        │   └── …
        └── jp/               ← Japanese notes
            ├── _meta.json
            └── …
```

## Quick start

### Browse locally

```bash
git clone https://github.com/tiagoyamashita/content.git
cd content
```

Open the folder in **Cursor** or VS Code. Read and edit Markdown under `src/content/en/` (or `jp/`).

### Load from GitHub in Cursor Notes

1. Open **GitHub** settings from the Notes menu.
2. Set **owner/repo** to `tiagoyamashita/content`.
3. Set **branch** to **`main`**.
4. Set **content path** to **`src/content`** (or `src/content/en` if your viewer expects a single locale root).
5. For a private fork, use a token with **Contents: Read** (or write, if you edit through the UI).

After pushing new folders or files, refresh or resync so the sidebar updates.

## Authoring conventions

Every note starts with YAML frontmatter:

```yaml
---
label: "I"
subtitle: "Overview"
group: "SWE101"
order: 1
---
```

Filenames follow **`{label}-{subtitle-slug}.md`** in kebab-case (e.g. `i-overview.md`, `iii-sequence-diagrams.md`).

Each folder that appears in the sidebar needs **`_meta.json`**:

```json
{
  "label": "Human-readable title",
  "order": 3
}
```

**Cross-links** between notes use markdown with relative paths:

```markdown
See [Core building blocks](../sysdesign/i-core-building-blocks.md).
```

Full rules — naming, nested submenus, link style, checklists — are in the in-repo guide:

**[Topics and folders](src/content/en/getting-started/guide-topics-and-folders.md)**

Intro walkthrough: **[Installation](src/content/en/getting-started/intro/i-installation.md)** · **[Setup](src/content/en/getting-started/intro/ii-setup.md)**

## Maintenance scripts

Python utilities under **`scripts/`** (stdlib + optional deps; run from repo root):

| Script | Purpose |
|--------|---------|
| **`generate-en-mindmap.py`** | One Mermaid mindmap per `src/content/en/` track → `scripts/output/en-mindmaps/` |
| **`linkify-content-refs.py`** | Turn bare `` `path/to/note.md` `` references into markdown links |
| **`build-content-graph.py`** | Export note graph / cluster JSON to `scripts/output/` |
| **`translate-content-ja.py`** | Translate English prose to Japanese under `src/content/jp/` |
| **`migrate-ai-applied.py`** | One-off migration helpers for AI101 folder moves |
| **`restore-content-en.py`** | Restore / repair English content from backups |

Examples:

```bash
python scripts/generate-en-mindmap.py
python scripts/linkify-content-refs.py
python scripts/build-content-graph.py --format both --locale en
```

## Contributing

This is a personal notes repository. If you fork it:

- Keep **`_meta.json`** `order` values consistent among siblings.
- Match existing frontmatter and filename patterns.
- Prefer **`git mv`** when renaming files so links and history stay clean.
- Run **`linkify-content-refs.py`** after bulk path or reference edits.

Default branch: **`main`**.

## License

No license file is included. Treat content as personal notes unless the owner adds an explicit license.
