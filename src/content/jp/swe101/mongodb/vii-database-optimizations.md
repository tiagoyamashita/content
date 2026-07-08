---
label: "VII"
subtitle: "データベースの最適化"
group: "MongoDB"
order: 7
---
MongoDB — データベースの最適化


How to make MongoDB faster: **measure**, fix **query shape and indexes**, then scale. Index and explain basics are in [Queries & indexes](iv-queries-and-indexes.md); cross-store patterns in [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md).

## 1. 最適化ワークフロー

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

低速クエリ プロファイリングを有効にする (開発/ステージング):

```javascript
db.setProfilingLevel(1, { slowms: 100 })  // log ops > 100ms
db.system.profile.find().sort({ ts: -1 }).limit(10)
```

Atlas: **パフォーマンス アドバイザー** は、ワークロード サンプルからのインデックスを提案します。

## 2. 順序を修正します (最も安いものが最初に勝ちます)

| Priority | Lever | Example |
|----------|-------|---------|
| 1 | **Schema** | Embed for single-read; split huge arrays |
| 2 | **Query shape** | `$match` first in aggregation; project only needed fields |
| 3 | **Index** | Compound index matches filter + sort |
| 4 | **Pagination** | Keyset instead of large `skip` |
| 5 | **Read path** | Primary for read-your-writes; cache hot keys |
| 6 | **Scale** | Bigger instance, shard, separate analytics |

## 3. クエリのリライト

**投影**により、ワイヤ サイズとデコード作業が削減されます。

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

## 4. インデックス戦略

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

重複または冗長なインデックスは RAM を無駄にします — Atlas Advisor はいくつかのケースにフラグを立てます。

## 5. 書き込みパフォーマンス

| Pattern | Prefer |
|---------|--------|
| Many single inserts | **`insertMany`** batches |
| Upserts in loop | **`bulkWrite`** |
| Huge documents | Split collection; reference |
| Frequent small updates on big doc | Restructure — whole doc rewrites |

**Write concern:** `w: "majority"` for durability on replica set; tune only with understanding of rollback risk.

## 6. 読み取り設定と一貫性

```javascript
collection.find(filter).readPref("secondaryPreferred")
```

|モード |トレードオフ |
|------|-----------|
| **プライマリ** |読み取り書き込みのデフォルト |
| **セカンダリ** |スケールの読み取り値。レプリケーションの遅延 |
| **因果的一貫性** |セッション トークン - 書き込み後の順序付き読み取り |

書き込み後、ラグが許容できない限り、ユーザー側の読み取りは **プライマリ** に達する必要があります。

## 7. キャッシュとハイブリッド スタック

MongoDB はキャッシュではありません:

|レイヤー |役割 |
|------|------|
| **Redis** |セッション、レート制限、ホットキー |
| **MongoDB** |耐久性のある文書保管庫 |
| **倉庫 / SQL** |分析、JOIN のレポート |

See [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md).

## 8. ワークロードを SQL に移動するタイミング

| Signal | Consider Postgres |
|--------|-------------------|
| Heavy cross-entity reporting | SQL + warehouse |
| Complex multi-row invariants | Relational constraints |
| Many `$lookup` in hot path | Normalized schema |
| Ad-hoc JOINs by analysts | SQL BI tools |

ポリグロットの永続性は正常です。各ストアをそのジョブに合わせて最適化します。

## 9. チェックリスト

- [ ] Slow ops identified (profiler / Atlas / APM)
- [ ] **`explain("executionStats")`** on top queries — no surprise COLLSCAN at scale
- [ ] Compound indexes match filter + sort
- [ ] Projections trim fields on list APIs
- [ ] Pagination uses keyset, not large `skip`
- [ ] Document sizes bounded (no unbounded arrays)
- [ ] Backups and restore tested ([Operations & backups](vi-operations-and-backups.md))

## 関連メモ

- [Queries & indexes](iv-queries-and-indexes.md) — find, aggregation, index types
- [Schema & modeling](iii-schema-and-modeling.md) — embed vs reference
- [Document databases](../../CS101/databases/iv-document.md) — conceptual foundation
- [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md) — shared tuning mindset
