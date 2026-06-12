---
label: "I"
subtitle: "Overview"
group: "CSS"
order: 1
---
CSS — overview
**CSS** styles HTML — layout, typography, color, and responsive behavior. In SWE101 this track covers **preprocessors** (Sass, Less) that extend plain CSS and **Bootstrap**, a widely used component and utility framework. For client behavior on top of styled pages, see [JavaScript](../javascript/i-overview.md) or server-driven [HTMX](../htmx/i-overview.md).

## Map of this track

| Submenu | Focus |
|---------|--------|
| **Sass** | Variables, nesting, mixins, partials — compile to CSS |
| **Less** | Similar preprocessor model, Less-specific syntax and tooling |
| **Bootstrap** | Grid, utilities, components; CSS-first with optional JS |

## Where CSS fits in the stack

```text
Browser  →  HTML (structure)  →  CSS (presentation)  →  JavaScript (behavior)
Build    →  Sass/Less compile to CSS; Bootstrap via CDN or bundled import
```

| Layer | Role |
|-------|------|
| **Plain CSS** | Selectors, cascade, flexbox, grid, media queries |
| **Preprocessor** | Sass or Less source → `.css` at build time |
| **Framework** | Bootstrap (or similar) — ready-made layout and components |
| **Build tool** | Vite, webpack, `sass` CLI, PostCSS — compile and bundle |

## Picking an approach

| Situation | Reasonable default |
|-----------|-------------------|
| Small site, few styles | **Plain CSS** or a single stylesheet |
| Large app, shared tokens and mixins | **Sass** (most common in modern stacks) |
| Legacy Less codebase | Maintain with **Less**; migrate only if justified |
| Admin UI, prototypes, Bootstrap docs | **Bootstrap** CSS (+ JS only if you need modals, dropdowns) |
| Component library in React/Angular | Framework CSS modules or Tailwind — Bootstrap optional |

## Shared concepts (all three)

| Concept | Meaning |
|---------|---------|
| **Cascade** | Later or more specific rules win; `!important` overrides |
| **Specificity** | ID > class > element — avoid fighting the cascade |
| **Box model** | content → padding → border → margin |
| **Flexbox / Grid** | One-dimensional vs two-dimensional layout |
| **Custom properties** | CSS variables (`--color-primary`) — native alternative to preprocessor vars |
| **Media queries** | Responsive breakpoints (`@media (min-width: 768px)`) |

## Next

- [Sass overview](sass/i-overview.md) — `$variables`, nesting, `@mixin`
- [Less overview](less/i-overview.md) — `@variables`, mixins, imports
- [Bootstrap overview](bootstrap/i-overview.md) — grid, utilities, components
