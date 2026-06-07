---
label: "IV"
subtitle: "Patterns & use cases"
group: "Redis"
order: 4
---
Redis — patterns & use cases
Production Redis usage centers on a few **repeatable patterns**. Each assumes a durable store ([Postgres](../postgres/i-overview.md), [MongoDB](../mongodb/i-overview.md)) holds source of truth unless noted.

## 1. Cache-aside

```text
READ:
  1. GET cache:key
  2. hit  → return
  3. miss → load from DB → SET cache:key EX ttl → return

WRITE:
  1. UPDATE database
  2. DEL cache:key   (or SET new value)
```

```text
GET cache:product:8812
# miss
SET cache:product:8812 "{...json...}" EX 600
```

| Pitfall | Fix |
|---------|-----|
| **Stale cache** | Invalidate on write; or short TTL + accept staleness |
| **Thundering herd** | Lock key `SET lock:… NX EX` while one worker rebuilds |
| **Caching null** | Cache short “not found” to protect DB |

Define **TTL** by freshness needs — product catalog 10m, user profile 1m, config 5s.

## 2. Session store

Web app stores **session id** in cookie; server stores blob in Redis:

```text
SET session:sess_abc123 "{\"userId\":42,\"roles\":[\"user\"]}" EX 86400
GET session:sess_abc123
DEL session:sess_abc123    # logout
```

Benefits: **horizontal scale** without sticky sessions; instant logout via **DEL**.

Spring Session Redis and similar libraries handle serialization and cookie wiring — see [App integration](v-app-integration.md).

## 3. Rate limiting

**Fixed window** — simple:

```text
INCR ratelimit:api:10.0.0.1:2026051914
EXPIRE ratelimit:api:10.0.0.1:2026051914 60
# if count > 100 → 429 Too Many Requests
```

**Sliding window** — use **sorted set** with timestamps as scores, trim old entries, count members — more accurate, more complex.

For API gateways, consider dedicated limiter (Kong, Envoy) — Redis still common at app layer.

## 4. Distributed lock (careful)

```text
SET lock:import:20260519 worker-7 NX EX 30
# do work
DEL lock:import:20260519   # only if value matches (use Lua script)
```

| Risk | Mitigation |
|------|------------|
| **Lock expires before work done** | Extend TTL with watchdog; keep tasks short |
| **Unlock wrong holder** | Compare token in value; use Redisson-style libraries |
| **Split brain** | Redlock is debated — prefer DB constraints or queue with single consumer when possible |

Use locks sparingly — **idempotent** jobs and **unique constraints** in Postgres often beat distributed locks.

## 5. Pub/sub

Fire-and-forget broadcast — not durable:

```text
SUBSCRIBE notifications
PUBLISH notifications "{\"type\":\"deploy\",\"env\":\"staging\"}"
```

Subscribers must be online; messages not replayed. For durable fan-out use **Streams**, Kafka, or SQS.

## 6. Streams (lightweight queue)

```text
XADD jobs * type email to ada@example.com
XREAD COUNT 10 BLOCK 5000 STREAMS jobs 0
XGROUP CREATE jobs workers $ MKSTREAM
XREADGROUP GROUP workers consumer1 COUNT 1 STREAMS jobs >
XACK jobs workers <message-id>
```

Consumer groups give **at-least-once** delivery with ack — good for moderate job volume; monitor pending list length.

## 7. Feature flags and config

```text
HSET config:flags dark_mode on beta_checkout off
HGET config:flags dark_mode
```

Pub/sub **`CONFIG`** channel to notify apps to refresh — or poll with short TTL cache in app memory.

## 8. What not to put in Redis

| Avoid | Use instead |
|-------|-------------|
| Sole copy of financial records | Postgres + audit log |
| Large blobs (> few MB) | Object storage (S3) |
| Complex queries across entities | SQL / MongoDB |
| Long-term analytics | Warehouse |

## Next

Continue with [App integration](v-app-integration.md) for Lettuce, Spring Data Redis, and redis-py.
