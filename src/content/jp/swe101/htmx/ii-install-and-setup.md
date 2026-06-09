---
label: "II"
subtitle: "インストールとセットアップ"
group: "HTMX"
order: 2
---
HTMX — インストールとセットアップ

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

## 2. Verify it works

Minimal server route returns a fragment:

```python
# Flask example
@app.get("/hello")
def hello():
    return "<p>Hello from the server</p>"
```

Click the button — `#out` should fill without a full reload. Open DevTools **Network**: request is `GET /hello`, response is HTML, not JSON.

## Next

Continue with [Core attributes & swapping](iii-core-attributes-and-swapping.md) for targets, swap modes, and triggers.
