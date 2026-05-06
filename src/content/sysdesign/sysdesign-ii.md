---
label: "II"
subtitle: "Scalable Patterns"
group: "System design"
order: 2
---
System Design — Part II: Scalable Patterns
APIs, async, rate limiting, search, CDN, distributed transactions.

## 1. API design (REST & gRPC)
REST — resource-oriented, HTTP verbs, stateless:
- GET    /users/{id}       — read
- POST   /users            — create
- PUT    /users/{id}       — full replace
- PATCH  /users/{id}       — partial update
- DELETE /users/{id}       — remove

Versioning: /v1/users — never break existing clients.
Pagination: cursor-based preferred over offset for large/live datasets.
- Offset: LIMIT 20 OFFSET 100 — simple but skips/dupes on inserts.
- Cursor: WHERE id > :last_seen LIMIT 20 — stable regardless of inserts.

gRPC — binary (Protocol Buffers), HTTP/2, strongly typed:
- 5–10× smaller payload vs JSON; generated client stubs in any language.
- Supports server-streaming, client-streaming, and bidirectional streaming.
- Use for: internal service-to-service calls where performance matters.
- Less human-readable; harder to debug without tooling.

GraphQL — client specifies exact shape of response:
- Eliminates over-fetching and under-fetching.
- N+1 query problem: naive resolvers make N DB calls; use DataLoader (batching).
- Good fit for: product APIs consumed by multiple client types (mobile, web).

## 2. Message queues & async flows
Synchronous call: caller blocks until callee responds.
+ Simple, immediate feedback.
− Caller is tightly coupled to callee availability and speed.

Async via message queue: producer puts message on queue; consumer processes later.
+ Decouples producer from consumer; absorbs traffic spikes.
+ Consumer can retry failed messages.
− Adds latency; harder to debug end-to-end.

Patterns:
- Task queue:    one producer → one consumer (work distribution). SQS, Celery.
- Pub/Sub:       one event → many consumers (fan-out). SNS, Kafka topics.
- Dead-letter queue (DLQ): messages that fail N retries go here for inspection.

Exactly-once vs at-least-once:
- At-least-once: message delivered ≥ 1 time; consumer must be idempotent.
- Exactly-once: harder (2PC or transactional outbox); most systems use at-least-once.

Transactional outbox pattern:
Write event to outbox table in the same DB transaction as the business data.
A relay process reads the outbox and publishes to the broker.
→ Guarantees event is published if and only if the transaction commits.

## 3. Rate limiting
Why: protect services from abuse, ensure fair usage, control costs.

Algorithms:
- Token bucket: bucket holds up to N tokens; refilled at rate R/s.
Each request consumes 1 token; bucket empties → requests dropped.
Allows bursting up to bucket size.

- Leaky bucket: requests enter a queue; processed at fixed rate.
Queue full → drop. Smooths bursts completely.

- Fixed window counter: count requests per minute window.
Reset at window boundary → burst at boundary exploitable.

- Sliding window log: record timestamps; count in last 60 s.
Accurate but memory-intensive for high volume.

- Sliding window counter: blend fixed windows — accurate & memory-efficient.

Where to enforce:
- API Gateway (centralised) — single enforcement point.
- Per service (distributed) — requires shared counter in Redis.
- Key: user_id, IP, or API key.

Response: HTTP 429 Too Many Requests + Retry-After header.

## 4. Search systems
Full-text search needs an inverted index:
- Token → list of (doc_id, positions). Built offline; updated on write.
- Elasticsearch / OpenSearch: distributed inverted index; near-real-time.

Write path:
Document → tokenise → normalise (lower, stem) → index shards.

Read path:
Query → parse → fetch posting lists → score (BM25 / TF-IDF) → rank → return.

Sync strategy:
- Dual-write: app writes to DB and search index simultaneously.
Risk: partial failure leaves index out of sync.
- CDC (Change Data Capture): read DB binary log → stream changes to index.
Debezium + Kafka → Elasticsearch is a common stack.

Vector / semantic search:
- Embed queries and documents into dense vectors (embedding model).
- ANN (Approximate Nearest Neighbour): HNSW or IVF index in pgvector, Pinecone.
- Hybrid: combine BM25 (keyword) + vector (semantic) scores (RRF fusion).

## 5. Content delivery & CDN
CDN (Content Delivery Network):
- Network of edge PoPs caching content close to users.
- Request hits nearest PoP; miss → fetch from origin once → cache.

What to put on CDN:
- Static: images, JS/CSS bundles, fonts, videos.
- Dynamic: cacheable API responses (short TTL), personalised pages (vary by cookie).

Cache invalidation:
- TTL expiry: simplest; stale during TTL window.
- Versioned URLs: /app.v3.js — old URL stays cached; new version is new URL.
- Purge API: instantly evict a URL from all PoPs (use for urgent fixes).

Push vs pull CDN:
- Pull: origin fetched on first miss — easy to set up; cold start latency.
- Push: you upload assets directly to CDN — full control; must manage uploads.

## 6. Distributed transactions
Problem: update data in two separate services/databases atomically.

Two-Phase Commit (2PC):
Phase 1 (Prepare): coordinator asks all participants if they can commit.
Phase 2 (Commit): if all say yes → commit; any no → rollback.
− Coordinator is a single point of failure; blocking protocol.
− Rarely used across microservices; fine within a single DB cluster.

Saga pattern (preferred for microservices):
- Sequence of local transactions; each publishes an event on success.
- On failure: execute compensating transactions in reverse.

Choreography saga:
Each service listens for events and decides what to do.
+ No central coordinator. − Hard to track state; spaghetti event flows.

Orchestration saga:
Central saga orchestrator tells each service what to do.
+ Clear flow; easy to monitor. − Orchestrator is a coordination bottleneck.

Idempotency key: include a unique request ID; services deduplicate retries.
→ Safe at-least-once delivery without double-processing side effects.

## 7. Observability at scale
At high scale a single slow or failing component cascades; you need fast signal.

Alerting strategy:
- Alert on symptoms (high error rate, high latency) not causes (CPU%).
- SLO-based alerts: page when error budget burn rate is too fast.
- Runbook: every alert links to a runbook with investigation steps.

Distributed tracing in practice:
- Inject trace-id at API gateway; propagate via HTTP headers (W3C TraceContext).
- Spans record service name, operation, duration, status.
- Visualise in Jaeger / Zipkin / Tempo; find the slow span in a waterfall view.

Capacity planning:
- Track p50/p95/p99 latency and throughput over time.
- Model growth: if DAU grows 20%/month, when do you need to scale?
- Load test before launches: k6, Locust, Gatling.

Chaos engineering:
- Deliberately inject failures (kill instances, add latency) in staging/prod.
- Verify system degrades gracefully and alerts fire correctly.
- AWS Fault Injection Service, Netflix Chaos Monkey.

## 8. Remember & rehearse
- What is the difference between cursor-based and offset pagination?
- Explain the transactional outbox pattern and why it is needed.
- Compare token bucket vs leaky bucket rate limiting.
- How does an inverted index work?
- What is CDC and how does it keep a search index in sync with the DB?
- Explain the Saga pattern. When would you choose orchestration over choreography?
- What is an idempotency key?
