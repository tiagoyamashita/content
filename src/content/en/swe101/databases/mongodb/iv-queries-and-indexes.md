---
label: "IV"
subtitle: "Queries & indexes"
group: "MongoDB"
order: 4
---
MongoDB — queries & indexes
Filter with **`find`**, reshape with **aggregation**, and speed hot paths with **indexes**. Always confirm with **`explain()`**.

## 1. Find basics

```javascript
// Equality + range + array membership
db.products.find({
  tags: "hardware",
  price: { $gte: 50, $lt: 200 },
  "specs.layout": "TKL"
})

// Projection — return fewer fields
db.products.find(
  { tags: "hardware" },
  { title: 1, price: 1, _id: 0 }
)

// Sort + limit (pagination)
db.products.find({ tags: "hardware" })
  .sort({ price: -1 })
  .limit(20)
```

| Operator | Meaning |
|----------|---------|
| **`$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`** | Comparisons |
| **`$in`, `$nin`** | Membership |
| **`$and`, `$or`, `$not`** | Logic |
| **`$exists`** | Field presence |
| **`$regex`** | Pattern match — use with care (index-friendly only if anchored) |

## 2. Updates

```javascript
db.products.updateOne(
  { _id: "prod_8812" },
  { $set: { price: 119.99 }, $push: { tags: "sale" } }
)

db.products.updateMany(
  { archived: true },
  { $unset: { featured: "" } }
)
```

Atomic on **one document** by default. Multi-document transactions:

```javascript
session = db.getMongo().startSession()
session.withTransaction(() => {
  db.accounts.updateOne({ _id: 1 }, { $inc: { balance: -100 } }, { session })
  db.accounts.updateOne({ _id: 2 }, { $inc: { balance: 100 } }, { session })
})
```

Requires **replica set** — not standalone for production txs.

## 3. Aggregation pipeline

```javascript
db.orders.aggregate([
  { $match: { status: "paid", createdAt: { $gte: ISODate("2026-05-01") } } },
  { $unwind: "$lines" },
  { $group: {
      _id: "$lines.sku",
      revenue: { $sum: { $multiply: ["$lines.qty", "$lines.price"] } },
      count: { $sum: "$lines.qty" }
  }},
  { $sort: { revenue: -1 } },
  { $limit: 10 }
])
```

| Stage | Role |
|-------|------|
| **`$match`** | Filter early — uses indexes like `find` |
| **`$group`** | Aggregate (like SQL `GROUP BY`) |
| **`$lookup`** | Left-outer join another collection |
| **`$project`** | Shape output |
| **`$unwind`** | Flatten arrays |

Put **`$match`** and **`$sort`/`$limit`** as early as possible to reduce documents flowing downstream.

## 4. Indexes

```javascript
// Single field
db.products.createIndex({ price: 1 })

// Compound — equality fields first, then range/sort
db.products.createIndex({ tags: 1, price: -1 })

// Nested field
db.products.createIndex({ "specs.layout": 1 })

// Unique
db.users.createIndex({ email: 1 }, { unique: true })

// Partial — index subset of collection
db.products.createIndex(
  { sku: 1 },
  { partialFilterExpression: { archived: false } }
)
```

| Index type | Use |
|------------|-----|
| **Single / compound** | Most queries |
| **Multikey** | Automatic on array fields |
| **Text** | Full-text search |
| **2dsphere** | Geo queries |
| **Wildcard** | Dynamic field names (`"$**"`) — use sparingly |

## 5. Explain plans

```javascript
db.products.find({ tags: "hardware", price: { $lt: 150 } }).explain("executionStats")
```

| Metric | Watch |
|--------|-------|
| **`totalDocsExamined` vs `nReturned`** | Large gap → missing/wrong index |
| **`COLLSCAN`** | Full collection scan — OK for tiny collections only |
| **`IXSCAN`** | Index used |
| **`executionTimeMillis`** | Latency under load |

Same ideas as [Postgres Indexes & EXPLAIN](../postgres/iv-indexes-and-explain.md) — different syntax.

## 6. Pagination

**Offset** (`skip`) slows down at large offsets:

```javascript
// Slow at high page numbers
db.products.find().sort({ _id: 1 }).skip(100000).limit(20)
```

**Keyset (seek)** pagination:

```javascript
db.products.find({ _id: { $gt: ObjectId("…lastSeen…") } })
  .sort({ _id: 1 })
  .limit(20)
```

Use a sort field that matches your index (often **`_id`** or **`createdAt` + `_id`**).

## Next

Continue with [App integration](v-app-integration.md) for Spring Data MongoDB and PyMongo.
