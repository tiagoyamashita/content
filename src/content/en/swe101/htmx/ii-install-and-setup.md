---
label: "II"
subtitle: "Install & setup"
group: "HTMX"
order: 2
---
HTMX — install & setup
HTMX ships as a **single JavaScript file**. Include it once per page (or in a layout template). No npm build is required for learning or many production apps — though bundling is fine if your stack already uses one.

## 1. CDN (fastest start)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>HTMX demo</title>
  <script src="https://unpkg.com/htmx.org@2.0.4" defer></script>
</head>
<body>
  <button hx-get="/hello" hx-target="#out">Say hello</button>
  <div id="out"></div>
</body>
</html>
```

| Source | Notes |
|--------|-------|
| **unpkg.com/htmx.org** | Common for demos; pin a version (`@2.0.4`) |
| **Self-hosted** | Copy `htmx.min.js` to your static folder — preferred for production control |
| **npm** | `npm install htmx.org` — import in Vite/webpack if you already bundle |

**`defer`** loads HTMX without blocking HTML parse; attributes work on elements present at load time.

## 2. Verify it works

Minimal server route returns a fragment:

```python
# Flask example
@app.get("/hello")
def hello():
    return "<p>Hello from the server</p>"
```

Click the button — `#out` should fill without a full reload. Open DevTools **Network**: request is `GET /hello`, response is HTML, not JSON.

## 3. Content Security Policy (CSP)

If your app sets CSP headers, allow HTMX inline handlers only if you use them (`hx-on:*`). Typical setup:

```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://unpkg.com; connect-src 'self'
```

| CSP directive | HTMX need |
|---------------|-----------|
| **`script-src`** | Host serving `htmx.org` or `'self'` |
| **`connect-src`** | Origins HTMX fetches (your API, SSE, WebSocket) |
| **`unsafe-inline`** | Avoid if possible; prefer external scripts + `hx-on` sparingly |

Self-hosting HTMX removes third-party `script-src` entries.

## 4. Local dev layout

```text
project/
  static/
    htmx.min.js
  templates/
    layout.html      # includes script
    pages/
      index.html
    partials/
      _item_row.html # fragments for hx-* responses
  app.py / Application.java
```

Keep **partials** in a dedicated folder — same templates your full-page views use, minus layout wrapper.

## 5. HTMX 1.x vs 2.x

| | **1.x** | **2.x** |
|---|---------|---------|
| **Browser support** | Includes IE11 workarounds | Modern browsers only |
| **API** | Stable attribute names | Same core attributes; cleaner internals |
| **Migration** | Change script URL; test extensions | See [htmx.org migration notes](https://htmx.org/docs/#migration) |

New projects should start on **2.x** unless you must support legacy browsers.

## 6. Debugging

```html
<!-- Log all HTMX events to console (dev only) -->
<body hx-ext="debug" _="on htmx:load log event">
```

Or in browser console:

```javascript
htmx.logAll();  // verbose request/swap logging
```

| Symptom | Check |
|---------|-------|
| Nothing happens | Script loaded? Typo in `hx-target` selector? |
| Full page returned | Server returned layout wrapper — return partial only |
| 403 on POST | CSRF token missing — see [Forms & requests](iv-forms-and-requests.md) |
| Swap in wrong place | `hx-target` / `hx-swap` on triggering element vs ancestor |

## Next

Continue with [Core attributes & swapping](iii-core-attributes-and-swapping.md) for targets, swap modes, and triggers.
