---
label: "IV"
subtitle: "JavaScript — Express"
group: "Observability"
order: 4
---
Observability template — JavaScript (Express)
**Pino-style structured JSON logs** + request **duration** on response finish. Works with plain `console` or real `pino`.

## Template

```javascript
const express = require("express");
const { randomUUID } = require("crypto");

function createLogger() {
  return {
    info(fields) {
      console.log(JSON.stringify({ level: "info", ...fields }));
    },
    debug(fields) {
      console.log(JSON.stringify({ level: "debug", ...fields }));
    },
  };
}

const log = createLogger();

function observabilityMiddleware(req, res, next) {
  const requestId = req.get("X-Request-Id") || randomUUID();
  req.requestId = requestId;
  res.setHeader("X-Request-Id", requestId);

  const start = process.hrtime.bigint();
  res.on("finish", () => {
    const durationMs = Number(process.hrtime.bigint() - start) / 1e6;
    log.info({
      requestId,
      method: req.method,
      path: req.path,
      status: res.statusCode,
      durationMs: Math.round(durationMs * 10) / 10,
    });
  });
  next();
}

const app = express();
app.use(express.json());
app.use(observabilityMiddleware);

// Item route example:
// app.get("/api/items/:id", (req, res, next) => {
//   log.debug({ requestId: req.requestId, itemId: req.params.id, msg: "fetching item" });
//   const item = itemRepo.findById(req.params.id);
//   if (!item) return next(AppError.notFound());
//   return res.json(item);
// });
```

For production: swap `createLogger` for `pino` + `pino-http` (auto request logging) or ship JSON to your collector.

## Notes

| Topic | Practice |
|-------|----------|
| **`finish` event** | Fires when response is sent — includes error responses |
| **Child loggers** | `req.log = log.child({ requestId })` if using Pino |
| **Metrics** | Export duration to Prometheus via `prom-client` histogram in the same middleware |
| **Trace context** | `@opentelemetry/instrumentation-express` for auto spans |

## Next

[Go — net/http](v-go-nethttp.md) · [Observability overview](i-overview.md).
