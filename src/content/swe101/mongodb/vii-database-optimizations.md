---
label: "VII"
subtitle: "データベースの最適化"
group: "モンゴDB"
order: 7
---
MongoDB — データベースの最適化

MongoDB を高速化する方法: **測定**、**クエリの形状とインデックス**を修正してから、スケーリングします。インデックスと説明の基本は [クエリとインデックス](iv-queries-and-indexes.md) にあります。 [データベース最適化 (Postgres)](../postgres/vii-database-optimizations.md) のクロスストア パターン。

## 1. 最適化ワークフロー

```text
1. Find slow ops        (profiler, Atlas Performance Advisor, APM)
2. explain("executionStats")
3. Fix access pattern   (embed, project, paginate)
4. Add/adjust index     (compound, partial)
5. Re-measure           (same data volume, same query)
```

|ステップ |スキップしないでください |
|------|---------------|
| **代表的なデータ** |空の開発 DB は COLLSCAN を非表示にします。
| **一度に 1 つの変更** |インデックスと書き換えを一緒に行うと、原因がわかりにくくなります。
| **実稼働読み取り設定** | `secondary` 読み取りは古い/遅い動作を示します |

低速クエリ プロファイリングを有効にする (開発/ステージング):

```javascript
db.setProfilingLevel(1, { slowms: 100 })  // log ops > 100ms
db.system.profile.find().sort({ ts: -1 }).limit(10)
```

Atlas: **パフォーマンス アドバイザー** は、ワークロード サンプルからのインデックスを提案します。

## 2. 順序を修正します (最も安いものが最初に勝ちます)

|優先順位 |レバー |例 |
|----------|----------|----------|
| 1 | **スキーマ** |シングルリード用に埋め込みます。巨大な配列を分割する |
| 2 | **クエリの形状** | `$match` 集計の最初。プロジェクトのみに必要なフィールド |
| 3 | **インデックス** |複合インデックスはフィルター + ソート | と一致します。
| 4 | **ページネーション** |大きな `skip` の代わりにキーセット |
| 5 | **読み取りパス** |読み取り書き込み用のプライマリ。ホットキーをキャッシュする |
| 6 | **スケール** |より大きなインスタンス、シャード、個別の分析 |

## 3. クエリのリライト

**投影**により、ワイヤ サイズとデコード作業が削減されます。

```javascript
db.products.find(
  { tags: "hardware" },
  { title: 1, price: 1, _id: 0 }
)
```

**大規模なコレクションでは無制限の `$lookup`** を避けてください — 両側を事前にフィルタリングします。

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

**対象となるクエリ** - インデックスには返されたすべてのフィールドが含まれます (除外されない限り `_id` を含みます)。

```javascript
db.products.createIndex({ tags: 1, price: 1, title: 1 })
db.products.find(
  { tags: "hardware" },
  { _id: 0, title: 1, price: 1 }
)
```

## 4. インデックス戦略

|ルール |詳細 |
|------|----------|
| **ESR ルール** (複合) | **E**quality → **S**ort → **R**ange フィールドのインデックス順 |
| **インデックスの爆発を避ける** |インデックスが多すぎると書き込みが遅くなります。
| **部分インデックス** |インデックスアクティブサブセット: `{ archived: false }` |
| **マルチキーに関する注意** |大きな配列のインデックスはインデックス エントリを倍増します。
| **未使用レビュー** | `$indexStats` — ゼロ操作でインデックスを削除します。

```javascript
db.products.aggregate([{ $indexStats: {} }])
```

重複または冗長なインデックスは RAM を無駄にします — Atlas Advisor はいくつかのケースにフラグを立てます。

## 5. 書き込みパフォーマンス

|パターン |優先する |
|----------|----------|
|多数の単一挿入 | **`insertMany`** バッチ |
|ループ内の更新/挿入 | **`bulkWrite`** |
|膨大な書類 |分割コレクション。参照 |
|大きなドキュメントの小さな更新を頻繁に行う |再構成 — ドキュメント全体を書き直す |

**懸念事項を記入してください:** レプリカ セットの耐久性については `w: "majority"`。ロールバックのリスクを理解した上でのみ調整してください。

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

MongoDB はキャッシュではありません。

|レイヤー |役割 |
|------|------|
| **Redis** |セッション、レート制限、ホットキー |
| **MongoDB** |耐久性のある文書保管庫 |
| **ウェアハウス / SQL** |分析、JOIN のレポート |

[データベースのボトルネック](../sysdesign/bottleneck-analysis/vi-database.md)を参照してください。

## 8. ワークロードを SQL に移動する場合

|信号 | Postgres を検討する |
|--------|--------|
|エンティティを越えた大量のレポート | SQL + ウェアハウス |
|複雑な複数行の不変式 |関係制約 |
|ホットパスに多数の`$lookup` |正規化されたスキーマ |
|アナリストによるアドホック JOIN | SQL BI ツール |

ポリグロットの永続性は正常です。各ストアをそのジョブに合わせて最適化します。

## 9. チェックリスト

- [ ] 遅い操作が特定されました (プロファイラー/アトラス/APM)
- [ ] **`explain("executionStats")`** 上位クエリ - 大規模な COLLSCAN も驚くべきことではありません
- [ ] 複合インデックスはフィルター + ソートに一致します
- [ ] プロジェクションはリスト API のフィールドをトリムします
- [ ] ページネーションではキーセットが使用されますが、大きくはありません `skip`
- [ ] ドキュメント サイズは制限されています (制限されていない配列はありません)
- [ ] テスト済みのバックアップと復元 ([操作とバックアップ](vi-operations-and-backups.md))

## 関連メモ

- [クエリとインデックス](iv-queries-and-indexes.md) — 検索、集計、インデックスタイプ
- [スキーマとモデリング](iii-schema-and-modeling.md) — 埋め込みと参照
- [文書データベース](../../CS101/databases/iv-document.md) — 概念的な基礎
- [データベースの最適化 (Postgres)](../postgres/vii-database-optimizations.md) — チューニングの考え方の共有
