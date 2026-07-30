---
label: "IV"
subtitle: "JavaScript — Express"
group: "Logging"
order: 4
---
Logging template — JavaScript (Express)
Use **Pino** for structured JSON, **`AsyncLocalStorage`** for request context, one access-log middleware, and a higher-order function for reusable operation logs.

## Logger and request context

```javascript
import { AsyncLocalStorage } from "node:async_hooks";
import { randomUUID } from "node:crypto";
import express from "express";
import pino from "pino";

const rootLogger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  redact: {
    paths: [
      "req.headers.authorization",
      "req.headers.cookie",
      "*.password",
      "*.token",
    ],
    censor: "[REDACTED]",
  },
});

const requestContext = new AsyncLocalStorage();

export function logger() {
  return requestContext.getStore()?.log ?? rootLogger;
}
```

## Access-log middleware

```javascript
export function accessLog(req, res, next) {
  const requestId = req.get("X-Request-Id") ?? randomUUID();
  const started = process.hrtime.bigint();
  const log = rootLogger.child({ requestId });

  res.setHeader("X-Request-Id", requestId);

  requestContext.run({ requestId, log }, () => {
    res.once("finish", () => {
      const durationMs = Number(process.hrtime.bigint() - started) / 1e6;
      log.info({
        event: "http.request.completed",
        method: req.method,
        route: req.route?.path ?? req.path,
        status: res.statusCode,
        durationMs: Math.round(durationMs * 10) / 10,
      });
    });

    next();
  });
}

const app = express();
app.use(express.json());
app.use(accessLog);
```

## Reusable operation wrapper

```javascript
export function loggedOperation(operation, functionToRun) {
  return async function logged(...args) {
    const started = process.hrtime.bigint();
    try {
      const result = await functionToRun.apply(this, args);
      logger().info({
        event: "operation.completed",
        operation,
        outcome: "success",
        durationMs: elapsedMs(started),
      });
      return result;
    } catch (error) {
      logger().error({
        event: "operation.completed",
        operation,
        outcome: "error",
        errorType: error.constructor?.name ?? "Error",
        durationMs: elapsedMs(started),
        err: error,
      });
      throw error;
    }
  };
}

function elapsedMs(started) {
  return Math.round(Number(process.hrtime.bigint() - started) / 100_000) / 10;
}
```

Wrap a service method once:

```javascript
export const createItem = loggedOperation(
  "item.create",
  async function createItem(request) {
    const item = await itemRepository.save({ name: request.name });
    logger().info({ event: "item.created", itemId: item.id });
    return item;
  },
);
```

## Notes

| Topic | Practice |
|-------|----------|
| **Child logger** | Bind `requestId` once; every downstream log inherits it |
| **Redaction** | Configure Pino paths centrally; still prefer safe-field allowlists |
| **No args/results** | The wrapper never serializes function inputs or output |
| **Response finish** | Logs the final status after Express sends the response |
| **Error ownership** | Wrapper rethrows; avoid logging the same error again in every layer |

## Next

[Go — net/http](v-go-nethttp.md) · [Logging overview](i-overview.md).
