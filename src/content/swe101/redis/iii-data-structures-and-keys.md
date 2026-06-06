---
label: "III"
subtitle: "Data structures & keys"
group: "Redis"
order: 3
---
Redis — data structures & keys
Redis values are not only strings — pick the **type** that matches your access pattern. **Key design** and **TTL** matter as much as in [Key-value stores](../../CS101/databases/iii-key-value.md).

## 1. Key naming

Use a **namespace** prefix — readable, grep-friendly in logs:

```text
cache:product:8812
session:sess_abc123
ratelimit:api:192.168.1.1:2026051914
user:42:profile
```

| Convention | Example |
|------------|---------|
| **`:` separator** | Hierarchy without nested folders |
| **Stable ids** | `user:42`, not `user:ada` if email changes |
| **Version suffix** | `cache:product:v2:8812` when cache shape changes |

Avoid one giant keyspace with ambiguous names (`data`, `temp`, `x`).

## 2. Strings

Default type — JSON blobs, counters, flags:

```text
SET feature:dark_mode "on"
GET feature:dark_mode

SET page:home HTML_EX 300
INCR stats:pageviews:home
INCRBY stats:bytes:served 4096
```

**`SET` options:**

| Option | Meaning |
|--------|---------|
| **`EX seconds`** | TTL |
| **`NX`** | Set only if key missing (lock, dedupe) |
| **`XX`** | Set only if key exists |

```text
SET lock:job:import worker-1 NX EX 30
```

## 3. Hashes

Field map under one key — compact user/session objects:

```text
HSET user:42 name Ada email ada@example.com plan pro
HGET user:42 email
HGETALL user:42
HMGET user:42 name email
HINCRBY cart:42 item_count 1
```

Prefer **hash** over JSON string when you update individual fields without parsing whole blob.

## 4. Lists

Linked list — queues, recent items (bounded):

```text
LPUSH events:recent "login" "purchase"
LRANGE events:recent 0 9
LTRIM events:recent 0 99    # keep last 100
```

**`BLPOP`** — blocking pop for simple worker queues (consider **Streams** for consumer groups).

## 5. Sets and sorted sets

**Set** — unique members, tags, presence:

```text
SADD online:users 42 99 101
SISMEMBER online:users 42
SMEMBERS online:users
```

**Sorted set (ZSET)** — score + member — leaderboards, time-ordered ranks:

```text
ZADD leaderboard 9850 "player:ada"
ZADD leaderboard 9200 "player:grace"
ZREVRANGE leaderboard 0 9 WITHSCORES
ZRANK leaderboard "player:ada"
```

| Type | Use |
|------|-----|
| **Set** | Unique tags, mutual followers (with care) |
| **ZSET** | Rankings, delayed jobs by timestamp score |

## 6. TTL and expiry

```text
SET session:tok EX 3600
EXPIRE cache:product:1 300
PERSIST session:tok          # remove TTL
TTL session:tok              # seconds remaining; -1 no TTL; -2 missing
```

**Lazy + periodic** expiry — do not rely on exact second of deletion for correctness; design keys to be safe if they linger briefly.

## 7. Other types (awareness)

| Type | Use |
|------|-----|
| **Stream** | Log, consumer groups — see [Patterns & use cases](iv-patterns-and-use-cases.md) |
| **HyperLogLog** | Approx unique counts |
| **Bitmap** | Feature flags per user id, daily active bits |
| **GEO** | Location radius queries |

## 8. Serialization

Store **JSON** in strings when the app already speaks JSON:

```text
SET cache:product:8812 "{\"title\":\"Keyboard\",\"price\":129.99}"
```

Use **hash** for partial updates; **MessagePack** if size matters — always document encoding in your service layer.

## Next

Continue with [Patterns & use cases](iv-patterns-and-use-cases.md) for cache-aside, sessions, and rate limiting.
