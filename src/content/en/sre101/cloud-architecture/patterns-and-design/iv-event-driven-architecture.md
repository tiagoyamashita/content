---
label: "IV"
subtitle: "Event-driven architecture"
group: "Cloud architecture"
order: 4
---
Event-driven architecture
Services communicate via **events** on a **message broker** instead of synchronous chains. Decouples producers from consumers and absorbs traffic spikes.

## 1. Sync vs async

| Synchronous (HTTP) | Asynchronous (events) |
|--------------------|------------------------|
| Caller waits | Producer fires and forgets |
| Tight coupling | Loose coupling in time |
| Simple debugging | Needs idempotency, DLQ |
| Cascade latency | Buffering under load |

```text
Sync:  Order Svc ──HTTP──▶ Inventory Svc ──HTTP──▶ Payment Svc
       (failure in payment blocks whole chain)

Async: Order Svc ──▶ queue ──▶ Inventory worker
                    └──▶ Payment worker (parallel)
```

## 2. Message queue (point-to-point)

**One consumer** processes each message (competing consumers).

```text
Producer ──▶ [ Queue ] ──▶ Consumer A
                    └──▶ Consumer B  (only one gets each message)
```

| Cloud service | Model |
|---------------|-------|
| **AWS SQS** | Standard or FIFO queue |
| **Azure Service Bus** | Queues |
| **Google Cloud Tasks** | Task queue |

**Use when:** job processing, work distribution, back-pressure (producer faster than consumer).

```json
{
  "eventType": "OrderPlaced",
  "orderId": "ord-9281",
  "items": [{"sku": "WIDGET-1", "qty": 2}],
  "timestamp": "2026-05-19T14:22:00Z"
}
```

## 3. Pub/sub (fan-out)

**Each subscriber** receives a copy of the message.

```text
Publisher ──▶ [ Topic ] ──▶ Subscriber A (email)
                    ├──▶ Subscriber B (analytics)
                    └──▶ Subscriber C (inventory)
```

| Cloud service | Pattern |
|---------------|---------|
| **AWS SNS** + SQS | SNS fan-out to multiple SQS queues |
| **Google Pub/Sub** | Native pub/sub |
| **Azure Event Grid** | Event routing |

**Use when:** notify multiple systems of same fact (`UserRegistered` → welcome email + CRM + audit).

## 4. Queue vs pub/sub

| | Queue | Pub/sub |
|---|-------|---------|
| Delivery | One consumer per message | All subscribers get copy |
| Ordering | FIFO queue optional | Topic ordering varies |
| Example | Process payment job | Broadcast config change |
| Back-pressure | Queue depth metric | Slow subscriber needs own queue |

## 5. Event streaming

**Ordered, replayable log** — consumers track offset.

```text
Producer ──▶ [ Kafka topic: orders ] ──▶ Consumer group A (analytics)
                                   └──▶ Consumer group B (fraud)
```

| Platform | Characteristics |
|----------|-----------------|
| **Apache Kafka** | Partitions, retention, replay |
| **AWS Kinesis** | Shards, stream processing |
| **Azure Event Hubs** | Kafka-compatible endpoint |

**Use when:**

- **Audit trail** — replay history
- **Event sourcing** — state derived from event log
- **Multiple independent consumers** at different speeds
- **Stream processing** — Flink, ksqlDB, Lambda

## 6. Saga pattern

Distributed transaction across services — **no single DB transaction**.

### Choreography (events only)

```text
OrderCreated ──▶ ReserveInventory ──▶ PaymentCaptured ──▶ OrderConfirmed
                      │ fail
                      └──▶ ReleaseInventory (compensating)
```

Each service listens and publishes next step or compensation.

### Orchestration (central coordinator)

```text
Saga orchestrator
  1. call inventory.reserve()
  2. call payment.charge()
  3. on failure → payment.refund(), inventory.release()
```

| | Choreography | Orchestration |
|---|--------------|---------------|
| Coupling | Loose | Orchestrator knows all steps |
| Visibility | Harder to trace | Central state machine |
| Tooling | Event bus | Temporal, Step Functions |

## 7. Reliability patterns

| Pattern | Purpose |
|---------|---------|
| **Dead-letter queue (DLQ)** | Poison messages after N retries |
| **Idempotent consumer** | Same `orderId` processed once |
| **Outbox pattern** | DB commit + event publish atomically |
| **Visibility timeout** | SQS redelivery if worker crashes |

```java
// Idempotent consumer — Java 22
void handle(OrderPlaced event) {
  if (processedEvents.exists(event.id())) return;
  process(event);
  processedEvents.mark(event.id());
}
```

## 8. When not to use events

| Situation | Prefer |
|-----------|--------|
| User waiting for immediate response | Sync HTTP/gRPC |
| Strong consistency required | Single DB transaction |
| Two-service startup | Direct call until complexity grows |

**Related:** [Microservices vs monolith](iii-microservices-vs-monolith.md), [API Gateway & service mesh](v-api-gateway-and-service-mesh.md).
