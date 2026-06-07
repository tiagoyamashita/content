---
label: "IV"
subtitle: "インデックスと EXPLAIN"
group: "Postgres"
order: 4
---
Postgres — インデックスと EXPLAIN


Slow queries are normal until you **measure**. Use **`EXPLAIN (ANALYZE, BUFFERS)`** to read plans, add the right **indexes**, and avoid common foot-guns.

## 1. インデックスがどのように役立つか

Postgres デフォルト **B-tree** インデックスは以下をサポートします。

- `WHERE id = 42`
- `WHERE email = 'a@example.com'`
- `WHERE created_at > '2026-01-01'` (range scans)
- `ORDER BY created_at DESC` (when compatible with index order)

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

## 2. `EXPLAIN` reading guide

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

- **Actual time** (ms) vs **Planning time**
- **Rows** estimate vs **actual** — large mismatch → run **`ANALYZE table`**
- **Buffers: shared hit/read** — high `read` → cache cold or table bigger than memory

## 3. インデックスの種類 (B-tree だけでは不十分な場合)

| Index | Use case |
|-------|----------|
| **B-tree** (default) | Equality, range, sorting |
| **GIN** | `JSONB`, arrays, full-text |
| **GiST** | Geometry (PostGIS), nearest-neighbor |
| **Hash** | Rare; equality only, not WAL-safe for all ops |

部分インデックス — サブセットのインデックスを作成します。

```sql
CREATE INDEX posts_unpublished_idx ON posts (account_id)
  WHERE NOT published;
```

## 4. 書き込みをブロックせずにインデックスを作成する

```sql
CREATE INDEX CONCURRENTLY posts_body_trgm_idx ON posts USING GIN (body gin_trgm_ops);
```

**`CONCURRENTLY`** avoids long write locks but:

- トランザクションブロック内では実行できません
- 失敗した場合は **INVALID** インデックスを残します - 削除して再試行します

## 5. よくある問題

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Slow `WHERE lower(email) = …` | Function on column | Expression index: `(lower(email))` or store normalized column |
| Slow `LIKE '%foo%'` | Leading wildcard | Full-text / trigram (`pg_trgm`) |
| Plan uses wrong index | Stale stats | `ANALYZE posts;` |
| Index unused | Low selectivity, small table | Seq scan may be correct — measure |
| Too many indexes | Slow writes | Drop unused; composite instead of many singles |

## 6. N+1 クエリ (アプリケーション層)

ORM ループは一度に 1 行ずつクエリを実行します。

```text
Bad:  SELECT * FROM posts WHERE account_id = $1  (×1000 accounts)
Good: SELECT * FROM posts WHERE account_id = ANY($1)  or JOIN in one query
```

Fix in app code or with **`JOIN FETCH`** (JPA) — indexes alone do not fix N+1.

## 7. 遅いクエリの監視

Enable **`log_min_duration_statement`** in dev/staging:

```conf
log_min_duration_statement = 200ms
```

Managed services (RDS, etc.) expose **Performance Insights** or **`pg_stat_statements`** for top queries by total time. For the full tuning workflow, see [Database optimizations](vii-database-optimizations.md).

＃＃ 次

Continue with [App integration](v-app-integration.md) for JDBC, pools, and Spring Data JPA against Postgres.
