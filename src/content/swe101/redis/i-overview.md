---
label: "I"
subtitle: "概要"
group: "Redis"
order: 1
---
Redis — 概要


**Redis** is an **in-memory data store** with optional persistence. It excels at **low-latency key access**, **TTL-based expiry**, and **atomic primitives** — cache, sessions, rate limits, pub/sub, and lightweight queues. It is usually **not** your system of record; pair it with [Postgres](../postgres/i-overview.md) or [MongoDB](../mongodb/i-overview.md).

For key-value concepts (cache-aside, sessions, when not to use KV alone), see [Key-value stores](../../CS101/databases/iii-key-value.md).

## このトラックの地図

|パート |フォーカス |
|------|----------|
| **I — 概要** |スタック内の役割、語彙、Redis をいつ使用するか |
| **II — インストールと redis-cli** | Docker、接続 URI、シェルの基本 |
| **III — データ構造とキー** |文字列、ハッシュ、セット、TTL、命名 |
| **IV — パターンと使用例** |キャッシュアサイド、セッション、レート制限、パブリッシュ/サブスクライブ |
| **V — アプリの統合** |レタス、Spring データ Redis、redis-py |
| **VI — 操作と永続性** | RDB、AOF、レプリケーション、メモリ制限 |
| **VII — パフォーマンスと最適化** |パイプライン、メモリ、ホットキー、チェックリスト |

## Redis を使用する理由 (アプリの場合)

| Strength | What it means in practice |
|----------|---------------------------|
| **Sub-ms reads/writes** | Hot data in RAM — offload Postgres/MongoDB |
| **TTL built in** | Sessions and cache entries expire automatically |
| **Atomic ops** | `INCR`, `SET NX`, lists — no read-modify-write races |
| **Rich types** | Not only strings — hashes, sorted sets, streams |
| **Simple ops model** | Easy to reason about vs full document/SQL query |

## 主要な語彙

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

## Redis が適合する場合

| Good fit | Poor default |
|----------|--------------|
| Cache in front of SQL/document DB | Primary store for orders/ledger |
| Session store for stateless web tier | Full-text search at scale (use OpenSearch/ES) |
| Rate limiting, feature flags | Complex relational reporting |
| Leaderboards (`sorted set`) | Large values (>512 MB per key — design mistake) |
| Pub/sub, Streams (light queues) | Durable heavy job queue alone (often add Kafka/SQS) |

**ルール:** Postgres/MongoDB は真実を保持します。 Redis は加速または調整します。

## メモリと耐久性 (プレビュー)

- Data lives in **RAM** — plan capacity and **maxmemory** policy.
- **RDB** snapshots and **AOF** append log trade durability vs speed — see [Operations & persistence](vi-operations-and-persistence.md).
- Treat cache as ** disposable** — always be able to rebuild from the database.

＃＃ 次

Continue with [Install & redis-cli](ii-install-and-redis-cli.md) to run Redis locally and try commands.
