---
label: "V"
subtitle: "Server responses & templates"
group: "HTMX"
order: 5
---
HTMX — server responses & templates
The server’s job in an HTMX app is to return **the right HTML for the requesting context** — often a **partial** without layout chrome. Use response **headers** to trigger client-side actions (redirect, refresh regions, toasts).

## 1. Detect HTMX requests

HTMX sets **`HX-Request: true`**. Branch in your controller:

```java
@GetMapping("/items/{id}")
public String item(@PathVariable long id, Model model,
                   @RequestHeader(value = "HX-Request", defaultValue = "false") boolean htmx) {
  model.addAttribute("item", repo.findById(id));
  return htmx ? "partials/item-row :: row" : "items/detail";
}
```

```python
# Flask
from flask import request, render_template

@app.get("/items/<id>")
def item(id):
    tpl = "partials/item_row.html" if request.headers.get("HX-Request") else "item_detail.html"
    return render_template(tpl, item=Item.get(id))
```

| Request type | Return |
|--------------|--------|
| Normal navigation | Full page with layout |
| **`HX-Request`** | Fragment only |
| **`HX-Boosted`** | Fragment for boosted link/form |

## 2. Template partials

**Thymeleaf** fragment:

```html
<!-- partials/item-row.html -->
<tr th:fragment="row" th:id="${'row-' + item.id}">
  <td th:text="${item.title}"></td>
  <td><button hx-get="@{/items/{id}/edit(id=${item.id})}" hx-target="closest tr" hx-swap="outerHTML">Edit</button></td>
</tr>
```

**Jinja2**:

```html
{# partials/item_row.html #}
<tr id="row-{{ item.id }}">
  <td>{{ item.title }}</td>
</tr>
```

Reuse the same partial in full-page table and HTMX swap responses — **one source of truth** for markup.

## 3. Response headers

| Header | Effect |
|--------|--------|
| **`HX-Redirect: /path`** | Client navigates (full page) |
| **`HX-Location: /path`** | Client `pushState` + GET (SPA-like) |
| **`HX-Refresh: true`** | Full page reload |
| **`HX-Retarget: #selector`** | Override request’s target |
| **`HX-Reswap: outerHTML`** | Override swap mode |
| **`HX-Trigger: eventName`** | Dispatch event after swap |
| **`HX-Trigger-After-Swap: …`** | Fire after DOM updated |

```java
return ResponseEntity.ok()
    .header("HX-Trigger", "itemSaved")
    .body(fragmentHtml);
```

Use **`HX-Redirect`** after create → list when the whole view should reset.

## 4. Status codes

| Code | Typical use |
|------|-------------|
| **200** | Success — swap body |
| **204** | Success — no body (`hx-swap="none"`) |
| **422** | Validation failure — re-render form partial |
| **404** | Not found — error partial |
| **500** | Server error — `htmx:responseError` on client |

HTMX treats **4xx/5xx** as errors unless **`htmx:beforeSwap`** allows swap — you can still return HTML error partials on 422 by configuring swap for that code.

```javascript
document.body.addEventListener('htmx:beforeSwap', (e) => {
  if (e.detail.xhr.status === 422) {
    e.detail.shouldSwap = true;
    e.detail.isError = false;
  }
});
```

## 5. Empty vs delete responses

After DELETE, return **empty 200** with **`hx-swap="delete"`** on the button, or return replacement HTML.

```html
<button hx-delete="/items/42" hx-target="closest tr" hx-swap="outerHTML swap:1s">
  Delete
</button>
```

Server can return empty body; swap **`delete`** removes the row.

## 6. Caching

Dynamic HTMX fragments should **not** be cached at CDN with long TTL. Set:

```http
Cache-Control: no-store
```

Static **`htmx.min.js`** belongs on [CDN](../cdn/v-static-assets-and-spas.md) with hashed long TTL.

## 7. Security

| Risk | Mitigation |
|------|------------|
| **XSS in swapped HTML** | Escape in templates; never reflect raw user HTML |
| **CSRF** | Tokens on mutating requests — see [Forms & requests](iv-forms-and-requests.md) |
| **Open redirects** | Validate **`HX-Redirect`** targets server-side |
| **Auth** | Same session/cookie auth as MPA; return 401 partial or redirect |

HTMX requests carry **cookies** — same-origin policy applies. For API-only JWT in `localStorage`, HTMX is a poor fit unless you wire **`htmx:configRequest`**.

## Next

Continue with [Events & extensions](vi-events-and-extensions.md) for client hooks, SSE, and WebSockets.
