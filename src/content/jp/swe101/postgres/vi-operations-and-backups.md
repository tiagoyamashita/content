---
label: "VI"
subtitle: "操作とバックアップ"
group: "Postgres"
order: 6
---
Postgres — 操作とバックアップ

本番環境 Postgres には、**役割の分離**、**定期的なバックアップ**、および**リストア**と**フェイルオーバー**の計画が必要です。初日から DBA である必要はありませんが、これらのデフォルトを知っておく必要があります。

## 1. 役割と権限

| Role type | Typical permissions |
|-----------|---------------------|
| **`postgres` superuser** | Break-glass admin only — not for apps |
| **App role** | `CONNECT`, `USAGE` on schema, DML on app tables |
| **Migration role** | DDL for deploy user / CI |
| **Read-only analytics** | `SELECT` on specific tables or views |

```sql
CREATE ROLE app_reader NOINHERIT;
GRANT CONNECT ON DATABASE myapp TO app_reader;
GRANT USAGE ON SCHEMA public TO app_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO app_reader;
```

Rotate passwords via managed-console or **`ALTER ROLE … PASSWORD`**.

## 2. Backup with `pg_dump`

論理バックアップ — ポータブル SQL またはカスタム形式:

```bash
# Plain SQL (human-readable, slower restore)
pg_dump -h localhost -U postgres -d myapp -F p -f myapp-$(date +%F).sql

# Custom format (compressed, parallel restore)
pg_dump -h localhost -U postgres -d myapp -F c -f myapp.dump
```

復元する：

```bash
pg_restore -h localhost -U postgres -d myapp_restored -F c myapp.dump
```

| Method | Pros | Cons |
|--------|------|------|
| **`pg_dump`** | Simple, version-portable | Point-in-time needs WAL archiving too |
| **Volume snapshot** | Fast for huge DBs | Must be crash-consistent or use PG APIs |
| **Managed auto-backup** | PITR, retention policies | Vendor lock-in, cost |

**四半期ごとにリストアをテストします** - テストされていないバックアップは推測です。

## 3. ポイントインタイムリカバリ (概念)

```text
Base backup (pg_dump or physical)  +  continuous WAL archive  →  restore to any second
```

Managed Postgres (RDS, Cloud SQL, Neon) exposes PITR in the console. Self-hosted needs **`archive_mode`** and WAL shipping configured.

## 4. レプリケーションの基本

|モード |目的 |
|-----|----------|
| **ストリーミング レプリケーション** |フェイルオーバーと読み取りスケールのためのホット スタンバイ |
| **論理レプリケーション** |選択テーブル、クロスバージョンアップグレード |

アプリケーションは書き込み用に 1 つの **プライマリ** を認識します。レプリカはミリ秒から数秒まで遅れる可能性があります。書き込み後にそれに応じて UI を設計します。

## 5.真空と膨満感

Postgres uses **MVCC** — `UPDATE`/`DELETE` leave dead rows until **VACUUM** reclaims space.

| Command | Who runs it |
|---------|-------------|
| **Autovacuum** | Background worker (default on) |
| **`VACUUM ANALYZE`** | Manual after large deletes |
| **`VACUUM FULL`** | Rewrites table — locks heavily; rare |

Watch **`pg_stat_user_tables`** (`n_dead_tup`, last autovacuum) if tables grow without reason.

## 6. ヘルスチェック

```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

SELECT schemaname, relname, seq_scan, idx_scan
FROM pg_stat_user_tables
ORDER BY seq_scan DESC
LIMIT 10;
```

| Signal | Action |
|--------|--------|
| Connection count near **`max_connections`** | Reduce pool size or add PgBouncer |
| High **`seq_scan`** on large tables | Review queries and indexes |
| Disk growth | Bloat, WAL, logs — investigate per directory |
| Replication lag | Scale replica, fix slow queries on primary |

## 7. PgBouncer (接続多重化)

多くのアプリ インスタンスがそれぞれプールを保持する場合:

```text
Apps (many pools)  →  PgBouncer  →  Postgres (fewer real connections)
```

**トランザクション プーリング** モードは慎重に使用してください。構成されていない場合、セッション機能 (準備されたステートメント、一時テーブル) が機能しなくなる可能性があります。

## 8. 生産前のチェックリスト

- [ ] アプリは最小権限の DB ロールを使用します
- [ ] デプロイパイプラインで自動化された移行
- [ ] スケジュールされたバックアップ + テスト済みの復元
- [ ] 接続制限のサイズ (アプリ × プール + 管理者)
- [ ] 低速クエリ ログまたは APM が有効になっています
- [ ] env / vault のシークレット — git にはありません

## 関連メモ

- [Relational (SQL)](../../CS101/databases/ii-relational.md) — SQL and transaction theory
- [Database optimizations](vii-database-optimizations.md) — full tuning workflow and checklist
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — scaling reads, caching, sharding
- [JPA & transactional](../java/springboot/v-jpa-and-transactional.md) — ORM transaction boundaries
