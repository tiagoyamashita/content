---
label: "VII"
subtitle: "Database optimizations"
group: "MongoDB"
order: 7
---
MongoDB — database optimizations
How to make MongoDB faster: **measure**, fix **query shape and indexes**, then scale. Index and explain basics are in [Queries & indexes](iv-queries-and-indexes.md); cross-store patterns in [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md).

## 1. Optimization workflow

```text
1. Find slow ops        (profiler, Atlas Performance Advisor, APM)
2. explain("executionStats")
3. Fix access pattern   (embed, project, paginate)
4. Add/adjust index     (compound, partial)
5. Re-measure           (same data volume, same query)
```

| Step | Do not skip |
|------|-------------|
| **Representative data** | Empty dev DB hides COLLSCAN |
| **One change at a time** | Index + rewrite together obscures cause |
| **Production read preference** | `secondary` reads show stale/laggy behavior |

Enable slow query profiling (dev/staging):

```javascript
db.setProfilingLevel(1, { slowms: 100 })  // log ops > 100ms
db.system.profile.find().sort({ ts: -1 }).limit(10)
```

Atlas: **Performance Advisor** suggests indexes from workload samples.

## 2. Fix order (cheapest wins first)

| Priority | Lever | Example |
|----------|-------|---------|
| 1 | **Schema** | Embed for single-read; split huge arrays |
| 2 | **Query shape** | `$match` first in aggregation; project only needed fields |
| 3 | **Index** | Compound index matches filter + sort |
| 4 | **Pagination** | Keyset instead of large `skip` |
| 5 | **Read path** | Primary for read-your-writes; cache hot keys |
| 6 | **Scale** | Bigger instance, shard, separate analytics |

## 3. Query rewrites

**Projection** reduces wire size and decode work:

```javascript
db.products.find(
  { tags: "hardware" },
  { title: 1, price: 1, _id: 0 }
)
```

**Avoid unbounded `$lookup`** on large collections — pre-filter both sides:

```javascript
db.orders.aggregate([
  { $match: { status: "open", userId: "user_42" } },
  { $lookup: {
      from: "products",
      localField: "lines.sku",
      foreignField: "sku",
      as: "productDetails"
  }}
])
```

**Covered queries** — index includes all returned fields (includes `_id` unless excluded):

```javascript
db.products.createIndex({ tags: 1, price: 1, title: 1 })
db.products.find(
  { tags: "hardware" },
  { _id: 0, title: 1, price: 1 }
)
```

## 4. Index strategy

| Rule | Detail |
|------|--------|
| **ESR rule** (compound) | **E**quality → **S**ort → **R**ange fields in index order |
| **Avoid index explosion** | Too many indexes slow writes |
| **Partial indexes** | Index active subset: `{ archived: false }` |
| **Multikey caution** | Index on large arrays multiplies index entries |
| **Review unused** | `$indexStats` — drop indexes with zero ops |

```javascript
db.products.aggregate([{ $indexStats: {} }])
```

Duplicate or redundant indexes waste RAM — Atlas Advisor flags some cases.

## 5. Write performance

| Pattern | Prefer |
|---------|--------|
| Many single inserts | **`insertMany`** batches |
| Upserts in loop | **`bulkWrite`** |
| Huge documents | Split collection; reference |
| Frequent small updates on big doc | Restructure — whole doc rewrites |

**Write concern:** `w: "majority"` for durability on replica set; tune only with understanding of rollback risk.

## 6. Read preference and consistency

```javascript
collection.find(filter).readPref("secondaryPreferred")
```

| Mode | Trade-off |
|------|-----------|
| **Primary** | Read-your-writes default |
| **Secondary** | Scale reads; replication lag |
| **Causal consistency** | Session token — ordered reads after writes |

After a write, user-facing reads should hit **primary** unless lag is acceptable.

## 7. Caching and hybrid stacks

MongoDB is not a cache:

| Layer | Role |
|-------|------|
| **Redis** | Sessions, rate limits, hot keys |
| **MongoDB** | Durable document store |
| **Warehouse / SQL** | Analytics, reporting JOINs |

See [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md).

## 8. When to move workload to SQL

| Signal | Consider Postgres |
|--------|-------------------|
| Heavy cross-entity reporting | SQL + warehouse |
| Complex multi-row invariants | Relational constraints |
| Many `$lookup` in hot path | Normalized schema |
| Ad-hoc JOINs by analysts | SQL BI tools |

Polyglot persistence is normal — optimize each store for its job.

## 9. Checklist

- [ ] Slow ops identified (profiler / Atlas / APM)
- [ ] **`explain("executionStats")`** on top queries — no surprise COLLSCAN at scale
- [ ] Compound indexes match filter + sort
- [ ] Projections trim fields on list APIs
- [ ] Pagination uses keyset, not large `skip`
- [ ] Document sizes bounded (no unbounded arrays)
- [ ] Backups and restore tested ([Operations & backups](vi-operations-and-backups.md))

## Related notes

- [Queries & indexes](iv-queries-and-indexes.md) — find, aggregation, index types
- [Schema & modeling](iii-schema-and-modeling.md) — embed vs reference
- [Document databases](../../CS101/databases/iv-document.md) — conceptual foundation
- [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md) — shared tuning mindset
