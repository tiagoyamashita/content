---
label: "VI"
subtitle: "Operations & backups"
group: "MongoDB"
order: 6
---
MongoDB — operations & backups
Production MongoDB runs as a **replica set** (minimum three members for fault tolerance) or **Atlas** (managed). Plan **backups**, **monitoring**, and **restore tests** before you need them.

## 1. Deployment shapes

| Shape | Use |
|-------|-----|
| **Standalone** | Local dev only |
| **Replica set** | Production HA, transactions, oplog |
| **Sharded cluster** | Data or throughput beyond one replica set |
| **Atlas** | Managed replica set / sharded cluster |

```text
Replica set (conceptual)
  Primary  ──replication──►  Secondary 1
       │                           │
       └──────────replication──────►  Secondary 2
```

Writes go to **primary**; secondaries replicate the **oplog**. Reads from secondaries may lag.

## 2. Roles and auth

```javascript
use myapp_dev
db.createUser({
  user: "app_rw",
  pwd: "…",
  roles: [{ role: "readWrite", db: "myapp_dev" }]
})

db.createUser({
  user: "app_ro",
  pwd: "…",
  roles: [{ role: "read", db: "myapp_dev" }]
})
```

| Role | Scope |
|------|-------|
| **`read` / `readWrite`** | Database-level app access |
| **`dbAdmin`** | Indexes, stats — migration job only |
| **`clusterAdmin`** | Break-glass ops — not for apps |

Atlas IAM + database users replace manual setup on cloud.

## 3. Backup with `mongodump` / `mongorestore`

Logical backup (BSON + metadata):

```bash
mongodump --uri="mongodb://localhost:27017/myapp_dev" --out=./backup-2026-05-19

mongorestore --uri="mongodb://localhost:27017/myapp_dev_restored" ./backup-2026-05-19/myapp_dev
```

| Method | Pros | Cons |
|--------|------|------|
| **`mongodump`** | Portable, collection-level | Large datasets slower than snapshots |
| **Atlas continuous backup** | Point-in-time restore | Vendor-specific |
| **Volume snapshot** | Fast at scale | Must coordinate with filesystem snapshot API |

**Test restores** on a schedule — untested backups fail when it matters.

## 4. Monitoring signals

| Signal | Action |
|--------|--------|
| **Replication lag** | Secondary falls behind — check load, network, index builds |
| **Opcounters / QPS** | Capacity planning |
| **Slow query log** | Enable `operationProfiling` or Atlas Performance Advisor |
| **Disk usage** | TTL, archival, compaction (WiredTiger) |
| **Connections** | Pool sizing — too many clients |

Atlas: **Metrics**, **Alerts**, **Performance Advisor** (index suggestions).

## 5. Index builds in production

Large index creation blocks writes on older versions; prefer:

```javascript
db.products.createIndex({ sku: 1 }, { background: true })  // legacy option; behavior varies by version
```

On recent MongoDB, index builds are more concurrent — still schedule heavy builds off-peak. Verify with staging data volume.

## 6. Sharding (awareness)

When a single replica set maxes CPU/RAM/disk:

- Choose a **shard key** with high cardinality and even distribution — **hard to change later**.
- Bad key: monotonic `_id` only on one shard → hot shard.
- Good key: compound including tenant id + time, or hashed `_id`.

Most apps start **unsharded** until metrics prove the need.

## 7. Checklist before production

- [ ] **Replica set** or Atlas (not standalone)
- [ ] Auth enabled; app uses least-privilege user
- [ ] Backups + documented restore runbook
- [ ] Indexes for production query patterns
- [ ] Connection pools sized across all app instances
- [ ] Alerts on disk, replication lag, primary failover

## Related notes

- [Database optimizations](vii-database-optimizations.md) — slow query triage
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — caching, read scaling
- [Postgres operations](../postgres/vi-operations-and-backups.md) — parallel ops mindset for polyglot stacks
