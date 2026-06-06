---
label: "IV"
subtitle: "索引とEXPLAIN"
group: "ポストグレ"
order: 4
---
Postgres — インデックスと EXPLAIN

**測定**するまでは、クエリが遅いのは正常です。 **`EXPLAIN (ANALYZE, BUFFERS)`** を使用して計画を読み、適切な**インデックス**を追加し、一般的なフットガンを避けてください。

## 1. インデックスがどのように役立つか

Postgres のデフォルト **B ツリー** インデックスは以下をサポートしています。

- `WHERE id = 42`
- `WHERE email = 'a@example.com'`
- `WHERE created_at > '2026-01-01'` (範囲スキャン)
- `ORDER BY created_at DESC` (インデックス順と互換性がある場合)

一致するインデックスがないと、Postgres は **Seq Scan** — テーブル内のすべての行を読み取る可能性があります。小さなテーブルには最適です。数百万行になるとコストがかかります。

```sql
CREATE INDEX posts_account_created_idx
  ON posts (account_id, created_at DESC);
```

サポート:

```sql
SELECT * FROM posts
WHERE account_id = 7
ORDER BY created_at DESC
LIMIT 20;
```

## 2. `EXPLAIN` 読書ガイド

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM posts WHERE account_id = 7 ORDER BY created_at DESC LIMIT 20;
```

|ノード |意味 |
|-----|----------|
| **シーケンススキャン** |テーブル全体の読み取り — 行数とフィルターを確認する |
| **インデックス スキャン / インデックスのみのスキャン** |インデックスを使用します。可視性マップが許可する場合、「スキャンのみ」はヒープをスキップします。
| **ビットマップ インデックス スキャン** |複数のインデックス条件を組み合わせる |
| **入れ子になったループ** | A の各行について、B を検索します。B のインデックスがあれば問題ありません。
| **ハッシュ結合 / マージ結合** |大規模なセットの結合戦略 |

焦点を当てる：

- **実際の時間** (ミリ秒) 対 **計画時間**
- **行** 推定値と **実際** — 大きな不一致 → 実行 **`ANALYZE table`**
- **バッファ: 共有ヒット/読み取り** — 高 `read` → キャッシュ コールドまたはテーブルがメモリより大きい

## 3. インデックスの種類（B-treeでは不十分な場合）

|インデックス |使用例 |
|------|----------|
| **B ツリー** (デフォルト) |等価性、範囲、並べ替え |
| **ジン** | `JSONB`、配列、フルテキスト |
| **GiST** |ジオメトリ (PostGIS)、最近傍 |
| **ハッシュ** |レア;等価性のみ、すべての操作に対して WAL セーフではない |

部分インデックス — サブセットのインデックスを作成します。

```sql
CREATE INDEX posts_unpublished_idx ON posts (account_id)
  WHERE NOT published;
```

## 4. 書き込みをブロックせずにインデックスを作成する

```sql
CREATE INDEX CONCURRENTLY posts_body_trgm_idx ON posts USING GIN (body gin_trgm_ops);
```

**`CONCURRENTLY`** は長時間の書き込みロックを回避しますが、次のとおりです。

- トランザクションブロック内では実行できません
- 失敗した場合は **INVALID** インデックスが残ります - 削除して再試行してください

## 5. よくある問題

|症状 |考えられる原因 |修正 |
|----------|--------------|-----|
|遅い `WHERE lower(email) = …` |列の関数 |式インデックス: `(lower(email))` または正規化された列を格納 |
|遅い `LIKE '%foo%'` |先頭のワイルドカード |全文/トリグラム (`pg_trgm`) |
|計画では間違ったインデックスが使用されています |古い統計 | `ANALYZE posts;` |
|インデックスは未使用 |選択性が低く、テーブルが小さい | Seq スキャンは正しい可能性があります — 測定 |
|インデックスが多すぎます |書き込みが遅い |未使用のままドロップします。多くのシングルの代わりにコンポジット |

## 6. N+1 クエリ (アプリケーション層)

一度に 1 行ずつクエリを実行する ORM ループ:

```text
Bad:  SELECT * FROM posts WHERE account_id = $1  (×1000 accounts)
Good: SELECT * FROM posts WHERE account_id = ANY($1)  or JOIN in one query
```

アプリ コードまたは **`JOIN FETCH`** (JPA) で修正します。インデックスだけでは N+1 を修正できません。

## 7. 遅いクエリの監視

開発/ステージングで **`log_min_duration_statement`** を有効にします。

```conf
log_min_duration_statement = 200ms
```

マネージド サービス (RDS など) は、合計時間の上位クエリに関する **Performance Insights** または **`pg_stat_statements`** を公開します。完全なチューニングワークフローについては、「データベースの最適化」(vii-database-optimizations.md)を参照してください。

＃＃ 次

Postgres に対する JDBC、プール、および Spring Data JPA の [アプリ統合](v-app-integration.md) に進みます。
