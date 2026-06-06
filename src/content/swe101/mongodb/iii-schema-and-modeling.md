---
label: "III"
subtitle: "スキーマとモデリング"
group: "モンゴDB"
order: 3
---
MongoDB — スキーマとモデリング

MongoDB は **スキーマフリー**ではなく、**スキーマ柔軟**です。優れたモデルは **読み取りパターンと書き込みパターン** に一致します。これは、[ドキュメント データベース](../../CS101/databases/iv-document.md) と同じ、埋め込みと参照のトレードオフです。

## 1. アクセスパターンから設計する

まず質問してください:

1. アプリは 1 つの画面/API 呼び出しで何を**読み取り**しますか?
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

|パターン | | の場合に使用します。
|----------|----------|
| **埋め込む** | 1 対数。制限されたサイズ。いつも一緒に読んでください |
| **参考** | 1 対多の巨大な。共有サブドキュメント。独立したアップデート |
| **`$lookup`** |読み取り時に参加 — 分析にはOK、大規模には高価 |

**経験則:** 配列が **数百** の要素、または **MB** のデータ、参照、またはバケット (別個のコレクション) を超える可能性がある場合。

## 3. `_id` とナチュラルキー

ほとんどのアプリではデフォルトの **`ObjectId`** で問題ありません。時間順に並べ替え可能で、シャード間で一意です。

安定していて一意である場合は **自然キー** を使用します。

```json
{ "_id": "user:ada@example.com", "displayName": "Ada" }
```

カスタム文字列 `_id` は、外部システムからの冪等 UPSERT を簡素化します。

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

|レベル |行動 |
|------|----------|
| **`strict`** |挿入と更新を検証します。
| **`moderate`** |検証されたフィールドに影響を与える挿入と更新を検証します。

アプリの検証は引き続き必要です — DB 検証はセーフティ ネットです。

## 5. `ALTER TABLE` を使用しない移行

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

git でスクリプトを追跡します (Flyway スタイルの番号付けまたは `migrations/20260519_add_archived.js`)。 prod の前に CI/ステージングで実行します。

## 6. 重複と一貫性

重複データの埋め込み - 10,000 個の注文スナップショットで製品名を更新するのは面倒です。

|戦略 |いつ |
|----------|------|
| **スナップショットを埋め込む** |歴史的真実（購入時の価格） |
| **参照 + ルックアップ** |ライブカタログデータ |
| **ストリーム/イベントの変更** |更新を非同期的に伝達する |

お金のような流れについては、**Postgres** または **複数ドキュメント トランザクション** を検討してください。[Postgres の概要](../postgres/i-overview.md) を参照してください。

## 7. 時系列とTTL

大規模なイベント:

```javascript
db.events.createIndex({ createdAt: 1 }, { expireAfterSeconds: 604800 }) // 7 days TTL
```

または、自動バケット化を備えたメトリクス/ログには **時系列コレクション** (MongoDB 5+) を使用します。

＃＃ 次

[クエリとインデックス](iv-queries-and-indexes.md) に進み、フィルタ、集計、インデックスの設計を行います。
