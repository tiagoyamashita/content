---
label: "IV"
subtitle: "Links, graph & tags"
group: "Obsidian"
order: 4
---
Obsidian — Part IV
**Links** turn isolated notes into a **knowledge graph**. **Backlinks**, the **graph view**, **tags**, and **MOCs** (maps of content) help you navigate without a rigid folder hierarchy.

## 1. Wikilinks in practice

Prefer **meaningful note titles** — the title is the link target:

```markdown
# Redis cache-aside

When read load dominates, use [[Postgres]] as source of truth and [[Redis]] as cache.

Related: [[sysdesign/scalable-patterns/ii-caching]] (if vault includes course notes).
```

| Pattern | Example |
|---------|---------|
| **Concept note** | `[[Cache-aside]]` — one idea, many inbound links |
| **Project hub** | `[[Project Checkout v2]]` — links to ADRs, meetings, tasks |
| **Stub** | Create empty `[[Saga pattern]]` while writing; fill later |

**Outgoing links** are in the note you edit; **backlinks** appear in the right sidebar (linked mentions).

## 2. Backlinks and unlinked mentions

| Panel | Shows |
|-------|--------|
| **Backlinks** | Notes that link *to* the current note |
| **Outgoing links** | Notes linked *from* the current note |
| **Unlinked mentions** | Text that matches a note title but is not yet a wikilink — click to convert |

This is how a folder named `redis/` and a note `Cache-aside` stay connected even if you forgot to file under `redis/`.

## 3. Graph view

**Open graph view** from the ribbon or command palette.

| Control | Use |
|---------|-----|
| **Local graph** | Current note ± N hops — day-to-day navigation |
| **Global graph** | Entire vault — discovery, gaps |
| **Filters** | Hide tags, folders, orphans |
| **Groups** | Color by tag or path prefix |

```text
        [Postgres]
            ↑
    [Cache-aside] ←→ [Redis]
            ↓
      [Order API ADR]
```

Graph view is for **exploration**, not primary navigation — use links, search, and MOCs for daily work.

## 4. Tags

Tags are `#inline` or in frontmatter:

```markdown
---
tags:
  - runbook
  - on-call
  - payments
---

# Payments on-call runbook

#runbook #payments
```

| Tags vs folders | Guidance |
|-----------------|----------|
| **Folders** | One primary location; good for repo-style structure |
| **Tags** | Cross-cutting labels — `adr`, `draft`, `sre`, `java` |
| **Both** | File under `projects/checkout/` and tag `#adr` |

Avoid tag explosion — prefer a **controlled vocabulary** on team vaults (e.g. max ~20 common tags).

## 5. MOCs (maps of content)

A **MOC** is an index note that curates links — not a folder listing:

```markdown
# MOC — System design

## Patterns
- [[Cache-aside]]
- [[Transactional outbox]]
- [[Saga pattern]]

## Course track
- [[sysdesign/scalable-patterns/i-overview]]

## External
- [SWE101 scalable patterns](../sysdesign/scalable-patterns/i-overview.md)
```

Use MOCs for **onboarding** ("start here") and **topic hubs** too large for one folder.

## 6. Search

| Method | When |
|--------|------|
| **Quick switcher** (`Ctrl/Cmd+O`) | Open note by name |
| **Search** (`Ctrl/Cmd+Shift+F`) | Full-text across vault |
| **Search operators** | `path:projects tag:#adr "exact phrase"` |

For code repos, combine Obsidian search with `rg` in the terminal on the same vault path.

## 7. Aliases (frontmatter)

Disambiguate link text without renaming files:

```yaml
---
aliases:
  - cache aside
  - cache-aside pattern
---
```

`[[cache aside]]` resolves to this note.

## Rehearsal

- Backlinks vs outgoing links?
- When would you use a **MOC** instead of a deeper folder tree?

## Next

Continue with [Plugins & customization](v-plugins-and-customization.md) for core and community plugins.
