---
label: "IV"
subtitle: "Indexes & EXPLAIN"
group: "Postgres"
order: 4
---
Postgres — indexes & EXPLAIN
Slow queries are normal until you **measure**. Use **`EXPLAIN (ANALYZE, BUFFERS)`** to read plans, add the right **indexes**, and avoid common foot-guns.

## 1. How indexes help

Postgres default **B-tree** index supports:

- `WHERE id = 42`
- `WHERE email = 'a@example.com'`
- `WHERE created_at > '2026-01-01'` (range scans)
- `ORDER BY created_at DESC` (when compatible with index order)

Without a matching index, Postgres may **Seq Scan** — read every row in the table. Fine for small tables; costly at millions of rows.

```sql
CREATE INDEX posts_account_created_idx
  ON posts (account_id, created_at DESC);
```

Supports:

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

| Node | Meaning |
|------|---------|
| **Seq Scan** | Full table read — check row count and filters |
| **Index Scan / Index Only Scan** | Uses index; "only scan" skips heap if visibility map allows |
| **Bitmap Index Scan** | Combines multiple index conditions |
| **Nested Loop** | For each row in A, lookup in B — good with index on B |
| **Hash Join / Merge Join** | Join strategies for larger sets |

Focus on:

- **Actual time** (ms) vs **Planning time**
- **Rows** estimate vs **actual** — large mismatch → run **`ANALYZE table`**
- **Buffers: shared hit/read** — high `read` → cache cold or table bigger than memory

## 3. Index types (when B-tree is not enough)

| Index | Use case |
|-------|----------|
| **B-tree** (default) | Equality, range, sorting |
| **GIN** | `JSONB`, arrays, full-text |
| **GiST** | Geometry (PostGIS), nearest-neighbor |
| **Hash** | Rare; equality only, not WAL-safe for all ops |

Partial index — index a subset:

```sql
CREATE INDEX posts_unpublished_idx ON posts (account_id)
  WHERE NOT published;
```

## 4. Create indexes without blocking writes

```sql
CREATE INDEX CONCURRENTLY posts_body_trgm_idx ON posts USING GIN (body gin_trgm_ops);
```

**`CONCURRENTLY`** avoids long write locks but:

- Cannot run inside a transaction block
- Fails leave an **INVALID** index — drop and retry

## 5. Common problems

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Slow `WHERE lower(email) = …` | Function on column | Expression index: `(lower(email))` or store normalized column |
| Slow `LIKE '%foo%'` | Leading wildcard | Full-text / trigram (`pg_trgm`) |
| Plan uses wrong index | Stale stats | `ANALYZE posts;` |
| Index unused | Low selectivity, small table | Seq scan may be correct — measure |
| Too many indexes | Slow writes | Drop unused; composite instead of many singles |

## 6. N+1 queries (application layer)

ORM loops that query one row at a time:

```text
Bad:  SELECT * FROM posts WHERE account_id = $1  (×1000 accounts)
Good: SELECT * FROM posts WHERE account_id = ANY($1)  or JOIN in one query
```

Fix in app code or with **`JOIN FETCH`** (JPA) — indexes alone do not fix N+1.

## 7. Monitoring slow queries

Enable **`log_min_duration_statement`** in dev/staging:

```conf
log_min_duration_statement = 200ms
```

Managed services (RDS, etc.) expose **Performance Insights** or **`pg_stat_statements`** for top queries by total time. For the full tuning workflow, see [Database optimizations](vii-database-optimizations.md).

## Next

Continue with [App integration](v-app-integration.md) for JDBC, pools, and Spring Data JPA against Postgres.
