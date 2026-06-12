---
label: "I"
subtitle: "Overview"
group: "Redis"
order: 1
---
Redis — overview
**Redis** is an **in-memory data store** with optional persistence. It excels at **low-latency key access**, **TTL-based expiry**, and **atomic primitives** — cache, sessions, rate limits, pub/sub, and lightweight queues. It is usually **not** your system of record; pair it with [Postgres](../postgres/i-overview.md) or [MongoDB](../mongodb/i-overview.md).

For key-value concepts (cache-aside, sessions, when not to use KV alone), see [Key-value stores](../../CS101/databases/iii-key-value.md).

## Map of this track

| Part | Focus |
|------|--------|
| **I — Overview** | Role in the stack, vocabulary, when to use Redis |
| **II — Install & redis-cli** | Docker, connection URI, shell basics |
| **III — Data structures & keys** | Strings, hashes, sets, TTL, naming |
| **IV — Patterns & use cases** | Cache-aside, sessions, rate limits, pub/sub |
| **V — App integration** | Lettuce, Spring Data Redis, redis-py |
| **VI — Operations & persistence** | RDB, AOF, replication, memory limits |
| **VII — Performance & optimizations** | Pipelines, memory, hot keys, checklist |
| **VIII — Shared sessions across apps** | Subdomain cookies + Redis; SSO when domains differ |

## Why Redis (for apps)

| Strength | What it means in practice |
|----------|---------------------------|
| **Sub-ms reads/writes** | Hot data in RAM — offload Postgres/MongoDB |
| **TTL built in** | Sessions and cache entries expire automatically |
| **Atomic ops** | `INCR`, `SET NX`, lists — no read-modify-write races |
| **Rich types** | Not only strings — hashes, sorted sets, streams |
| **Simple ops model** | Easy to reason about vs full document/SQL query |

## Core vocabulary

```text
Redis server
  └── Logical DB 0..N (default 0)
        └── Key  →  Value (string, hash, list, set, …)
```

| Term | Role |
|------|------|
| **Key** | String identifier — you design naming (`user:42:session`) |
| **Value** | Bytes interpreted by your app (or Redis type) |
| **TTL / EXPIRE** | Key auto-deletes after seconds |
| **Eviction** | When memory full, policy drops keys (e.g. `allkeys-lru`) |
| **Replica** | Read copy + failover target |
| **Cluster** | Sharded keys across nodes (hash slots) |

## When Redis fits

| Good fit | Poor default |
|----------|--------------|
| Cache in front of SQL/document DB | Primary store for orders/ledger |
| Session store for stateless web tier | Full-text search at scale (use OpenSearch/ES) |
| Rate limiting, feature flags | Complex relational reporting |
| Leaderboards (`sorted set`) | Large values (>512 MB per key — design mistake) |
| Pub/sub, Streams (light queues) | Durable heavy job queue alone (often add [Kafka](../kafka/i-overview.md)/SQS) |

**Rule:** Postgres/MongoDB holds truth; Redis accelerates or coordinates.

## Memory and durability (preview)

- Data lives in **RAM** — plan capacity and **maxmemory** policy.
- **RDB** snapshots and **AOF** append log trade durability vs speed — see [Operations & persistence](vi-operations-and-persistence.md).
- Treat cache as ** disposable** — always be able to rebuild from the database.

## Next

Continue with [Install & redis-cli](ii-install-and-redis-cli.md) to run Redis locally and try commands.
