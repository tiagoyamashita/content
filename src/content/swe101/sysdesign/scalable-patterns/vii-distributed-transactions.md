---
label: "VII"
subtitle: "Distributed transactions"
group: "System design"
order: 7
---
Distributed transactions
When one business action touches **multiple services** or **databases**, you cannot rely on a single local `COMMIT` — you need **coordination patterns**.

## 1. The problem

```text
Order service (DB A)     Payment service (DB B)
        │                         │
        └──── both must succeed or neither ────┘
```

Network partitions and independent failures break naive “call A then B” flows.

## 2. Two-phase commit (2PC)

| Phase | Action |
|-------|--------|
| **Prepare** | Coordinator asks participants: “Can you commit?” |
| **Commit** | All yes → commit all; any no → abort all |

| Pros | Cons |
|------|------|
| Strong atomicity within cluster | **Blocking** if coordinator dies |
| Well understood in RDBMS | **Poor fit** across microservices |
| | Latency + availability cost |

Use **inside** one database cluster or tightly coupled store — **not** as default across 10 microservices.

## 3. Saga pattern

**Saga** = sequence of **local transactions**; each step publishes success; on failure run **compensating** steps in reverse.

Example: **Create order → Charge payment → Reserve inventory**

| Step | Forward | Compensation |
|------|---------|--------------|
| 1 | Create order (pending) | Cancel order |
| 2 | Charge card | Refund |
| 3 | Reserve stock | Release stock |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 120" role="img" aria-label="Saga forward steps and compensating rollback">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Orchestration saga</text>
  <rect x="12" y="36" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="24" y="54" fill="#e4e4e7" font-size="8">1. Order OK</text>
  <path d="M84 50 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="36" width="72" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="54" fill="#e4e4e7" font-size="8">2. Pay OK</text>
  <path d="M180 50 H204" stroke="#f87171" stroke-width="1.5"/>
  <rect x="204" y="36" width="72" height="28" rx="3" fill="rgba(248,113,113,0.15)" stroke="#f87171"/>
  <text x="214" y="54" fill="#e4e4e7" font-size="8">3. Stock FAIL</text>
  <text x="12" y="82" fill="#fbbf24" font-size="9">Compensate: refund (2) → cancel order (1)</text>
  <path d="M180 90 H108" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 2"/>
  <path d="M108 90 H36" stroke="#fbbf24" stroke-width="1" stroke-dasharray="3 2"/>
</svg></figure>

### Choreography vs orchestration

| | Choreography | Orchestration |
|---|--------------|---------------|
| Control | Each service reacts to **events** | **Central orchestrator** sends commands |
| Pros | No single coordinator SPOF | Clear state machine, easier debug |
| Cons | Hard to see global state | Orchestrator availability matters |
| Fit | Few steps, mature event culture | Complex flows, visibility needed |

## 4. Idempotency keys

Clients send **`Idempotency-Key: uuid`** on POST; service stores key → response mapping.

| Retry | Behavior |
|-------|----------|
| Same key, in progress | Wait or return same result |
| Same key, completed | Return cached response |
| New key | New operation |

Enables **at-least-once** messaging and HTTP retries without double charge.

## 5. Pattern selection

| Situation | Pattern |
|-----------|---------|
| Single Postgres transaction | Local ACID |
| Same DB, multiple tables | Local ACID |
| Microservices, long-running | **Saga** + outbox |
| Strong cross-shard in one DB | 2PC / XA (rare at app layer) |
| Read models | Eventual consistency + CDC |

**Related:** [Message queues & async](iii-message-queues-and-async.md) (outbox, events), [API design](ii-api-design.md) (Idempotency-Key).
