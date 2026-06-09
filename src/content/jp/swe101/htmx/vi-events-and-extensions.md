---
label: "VI"
subtitle: "イベントと拡張"
group: "HTMX"
order: 6
---
HTMX — イベントと拡張

HTMX exposes a **rich event system** for lifecycle hooks. **Extensions** add JSON encoding, SSE, WebSockets, and more — load only what you need.

## 1. Event lifecycle

```text
htmx:validate → htmx:beforeRequest → htmx:send → htmx:xhr:loadstart
  → htmx:beforeSwap → htmx:afterSwap → htmx:load
```

Listen globally with **`document.body.addEventListener('htmx:afterSwap', …)`** or declaratively with **`hx-on::after-swap`**.

## 2. Extensions

| Extension | Purpose |
|-----------|---------|
| **`json-enc`** | POST JSON bodies |
| **`sse`** | Server-Sent Events → DOM updates |
| **`ws`** | WebSocket messages → swaps |
| **`head-support`** | Merge `<title>` / `<head>` from responses |

## 3. Third-party JS after swap

Libraries that scan DOM on load need re-init on **`htmx:afterSwap`** — scope to **`e.detail.target`**.

## Next

Continue with [Patterns & app integration](vii-patterns-and-app-integration.md) for pagination, modals, and backend examples.
