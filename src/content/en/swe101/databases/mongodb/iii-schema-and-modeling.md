---
label: "III"
subtitle: "Schema & modeling"
group: "MongoDB"
order: 3
---
MongoDB — schema & modeling
MongoDB is **schema-flexible**, not **schema-free**. Good models match **read and write patterns** — same embed-vs-reference tradeoffs as in [Document databases](../../CS101/databases/iv-document.md).

## 1. Design from access patterns

Ask first:

1. What does the app **read** in one screen/API call?
2. What must update **atomically**?
3. How big can nested arrays grow?

```text
Read path drives layout  →  embed what you fetch together
Write path drives splits →  reference what changes independently
```

## 2. Embedding vs referencing

**Embed** (one document):

```json
{
  "_id": "order_99",
  "userId": "user_42",
  "status": "paid",
  "lines": [
    { "sku": "KB-01", "qty": 1, "price": 129.99 }
  ],
  "shipping": { "city": "Portland", "zip": "97201" }
}
```

**Reference** (two collections):

```json
// orders
{ "_id": "order_99", "userId": "user_42", "lineIds": ["line_a", "line_b"] }

// order_lines
{ "_id": "line_a", "orderId": "order_99", "sku": "KB-01", "qty": 1 }
```

| Pattern | Use when |
|---------|----------|
| **Embed** | One-to-few; bounded size; always read together |
| **Reference** | One-to-many huge; shared sub-documents; independent updates |
| **`$lookup`** | Join at read time — OK for analytics, expensive at scale |

**Rule of thumb:** if an array might exceed **hundreds** of elements or **MB** of data, reference or bucket (separate collection).

## 3. `_id` and natural keys

Default **`ObjectId`** is fine for most apps — time-sortable, unique across shards.

Use **natural keys** when stable and unique:

```json
{ "_id": "user:ada@example.com", "displayName": "Ada" }
```

Custom string `_id` simplifies idempotent upserts from external systems.

## 4. Schema validation

Enforce shape at the database (optional but recommended in production):

```javascript
db.createCollection("products", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "price", "createdAt"],
      properties: {
        title: { bsonType: "string" },
        price: { bsonType: "double", minimum: 0 },
        tags: { bsonType: "array", items: { bsonType: "string" } },
        createdAt: { bsonType: "date" }
      }
    }
  },
  validationLevel: "moderate",
  validationAction: "error"
})
```

| Level | Behavior |
|-------|----------|
| **`strict`** | Validates inserts and updates |
| **`moderate`** | Validates inserts + updates that touch validated fields |

App validation still required — DB validation is a safety net.

## 5. Migrations without `ALTER TABLE`

Schema changes are **data migrations**:

```javascript
// Add default field to existing docs
db.products.updateMany(
  { archived: { $exists: false } },
  { $set: { archived: false } }
)

// Rename field (batched in app/script)
db.products.updateMany({}, { $rename: { "desc": "description" } })
```

Track scripts in git (Flyway-style numbering or `migrations/20260519_add_archived.js`). Run in CI/staging before prod.

## 6. Duplication and consistency

Embedding duplicates data — updating a product name in 10,000 order snapshots is painful.

| Strategy | When |
|----------|------|
| **Embed snapshot** | Historical truth (price at purchase time) |
| **Reference + lookup** | Live catalog data |
| **Change streams / events** | Propagate updates asynchronously |

For money-like flows, consider **Postgres** or **multi-document transactions** — see [Postgres overview](../postgres/i-overview.md).

## 7. Time-series and TTL

High-volume events:

```javascript
db.events.createIndex({ createdAt: 1 }, { expireAfterSeconds: 604800 }) // 7 days TTL
```

Or use **Time Series collections** (MongoDB 5+) for metrics/logs with automatic bucketing.

## Next

Continue with [Queries & indexes](iv-queries-and-indexes.md) for filters, aggregation, and index design.
