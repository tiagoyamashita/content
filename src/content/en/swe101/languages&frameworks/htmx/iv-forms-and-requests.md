---
label: "IV"
subtitle: "Forms & requests"
group: "HTMX"
order: 4
---
HTMX — forms & requests
Forms are the most common HTMX entry point: submit without full page reload, show validation errors inline, and keep field values on failure.

## 1. Basic form POST

```html
<form hx-post="/items" hx-target="#item-list" hx-swap="afterbegin">
  <input name="title" required>
  <button type="submit">Add</button>
</form>
<ul id="item-list"></ul>
```

Server returns a new `<li>…</li>` (or error partial). **`type="submit"`** triggers **`submit`** event — HTMX intercepts before navigation.

## 2. Validation errors (422)

Return **422 Unprocessable Entity** with the form partial including error messages:

```html
<!-- Server re-renders on failure -->
<form hx-post="/items" hx-target="this" hx-swap="outerHTML">
  <input name="title" value="ab" aria-invalid="true">
  <p class="error">Title must be at least 3 characters</p>
  <button type="submit">Add</button>
</form>
```

HTMX swaps the entire form — user edits and resubmits. Same pattern as classic server-side validation, without JSON error DTOs.

## 3. CSRF tokens

Frameworks require CSRF on POST. Include the token in the form; HTMX sends it with **`application/x-www-form-urlencoded`** or **`multipart/form-data`**.

**Django / Flask-WTF:**

```html
<form hx-post="/items" hx-target="#list">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  …
</form>
```

**Spring Security** — hidden `_csrf` field in form; or configure **`hx-headers`** globally:

```html
<meta name="_csrf" content="${_csrf.token}">
<meta name="_csrf_header" content="${_csrf.headerName}">
<script>
  document.body.addEventListener('htmx:configRequest', (e) => {
    e.detail.headers[document.querySelector('meta[name=_csrf_header]').content]
      = document.querySelector('meta[name=_csrf]').content;
  });
</script>
```

## 4. JSON APIs (when needed)

HTMX defaults to form encoding. For JSON endpoints:

```html
<button hx-post="/api/items"
        hx-ext="json-enc"
        hx-vals='{"title": "Widget", "qty": 2}'>
  Create via JSON
</button>
```

Prefer **HTML-first routes** (`/items` returning fragments) when building HTMX apps — one template path, not parallel JSON + React.

## 5. PUT / PATCH / DELETE from forms

HTML forms only support GET/POST. Use **`hx-delete`**, **`hx-put`**, or POST with method override:

```html
<button hx-delete="/items/42" hx-target="#row-42" hx-swap="delete">
  Delete
</button>
```

Or hidden `_method` field if your backend expects POST + override (Rails, some Java filters).

## 6. File uploads

Use **`enctype="multipart/form-data"`** — HTMX supports **`FormData`**:

```html
<form hx-post="/upload" hx-encoding="multipart/form-data" hx-target="#status">
  <input type="file" name="document">
  <button type="submit">Upload</button>
</form>
<div id="status"></div>
```

Large files: consider progress via **`htmx:xhr:progress`** event or a dedicated upload endpoint with chunked API.

## 7. Prevent double submit

```html
<form hx-post="/pay" hx-disabled-elt="find button">
  …
</form>
```

Or server-side idempotency keys for payments — HTMX does not replace transactional safety.

## 8. GET forms (search)

```html
<form hx-get="/search" hx-target="#results" hx-push-url="true">
  <input name="q" autofocus>
  <button type="submit">Search</button>
</form>
```

Query string syncs to URL — shareable bookmarks, back button works with **`hx-push-url`**.

## Next

Continue with [Server responses & templates](v-server-responses-and-templates.md) for partial rendering and response headers.
