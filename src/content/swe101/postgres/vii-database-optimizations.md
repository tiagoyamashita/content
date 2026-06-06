---
label: "VII"
subtitle: "データベースの最適化"
group: "Postgres"
order: 7
---
Postgres — データベースの最適化


A practical **how-to** for making Postgres faster: measure first, fix the highest-impact layer, verify with the same workload. Deep index and plan reading lives in [Indexes & EXPLAIN](iv-indexes-and-explain.md); system-design scaling patterns in [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md).

## 1. 最適化ワークフロー

```text
1. Find slow queries     (logs, pg_stat_statements, APM)
2. Reproduce with EXPLAIN (ANALYZE, BUFFERS)
3. Fix root cause        (query, index, schema, app pattern)
4. Re-measure            (same SQL, same data volume)
5. Ship + monitor        (regression alerts)
```

|ステップ |スキップしないでください |
|------|---------------|
| **ベースライン** |レコード p50/p95 レイテンシーと検査された行 |
| **一度に 1 つの変更** |インデックスとリライトを一緒に行うと、何が役に立ったかが隠されます。
| **本番環境に近いデータ** |空の開発 DB はシーケンス スキャンについて嘘をつきます。

Enable **`pg_stat_statements`** (extension) for “top queries by total time”:

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT calls, round(total_exec_time::numeric, 2) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       left(query, 120) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;
```

Reset stats after a deploy window if you need a clean slice: **`SELECT pg_stat_statements_reset();`**

## 2. 順序を修正します (最も安いものが最初に勝ちます)

| Priority | Lever | Example |
|----------|-------|---------|
| 1 | **App pattern** | Remove N+1; batch `IN` / JOIN |
| 2 | **Query shape** | Select only needed columns; filter early |
| 3 | **Index** | Composite index matching `WHERE` + `ORDER BY` |
| 4 | **Statistics** | `ANALYZE` after large load |
| 5 | **Schema** | Normalize hot wide rows; archive cold history |
| 6 | **Hardware / scale** | Read replica, bigger instance, PgBouncer |

欠落しているインデックスを修正する前に RAM を追加すると、5,000 万行のテーブルの Seq スキャンが修正されることはほとんどありません。

## 3. 重要なクエリのリライト

**Avoid `SELECT *`** on wide tables — less I/O, better index-only scans:

```sql
-- Prefer
SELECT id, title, created_at FROM posts WHERE account_id = $1 ORDER BY created_at DESC LIMIT 20;

-- Not for list APIs
SELECT * FROM posts WHERE account_id = $1;
```

**Pagination** — keyset (seek) beats large `OFFSET`:

```sql
-- Slow at high offset
SELECT id, title FROM posts ORDER BY created_at DESC OFFSET 100000 LIMIT 20;

-- Fast when you have the last seen tuple
SELECT id, title FROM posts
WHERE (created_at, id) < ($last_ts, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

Requires an index on **`(created_at DESC, id DESC)`**.

**はい/いいえだけが必要な場合は**存在するかどうか**:

```sql
SELECT EXISTS (SELECT 1 FROM orders WHERE user_id = $1 AND status = 'open');
```

## 4. インデックス戦略（概要）

See [Indexes & EXPLAIN](iv-indexes-and-explain.md) for full detail. Quick rules:

| Rule | Detail |
|------|--------|
| **Match predicates** | Leading columns = equality filters, then range |
| **One composite > many singles** | `(account_id, created_at)` beats two separate indexes for one query |
| **Partial indexes** | Index only active rows: `WHERE NOT archived` |
| **Drop unused** | `pg_stat_user_indexes.idx_scan = 0` for months → candidate to drop |
| **Create CONCURRENTLY** | In production: `CREATE INDEX CONCURRENTLY …` |

```sql
SELECT schemaname, relname, indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;
```

## 5. バキューム、膨張、プランナーの統計

統計が古い → 行の推定値が間違っている → 結合が間違っている。

```sql
ANALYZE posts;
VACUUM (ANALYZE) posts;   -- after large DELETE/UPDATE
```

| Symptom | Action |
|---------|--------|
| Table huge but row count flat | Check autovacuum; consider `VACUUM FULL` off-peak (locks) |
| Plan flipped after bulk load | `ANALYZE` all touched tables |
| Index never used | Verify query text; check selectivity |

Monitor **`n_dead_tup`** in **`pg_stat_user_tables`**.

## 6. トランザクションと接続

短いトランザクションによりロックが解放され、肥大化が軽減されます。

```sql
BEGIN;
UPDATE inventory SET qty = qty - 1 WHERE sku = 'ABC';
INSERT INTO order_lines (sku, qty) VALUES ('ABC', 1);
COMMIT;
-- Do not hold open while calling HTTP APIs
```

| Knob | Guidance |
|------|----------|
| **Pool size** | See [App integration](v-app-integration.md) — often 10–30 per instance |
| **`max_connections`** | Sum of all pools + admin < Postgres limit |
| **PgBouncer** | When connection count explodes |
| **Idle in transaction** | Kill long idle txs; fix app leak |

## 7. 間違った答えを出さずにスケーリングを読む

|パターン | | の場合に使用します。
|----------|----------|
| **リードレプリカ** |レポート、ダッシュボードは数秒の遅延を許容します |
| **書き込み + クリティカル読み取り用のプライマリ** | 「支払ってレシートを見る」フロー |
| **具体化されたビュー** |高価なアグリゲートがスケジュールどおりに更新される |

```sql
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT date_trunc('day', created_at) AS day, sum(amount) AS revenue
FROM orders
GROUP BY 1;

CREATE UNIQUE INDEX ON daily_revenue (day);
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;
```

**Cache (Redis)** in front of Postgres for hot keys — see [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md). Invalidate on write, not TTL-only for money.

## 8. パーティショニング (大きなテーブル)

単一テーブルが快適なバキューム/バックアップ サイズ (多くの場合、1 億行以上または時系列) を超える場合:

```sql
CREATE TABLE events (
  id         BIGSERIAL,
  created_at TIMESTAMPTZ NOT NULL,
  payload    JSONB NOT NULL
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_05 PARTITION OF events
  FOR VALUES FROM ('2026-05-01') TO ('2026-06-01');
```

Queries that filter on **`created_at`** prune old partitions — less data scanned per query.

## 9. 「DB をスケールする」前のチェックリスト

- [ ] Top 5 queries by **`pg_stat_statements`** reviewed
- [ ] **`EXPLAIN (ANALYZE, BUFFERS)`** on each slow path
- [ ] No fixable N+1 in app / ORM
- [ ] Indexes match real `WHERE` / `ORDER BY`
- [ ] **`ANALYZE`** after schema or bulk data change
- [ ] Connection pool sized; no idle-in-transaction leaks
- [ ] Backups and restore tested ([Operations & backups](vi-operations-and-backups.md))

## 関連メモ

- [Indexes & EXPLAIN](iv-indexes-and-explain.md) — plans, index types, `CONCURRENTLY`
- [Database optimizations (PL/SQL)](../plsql/vii-database-optimizations.md) — Oracle-side tuning parallels
- [Relational (SQL)](../../CS101/databases/ii-relational.md) — joins, transactions, normalization
