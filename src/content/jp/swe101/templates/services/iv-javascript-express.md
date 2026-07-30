---
label: "IV"
subtitle: "JavaScript — Express"
group: "Services"
order: 4
---
Service template — JavaScript (Express)
**`itemService`** module — plain functions or a class; no `req` / `res` here. DTOs: [DTOs](../dtos/iv-javascript-express.md) · router: [Controllers](../controllers/iv-javascript-express.md).

## Template

```javascript
const { randomUUID } = require("crypto");

/** @typedef {{ id: string, name: string }} Item */

/** In-memory store — replace with DB repository module. */
function createItemRepository() {
  const store = new Map();

  return {
    findAll() {
      return [...store.values()];
    },
    findById(id) {
      return store.get(id) ?? null;
    },
    save(item) {
      store.set(item.id, item);
      return item;
    },
    deleteById(id) {
      return store.delete(id);
    },
  };
}

function createItemService(repository) {
  return {
    list() {
      return repository.findAll();
    },

    get(id) {
      return repository.findById(id);
    },

    create({ name }) {
      const item = { id: randomUUID(), name: name.trim() };
      return repository.save(item);
    },

    update(id, { name }) {
      if (!repository.findById(id)) return null;
      return repository.save({ id, name: name.trim() });
    },

    delete(id) {
      return repository.deleteById(id);
    },
  };
}

const repository = createItemRepository();
const itemService = createItemService(repository);

module.exports = { createItemRepository, createItemService, itemService };
```

Usage in a route handler:

```javascript
const { itemService } = require("./itemService");

router.post("/", (req, res) => {
  const name = req.body?.name;
  if (typeof name !== "string" || name.trim() === "") {
    return res.status(400).json({ error: "name is required" });
  }
  const item = itemService.create({ name });
  return res.status(201).json(item);
});
```

## Notes

| Topic | Practice |
|-------|----------|
| **Factory pattern** | `createItemService(repo)` makes tests easy |
| **No HTTP in service** | Return data or `null` — handler sets status |
| **Validation** | Parse DTOs in middleware before calling service |
| **TypeScript** | Same shape with interfaces + explicit return types |

## Next

[Go — net/http](v-go-nethttp.md) · [Services overview](i-overview.md).
