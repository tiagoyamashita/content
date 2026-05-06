---
label: "IV"
subtitle: "Bottleneck Analysis"
group: "System design"
order: 4
---
System Design — Part IV: Bottleneck Analysis
Find, measure, and eliminate every layer of system bottleneck.

## 1. Identifying bottlenecks
A bottleneck is the single resource whose saturation limits overall throughput.
Little's Law: L = λ × W
L = avg number of requests in the system
λ = avg arrival rate (req/s)
W = avg time a request spends in the system
→ If W rises, L rises even at constant λ — the system is backing up.

Universal Scalability Law (USL) — throughput X(N) with N workers:
X(N) = N / (1 + α(N−1) + βN(N−1))
α = contention penalty (serialisation); β = coherency penalty.
→ Even perfect horizontal scaling is capped by serial fractions (Amdahl).

How to find the bottleneck systematically:
1. Define the metric that is hurting (latency, throughput, error rate).
2. Profile end-to-end: where does request time go? (APM / distributed trace)
3. Look at utilisation of each resource: CPU, memory, disk I/O, network.
4. The resource closest to 100% utilisation is likely the bottleneck.
5. Relieve it — and watch the next bottleneck surface (whack-a-mole).

USE method (Brendan Gregg):
For every resource, check: Utilisation, Saturation, Errors.
- Utilisation > 70% sustained → approaching saturation.
- Saturation: queue length / wait time non-zero → work is piling up.
- Errors: retries, timeouts, dropped packets → hard failures.

RED method (for services):
Rate (req/s), Errors (error/s), Duration (latency distribution).
→ Combine USE (infrastructure) + RED (service) for full picture.

