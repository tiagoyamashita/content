---
label: "VI"
subtitle: "Events & extensions"
group: "HTMX"
order: 6
---
HTMX — events & extensions
HTMX exposes a **rich event system** for lifecycle hooks. **Extensions** add JSON encoding, SSE, WebSockets, and more — load only what you need.

## 1. Event lifecycle

```text
htmx:validate → htmx:beforeRequest → htmx:send → htmx:xhr:loadstart
  → htmx:beforeSwap → htmx:afterSwap → htmx:load
```

| Event | Use |
|-------|-----|
| **`htmx:beforeRequest`** | Cancel or modify URL/headers |
| **`htmx:afterSwap`** | Focus first input, init widgets |
| **`htmx:responseError`** | Toast on 500 |
| **`htmx:historyRestore`** | Back button restored cached content |
| **`htmx:oobAfterSwap`** | After out-of-band updates |

Listen globally:

```javascript
document.body.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target.id === 'modal') {
    e.detail.target.querySelector('[autofocus]')?.focus();
  }
});
```

Or declaratively with **`hx-on::after-swap`** (HTMX 2):

```html
<div hx-get="/panel" hx-target="this"
     hx-on::after-swap="this.querySelector('input')?.focus()"></div>
```

## 2. Custom triggers from server

Server header **`HX-Trigger`** fires a client event after swap:

```http
HX-Trigger: {"itemDeleted": {"id": 42}, "showToast": "Item removed"}
```

```javascript
document.body.addEventListener('itemDeleted', (e) => {
  console.log('deleted', e.detail.id);
});
```

Combine with **`HX-Trigger-After-Settle`** when CSS transitions must finish first.

## 3. `htmx:configRequest`

Central place for auth headers, tracing, or query params:

```javascript
document.body.addEventListener('htmx:configRequest', (e) => {
  e.detail.headers['X-Request-Id'] = crypto.randomUUID();
});
```

## 4. Extensions

Load after core HTMX:

```html
<script src="/htmx.min.js"></script>
<script src="/ext/json-enc.js"></script>
<script src="/ext/sse.js"></script>
```

| Extension | Purpose |
|-----------|---------|
| **`json-enc`** | POST JSON bodies |
| **`sse`** | Server-Sent Events → DOM updates |
| **`ws`** | WebSocket messages → swaps |
| **`head-support`** | Merge `<title>` / `<head>` from responses |
| **`preload`** | Prefetch on hover |

**SSE example:**

```html
<div hx-ext="sse" sse-connect="/events" sse-swap="message">
  Waiting for updates…
</div>
```

Server streams named events; each message can carry HTML to swap.

## 5. WebSockets (when SSE is not enough)

**`ws` extension** maps messages to targets. Prefer **SSE** for server→client fanout (simpler, HTTP-friendly). Use WebSockets for bidirectional low-latency (chat, games) — often paired with a dedicated client layer rather than pure HTMX.

## 6. History and back button

**`hx-push-url="true"`** + **`hx-history="false"`** on sensitive widgets control browser history.

**`htmx:historyRestore`** fires when user navigates back — re-fetch stale regions if needed:

```javascript
document.body.addEventListener('htmx:historyRestore', (e) => {
  htmx.trigger('#notifications', 'refresh');
});
```

## 7. Animations

Use **`hx-swap="innerHTML swap:300ms settle:300ms"`** for fade transitions, or CSS on **`htmx-swapping`** / **`htmx-settling`** classes HTMX adds during swap.

```css
.htmx-swapping { opacity: 0; transition: opacity 300ms; }
.htmx-settling { opacity: 1; }
```

## 8. Third-party JS after swap

Libraries that scan DOM on load (tooltips, date pickers) need re-init **`htmx:afterSwap`**:

```javascript
document.body.addEventListener('htmx:afterSwap', () => {
  initDatePickers(document.body);
});
```

Scope init to **`e.detail.target`** to avoid re-processing the whole page.

## Next

Continue with [Patterns & app integration](vii-patterns-and-app-integration.md) for pagination, modals, and backend examples.
