---
label: "IV"
subtitle: "自作とインデックス"
group: "MongoDB"
order: 4
---
MongoDB — 投稿とインデックス






**でフィルタリングする`find`**、**集約**で再形成し、**インデックス**でホットパスを高速化します。必ず**で確認してください`explain()`**。

## 1.基本を見つける

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

## 2.アップデート

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

## 3. 訓練パイプライン

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
| **`$match`** |早期にフィルタリング — 次のようなインデックスを使用します`find`|
| **`$group`** |集計 (SQL など)`GROUP BY`) |
| **`$lookup`** |左外側で別のコレクションに参加 |
| **`$project`** |形状出力 |
| **`$unwind`** |配列を平坦化する |

置く **`$match`** そして **`$sort`/`$limit`** 文書が下流に流れるのを減らすために、できるだけ早く。

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
| **ワイルドカード** |動的フィールド名 (`"$**"`) — 使用は控えめに |

## 5. 計画について説明する

```javascript
db.products.find({ tags: "hardware", price: { $lt: 150 } }).explain("executionStats")
```

|メトリック |見る |
|------|------|
| **`totalDocsExamined`対`nReturned`** |大きなギャップ → インデックスが見つからない/間違っている |
| **`COLLSCAN`** |コレクション全体のスキャン - 小さなコレクションのみの OK |
| **`IXSCAN`** |使用されるインデックス |
| **`executionTimeMillis`** |負荷時のレイテンシ |

[Postgres インデックスと EXPLAIN]( と同じ考え方)../postgres/iv-indexes-and-explain.md) — 異なる構文。

## 6. ページ国家

**オフセット** (`skip`) オフセットが大きい場合は速度が低下します。

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

インデックスと一致する並べ替えフィールドを使用します (通常は **`_id`** または **`createdAt`+`_id`**)。

＃＃次

[アプリの統合] に進みます(v-app-integration.md) Spring Data MongoDB および PyMongo の場合。
