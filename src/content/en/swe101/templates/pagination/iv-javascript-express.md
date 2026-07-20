---
label: "IV"
subtitle: "JavaScript — Express"
group: "Pagination"
order: 4
---
Pagination template — JavaScript (Express)
**Query parsing** + **response envelope** for listing `Item` (`id`, `name`). Router wiring: [Controllers](../controllers/iv-javascript-express.md).

## Dependencies

```bash
npm install zod
```

## Template code

```javascript
const { z } = require("zod");

const DEFAULT_SIZE = 20;
const MAX_SIZE = 100;

const PageQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  size: z.coerce.number().int().min(1).max(MAX_SIZE).default(DEFAULT_SIZE),
});

const CursorQuerySchema = z.object({
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(MAX_SIZE).default(DEFAULT_SIZE),
});

/** @typedef {{ id: string, name: string }} ItemResponse */

/**
 * @template T
 * @typedef {Object} PagedResponse
 * @property {T[]} items
 * @property {string | null} [nextCursor]
 * @property {number | null} [total]
 */

function parsePageQuery(query) {
  const parsed = PageQuerySchema.parse(query);
  return {
    ...parsed,
    offset: (parsed.page - 1) * parsed.size,
  };
}

function parseCursorQuery(query) {
  return CursorQuerySchema.parse(query);
}

/** @returns {PagedResponse<ItemResponse>} */
function emptyPage() {
  return { items: [], nextCursor: null, total: null };
}

// GET /api/items — offset style
// router.get("/", (req, res) => {
//   const { offset, size } = parsePageQuery(req.query);
//   const items = itemRepo.findPage(offset, size);
//   const total = itemRepo.count(); // skip when expensive
//   res.json({ items, nextCursor: null, total });
// });

// GET /api/items?cursor=... — cursor style
// router.get("/", (req, res) => {
//   if (req.query.cursor !== undefined) {
//     const { cursor, limit } = parseCursorQuery(req.query);
//     const { items, nextCursor } = itemRepo.findAfterCursor(cursor ?? null, limit);
//     return res.json({ items, nextCursor, total: null });
//   }
//   ...
// });

module.exports = {
  PageQuerySchema,
  CursorQuerySchema,
  parsePageQuery,
  parseCursorQuery,
  emptyPage,
};
```

## Notes

| Topic | Practice |
|-------|----------|
| **`z.coerce.number()`** | Query strings arrive as strings — coerce before validation |
| **Clamp in one place** | Schema max + default — don't duplicate in handlers |
| **`total: null`** | Document in API spec when count is omitted |
| **Never `findAll()`** | Repository exposes `findPage(offset, limit)` only |

## Next

[Go — net/http](v-go-nethttp.md) · [Pagination overview](i-overview.md).
