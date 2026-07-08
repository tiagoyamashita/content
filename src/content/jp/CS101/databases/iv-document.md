---
label: "IV"
subtitle: "書類"
group: "データベース"
order: 4
---
文書データベース

**ドキュメント** ストアは、**`_id`** とオプションの **スキーマ検証** を備えた **自己完結型ドキュメント** (通常は **JSON** または **BSON**) として各レコードを扱います。ネストされたオブジェクトと配列は、多数の正規化された SQL テーブルではなく、1 つのドキュメント内**に存在します。

## 1. データモデル

1 つのドキュメント = 1 つの論理エンティティ (ユーザー プロファイル、製品、ブログ投稿):

```json
{
  "_id": "prod_8812",
  "title": "Mechanical keyboard",
  "price": 129.99,
  "tags": ["hardware", "peripherals"],
  "specs": {
    "switch": "linear",
    "layout": "TKL"
  },
  "reviews": [
    { "user": "ada", "stars": 5, "text": "Great feel" }
  ]
}
```

```text
SQL approach              Document approach
──────────────            ─────────────────
products table            one product document
product_tags join         tags: [ ... ] array inside
reviews table             reviews: [ ... ] embedded
specs columns or EAV      specs: { nested object }
```

## 2. スキーマの柔軟性

|モード |トレードオフ |
|------|-----------|
| **スキーマレス** |高速な反復。アプリは形状を検証します |
| **JSON スキーマの検証** | DB が不正なドキュメントを拒否する (MongoDB `$jsonSchema`) |
| **移行** |フィールドの意味が変わっても引き続き必要 |

**異なるレコードに異なるフィールドがある** (カタログ、CMS、ユーザー生成コンテンツ) 場合に適しています。

## 3. クエリ

ドキュメント DB は、任意のテーブルにわたる SQL JOIN の代わりに **APIs** または **集計パイプライン** を公開します。

MongoDB スタイルの例:

```javascript
// Find cheap hardware-tagged products
db.products.find({
  tags: "hardware",
  price: { $lt: 150 }
});

// Aggregation: average price by tag
db.products.aggregate([
  { $unwind: "$tags" },
  { $group: { _id: "$tags", avgPrice: { $avg: "$price" } } }
]);
```

ネストされたフィールド (`specs.switch`) の **インデックス** によりフィルターが高速になります。SQL と同じ B ツリーの考え方ですが、構文が異なります。

## 4. 埋め込みと参照

|パターン | | の場合に使用します。
|----------|----------|
| **親に配列/オブジェクトを埋め込む | 1 対数。一緒に読んでください。制限されたサイズ |
| **参考** 別のドキュメントの `_id` を格納 | 1 対多の巨大なセット。共有サブドキュメント |

参考例:

```json
{ "_id": "order_99", "userId": "user_42", "lines": [ ... ] }
{ "_id": "user_42", "name": "Ada", "email": "..." }
```

アプリケーションは **2 つの検索** または **`$lookup`** (左外部結合) を実行します。すべての形状に対して無料のリレーショナル JOIN オプティマイザーはありません。

## 5. トランザクションと一貫性

最新のドキュメント DB (MongoDB 4+) は、レプリカ セット上で **複数ドキュメント ACID トランザクション**をサポートします。これはお金のような更新に使用されますが、可能であれば **単一ドキュメントの書き込み用に設計**します (よりシンプルで高速)。

**結果整合性**は、セカンダリから読み取る場合、**レプリカ読み取り**に引き続き表示されます。これは、SQL リードレプリカと同じクラスのバグです。

## 6. 強みと限界

**強み**

- **JSON API とモバイル クライアントに自然に適合**
- `_id` または多くの製品のシャード キーによる **水平シャーディング**
- 進化する製品のための **柔軟なスキーマ**
- データが埋め込まれている場合、**ネストされた読み取り**を 1 往復で実行

**制限**

- **1 つのドキュメント内の **無制限の配列** → ドキュメントのサイズ制限 (MongoDB で 16 MB)
- エンティティ全体にわたる **アドホック分析** は SQL 倉庫よりも困難
- **埋め込み時のデータの重複** - 共有フィールドを変更するには多くのドキュメントを更新します
- **複雑な多対多**のレポートは、**SQL** または **ウェアハウス** に移動されることがよくあります

## 7. ドキュメントを選択する場合

- コンテンツ プラットフォーム、さまざまな属性を持つカタログ
- **フロントエンド用バックエンド** API 形状の BLOB を保存する
- スキーマ チャーンが多いプロトタイプ
- **NOT** は、テーブル間の不変条件が重い厳密な財務台帳のデフォルト — **リレーショナル** が優先されることが多い

## 8. 例

|製品 |メモ |
|----------|----------|
| **MongoDB** |一般的なドキュメント ストア、集約フレームワーク |
| **CouchDB** | HTTP API、マルチマスター レプリケーション |
| **ファイアストア** |マネージド、モバイル/Web SDK、リアルタイム リスナー |
| **PostgreSQL JSONB** |ハイブリッド: SQL + 1 つのエンジン内のドキュメント列 |

## 9. Java スケッチ (MongoDB ドライバー)

```java
// Compile: javac --release 22 …
// org.mongodb:mongodb-driver-sync (conceptual)
Document filter = new Document("tags", "hardware")
    .append("price", new Document("$lt", 150));
collection.find(filter).into(new ArrayList<>());
```

Spring Data MongoDB は、JPA と同様に **`@Document`** エンティティをマップします。

## 10. 関連

- **概要** — [データベースの概要](i-overview.md)
- **リレーショナル** — JOIN と厳密なスキーマが優勢な場合 [リレーショナル (SQL)](ii-relational.md)
- **ワイドカラム** — 書き込みの多いワイド行用の別の NoSQL ファミリ [ワイドカラム](v-wide-column.md)
