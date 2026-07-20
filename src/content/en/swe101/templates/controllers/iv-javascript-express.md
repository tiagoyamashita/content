---
label: "IV"
subtitle: "JavaScript — Express"
group: "Controllers"
order: 4
---
Controller template — JavaScript (Express)
Minimal **router** for a resource. Language track: [JavaScript](../../languages&frameworks/javascript/i-overview.md).

## Dependencies

```bash
npm init -y
npm install express
# optional validation: npm install zod
```

## Template

```javascript
const express = require("express");
const { randomUUID } = require("crypto");

const app = express();
app.use(express.json());

const router = express.Router();

// Demo only — replace with a service + DB
const store = new Map();

router.get("/", (_req, res) => {
  res.json([...store.values()]);
});

router.get("/:id", (req, res) => {
  const item = store.get(req.params.id);
  if (!item) return res.status(404).json({ error: "Not found" });
  return res.json(item);
});

router.post("/", (req, res) => {
  const name = req.body?.name;
  if (typeof name !== "string" || name.trim() === "") {
    return res.status(400).json({ error: "name is required" });
  }
  const id = randomUUID();
  const item = { id, name: name.trim() };
  store.set(id, item);
  return res.status(201).location(`/api/items/${id}`).json(item);
});

router.put("/:id", (req, res) => {
  if (!store.has(req.params.id)) {
    return res.status(404).json({ error: "Not found" });
  }
  const name = req.body?.name;
  if (typeof name !== "string" || name.trim() === "") {
    return res.status(400).json({ error: "name is required" });
  }
  const item = { id: req.params.id, name: name.trim() };
  store.set(item.id, item);
  return res.json(item);
});

router.delete("/:id", (req, res) => {
  if (!store.delete(req.params.id)) {
    return res.status(404).json({ error: "Not found" });
  }
  return res.status(204).send();
});

app.use("/api/items", router);

app.listen(3000, () => {
  console.log("listening on http://localhost:3000");
});
```

## Notes

| Topic | Practice |
|-------|----------|
| **Thin handlers** | Call `itemService.create(...)` instead of touching `Map` |
| **Validation** | Prefer Zod/Joi middleware over ad-hoc checks |
| **TypeScript** | Same shape with `Router` + typed `Request`/`Response` |

## Next

[Go — net/http](v-go-nethttp.md) · [Controllers overview](i-overview.md).
