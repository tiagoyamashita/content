---
label: "VIII"
subtitle: "使い分けとトレードオフ"
group: "HTMX"
order: 8
---
HTMX — 使い分けとトレードオフ

HTMX is a **deliberate architectural choice**: hypermedia on the server, minimal client state. Choose based on product constraints, not hype.

## 1. Decision matrix

| Factor | Favor HTMX | Favor SPA |
|--------|------------|-----------|
| Team strength | Backend-heavy, strong templates | Deep frontend specialists |
| UI complexity | Forms, tables, dashboards | Rich editors, canvases |
| Time to MVP | Few moving parts | More tooling, state management |

## 2. Hybrid architectures

Marketing site (static/SSR) + HTMX app shell for authenticated CRUD + JSON API for mobile + React **islands** for heavy widgets.

## 3. When not to use HTMX

Collaborative editing (OT/CRDT), media/CAD/games, native mobile shells, strict API-only backends.

## 4. Related SWE101 tracks

[Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md), [Python](../python/i-basics-and-syntax.md), [Postgres](../postgres/i-overview.md), [CDN](../cdn/i-overview.md), [API gateway](../api-gateway/i-overview.md).

## Further reading

- [htmx.org documentation](https://htmx.org/docs/)
- [hypermedia.systems](https://hypermedia.systems/)
