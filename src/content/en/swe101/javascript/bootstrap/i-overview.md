---
label: "I"
subtitle: "Overview"
group: "Bootstrap"
order: 1
---
Bootstrap JS — overview
**Bootstrap** ships CSS for layout and components plus **JavaScript plugins** for interactive UI — modals, dropdowns, collapse, tabs, toasts, and more. **Bootstrap 5+** plugins are **vanilla JS** (no jQuery required). Pair with server-rendered pages, [HTMX](../../htmx/i-overview.md), or static sites.

Parent track: [JavaScript overview](../i-overview.md).

## What Bootstrap JS provides

| Plugin | Typical use |
|--------|-------------|
| **Modal** | Dialogs, confirmations, forms |
| **Dropdown** | Menus, split buttons |
| **Collapse** | Accordions, expandable panels |
| **Tab** | Tabbed content without routing |
| **Toast** | Lightweight notifications |
| **Tooltip / Popover** | Hints on hover or click |
| **Offcanvas** | Slide-in sidebar (mobile nav) |
| **Carousel** | Image/content sliders |

## Include scripts

**CDN (quick start):**

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" defer></script>
```

**`bootstrap.bundle.min.js`** includes **Popper** (needed for dropdowns, tooltips, popovers).

**npm:**

```text
npm install bootstrap @popperjs/core
```

```javascript
import 'bootstrap/dist/css/bootstrap.min.css';
import { Modal, Collapse } from 'bootstrap';
```

## Declarative: `data-bs-*` attributes

Most behavior works **without writing JS** — markup drives the plugin:

```html
<!-- Button opens modal by id -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#saveModal">
  Save
</button>

<div class="modal fade" id="saveModal" tabindex="-1" aria-labelledby="saveLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="saveLabel">Confirm</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">Save changes?</div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>
```

| Attribute | Role |
|-----------|------|
| **`data-bs-toggle`** | Plugin name (`modal`, `collapse`, `dropdown`, …) |
| **`data-bs-target`** | CSS selector of element to control |
| **`data-bs-dismiss`** | Close modal, alert, offcanvas |

## Programmatic API

When you need to open/close from code (e.g. after an HTMX swap):

```javascript
const el = document.getElementById('saveModal');
const modal = bootstrap.Modal.getOrCreateInstance(el);
modal.show();

// Listen for events
el.addEventListener('hidden.bs.modal', () => { /* cleanup */ });
```

**Re-init after dynamic HTML:** Bootstrap attaches listeners at load. Content injected later (HTMX, fetch) may need **`new bootstrap.Tooltip(el)`** or **`Modal.getOrCreateInstance`** on new nodes.

```javascript
document.body.addEventListener('htmx:afterSwap', (e) => {
  e.detail.target.querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(node => new bootstrap.Tooltip(node));
});
```

## Collapse + accordion

```html
<button class="btn btn-outline-secondary" data-bs-toggle="collapse" data-bs-target="#panel1">
  Toggle panel
</button>
<div class="collapse" id="panel1">
  <div class="card card-body">Hidden until expanded.</div>
</div>
```

Wrap multiple **`collapse`** items in **`.accordion`** for one-open-at-a-time behavior.

## When Bootstrap JS fits

| Good fit | Poor default |
|----------|--------------|
| Admin UI, marketing site, internal tools | Highly custom design system (build components) |
| Fast prototype with accessible defaults | Full SPA — use React/Angular component libs |
| Server HTML + sprinkles of interactivity | Complex client state across many screens |
| Works with [HTMX](../../htmx/i-overview.md) partials | Replacing a design-heavy product UI |

## vs jQuery / React / Angular

| | **Bootstrap JS** | **jQuery** | **React / Angular** |
|---|------------------|------------|---------------------|
| **Scope** | UI plugins + CSS system | General DOM/AJAX | Full app UI |
| **Markup** | `data-bs-*` first | `$('.x').modal()` (BS4 era) | Components |
| **Bundle** | One JS file or tree-shake imports | jQuery + optional BS | App bundle |

## Accessibility notes

- Modals manage **focus trap** and **`aria-*`** when markup is correct.
- Always include **`aria-label`** on close buttons and **`tabindex="-1"`** on modal root.
- Prefer **`data-bs-*`** defaults before custom JS — plugins handle keyboard (Esc to close modal).

## Next steps (future notes)

Forms validation styles, navbar toggler, customizing with Sass, and tree-shaking only the plugins you import.
