---
label: "III"
subtitle: "スキーマとモデリング"
group: "MongoDB"
order: 3
---
MongoDB — スキーマとモデリング


MongoDB is **schema-flexible**, not **schema-free**. Good models match **read and write patterns** — same embed-vs-reference tradeoffs as in [Document databases](../../CS101/databases/iv-document.md).

## 1. アクセスパターンから設計する

まず質問してください:

1. 1 つの画面/API で **読み取られる** アプリは何を呼び出しますか?
2. **アトミック**に更新する必要があるものは何ですか?
3. ネストされた配列はどれくらい大きくなりますか?

```text
Read path drives layout  →  embed what you fetch together
Write path drives splits →  reference what changes independently
```

## 2. 埋め込みと参照

**埋め込み** (1 つのドキュメント):

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

**参考** (2 つのコレクション):

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

**経験則:** 配列が **数百** の要素、または **MB** のデータ、参照、またはバケット (別個のコレクション) を超える可能性がある場合。

## 3. `_id` and natural keys

Default **`ObjectId`** is fine for most apps — time-sortable, unique across shards.

安定していて一意である場合は **自然キー** を使用します。

```json
{ "_id": "user:ada@example.com", "displayName": "Ada" }
```

Custom string `_id` simplifies idempotent upserts from external systems.

## 4. スキーマの検証

データベースで形状を強制します (オプションですが、運用環境では推奨されます)。

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

アプリの検証は引き続き必要です — DB 検証はセーフティ ネットです。

## 5. Migrations without `ALTER TABLE`

スキーマの変更は **データ移行**です。

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

## 6. 重複と一貫性

重複データの埋め込み - 10,000 個の注文スナップショットで製品名を更新するのは面倒です。

|戦略 |いつ |
|----------|------|
| **スナップショットを埋め込む** |歴史的真実（購入時の価格） |
| **参照 + ルックアップ** |ライブカタログデータ |
| **ストリーム/イベントの変更** |更新を非同期的に伝達する |

For money-like flows, consider **Postgres** or **multi-document transactions** — see [Postgres overview](../postgres/i-overview.md).

## 7. 時系列と TTL

大規模なイベント:

```javascript
db.events.createIndex({ createdAt: 1 }, { expireAfterSeconds: 604800 }) // 7 days TTL
```

または、自動バケット化を備えたメトリクス/ログには **時系列コレクション** (MongoDB 5+) を使用します。

＃＃ 次

Continue with [Queries & indexes](iv-queries-and-indexes.md) for filters, aggregation, and index design.
