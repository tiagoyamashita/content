---
label: "V"
subtitle: "サーバー応答とテンプレート"
group: "HTMX"
order: 5
---
HTMX — サーバー応答とテンプレート

The server’s job in an HTMX app is to return **the right HTML for the requesting context** — often a **partial** without layout chrome. Use response **headers** to trigger client-side actions (redirect, refresh regions, toasts).

## 1. Detect HTMX requests

HTMX sets **`HX-Request: true`**. Branch in your controller to return partial vs full page.

## 2. Template partials

Reuse the same partial in full-page table and HTMX swap responses — **one source of truth** for markup (Thymeleaf fragments, Jinja2 includes).

## 3. Response headers

| Header | Effect |
|--------|--------|
| **`HX-Redirect: /path`** | Client navigates (full page) |
| **`HX-Location: /path`** | Client `pushState` + GET (SPA-like) |
| **`HX-Refresh: true`** | Full page reload |
| **`HX-Trigger: eventName`** | Dispatch event after swap |

## 4. Security

Escape in templates; CSRF on mutating requests; validate **`HX-Redirect`** targets server-side.

## Next

Continue with [Events & extensions](vi-events-and-extensions.md) for client hooks, SSE, and WebSockets.
