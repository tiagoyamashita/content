---
label: "I"
subtitle: "Overview"
group: "Bootstrap"
order: 1
---
Bootstrap — overview
**Bootstrap** is a **CSS-first UI framework** — responsive grid, utility classes, and styled components (buttons, navbars, forms, cards). Optional **JavaScript** powers interactive pieces (modals, dropdowns, collapse). Widely used for **admin panels**, **prototypes**, and **documentation sites**.

Parent track: [CSS overview](../i-overview.md). Pair with [JavaScript](../javascript/i-overview.md) when you add Bootstrap’s JS plugins or build a SPA on top.

## CSS vs JS in Bootstrap

| Part | Delivers | Required? |
|------|----------|-------------|
| **CSS** | Grid, typography, spacing utilities, static components | Yes — core value |
| **JS** | Modals, dropdowns, tooltips, carousel, offcanvas | Only for interactive widgets |
| **Bundle** | `bootstrap.bundle.min.js` includes **Popper** for positioning | Use when loading Bootstrap JS |

You can link **CSS only** and get a fully styled layout without any Bootstrap JavaScript.

## Quick start (CDN)

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<!-- Optional — only if you use modals, dropdowns, etc. -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
```

## Core CSS pieces

| Piece | Role |
|-------|------|
| **Grid** | `.container`, `.row`, `.col-*` — 12-column responsive layout |
| **Utilities** | `m-*`, `p-*`, `d-flex`, `text-center` — spacing and display |
| **Components** | `.btn`, `.navbar`, `.card`, `.form-control` — pre-styled UI |
| **Reboot** | Normalized base styles on top of browser defaults |
| **Breakpoints** | `sm`, `md`, `lg`, `xl`, `xxl` — mobile-first media queries |

## Mental model

```text
HTML markup + Bootstrap classes  →  styled page (no custom CSS required)
Optional data-bs-* attributes + bootstrap.js  →  toggles, modals, dropdowns
Customize  →  Sass variables (_variables.scss) or override CSS custom properties
```

## When Bootstrap makes sense

| Good fit | Poor default |
|----------|--------------|
| Internal admin, CRUD dashboards | Highly custom brand-heavy marketing site |
| Fast prototype or hackathon UI | Design system already built in React + Tailwind |
| Team knows Bootstrap docs by heart | Every pixel must be bespoke |

## Minimal grid example

```html
<div class="container py-4">
  <div class="row g-3">
    <div class="col-md-8">Main</div>
    <div class="col-md-4">Sidebar</div>
  </div>
</div>
```

## vs preprocessors / other CSS

| | **Bootstrap** | **Sass/Less alone** | **Utility-first (e.g. Tailwind)** |
|---|---------------|---------------------|-----------------------------------|
| **Delivers** | Ready components + grid | Language extensions | Atomic utility classes |
| **Learning curve** | Class names from docs | Syntax + architecture | Config + class vocabulary |
| **Customization** | Sass maps, CSS variables | Full control | `tailwind.config` |

## Next steps (future notes)

npm install, Sass customization, forms and validation styles, and when to add JS components vs plain CSS.
