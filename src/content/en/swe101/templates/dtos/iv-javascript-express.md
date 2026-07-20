---
label: "IV"
subtitle: "JavaScript — Express"
group: "DTOs"
order: 4
---
DTO template — JavaScript (Express)
**Zod schemas** (recommended) or plain shapes with JSDoc typedefs. Router usage: [Controllers](../controllers/iv-javascript-express.md).

## Dependencies

```bash
npm install zod
# optional TypeScript: npm install -D typescript @types/express
```

## Template (Zod)

```javascript
const { z } = require("zod");

/** @typedef {{ id: string, name: string }} ItemResponse */

const CreateItemRequest = z.object({
  name: z.string().trim().min(1).max(200),
});

const ItemResponse = z.object({
  id: z.string().uuid(),
  name: z.string(),
});

/** Parse and validate request body — throws ZodError on failure. */
function parseCreateItemRequest(body) {
  return CreateItemRequest.parse(body);
}

module.exports = { CreateItemRequest, ItemResponse, parseCreateItemRequest };
```

Middleware helper:

```javascript
function validateBody(schema) {
  return (req, res, next) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({ error: result.error.flatten() });
    }
    req.validated = result.data;
    return next();
  };
}

// router.post("/", validateBody(CreateItemRequest), (req, res) => { ... });
```

## Plain JS (no library)

```javascript
/**
 * @typedef {Object} CreateItemRequest
 * @property {string} name
 */

/**
 * @typedef {Object} ItemResponse
 * @property {string} id
 * @property {string} name
 */

function parseCreateItemRequest(body) {
  const name = body?.name;
  if (typeof name !== "string" || name.trim() === "") {
    throw new Error("name is required");
  }
  return { name: name.trim() };
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **DTO ≠ DAO** | Schemas / parse helpers are wire shapes; persistence is [Repositories](../repositories/iv-javascript-express.md) — see [overview](i-overview.md#dto-vs-dao-do-not-mix-these-up) |
| **Validate once** | Middleware or a `parse*` helper at the edge |
| **Response shape** | Keep `ItemResponse` consistent across all routes |
| **TypeScript** | Replace JSDoc with `interface` / `type` + Zod inference |

## Next

[Go — net/http](v-go-nethttp.md) · [DTOs overview](i-overview.md).
