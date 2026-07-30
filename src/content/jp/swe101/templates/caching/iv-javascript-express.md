---
label: "IV"
subtitle: "JavaScript — Express"
group: "Caching"
order: 4
---
Caching template — JavaScript (Express)
**`Cache-Control` + `ETag`** on GET item; **304** when **`If-None-Match`** matches.

## Template

```javascript
const crypto = require("crypto");
const express = require("express");

const router = express.Router();

function computeEtag(item) {
  const payload = `${item.id}|${item.name}|${item.updatedAt}`;
  const hash = crypto.createHash("sha256").update(payload).digest("hex").slice(0, 16);
  return `"${hash}"`;
}

router.get("/:id", (req, res, next) => {
  const item = itemRepo.findById(req.params.id); // + optional Redis
  if (!item) {
    return res.status(404).json({ error: "Item not found" });
  }

  const etag = computeEtag(item);
  res.set("Cache-Control", "public, max-age=60");
  res.set("ETag", etag);

  if (req.get("If-None-Match") === etag) {
    return res.status(304).end();
  }

  return res.json(item);
});

// On PUT/DELETE — invalidate app cache:
// redis.del(`item:${req.params.id}`);
// res.set("Cache-Control", "no-store");

module.exports = router;
```

Mount under `/api/items`. Use `res.status(304).end()` — no JSON body on not-modified.

## Notes

| Topic | Practice |
|-------|----------|
| **304 vs 200** | Same headers; 304 has no body — saves bandwidth |
| **ETag on lists** | Hash sorted IDs + max `updatedAt` — invalidate when any row changes |
| **Personalized JSON** | `Cache-Control: private, no-store` — or `Vary: Authorization` |
| **CDN** | `public, max-age=N` only when response is identical for all users |

## Next

[Go — net/http](v-go-nethttp.md) · [Caching overview](i-overview.md).
