---
label: "III"
subtitle: "コア属性とスワップ"
group: "HTMX"
order: 3
---
HTMX — コア属性とスワップ

HTMX behavior is declared with **`hx-*` attributes**. The triggering element (button, link, form, div) specifies **what** to request, **where** to put the response, and **how** to insert it.

## 1. Request attributes

| Attribute | Effect |
|-----------|--------|
| **`hx-get="/path"`** | `GET` on click (default trigger) |
| **`hx-post="/path"`** | `POST` |
| **`hx-put` / `hx-patch` / `hx-delete`** | REST verbs |
| **`hx-push-url="true"`** | Update browser URL bar after swap |
| **`hx-select="#fragment"`** | Extract matching node from response before swap |

## 2. Target & swap

| Attribute | Default | Meaning |
|-----------|---------|---------|
| **`hx-target`** | triggering element | CSS selector for swap destination |
| **`hx-swap`** | `innerHTML` | Insertion strategy |

Common **`hx-swap`** values: **`innerHTML`**, **`outerHTML`**, **`beforebegin`**, **`afterbegin`**, **`beforeend`**, **`afterend`**, **`delete`**, **`none`**.

## 3. Triggers

Default: **`click`** for most elements, **`submit`** for forms.

```html
<input name="q" hx-get="/search" hx-trigger="keyup changed delay:300ms"
       hx-target="#results" placeholder="Search…">
<div id="results"></div>
```

## 4. Boost — progressive enhancement

**`hx-boost="true"`** on `<body>` or a container upgrades **normal links and forms** to AJAX.

## Next

Continue with [Forms & requests](iv-forms-and-requests.md) for POST bodies, CSRF, and file uploads.
