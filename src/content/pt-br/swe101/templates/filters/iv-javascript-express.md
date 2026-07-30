---
label: "IV"
subtitle: "JavaScript — Express"
group: "Filters"
order: 4
---
Filter template — JavaScript (Express)
**Edge middleware** — rate-limit stub and helmet-like security headers. Request ID / logging: [Middleware](../middleware/iv-javascript-express.md).

## Template

```javascript
const express = require("express");

const WINDOW_MS = 60_000;
const MAX_REQUESTS = 60;
const hits = new Map();

function rateLimit(req, res, next) {
  const key = req.ip;
  const now = Date.now();
  const window = hits.get(key) ?? [];
  const recent = window.filter((t) => now - t < WINDOW_MS);

  if (recent.length >= MAX_REQUESTS) {
    res.setHeader("Retry-After", "60");
    return res.status(429).json({ error: "rate limit exceeded" });
  }

  recent.push(now);
  hits.set(key, recent);
  next();
}

function securityHeaders(req, res, next) {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
  next();
}

function requireJson(req, res, next) {
  if (!["POST", "PUT", "PATCH"].includes(req.method)) {
    return next();
  }

  const contentType = req.get("Content-Type") || "";
  if (!contentType.startsWith("application/json")) {
    return res.status(415).json({ error: "application/json required" });
  }

  const length = Number(req.get("Content-Length") || 0);
  if (length > 1_048_576) {
    return res.status(413).json({ error: "payload too large" });
  }

  next();
}

const app = express();
app.set("trust proxy", 1); // correct client IP behind reverse proxy

// Order: requestContext (middleware template) → edge policy → body parser → routes
// app.use(requestContext);
app.use(securityHeaders);
app.use(rateLimit);
app.use(express.json({ limit: "1mb" }));
app.use(requireJson);

// ... routes ...
```

Production: prefer **`express-rate-limit`** + **`helmet`** — these stubs show what they do.

## Notes

| Topic | Practice |
|-------|----------|
| **Registration order** | Security headers early; `express.json` after size/content checks or rely on its `limit` |
| **429 vs next(err)** | Short-circuit with `res.status(429).json(...)` — don't call `next()` |
| **trust proxy** | Required for accurate IP-based limits behind nginx / load balancers |
| **Helmet** | Sets the same headers plus CSP — use in real apps |
| **Separate concerns** | Keep [Middleware](../middleware/iv-javascript-express.md) for request ID only |

## Next

[Go — net/http](v-go-nethttp.md) · [Filters overview](i-overview.md).
