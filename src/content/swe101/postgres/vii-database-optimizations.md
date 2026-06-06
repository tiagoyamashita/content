---
label: "VII"
subtitle: "データベースの最適化"
group: "ポストグレ"
order: 7
---
Postgres — データベースの最適化

Postgres を高速化するための実践的な**ハウツー**: 最初に測定し、最も影響の大きいレイヤーを修正し、同じワークロードで検証します。詳細なインデックスとプランの読み取りは [インデックスと説明](iv-indexes-and-explain.md) にあります。 [データベースのボトルネック](../sysdesign/bottleneck-analysis/vi-database.md) のシステム設計のスケーリング パターン。

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
| **本番環境に近いデータ** |空の開発 DB はシーケンススキャンについて嘘をつきます |

「合計時間別上位クエリ」の **`pg_stat_statements`** (拡張子) を有効にします。

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT calls, round(total_exec_time::numeric, 2) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms,
       left(query, 120) AS query
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 15;
```

クリーンなスライスが必要な場合は、デプロイウィンドウの後に統計をリセットします: **`SELECT pg_stat_statements_reset();`**

## 2. 順序を修正します (最も安いものが最初に勝ちます)

|優先順位 |レバー |例 |
|----------|----------|----------|
| 1 | **アプリのパターン** | N+1 を削除します。バッチ `IN` / 参加 |
| 2 | **クエリの形状** |必要な列のみを選択します。早めにフィルターする |
| 3 | **インデックス** | `WHERE` + `ORDER BY` に一致する複合インデックス |
| 4 | **統計** |大きな負荷後 `ANALYZE` |
| 5 | **スキーマ** |ホットワイド行を正規化します。コールド履歴をアーカイブ |
| 6 | **ハードウェア / スケール** |リードレプリカ、より大きなインスタンス、PgBouncer |

欠落しているインデックスを修正する前に RAM を追加すると、5,000 万行のテーブルの Seq スキャンが修正されることはほとんどありません。

## 3. 重要なクエリのリライト

**幅の広いテーブルでは `SELECT *`** を避けてください。I/O が減り、インデックスのみのスキャンが向上します。

```sql
-- Prefer
SELECT id, title, created_at FROM posts WHERE account_id = $1 ORDER BY created_at DESC LIMIT 20;

-- Not for list APIs
SELECT * FROM posts WHERE account_id = $1;
```

**ページネーション** — キーセット (シーク) が大 `OFFSET` を上回る:

```sql
-- Slow at high offset
SELECT id, title FROM posts ORDER BY created_at DESC OFFSET 100000 LIMIT 20;

-- Fast when you have the last seen tuple
SELECT id, title FROM posts
WHERE (created_at, id) < ($last_ts, $last_id)
ORDER BY created_at DESC, id DESC
LIMIT 20;
```

**`(created_at DESC, id DESC)`** のインデックスが必要です。

**はい/いいえだけが必要な場合は**存在するかどうか**:

```sql
SELECT EXISTS (SELECT 1 FROM orders WHERE user_id = $1 AND status = 'open');
```

## 4. インデックス戦略（概要）

詳細については、[索引と説明](iv-indexes-and-explain.md)を参照してください。簡単なルール:

|ルール |詳細 |
|------|----------|
| **述語の一致** |先頭の列 = 等価フィルター、次に範囲 |
| **1 つのコンポジット > 多数のシングル** | `(account_id, created_at)` は 1 つのクエリに対して 2 つの別々のインデックスを上回ります。
| **部分インデックス** |アクティブな行のみにインデックスを付けます: `WHERE NOT archived` |
| **未使用のドロップ** | `pg_stat_user_indexes.idx_scan = 0` ヶ月 → 削除候補者 |
| **同時に作成** |生産中: `CREATE INDEX CONCURRENTLY …` |

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

|症状 |アクション |
|----------|----------|
|テーブルは巨大だが行数は横ばい |自動バキュームをチェックします。 `VACUUM FULL` オフピーク (ロック) を検討してください。
|一括ロード後に計画が反転 | `ANALYZE` タッチされたすべてのテーブル |
|インデックスは使用されていません |クエリテキストを検証します。選択性をチェックする |

**`pg_stat_user_tables`**で**`n_dead_tup`**を監視します。

## 6. トランザクションと接続

短いトランザクションによりロックが解放され、肥大化が軽減されます。

```sql
BEGIN;
UPDATE inventory SET qty = qty - 1 WHERE sku = 'ABC';
INSERT INTO order_lines (sku, qty) VALUES ('ABC', 1);
COMMIT;
-- Do not hold open while calling HTTP APIs
```

|ノブ |ガイダンス |
|------|----------|
| **プールのサイズ** | [アプリの統合](v-app-integration.md) を参照してください。多くの場合、インスタンスごとに 10 ～ 30 |
| **`max_connections`** |すべてのプールの合計 + 管理者 < Postgres の制限 |
| **PgBouncer** |接続数が爆発的に増加したとき |
| **トランザクション中のアイドル状態** |長時間アイドル状態のTXを強制終了します。アプリのリークを修正 |

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

**ホット キー用に Postgres の前にキャッシュ (Redis)** します。[データベースのボトルネック](../sysdesign/bottleneck-analysis/vi-database.md) を参照してください。お金のための TTL のみではなく、書き込み時に無効化します。

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

**`created_at`** でフィルタリングするクエリは古いパーティションを削除します。つまり、クエリごとにスキャンされるデータが少なくなります。

## 9. 「DB をスケールする」前のチェックリスト

- [ ] **`pg_stat_statements`** による上位 5 件のクエリがレビューされました
- 各低速パスで [ ] **`EXPLAIN (ANALYZE, BUFFERS)`**
- [ ] アプリ / ORM に修正可能な N+1 がありません
- [ ] インデックスは実数 `WHERE` / `ORDER BY` と一致します
- [ ] **`ANALYZE`** スキーマまたは一括データ変更後
- [ ] 接続プールのサイズ。トランザクション中のアイドルリークがない
- [ ] テスト済みのバックアップと復元 ([操作とバックアップ](vi-operations-and-backups.md))

## 関連メモ

- [索引と説明](iv-indexes-and-explain.md) — プラン、索引タイプ、`CONCURRENTLY`
- [データベース最適化 (PL/SQL)](../plsql/vii-database-optimizations.md) — Oracle 側の並列チューニング
- [リレーショナル (SQL)](../../CS101/databases/ii-relational.md) — 結合、トランザクション、正規化
