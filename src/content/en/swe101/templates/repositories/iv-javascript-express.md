---
label: "IV"
subtitle: "JavaScript — Express"
group: "Repositories"
order: 4
---
Repository template — JavaScript (Express)
**Module with `Map`** for `Item` (`id`, `name`). Export functions; keep HTTP out of this file.

## Template

```javascript
const { randomUUID } = require("crypto");

/** @typedef {{ id: string, name: string }} Item */

const store = new Map();

function findAll() {
  return [...store.values()];
}

function findById(id) {
  return store.get(id) ?? null;
}

function save(item) {
  const id = item.id || randomUUID();
  const saved = { id, name: item.name };
  store.set(id, saved);
  return saved;
}

function deleteById(id) {
  return store.delete(id);
}

module.exports = { findAll, findById, save, deleteById };
```

Usage in a route handler:

```javascript
const itemRepo = require("./itemRepository");

router.get("/:id", (req, res) => {
  const item = itemRepo.findById(req.params.id);
  if (!item) return res.status(404).json({ error: "Not found" });
  return res.json(item);
});
```

## Notes

| Topic | Practice |
|-------|----------|
| **No `req`/`res` here** | Repository returns data; router maps to status codes |
| **Production swap** | Replace `Map` with Prisma / Knex / pg queries behind the same exports |
| **TypeScript** | Export an `ItemRepository` interface + `InMemoryItemRepository` class |
| **Testing** | Require the module in tests; or inject a factory from `app.locals` |

## Next

[Go — net/http](v-go-nethttp.md) · [Repositories overview](i-overview.md).
