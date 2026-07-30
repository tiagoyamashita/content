---
label: "IV"
subtitle: "フォームとリクエスト"
group: "HTMX"
order: 4
---
HTMX — フォームとリクエスト

Forms are the most common HTMX entry point: submit without full page reload, show validation errors inline, and keep field values on failure.

## 1. Basic form POST

```html
<form hx-post="/items" hx-target="#item-list" hx-swap="afterbegin">
  <input name="title" required>
  <button type="submit">Add</button>
</form>
<ul id="item-list"></ul>
```

## 2. Validation errors (422)

Return **422 Unprocessable Entity** with the form partial including error messages. HTMX swaps the entire form — user edits and resubmits.

## 3. CSRF tokens

Include the token in the form; HTMX sends it with **`application/x-www-form-urlencoded`** or **`multipart/form-data`**.

**Spring Security** — configure **`htmx:configRequest`** to attach CSRF header from meta tags.

## 4. File uploads

Use **`enctype="multipart/form-data"`** and **`hx-encoding="multipart/form-data"`**.

## Next

Continue with [Server responses & templates](v-server-responses-and-templates.md) for partial rendering and response headers.
