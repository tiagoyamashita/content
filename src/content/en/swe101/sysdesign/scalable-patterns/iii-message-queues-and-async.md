---
label: "III"
subtitle: "Message queues & async"
group: "System design"
order: 3
---
Message queues and async flows
**Async messaging** decouples producers from consumers in time and scale — critical when peak traffic exceeds synchronous capacity.

## 1. Sync vs async

| | Synchronous HTTP/RPC | Async queue |
|---|---------------------|-------------|
| Coupling | Caller waits; callee must be up | Producer enqueues and continues |
| Latency to caller | Includes full processing | Ack after persist to broker only |
| Spike handling | Timeouts cascade | Queue absorbs backlog |
| Debugging | Single trace | Need correlation ids across hops |
| Consistency | Immediate read-your-writes | Eventual; design for delay |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 140" role="img" aria-label="Sync call vs async queue decoupling">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Sync vs async</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="9">Sync: API ──wait──▶ Worker (both must scale together)</text>
  <rect x="12" y="48" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="66" fill="#e4e4e7" font-size="9">API</text>
  <path d="M68 62 H140" stroke="#f87171" stroke-width="2"/>
  <rect x="140" y="48" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="148" y="66" fill="#e4e4e7" font-size="9">Worker</text>
  <text x="12" y="92" fill="#a1a1aa" font-size="9">Async: API ──▶ Queue ──▶ Worker (scale consumers independently)</text>
  <rect x="12" y="102" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="120" fill="#e4e4e7" font-size="9">API</text>
  <rect x="88" y="102" width="56" height="28" rx="3" fill="rgba(59,130,246,0.15)" stroke="#60a5fa"/>
  <text x="100" y="120" fill="#e4e4e7" font-size="9">Queue</text>
  <path d="M144 116 H200" stroke="#86efac" stroke-width="1.5"/>
  <rect x="200" y="102" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="208" y="120" fill="#e4e4e7" font-size="9">Worker</text>
</svg></figure>

## 2. Messaging patterns

| Pattern | Topology | Example products |
|---------|----------|------------------|
| **Task queue** | 1 producer → N competing consumers | SQS, RabbitMQ work queues, Celery |
| **Pub/Sub** | 1 event → many subscribers | SNS, Kafka topics, Google Pub/Sub |
| **Log / stream** | Ordered partition log; replay | Kafka, Kinesis, Pulsar |
| **Dead-letter queue (DLQ)** | Failed messages after N retries | SQS DLQ, RabbitMQ DLX |

## 3. Delivery guarantees

| Guarantee | Meaning | Your responsibility |
|-----------|---------|---------------------|
| **At-most-once** | May lose message | Rare for critical work |
| **At-least-once** | May duplicate | **Idempotent** consumers |
| **Exactly-once** | Hard end-to-end | Transactional outbox + idempotent sinks, or stream processing with EOS |

Most production systems: **at-least-once** + **idempotency keys**.

## 4. Transactional outbox

**Problem:** DB commit succeeds but message publish fails (or reverse) → inconsistent state.

**Solution:** write business row **and** outbox row in **one DB transaction**; separate **relay** publishes to broker and marks outbox sent.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Transactional outbox pattern">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Transactional outbox</text>
  <rect x="12" y="36" width="100" height="80" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="54" fill="#86efac" font-size="9" font-weight="600">Single DB txn</text>
  <text x="24" y="72" fill="#a1a1aa" font-size="8">INSERT order</text>
  <text x="24" y="86" fill="#a1a1aa" font-size="8">INSERT outbox_event</text>
  <path d="M112 76 H160" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="160" y="56" width="80" height="40" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="172" y="80" fill="#e4e4e7" font-size="9">Relay poller</text>
  <path d="M240 76 H288" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="288" y="56" width="72" height="40" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="300" y="80" fill="#e4e4e7" font-size="9">Kafka/SQS</text>
  <text x="12" y="128" fill="#71717a" font-size="9">Event published iff business transaction committed.</text>
</svg></figure>

| Step | Action |
|------|--------|
| 1 | `BEGIN; INSERT orders …; INSERT outbox (payload); COMMIT;` |
| 2 | Relay reads `outbox WHERE sent = false` |
| 3 | Publish to broker; mark row sent (or delete) |

## 5. Ordering and partitioning

- **Kafka:** order guaranteed **per partition** — choose partition key (e.g. `user_id`) for related events.
- **Global order:** single partition — limits throughput.
- **Poison message:** after max retries → DLQ + alert; don’t block whole queue.

## 6. When to use async

| Use async | Stay sync |
|-----------|-----------|
| Email, notifications, search indexing | User waiting for immediate result |
| Image/video processing | Strong read-your-writes on same request |
| Fan-out to many subscribers | Simple CRUD with low latency SLA |

**Worked example:** [Transactional outbox (checkout)](../examples/v-ecommerce-checkout-transactional-outbox.md).

**Related:** [Distributed transactions](vii-distributed-transactions.md) (saga events), [Search systems](v-search-systems.md) (CDC to index).
