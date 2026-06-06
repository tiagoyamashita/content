---
label: "IV"
subtitle: "クエリとインデックス"
group: "モンゴDB"
order: 4
---
MongoDB — クエリとインデックス

**`find`** でフィルタリングし、**集計**で再形成し、**インデックス**でホット パスを高速化します。必ず **`explain()`** で確認してください。

## 1. 基本を見つける

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

|オペレーター |意味 |
|----------|----------|
| **`$eq`、`$ne`、`$gt`、`$gte`、`$lt`、`$lte`** |比較 |
| **`$in`、`$nin`** |メンバーシップ |
| **`$and`、`$or`、`$not`** |ロジック |
| **`$exists`** |フィールドの存在 |
| **`$regex`** |パターン マッチ — 慎重に使用してください (アンカーされている場合のみインデックスに適しています)。

## 2. アップデート

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

デフォルトでは **1 つのドキュメント**に対してアトミックです。複数文書のトランザクション:

```javascript
session = db.getMongo().startSession()
session.withTransaction(() => {
  db.accounts.updateOne({ _id: 1 }, { $inc: { balance: -100 } }, { session })
  db.accounts.updateOne({ _id: 2 }, { $inc: { balance: 100 } }, { session })
})
```

**レプリカ セット**が必要です。実稼働 TXS にはスタンドアロンではありません。

## 3. 集約パイプライン

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

|ステージ |役割 |
|------|------|
| **`$match`** |早期にフィルタリング — `find` | のようなインデックスを使用します。
| **`$group`** |集計 (SQL `GROUP BY` など) |
| **`$lookup`** |左外側で別のコレクションに参加 |
| **`$project`** |形状出力 |
| **`$unwind`** |配列を平坦化する |

**`$match`** と **`$sort`/`$limit`** をできるだけ早く配置して、文書が下流に流れるのを減らします。

## 4. インデックス

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

|インデックスの種類 |使用 |
|-----------|-----|
| **単一 / 複合** |ほとんどのクエリ |
| **マルチキー** |配列フィールドで自動 |
| **テキスト** |全文検索 |
| **2dsphere** |地理クエリ |
| **ワイルドカード** |動的フィールド名 (`"$**"`) — 使用は慎重に |

## 5. 計画について説明する

```javascript
db.products.find({ tags: "hardware", price: { $lt: 150 } }).explain("executionStats")
```

|メトリック |見る |
|------|------|
| **`totalDocsExamined` vs `nReturned`** |大きなギャップ → インデックスが見つからない/間違っている |
| **`COLLSCAN`** |完全なコレクションのスキャン — 小さなコレクションのみに OK |
| **`IXSCAN`** |使用されるインデックス |
| **`executionTimeMillis`** |負荷時のレイテンシ |

[Postgres Indexes & EXPLAIN](../postgres/iv-indexes-and-explain.md) と同じ考え方 - 構文が異なります。

## 6. ページネーション

**オフセット** (`skip`) は、オフセットが大きいと速度が低下します。

```javascript
// Slow at high page numbers
db.products.find().sort({ _id: 1 }).skip(100000).limit(20)
```

**キーセット (シーク)** ページネーション:

```javascript
db.products.find({ _id: { $gt: ObjectId("…lastSeen…") } })
  .sort({ _id: 1 })
  .limit(20)
```

インデックスと一致する並べ替えフィールドを使用します (通常は **`_id`** または **`createdAt` + `_id`**)。

＃＃ 次

Spring Data MongoDB および PyMongo の [アプリ統合](v-app-integration.md) に進みます。
