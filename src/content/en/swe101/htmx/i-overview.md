---
label: "I"
subtitle: "Overview"
group: "HTMX"
order: 1
---
HTMX — overview
**HTMX** extends HTML with attributes so the browser can **fetch partial updates from the server** without writing a client-side SPA framework. The server returns **HTML fragments**; HTMX swaps them into the page. You keep **server-rendered templates** and gain **dynamic UX** — forms, tabs, infinite scroll, modals — with less JavaScript.

For REST and server-side rendering context, see [REST controllers](../java/springboot/iv-rest-controllers.md). For caching static assets vs dynamic HTML, see [CDN](../cdn/i-overview.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Hypermedia vs SPA, where HTMX fits |
| **II — Install & setup** | Script tag, CSP, local dev |
| **III — Core attributes & swapping** | `hx-get`, `hx-target`, `hx-swap`, triggers |
| **IV — Forms & requests** | POST, `hx-vals`, CSRF, uploads |
| **V — Server responses & templates** | Partials, `HX-*` headers, status codes |
| **VI — Events & extensions** | `htmx:*` events, SSE, WebSockets |
| **VII — Patterns & app integration** | Pagination, modals, Spring/Flask/FastAPI |
| **VIII — When to use & tradeoffs** | vs React/Vue, limits, team fit |
| **IX — Examples** | Runnable mini-apps — file tree + commented source |

## Hypermedia-driven apps

```text
Classic multi-page app (MPA)
  User click  →  full page reload  →  new HTML document

SPA (React/Vue)
  User click  →  JS fetches JSON  →  client renders DOM

HTMX
  User click  →  fetch HTML fragment  →  swap into existing page
```

| Approach | Server sends | Client does |
|----------|--------------|-------------|
| **MPA** | Full HTML page | Browser replaces document |
| **SPA** | JSON (+ separate static JS bundle) | Framework builds UI |
| **HTMX** | HTML partial (or full page) | Swap into target element |

HTMX is **not** anti-JavaScript — it removes **boilerplate fetch/render** for common CRUD and navigation patterns. You still add JS for rich widgets when needed.

## What HTMX adds to HTML

| Attribute family | Role |
|------------------|------|
| **`hx-get` / `hx-post` / …** | HTTP method + URL for the request |
| **`hx-target`** | CSS selector of element to update |
| **`hx-swap`** | How to insert response (`innerHTML`, `outerHTML`, `beforeend`, …) |
| **`hx-trigger`** | When to fire (click, submit, `keyup changed delay:500ms`, …) |
| **`hx-boost`** | Upgrade normal links/forms to AJAX without rewriting markup |

No build step required — one `<script>` tag from CDN or self-hosted static file.

## Where HTMX fits in the stack

```text
Browser  →  HTMX (attributes + swap)  →  HTTP  →  App server (templates)
                                                      ↓
                                              Postgres / Redis / …
```

| Layer | HTMX interaction |
|-------|------------------|
| **Templates** (Thymeleaf, Jinja, ERB, …) | Return partials for `hx-*` requests |
| **REST/ MVC controllers** | Same routes; branch on `HX-Request` header if needed |
| **Database** | Unchanged — HTMX is a UI transport layer |
| **CDN** | Cache static JS/CSS; dynamic HTML usually bypasses CDN |

Pair with [Postgres](../postgres/i-overview.md) or [MongoDB](../mongodb/i-overview.md) on the backend; use [Redis](../redis/i-overview.md) for sessions or cache as usual.

## Good fits

| Use case | Why HTMX works |
|----------|----------------|
| Admin dashboards, internal tools | Fast to ship; server owns validation |
| CRUD with inline edit | Swap table rows or form panels |
| Search-as-you-type | `hx-trigger="keyup changed delay:300ms"` |
| Tabs, accordions, modals | Partial HTML per tab/panel |
| Progressive enhancement | Works without JS; enhanced with HTMX |

## Poor default (consider SPA or native mobile instead)

| Situation | Reason |
|-----------|--------|
| Offline-first PWA | HTMX assumes network for each interaction |
| Heavy client state (canvas, games, spreadsheets) | DOM swap is wrong model |
| Complex client-only routing across 50+ screens | SPA router may be simpler |
| Real-time collaboration at Google Docs scale | Need dedicated client architecture |

## Core vocabulary

| Term | Meaning |
|------|---------|
| **Partial / fragment** | HTML snippet returned for one region of the page |
| **Swap** | Replace or append DOM with response HTML |
| **Boost** | Intercept normal navigation; request via AJAX |
| **`HX-Request`** | Request header HTMX sets — server detects partial requests |
| **Out-of-band (OOB)** | Response updates multiple targets via `hx-swap-oob` |

## Next

Continue with [Install & setup](ii-install-and-setup.md) to add HTMX to a page and verify the first swap.
