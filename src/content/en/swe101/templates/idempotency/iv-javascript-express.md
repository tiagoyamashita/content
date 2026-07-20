---
label: "IV"
subtitle: "JavaScript — Express"
group: "Idempotency"
order: 4
---
Idempotency template — JavaScript (Express)
**Middleware** validates `Idempotency-Key` on `POST /items`; **service** looks up key, replays response, or creates Item once.

Errors: [Errors](../errors/iv-javascript-express.md) · service: [Services](../services/iv-javascript-express.md).

## Template

```javascript
const express = require("express");
const crypto = require("crypto");
const { randomUUID } = require("crypto");

/** @typedef {{ bodyHash: string, statusCode: number, body: object, expiresAt: number }} IdempotencyRecord */

function createIdempotencyStore() {
  /** @type {Map<string, IdempotencyRecord>} */
  const data = new Map();
  const TTL_MS = 24 * 60 * 60 * 1000;

  return {
    get(key) {
      const rec = data.get(key);
      if (!rec) return null;
      if (Date.now() > rec.expiresAt) {
        data.delete(key);
        return null;
      }
      return rec;
    },
    put(key, record) {
      data.set(key, { ...record, expiresAt: Date.now() + TTL_MS });
    },
  };
}

function hashBody(body) {
  const canonical = JSON.stringify(body, Object.keys(body).sort());
  return crypto.createHash("sha256").update(canonical).digest("hex");
}

function createItemService(idempotencyStore) {
  const items = new Map();

  return {
    async createIdempotent(key, body) {
      const bodyHash = hashBody(body);
      const existing = idempotencyStore.get(key);

      if (existing) {
        if (existing.bodyHash !== bodyHash) {
          const err = new Error("Idempotency-Key reused with different body");
          err.statusCode = 409;
          err.code = "IDEMPOTENCY_CONFLICT";
          throw err;
        }
        return { statusCode: existing.statusCode, body: existing.body, replayed: true };
      }

      const item = { id: randomUUID(), name: String(body.name).trim() };
      items.set(item.id, item);

      idempotencyStore.put(key, {
        bodyHash,
        statusCode: 201,
        body: item,
      });

      return { statusCode: 201, body: item, replayed: false };
    },
  };
}

/** Middleware: require Idempotency-Key on POST /items */
function requireIdempotencyKey(req, res, next) {
  if (req.method !== "POST") return next();

  const key = req.headers["idempotency-key"];
  if (typeof key !== "string" || key.trim() === "") {
    return res.status(400).json({ error: "Idempotency-Key required", code: "MISSING_KEY" });
  }
  req.idempotencyKey = key.trim();
  return next();
}

const store = createIdempotencyStore();
const itemService = createItemService(store);

const app = express();
app.use(express.json());

app.post("/items", requireIdempotencyKey, async (req, res, next) => {
  try {
    const name = req.body?.name;
    if (typeof name !== "string" || name.trim() === "") {
      return res.status(400).json({ error: "name is required" });
    }

    const result = await itemService.createIdempotent(req.idempotencyKey, { name });
    if (result.replayed) res.set("Idempotency-Replayed", "true");
    return res.status(result.statusCode).json(result.body);
  } catch (err) {
    return next(err);
  }
});

module.exports = { requireIdempotencyKey, createItemService, itemService };
```

Mount middleware on the router for scoped paths:

```javascript
const router = express.Router();
router.use("/items", (req, res, next) => {
  if (req.method === "POST") return requireIdempotencyKey(req, res, next);
  return next();
});
```

## Notes

| Topic | Practice |
|-------|----------|
| **Middleware first** | Validate header before body parsing errors obscure the real problem |
| **Case-insensitive header** | Express lowercases headers — use `idempotency-key` |
| **Store backend** | Redis `SET key JSON EX ttl` — atomic for concurrent retries |
| **Replay header** | Optional `Idempotency-Replayed: true` helps clients and support |

## Next

[Go — net/http](v-go-nethttp.md) · [Idempotency overview](i-overview.md).
