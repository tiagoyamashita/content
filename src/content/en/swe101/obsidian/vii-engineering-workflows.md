---
label: "VII"
subtitle: "Engineering workflows"
group: "Obsidian"
order: 7
---
Obsidian — Part VII
Practical patterns for **software engineers**: daily notes, **ADRs**, **runbooks**, learning logs, and lightweight **PKM** frameworks — without turning the vault into a second issue tracker.

## 1. Daily notes

Enable **Daily notes** (core plugin). Each day: `daily/2026-07-06.md`.

```markdown
# 2026-07-06

## Standup
- Shipped [[ADR-003 idempotency]] review
- Blocked on staging Redis memory

## Log
- 14:00 incident #4421 — see [[runbook-payments-failures]]

## Links
- PR: https://github.com/org/repo/pull/120
```

| Use | Avoid |
|-----|--------|
| Timestamped work log, links to real artifacts | Duplicating entire ticket descriptions |
| Bridge to permanent notes | Leaving everything only in dailies |

Weekly: promote durable facts to **reference** or **project** notes; archive or trim old dailies.

## 2. Architecture Decision Records (ADRs)

One file per decision with stable ID:

```markdown
---
title: ADR-003 Idempotent checkout API
date: 2026-07-06
status: accepted
tags: [adr, payments]
---

# ADR-003 Idempotent checkout API

## Context
Duplicate POSTs from mobile clients can double-charge.

## Decision
Require `Idempotency-Key` header; store keys in [[Redis]] with 24h TTL.

## Consequences
- Clients must generate UUIDs
- See [[Postgres]] for ledger truth

## Alternatives considered
- DB unique constraint only — rejected (partial failures)
```

Link ADRs from a **MOC — Architecture** and from service READMEs in the code repo.

## 3. Runbooks and on-call

```markdown
---
tags: [runbook, on-call, payments]
severity: high
---

# Runbook — Payment gateway timeouts

## Symptoms
- Alert: `payment_latency_p99 > 2s`
- User reports: checkout spinner

## First steps
1. Check status page (vendor)
2. `kubectl logs deploy/payment-api --tail=100`
3. Compare with [[ADR-003 Idempotent checkout API]]

## Escalation
- #payments-oncall Slack
- [[MOC — On-call]]

## Post-incident
- Create note in `incidents/YYYY-MM-DD-short-title.md`
```

Keep commands copy-pasteable; link to dashboards rather than embedding secrets.

## 4. Learning and course notes

When studying SWE101 or a new stack:

```markdown
# MOC — Redis

- [[redis/i-overview]] — course summary
- [[Cache-aside pattern]] — my words + example
- Practice: [[redis-cli cheatsheet]]
```

Summarize in **your own notes**; link to canonical course paths — do not paste entire copyrighted tracks into the vault.

## 5. PARA and CODE (lightweight)

**PARA** — organize by actionability:

| Bucket | Contents |
|--------|----------|
| **Projects** | Active work with deadline — `projects/checkout-v2/` |
| **Areas** | Ongoing standards — `areas/engineering-health/` |
| **Resources** | Reference — `reference/kafka/`, cheatsheets |
| **Archives** | Inactive — `archives/` |

**CODE** — workflow:

1. **Capture** → `inbox/`
2. **Organize** → folders + links + tags
3. **Distill** → bold key ideas, add summaries at top of long notes
4. **Express** → ADRs, PR descriptions, blog drafts from notes

## 6. Integrate with the code repo

| Pattern | How |
|---------|-----|
| **Docs in repo, Obsidian opens repo** | Vault root = monorepo; edit `docs/` in Obsidian |
| **Separate vault, link out** | Notes link to GitHub paths and PRs |
| **Snippets** | Store reusable `curl` / SQL in reference notes; link from code comments sparingly |

Align with [Docs, repos & CI](../languages&frameworks/mermaid/vi-docs-repos-and-ci.md) (Mermaid) and [Docs, repos & CI](../languages&frameworks/plantuml/vi-docs-repos-and-ci.md) (PlantUML) when diagrams live in the same tree.

## 7. Anti-patterns

| Anti-pattern | Better approach |
|--------------|-----------------|
| Second Jira in Obsidian | Tickets in tracker; vault holds context and decisions |
| Thousand orphan notes | Weekly inbox processing + MOCs |
| No filenames discipline | Rename early; use `adr-`, `runbook-` prefixes |
| Pasting secrets | Reference secret *names*; values in vault store |
| Plugin hoarding | Start core-only; add Git + Templater when pain is real |

## Rehearsal

- What belongs in an **ADR** vs a **runbook**?
- How do **daily notes** connect to permanent project notes?

## Next

You have the full Obsidian track — pair it with **Git** essentials — [Overview](../git/essentials/i-overview.md) and diagram tracks (**Mermaid** — [Overview](../languages&frameworks/mermaid/i-overview.md), **PlantUML** — [Overview](../languages&frameworks/plantuml/i-overview.md)) for a docs workflow that stays in version control.
