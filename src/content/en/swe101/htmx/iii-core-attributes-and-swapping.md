---
label: "III"
subtitle: "Core attributes & swapping"
group: "HTMX"
order: 3
---
HTMX — core attributes & swapping
HTMX behavior is declared with **`hx-*` attributes**. The triggering element (button, link, form, div) specifies **what** to request, **where** to put the response, and **how** to insert it.

## 1. Request attributes

| Attribute | Effect |
|-----------|--------|
| **`hx-get="/path"`** | `GET` on click (default trigger) |
| **`hx-post="/path"`** | `POST` |
| **`hx-put` / `hx-patch` / `hx-delete`** | REST verbs |
| **`hx-push-url="true"`** | Update browser URL bar after swap |
| **`hx-select="#fragment"`** | Extract matching node from response before swap |

```html
<a hx-get="/items/42" hx-target="#detail" hx-push-url="true">
  View item 42
</a>
<div id="detail"></div>
```

## 2. Target & swap

| Attribute | Default | Meaning |
|-----------|---------|---------|
| **`hx-target`** | triggering element | CSS selector for swap destination |
| **`hx-swap`** | `innerHTML` | Insertion strategy |

Common **`hx-swap`** values:

| Value | Behavior |
|-------|----------|
| **`innerHTML`** | Replace children of target |
| **`outerHTML`** | Replace target element itself |
| **`beforebegin` / `afterbegin` / `beforeend` / `afterend`** | Adjacent insertion |
| **`delete`** | Remove target (ignore response body) |
| **`none`** | Fire events only — no DOM change |

```html
<button hx-get="/more" hx-target="#list" hx-swap="beforeend">
  Load more
</button>
<ul id="list">
  <li>Existing row</li>
</ul>
```

Response `<li>New row</li>` appends inside `#list`.

## 3. Triggers

Default: **`click`** for most elements, **`submit`** for forms.

```html
<input name="q" hx-get="/search" hx-trigger="keyup changed delay:300ms"
       hx-target="#results" placeholder="Search…">
<div id="results"></div>
```

| Trigger fragment | Use |
|------------------|-----|
| **`changed`** | Only when value differs from last request |
| **`delay:300ms`** | Debounce typing |
| **`every 2s`** | Polling |
| **`revealed`** | Infinite scroll when element enters viewport |
| **`load`** | Fire once when element loads |

Combine with commas: **`click, keyup[key=='Enter']`**.

## 4. Including values

| Attribute | Sends |
|-----------|-------|
| **`hx-include`** | Extra form fields or selectors |
| **`hx-vals`** | JSON or `js:` expressions |
| **`name` on inputs** | Included automatically from closest form |

```html
<form id="filters">
  <select name="status">…</select>
</form>
<button hx-get="/report" hx-include="#filters" hx-target="#report">
  Run report
</button>
```

## 5. Boost — progressive enhancement

**`hx-boost="true"`** on `<body>` or a container upgrades **normal links and forms** to AJAX:

```html
<body hx-boost="true">
  <nav>
    <a href="/dashboard">Dashboard</a>  <!-- partial navigation -->
  </nav>
  <main id="content">…</main>
</body>
```

Server should return **fragments for boosted requests** (detect via `HX-Request` header) or full pages for non-JS clients.

## 6. Loading & disabled states

```html
<button hx-get="/slow" hx-target="#out"
        hx-indicator="#spinner">
  Load
</button>
<img id="spinner" class="htmx-indicator" src="/spinner.svg" alt="">
```

**`htmx-indicator`** elements are shown while a request is in flight. Add **`hx-disabled-elt="this"`** to prevent double submits.

## 7. Swap lifecycle (events preview)

HTMX fires events such as **`htmx:beforeRequest`**, **`htmx:afterSwap`**, **`htmx:responseError`**. Use them for analytics, focus management, or to abort requests — details in [Events & extensions](vi-events-and-extensions.md).

```html
<div hx-get="/panel" hx-target="this" hx-swap="innerHTML"
     hx-on::after-swap="this.querySelector('input')?.focus()">
  …
</div>
```

## 8. Out-of-band swaps

One response can update **multiple** targets:

```html
<!-- Server response -->
<div id="cart-count" hx-swap-oob="innerHTML">3 items</div>
<tr id="row-42">…updated row…</tr>
```

Main swap goes to the request target; **`hx-swap-oob`** nodes update elsewhere. Useful for updating a header badge while editing a table row.

## Next

Continue with [Forms & requests](iv-forms-and-requests.md) for POST bodies, CSRF, and file uploads.
