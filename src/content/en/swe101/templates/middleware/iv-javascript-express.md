---
label: "IV"
subtitle: "JavaScript — Express"
group: "Middleware"
order: 4
---
Middleware template — JavaScript (Express)
**Request ID + logging middleware** and **`next(err)` passthrough** so errors reach the error handler.

## Template

```javascript
const express = require("express");
const { randomUUID } = require("crypto");

const app = express();
app.use(express.json());

function requestContext(req, res, next) {
  req.requestId = req.get("X-Request-Id") || randomUUID();
  res.setHeader("X-Request-Id", req.requestId);

  // Auth stub
  req.userId = req.get("X-User-Id") || null;

  const start = Date.now();
  res.on("finish", () => {
    const ms = Date.now() - start;
    console.log(`${req.requestId} ${req.method} ${req.originalUrl} ${res.statusCode} ${ms}ms`);
  });
  next();
}

function errorPassthrough(err, req, res, next) {
  // Attach request id for downstream error middleware
  err.requestId = req.requestId;
  next(err);
}

app.use(requestContext);

// ... routes ...

// After routes — forward unknown errors:
app.use(errorPassthrough);

// Error handler (see Errors template) registered last
```

Route handlers use `req.requestId` in logs; thrown/`next(err)` errors carry `requestId`.

## Notes

| Topic | Practice |
|-------|----------|
| **Registration order** | `requestContext` before routers; error handler after routes |
| **`res.on("finish")`** | Logs after response sent — includes status code |
| **Async errors** | Use `try/catch` + `next(err)` or `express-async-errors` |
| **Auth middleware** | Separate `requireAuth(req, res, next)` — 401 if `!req.userId` when enforced |

## Next

[Go — net/http](v-go-nethttp.md) · [Middleware overview](i-overview.md).
