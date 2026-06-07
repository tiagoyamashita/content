---
label: "VI"
subtitle: "Operations & persistence"
group: "Redis"
order: 6
---
Redis — operations & persistence
Redis is fast because data is **in memory** — plan **memory limits**, **persistence**, and **high availability** before production traffic.

## 1. Memory management

```text
INFO memory
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
```

| Policy | Behavior when `maxmemory` reached |
|--------|-----------------------------------|
| **`noeviction`** | Writes fail — safe if Redis is required store |
| **`allkeys-lru`** | Evict any key — typical **cache** |
| **`volatile-lru`** | Evict keys with TTL only |
| **`allkeys-lfu`** | Evict least frequently used (Redis 4+) |

Set **`maxmemory`** below host RAM — leave headroom for OS and replication buffers.

## 2. RDB (snapshots)

Point-in-time binary snapshot:

```conf
# redis.conf
save 900 1      # if 1 key changed in 900 sec
save 300 10
save 60 10000
dbfilename dump.rdb
dir /data
```

| Pros | Cons |
|------|------|
| Compact backup file | Between snapshots, recent writes can be lost |
| Fast restarts | `SAVE` blocks; `BGSAVE` forks (copy-on-write memory spike) |

Copy **`dump.rdb`** for cold backup when traffic is low or after **`BGSAVE`**.

## 3. AOF (append-only file)

Logs every write — more durable:

```conf
appendonly yes
appendfsync everysec   # balance; always | everysec | no
auto-aof-rewrite-percentage 100
```

| `appendfsync` | Trade-off |
|---------------|-----------|
| **`always`** | Safest; slowest |
| **`everysec`** | At most ~1s loss on crash — common default |
| **`no`** | OS buffer — faster, riskier |

Many teams use **both RDB + AOF** on managed Redis (ElastiCache, Redis Cloud).

## 4. Replication

```text
Primary (read/write)  ──stream──►  Replica (read, failover)
```

Configure replica:

```conf
replicaof primary-host 6379
```

| Use | Notes |
|-----|-------|
| **Read scaling** | Route read-only cache GETs to replica — watch replication lag |
| **Failover** | Sentinel or managed failover promotes replica |

**Cache on replica:** stale reads possible — usually acceptable for cache; not for locks without care.

## 5. Sentinel and Cluster (awareness)

| Mode | When |
|------|------|
| **Single instance** | Dev only |
| **Primary + replicas + Sentinel** | HA failover for one shard |
| **Redis Cluster** | Data sharded across nodes — key must hit same slot; multi-key ops need same hash tag `{user:42}:profile` |

Most app caches fit **one primary + replicas** until memory exceeds one machine.

## 6. Security

- **`requirepass`** or **ACL users** — never expose Redis to public internet unauthenticated.
- **TLS** (`rediss://`) on managed services and between AZs when required.
- Disable **`FLUSHALL`**, **`CONFIG`** for app users via ACL.
- Bind **`127.0.0.1`** in dev; VPC security groups in cloud.

## 7. Backup and restore

| Method | Steps |
|--------|--------|
| **RDB file** | Stop or `BGSAVE` → copy `dump.rdb` → restore to new instance data dir |
| **Managed snapshot** | ElastiCache/Redis Cloud automated backups + PITR where offered |
| **Rebuild from DB** | Cache empty → warm from Postgres — valid DR for cache-only data |

**Test restore** — especially if you store sessions in Redis (users logged out on loss).

## 8. Monitoring checklist

- [ ] Memory usage vs **`maxmemory`**
- [ ] Evicted keys per second (`INFO stats`)
- [ ] Connected clients vs **`maxclients`**
- [ ] Replication lag (`INFO replication`)
- [ ] Slow log (`SLOWLOG GET 10`)
- [ ] Hit rate for cache (app metric: hits / (hits + misses))

## Related notes

- [Performance & optimizations](vii-performance-and-optimizations.md) — pipelines, hot keys
- [Database bottlenecks](../sysdesign/bottleneck-analysis/vi-database.md) — cache in system design
- [Postgres operations](../postgres/vi-operations-and-backups.md) — source-of-truth backup mindset
