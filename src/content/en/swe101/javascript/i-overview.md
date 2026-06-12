---
label: "I"
subtitle: "Overview"
group: "JavaScript"
order: 1
---
JavaScript — overview
**JavaScript** runs in the browser, on servers (Node.js), and in mobile/desktop shells. In SWE101 this track covers **common UI stacks** — DOM helpers, CSS frameworks, and SPA libraries. For server-rendered HTML with less client JS, see [HTMX](../htmx/i-overview.md).

## Map of this track

| Submenu | Focus |
|---------|--------|
| **jQuery** | DOM selection, events, AJAX — legacy and maintenance codebases |
| **React** | Components, hooks, ecosystem — setup, rendering, auth, forms (5 parts) |
| **Angular** | TypeScript-first framework — setup, rendering, auth, forms (5 parts) |
| **Bootstrap** | CSS + JS plugins — modals, collapse, dropdowns (vanilla JS in v5+) |

## Where JS fits in the stack

```text
Browser  →  HTML/CSS  →  JavaScript (jQuery / Bootstrap / React / Angular / vanilla)
Server   →  Node.js, bundlers (Vite, webpack), npm
```

| Layer | Role |
|-------|------|
| **HTML** | Document structure |
| **CSS** | Layout and style |
| **JavaScript** | Behavior, client state, API calls |
| **Build tool** | Bundle, transpile, tree-shake (React/Angular); optional for jQuery CDN |

## Picking an approach

| Situation | Reasonable default |
|-----------|-------------------|
| Greenfield SPA, large team | **React** or **Angular** (team preference) |
| Existing jQuery site | Maintain with **jQuery**; migrate incrementally |
| Forms, dashboards, mostly server HTML | **[HTMX](../htmx/i-overview.md)** + templates, or **Bootstrap** plugins |
| Small widget on one page | **Vanilla JS**, **Bootstrap** `data-bs-*`, or Alpine.js |

## Shared concepts (all tracks)

| Concept | Meaning |
|---------|---------|
| **DOM** | Browser tree of elements JS can read and change |
| **Event loop** | Async callbacks, promises, `async/await` |
| **npm** | Package registry; `package.json` declares dependencies |
| **CORS** | Browser rules for calling APIs on other origins |
| **Bundling** | Combine modules for production (Vite, Angular CLI, etc.) |

## Next

- [jQuery overview](jquery/i-overview.md) — `$()`, events, `.ajax()`
- [React overview](react/i-overview.md) — components, JSX, hooks
- [Angular overview](angular/i-overview.md) — modules, services, TypeScript
- [Bootstrap overview](bootstrap/i-overview.md) — modals, collapse, `data-bs-*` plugins