## 2. CPU & memory bottlenecks
CPU bottleneck signals:
- CPU utilisation sustained > 80% on all cores.
- High run-queue length (vmstat r > # of CPUs).
- Latency scales linearly with load (no slack headroom).

Causes & fixes:
- Inefficient algorithms: O(n²) where O(n log n) exists.
Fix: profile with pprof / perf / py-spy; optimise hot paths.
- Serialised work: GIL (Python), global locks.
Fix: use async I/O, worker pools, language runtimes without GIL.
- JSON (de)serialisation at high rate: surprisingly CPU-heavy.
Fix: protobuf / msgpack; cache parsed results.
- Too many goroutines / threads: context-switch overhead.
Fix: bounded worker pool; async I/O instead of thread-per-request.

Memory bottleneck signals:
- OOM kills; swap usage > 0 (swap = slow disk acting as RAM).
- GC pause spikes (JVM, Go GC stop-the-world).
- High cache eviction rate (Redis evicted_keys rising).

Causes & fixes:
- Memory leak: allocations never freed. Fix: heap profiler; fix lifecycle.
- Over-caching: cache too much data. Fix: eviction policy tuning; TTLs.
- Large object copies: Fix: pass pointers / use streaming instead of buffering.
- GC pressure: Fix: reduce allocation rate; pool objects; tune GC flags.

## 3. I/O & storage bottlenecks
Disk I/O bottleneck signals:
- iowait % high (CPU sitting idle waiting for disk).
- Disk throughput at device limit (iostat %util → 100%).
- High read/write latency on SSD (> 1 ms random read is a warning sign).

Causes & fixes:
- Random small reads: Fix: sequential access patterns; read-ahead; index scans.
- Logging to disk synchronously: Fix: async log writes; use log aggregator.
- Missing DB index → full table scans: Fix: add index on query predicates.
- Too many small writes (fsync per write): Fix: batch writes; WAL tuning.
- Storage tier mismatch: spinning HDD under a latency-sensitive workload.
Fix: migrate to NVMe SSD; use io_uring for async I/O.

Object storage bottleneck:
- S3 prefix hot-spot: many requests to the same key prefix → throttling.
Fix: randomise key prefix (S3 now auto-partitions, but prefix diversity helps).
- Large object uploads: Fix: multipart upload (parallelise 5 MB–5 GB parts).

## 4. Network bottlenecks
Signals:
- NIC bandwidth saturated (sar -n DEV → rxkB/s near max).
- High TCP retransmit rate (ss --statistics).
- Latency spikes between services (cross-AZ, cross-region).
- Connection exhaustion: ephemeral port range used up (source port reuse).

Causes & fixes:
- Chatty protocol: many small round-trips.
Fix: batch requests; use streaming (gRPC); pipelining.
- Large uncompressed payloads:
Fix: gzip/Brotli compression; binary encoding (protobuf).
- Too many short-lived connections: TCP 3-way handshake overhead.
Fix: connection pooling; HTTP/2 multiplexing; keep-alive.
- Head-of-line blocking (HTTP/1.1):
Fix: HTTP/2 (multiplexed streams); HTTP/3 (QUIC — no TCP HOL blocking).
- Cross-region latency (physics — speed of light):
Fix: CDN edge caching; multi-region deployment; edge compute.
- Service mesh overhead: every request through sidecar proxy adds ~1 ms.
Fix: keep mesh for critical paths; bypass for ultra-low-latency internals.

## 5. Database bottlenecks
The database is the most common bottleneck in web systems.

Read bottlenecks:
- Full table scan: EXPLAIN shows Seq Scan → add index.
- N+1 queries: ORM fetches 1 parent + N children separately.
Fix: eager loading (JOIN or batch IN query); DataLoader pattern.
- Hot replica lag: reads sent to lagging replica → stale data.
Fix: route critical reads to primary; monitor replica lag metric.
- Lock contention on read: long-running transactions block SELECT.
Fix: MVCC-aware isolation (READ COMMITTED); short transactions.

Write bottlenecks:
- Single primary write throughput ceiling (~10 K–50 K writes/s for Postgres).
Fix: write sharding; use async queues to buffer writes; CQRS.
- Index write amplification: each INSERT updates all indexes.
Fix: reduce number of indexes on write-heavy tables; partial indexes.
- Locking / deadlocks: Fix: consistent lock order; optimistic locking (CAS).
- WAL I/O: Fix: faster disk; tune checkpoint_completion_target.

Connection pool exhaustion:
- DB allows 100 connections; 500 app pods × 10 connections = 5 000 → crash.
Fix: PgBouncer / RDS Proxy (connection pooler) in front of DB.
Rule of thumb: pool size ≈ (2 × CPU cores) + effective_disk_spindles.

Query-level fixes checklist:
□ EXPLAIN ANALYZE on slow queries.
□ Composite indexes for multi-column WHERE / ORDER BY.
□ Covering index: include all columns the query needs → index-only scan.
□ Partial index: WHERE active = true — smaller index for filtered queries.
□ Materialised views for expensive aggregations.
□ Partition large tables by date range (archival & query pruning).

## 6. Application-level bottlenecks
Synchronous blocking calls:
Every inbound request blocks a thread while waiting for DB / API.
Fix: async I/O (async/await, event loop, reactive frameworks).
Concurrency model: event-loop (Node.js) vs thread-pool (JVM, Go goroutines).

Thundering herd:
Cache expires → all concurrent requests miss → all hit DB simultaneously.
Fixes:
- Cache lock / mutex-on-miss: only one request refills; others wait.
- Probabilistic early expiration: re-compute before TTL expires stochastically.
- Background refresh: async job keeps cache warm; serve stale until ready.

Hot key / hot partition:
One cache key or DB shard receives disproportionate traffic.
Examples: viral tweet, popular product page.
Fixes:
- Local in-process cache: replicate hot key to each app instance's memory.
- Key sharding: append suffix hot_key#0…hot_key#N; scatter reads.
- Dedicated cache cluster for hot objects.

Slow external dependency:
Downstream API with p99 latency 2 s → entire request times out.
Fixes:
- Timeout + retry with exponential backoff + jitter.
- Circuit breaker: stop calling if error rate > threshold.
- Bulkhead: isolate threads/connections per dependency; one slow dep can't
exhaust the entire thread pool.
- Async / degrade gracefully: serve cached/default data while dep is down.

Code-level hot spots:
- Serialisation/deserialisation in a tight loop.
- Regex compilation on every request (pre-compile and cache).
- String concatenation in loop (O(n²)) → use builder / join.
Fix: profiler-driven (never optimise without measuring).

## 7. Bottleneck elimination playbook
A repeatable process for production incidents and design reviews:

Phase 1 — Measure, don't guess:
- Collect p50/p95/p99 latency, throughput, error rate.
- USE (infra) + RED (service) dashboards.
- Distributed trace: waterfall view → find the slow span.

Phase 2 — Isolate:
- Is it one endpoint or all endpoints?
- Is it correlated with a deploy, traffic spike, or cron job?
- Is it one AZ, one shard, one host?

Phase 3 — Fix in order of impact / cost:
1. Query optimisation (free): indexes, N+1 fix, covering index.
2. Caching (cheap): add Redis cache; increase TTL.
3. Async / queue (medium): move work off the hot path.
4. Scale out (medium): more instances behind LB.
5. Sharding / partitioning (expensive): only when above exhausted.
6. Architecture change (very expensive): last resort.

Phase 4 — Validate:
- Load test (k6 / Locust) before and after.
- Monitor p99 latency and error budget burn rate post-deploy.

Phase 5 — Prevent:
- Add the metric that caught this as a permanent alert.
- Add load test to CI/CD for regression detection.
- Document in runbook: symptom → likely cause → fix.

## 8. Remember & rehearse
- State Little's Law. What does it tell you when W starts rising?
- What are the USE and RED methods? When do you apply each?
- What causes a thundering herd? Name two mitigations.
- A service's p99 latency is fine but p50 is slow. Where do you look first?
- What is connection pool exhaustion? How does PgBouncer help?
- You added an index but the query is still slow. What else do you check?
- Describe the bottleneck elimination playbook in five phases.
- What is a hot key? How do you fix it in a Redis cache?
