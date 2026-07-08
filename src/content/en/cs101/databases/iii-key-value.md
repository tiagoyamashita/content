---
label: "III"
subtitle: "Key-value"
group: "Databases"
order: 3
---
Key-value stores
A **key-value** database maps an opaque **key** (string, bytes) to a **value** (string, bytes, or structured blob). Lookups are usually **O(1)** or near it. There is **no query language** for arbitrary field searches unless the product adds a secondary index layer.

## 1. Data model

```text
key                    value
─────────────────────  ─────────────────────────
session:abc123         { "userId": 42, "cart": [...] }
user:42:profile        "displayName=Ada"
feature:dark_mode      "on"
rate_limit:192.168.1.1 "37"
```

The application **names keys** and **interprets values** — the store does not understand your JSON schema.

## 2. Operations

| Operation | Meaning |
|-----------|---------|
| **GET** / **SET** | Read or write one key |
| **DELETE** | Remove key |
| **INCR** | Atomic integer bump (counters) |
| **EXPIRE / TTL** | Key vanishes after time — ideal for sessions and cache |
| **CAS** | Compare-and-set — write only if value unchanged (optimistic lock) |

Redis example (CLI):

```text
SET session:abc123 "{\"userId\":42}" EX 3600
GET session:abc123
INCR rate_limit:10.0.0.1
EXPIRE rate_limit:10.0.0.1 60
```

## 3. In-memory vs durable

| Style | Behavior | Examples |
|-------|----------|----------|
| **In-memory primary** | Fast; snapshot or AOF for durability | Redis |
| **Disk-backed, distributed** | Partitioned keys across nodes | DynamoDB, Riak |
| **Coordination** | Small keys, strong consistency for locks | etcd, ZooKeeper |

**Redis** is often a **cache** in front of PostgreSQL — not the system of record unless you accept loss on failure and design for it.

## 4. Common patterns

### Cache-aside

```text
1. READ:  app → cache GET key
           miss → DB → SET cache → return
2. WRITE: app → DB commit → DELETE cache key (or update)
```

Stale cache happens if you update DB without invalidating cache — define order in code.

### Session store

Web server stores session id in cookie; **session:{id}** in Redis holds user state — horizontal scaling without sticky sessions.

### Rate limiting

**INCR** key per IP + **EXPIRE** window — simple fixed-window limiter.

### Distributed lock (careful)

**SET key value NX EX ttl** — only one holder; must handle expiry and fencing tokens in production.

## 5. Java sketch (Lettuce / Redis)

```java
// Compile: javac --release 22 …
// Dependency: io.lettuce:lettuce-core (conceptual)
try (var redis = RedisClient.create("redis://localhost:6379").connect()) {
  var commands = redis.sync();
  commands.setex("session:abc", 3600, "{\"userId\":42}");
  String json = commands.get("session:abc");
}
```

Spring Cache with Redis backs **`@Cacheable`** methods — same key-value idea at the framework layer.

## 6. Strengths and limits

**Strengths**

- Extremely **low latency** reads/writes
- **Simple mental model** — one key, one blob
- **TTL** built in
- **Atomic** counters and lists (Redis data structures: hash, set, sorted set)

**Limits**

- No **JOIN** — you design keys to match access paths
- **Memory cost** for pure RAM stores
- **Hot keys** — one popular key saturates a shard
- **Not** a replacement for relational reporting without duplication

## 7. When to choose key-value

- **Cache** layer (HTML fragments, query results, objects)
- **Sessions**, **rate limits**, **feature flags**
- **Leaderboards** (sorted sets in Redis)
- **Pub/sub** and simple queues (with eyes open on durability)

## 8. Examples

| Product | Notes |
|---------|--------|
| **Redis** | Rich types, pub/sub, streams; de facto cache |
| **Amazon DynamoDB** | Managed; partition key + optional sort key |
| **etcd** | Kubernetes config, distributed locks |
| **Memcached** | Simple cache, no persistence focus |

## 9. Related

- **Overview** — [Databases overview](i-overview.md)
- **Relational** — source of truth behind cache [Relational (SQL)](ii-relational.md)
- **Hash table** — same key → slot idea (Data structures submenu)
