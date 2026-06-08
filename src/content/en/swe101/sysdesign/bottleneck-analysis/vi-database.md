---
label: "VI"
subtitle: "Database"
group: "System design"
order: 6
---
Database bottlenecks
The **database** is the most common bottleneck in web systems — reads, writes, locks, and **connection pools**.

## 1. Read bottlenecks

| Problem | Signal | Fix |
|---------|--------|-----|
| Full table scan | `EXPLAIN` → Seq Scan | Index on predicates |
| **N+1 queries** | ORM: 1 + N queries | JOIN, batch `IN`, DataLoader |
| Replica lag | Stale reads on replica | Critical reads → primary; monitor lag |
| Long transactions block reads | Lock waits | Short txs; READ COMMITTED / MVCC |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="N plus 1 query problem vs batched query">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">N+1 vs batch</text>
  <text x="12" y="38" fill="#f87171" font-size="9">1 query parents + N queries children</text>
  <text x="12" y="54" fill="#86efac" font-size="9">1 query parents + 1 WHERE id IN (...)</text>
  <text x="12" y="78" fill="#71717a" font-size="9">ORM lazy load is a common hidden bottleneck</text>
</svg></figure>

## 2. Write bottlenecks

| Problem | Fix |
|---------|-----|
| Single primary ceiling (~10K–50K writes/s Postgres) | Shard; async queue; CQRS |
| Index write amplification | Fewer indexes; partial indexes |
| Deadlocks | Consistent lock order; optimistic locking (CAS) |
| WAL / disk | Faster storage; tune checkpoints |

## 3. Connection pool exhaustion

```text
500 pods × 10 connections = 5 000  →  DB max_connections = 100  →  crash
```

| Fix | Role |
|-----|------|
| **PgBouncer** / **RDS Proxy** | Multiplex many app conns → few DB conns |
| Right-size pool | Rule of thumb: ~(2 × CPU cores) + disk spindles per instance |
| Short queries | Release conn quickly |

## 4. Query optimisation checklist

- [ ] `EXPLAIN (ANALYZE, BUFFERS)` on slow queries
- [ ] Composite index for multi-column WHERE / ORDER BY
- [ ] **Covering index** — index-only scan
- [ ] **Partial index** — `WHERE active = true`
- [ ] Materialised view for heavy aggregates
- [ ] **Partition** by date for prune + archival

## 5. Index added but still slow?

| Check | |
|-------|---|
| Wrong column order in composite index | |
| Function on column (`WHERE LOWER(email)`) — needs expression index | |
| Statistics stale — `ANALYZE` | |
| Row count wrong estimate — increase stats target | |
| Sort spills to disk — work_mem / index for ORDER BY | |
| Lock wait, not query plan | |

## 6. Read vs write scaling paths

| Path | When |
|------|--------|
| Read replicas | Read-heavy; tolerate lag |
| Cache (Redis) | Hot keys, repeated reads |
| Sharding | Write scale exceeds single primary |
| Denormalize | Read path cheaper; write complexity up |

**Related:** [Core building blocks](../i-core-building-blocks.md) (replication), [Database sharding](../scalable-patterns/ix-database-sharding.md), [Application-level](vii-application-level.md) (hot partition).
