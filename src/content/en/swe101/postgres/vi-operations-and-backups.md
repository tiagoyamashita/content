---
label: "VI"
subtitle: "Operations & backups"
group: "Postgres"
order: 6
---
Postgres — operations & backups
Production Postgres needs **role separation**, **regular backups**, and a plan for **restore** and **failover**. You do not need to be a DBA on day one — but you should know these defaults.

## 1. Roles and permissions

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

Logical backup — portable SQL or custom format:

```bash
# Plain SQL (human-readable, slower restore)
pg_dump -h localhost -U postgres -d myapp -F p -f myapp-$(date +%F).sql

# Custom format (compressed, parallel restore)
pg_dump -h localhost -U postgres -d myapp -F c -f myapp.dump
```

Restore:

```bash
pg_restore -h localhost -U postgres -d myapp_restored -F c myapp.dump
```

| Method | Pros | Cons |
|--------|------|------|
| **`pg_dump`** | Simple, version-portable | Point-in-time needs WAL archiving too |
| **Volume snapshot** | Fast for huge DBs | Must be crash-consistent or use PG APIs |
| **Managed auto-backup** | PITR, retention policies | Vendor lock-in, cost |

**Test restores** quarterly — an untested backup is a guess.

## 3. Point-in-time recovery (concept)

```text
Base backup (pg_dump or physical)  +  continuous WAL archive  →  restore to any second
```

Managed Postgres (RDS, Cloud SQL, Neon) exposes PITR in the console. Self-hosted needs **`archive_mode`** and WAL shipping configured.

## 4. Replication basics

| Mode | Purpose |
|------|---------|
| **Streaming replication** | Hot standby for failover and read scale |
| **Logical replication** | Selective tables, cross-version upgrades |

Application sees one **primary** for writes; replicas may lag by milliseconds to seconds — design UI accordingly after writes.

## 5. Vacuum and bloat

Postgres uses **MVCC** — `UPDATE`/`DELETE` leave dead rows until **VACUUM** reclaims space.

| Command | Who runs it |
|---------|-------------|
| **Autovacuum** | Background worker (default on) |
| **`VACUUM ANALYZE`** | Manual after large deletes |
| **`VACUUM FULL`** | Rewrites table — locks heavily; rare |

Watch **`pg_stat_user_tables`** (`n_dead_tup`, last autovacuum) if tables grow without reason.

## 6. Health checks

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

## 7. PgBouncer (connection multiplexing)

When many app instances each hold a pool:

```text
Apps (many pools)  →  PgBouncer  →  Postgres (fewer real connections)
```

Use **transaction pooling** mode carefully — session features (prepared statements, temp tables) may break unless configured.

## 8. Checklist before production

- [ ] App uses least-privilege DB role
- [ ] Migrations automated in deploy pipeline
- [ ] Backups scheduled + restore tested
- [ ] Connection limits sized (app × pool + admin)
- [ ] Slow query logging or APM enabled
- [ ] Secrets in env / vault — not in git

## Related notes

- [Relational (SQL)](../../CS101/databases/ii-relational.md) — SQL and transaction theory
- [Database optimizations](vii-database-optimizations.md) — full tuning workflow and checklist
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — scaling reads, caching, sharding
- [JPA & transactional](../java/springboot/v-jpa-and-transactional.md) — ORM transaction boundaries
