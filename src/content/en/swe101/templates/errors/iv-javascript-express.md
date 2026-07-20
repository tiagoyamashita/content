---
label: "IV"
subtitle: "JavaScript — Express"
group: "Errors"
order: 4
---
Error template — JavaScript (Express)
**`AppError` class + error middleware** — route handlers call `next(err)`; one middleware maps to status + JSON.

## Template

```javascript
const express = require("express");

class AppError extends Error {
  constructor(message, statusCode = 500, code = "INTERNAL_ERROR") {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }

  static notFound(message = "Item not found") {
    return new AppError(message, 404, "NOT_FOUND");
  }
}

const app = express();
app.use(express.json());

// Route example — pass errors to middleware:
// router.get("/:id", (req, res, next) => {
//   const item = itemRepo.findById(req.params.id);
//   if (!item) return next(AppError.notFound());
//   return res.json(item);
// });

// Must be registered AFTER routes:
app.use((err, req, res, _next) => {
  const status = err.statusCode || 500;
  const code = err.code || "INTERNAL_ERROR";
  const message = status === 500 ? "Internal server error" : err.message;
  if (status === 500) console.error(err);
  res.status(status).json({ error: message, code });
});
```

## Notes

| Topic | Practice |
|-------|----------|
| **Always `next(err)`** | Async routes: wrap in try/catch or use `express-async-errors` |
| **4-arg middleware** | Express only treats `(err, req, res, next)` as error handler |
| **Order matters** | Error middleware last; before it, 404 fallback: `app.use((req, res) => res.status(404)...)` |
| **Operational vs programmer** | `AppError` for expected cases; log and mask unexpected throws as 500 |

## Next

[Go — net/http](v-go-nethttp.md) · [Errors overview](i-overview.md).
