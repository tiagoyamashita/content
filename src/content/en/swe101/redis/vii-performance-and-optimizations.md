---
label: "VII"
subtitle: "Performance & optimizations"
group: "Redis"
order: 7
---
Redis — performance & optimizations
Redis is already fast — optimizations focus on **fewer round trips**, **right-sized values**, **memory**, and **avoiding hot keys**. Patterns are in [Patterns & use cases](iv-patterns-and-use-cases.md); SQL-side tuning in [Database optimizations (Postgres)](../postgres/vii-database-optimizations.md).

## 1. Optimization workflow

```text
1. Measure latency     (app metrics, Redis SLOWLOG, latency doctor)
2. Count round trips   (one request → how many commands?)
3. Shrink values       (compression, hash vs JSON blob)
4. Fix hot keys        (shard, local cache, read replicas)
5. Tune memory/eviction
6. Re-measure under load
```

```text
SLOWLOG GET 10
LATENCY DOCTOR
INFO stats    # keyspace hits/misses if tracked
```

## 2. Round trips dominate

Each command pays network RTT unless pipelined:

| Anti-pattern | Fix |
|--------------|-----|
| Loop of `GET` in app | **`MGET`** or pipeline |
| Loop of `SET` | **`MSET`** or pipeline |
| N sequential awaits | Batch with pipeline / transaction |

```text
MGET cache:product:1 cache:product:2 cache:product:3
```

Spring: **`RedisTemplate.executePipelined`**. Python: **`pipeline()`**.

Target **one pipeline per request** for bulk cache reads, not hundreds of sequential calls.

## 3. Memory optimization

| Technique | Detail |
|-----------|--------|
| **Shorter keys** | `c:p:8812` vs 200-char key — adds up at millions of keys |
| **Hash for objects** | Often more memory-efficient than JSON string for small objects |
| **TTL everywhere** | Cache keys must expire — prevent unbounded growth |
| **Compress large values** | Snappy/LZ4 in app before `SET` — CPU vs RAM trade-off |
| **`UNLINK` vs `DEL`** | Async free for large values (non-blocking) |

Inspect big keys (dev/staging):

```text
redis-cli --bigkeys
MEMORY USAGE cache:product:8812
```

## 4. Hot key problem

One key (viral product, global counter) saturates single Redis core in Cluster:

| Mitigation | Idea |
|------------|------|
| **Local in-process cache** | Caffeine/Guava in front of Redis for hottest keys |
| **Split counter** | `INCR views:8812:shard0` … `shardN` — sum in app |
| **Read replicas** | Spread GET load — accept lag |
| **Precompute** | Background job writes materialized cache key |

## 5. Cache hit rate

Track in application:

```text
hit_rate = cache_hits / (cache_hits + cache_misses)
```

| Low hit rate cause | Fix |
|--------------------|-----|
| TTL too short | Increase if staleness OK |
| Key per random id | Cache only hot entities |
| Invalidation too aggressive | Invalidate specific keys, not `FLUSHDB` |
| Wrong layer | Don't cache one-off queries |

## 6. Commands to use carefully

| Command | Risk |
|---------|------|
| **`KEYS pattern`** | O(N) — blocks — use **`SCAN`** |
| **`FLUSHALL` / `FLUSHDB`** | Production outage |
| **`MONITOR`** | Slows server |
| **`SMEMBERS` huge set** | Large response — paginate with **`SSCAN`** |
| **`LRANGE` huge list** | Same — use ranges |

## 7. Cluster and hash tags

Multi-key ops require same slot in Cluster:

```text
{user:42}:profile
{user:42}:sessions
```

Curly braces **`{user:42}`** force same hash slot — only when you need atomic multi-key ops.

## 8. When Redis is not the bottleneck

If DB queries dominate:

- Optimize [Postgres](../postgres/vii-database-optimizations.md) or [MongoDB](../mongodb/vii-database-optimizations.md) first.
- Add cache **after** measuring — premature cache adds invalidation bugs.

## 9. Checklist

- [ ] Pipelines / `MGET` for bulk reads
- [ ] TTL on all cache keys
- [ ] **`maxmemory`** + eviction policy set
- [ ] No `KEYS` in production code
- [ ] Slow log monitored
- [ ] Hot keys identified under load test
- [ ] Fallback path when Redis unavailable (degrade to DB)
- [ ] Sessions/cache recovery plan documented ([Operations](vi-operations-and-persistence.md))

## Related notes

- [Key-value stores](../../CS101/databases/iii-key-value.md) — conceptual patterns
- [Patterns & use cases](iv-patterns-and-use-cases.md) — cache-aside, rate limits
- [Database optimizations (MongoDB)](../mongodb/vii-database-optimizations.md) — document store tuning
