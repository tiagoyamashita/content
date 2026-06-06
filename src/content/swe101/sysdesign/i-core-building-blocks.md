---
label: "I"
subtitle: "Core Building Blocks"
group: "System design"
order: 1
---
System Design — Part I: Core Building Blocks
Estimation, caching, databases, replication, consistency.

## 1. How to approach any design question
A repeatable framework for interviews and real projects:

Step 1 — Clarify requirements (5 min):
- Functional: what does the system do? (core features, non-goals)
- Non-functional: scale, latency SLA, availability, consistency.
- Constraints: budget, team size, timeline.

Step 2 — Estimate scale (3 min):
- DAU (daily active users), read/write ratio, data size/year.
- Derive QPS (queries per second) and storage needs.

Step 3 — High-level design (10 min):
- Sketch the major components: client, API gateway, services, DB, cache, CDN.
- Show request flow for the most important use cases.

Step 4 — Deep dive (15 min):
- Pick the hardest or most interesting components.
- Discuss data models, API contracts, failure modes.

Step 5 — Identify bottlenecks & trade-offs:
- Single points of failure, hot spots, consistency vs availability choices.
- What would break at 10× scale? How would you fix it?

## 2. Capacity estimation
Back-of-envelope numbers every engineer should know:

Latency (approximate):
- L1 cache hit:          ~1 ns
- RAM access:            ~100 ns
- SSD random read:       ~100 µs
- Network round-trip (same DC): ~500 µs
- Network round-trip (cross-continent): ~150 ms
- HDD seek:              ~10 ms

Storage units:
- 1 KB = 10³ B, 1 MB = 10⁶ B, 1 GB = 10⁹ B, 1 TB = 10¹² B.

Traffic estimation example (Twitter-like):
- 300 M DAU, 10% post per day → 30 M writes/day
= 30 M / 86 400 s ≈ 350 writes/s
- Read:write ratio = 100:1 → 35 000 reads/s
- Tweet ~280 chars = ~500 B → 30 M × 500 B = 15 GB/day writes

Rule of thumb: always sanity-check by converting DAU → QPS.

## 3. DNS & load balancing
DNS resolves domain → IP. TTL controls caching in resolvers.
- Low TTL (30–60 s) enables fast failover.
- GeoDNS routes users to the nearest data centre.

Load balancer strategies:
- Round-robin:        simple; ignores server load.
- Least connections:  route to server with fewest active connections.
- IP hash:            sticky sessions — same client always hits same server.
- Weighted:           send more traffic to beefier servers.

Layer 4 vs Layer 7 (recap from Networking):
- L4 (TCP): fast, blind to content. AWS NLB.
- L7 (HTTP): path/header routing, SSL termination, WAF. AWS ALB.

Health checks: LB polls each backend; removes unhealthy instances automatically.
Horizontal scaling: add more backend instances behind the LB — scale out freely.

## 4. Caching strategies
Cache = fast in-memory store to avoid expensive repeated computation or DB reads.

Where to cache:
- Client-side:   browser cache, service worker.
- CDN edge:      static assets, cacheable API responses.
- Application:   in-process (dict/LRU) for per-instance hot data.
- Distributed:   Redis / Memcached — shared across all app instances.
- Database:      query result cache, buffer pool.

Cache-aside (lazy loading) — most common pattern:
1. App checks cache → hit: return. Miss: read from DB.
2. Write result to cache with TTL. Return to caller.
+ Cache only contains actually-requested data.
− First request after miss is slow; thundering herd on cold start.

Write-through:
Write to cache AND DB synchronously.
+ Cache always consistent. − Write latency doubles; cache polluted by cold data.

Write-behind (write-back):
Write to cache immediately; flush to DB asynchronously.
+ Low write latency. − Risk of data loss on crash.

Cache eviction policies:
- LRU (Least Recently Used):  evict the item unused for the longest time.
- LFU (Least Frequently Used): evict the item with the fewest accesses.
- TTL-based: evict after fixed time regardless of access pattern.

## 5. Databases: SQL vs NoSQL
Relational (SQL):
- Tables, rows, foreign keys, ACID transactions.
- Flexible queries via JOINs; schema enforced.
- Use when: complex relationships, strong consistency, ad-hoc queries.
- PostgreSQL, MySQL, CockroachDB.

NoSQL — four main families:
- Key-value:    Redis, DynamoDB — O(1) get/set; simple queries only.
- Document:     MongoDB, Firestore — JSON docs; flexible schema.
- Wide-column:  Cassandra, HBase — row key + columns; huge write throughput.
- Graph:        Neo4j — vertices + edges; social graphs, recommendations.

Choosing the right store:
- Need JOINs & transactions?          → SQL.
- Sub-millisecond key lookups?         → Redis.
- Flexible schema, document-oriented?  → MongoDB.
- Time-series / append-heavy at scale? → Cassandra.
- Relationship traversal?              → Graph DB.
- Most real systems use multiple stores (polyglot persistence).

## 6. Replication & sharding
Replication — copy data to multiple nodes:
- Primary-replica: primary handles writes; replicas serve reads.
– Read scale-out; replica lag can cause stale reads.
- Multi-primary: multiple nodes accept writes → conflict resolution needed.
- Synchronous replication: write ack only after replica confirms → no data loss, higher latency.
- Asynchronous replication: write ack immediately → lower latency, possible data loss on crash.

Sharding (horizontal partitioning) — split data across nodes:
- Range-based:  shard by key range (e.g. user_id 0–1M on shard 1).
− Hot shards if data isn't evenly distributed.
- Hash-based:   shard = hash(key) % N → even distribution.
− Range queries span all shards.
- Directory-based: lookup table maps key → shard.
− Flexible re-sharding; lookup table is a bottleneck.

Consistent hashing:
- Place nodes and keys on a hash ring.
- Key routed to the nearest node clockwise.
- Adding/removing a node only remaps keys from one neighbour — minimal reshuffling.
- Used in: DynamoDB, Cassandra, Memcached clusters.

## 7. CAP theorem & consistency
CAP theorem: a distributed system can guarantee at most two of:
- Consistency (C):  every read returns the most recent write.
- Availability (A): every request receives a (non-error) response.
- Partition tolerance (P): system works despite network splits.

In practice: network partitions happen → choose CP or AP:
- CP: reject requests when partitioned rather than serve stale data.
Examples: HBase, Zookeeper, etcd.
- AP: serve possibly stale data; reconcile after partition heals.
Examples: Cassandra, CouchDB, DynamoDB (eventual consistency default).

Consistency models (weakest → strongest):
- Eventual: all replicas converge given no new writes. (DNS, shopping cart)
- Read-your-writes: a client always sees its own writes.
- Monotonic read: once you read a value, you never see an older one.
- Strong (linearisability): reads always reflect the latest write globally.

PACELC extension: even without partitions, there is a latency vs consistency
trade-off — low latency requires async replication → weaker consistency.

## 8. Remember & rehearse
- Walk through the 5-step approach for designing a URL shortener.
- Estimate QPS for a service with 100 M DAU and 5 actions/user/day.
- What is the difference between cache-aside and write-through?
- When would you choose NoSQL over SQL? Name a specific example.
- Explain consistent hashing. Why is it preferred over hash(key) % N?
- What does CAP theorem say? Which guarantee do you drop in practice?
- What is replication lag and how can it affect user experience?
