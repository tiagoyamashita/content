---
label: "I"
subtitle: "Overview"
group: "System design"
order: 1
---
Examples — overview
**Worked system examples** that apply patterns from **Part I**, **Scalable patterns**, and **Classic designs** to concrete architectures — with diagrams, failure paths, and trade-offs spelled out.

Use these after you understand the pattern in theory; each example shows **how pieces fit together** in production-shaped designs.

## Map of this submenu

| Note | System | Pattern / focus |
|------|--------|-----------------|
| [E-commerce checkout saga](ii-ecommerce-checkout-saga.md) | Online store checkout | **Orchestrated saga** — Checkout service calls Order, Payment, Inventory |
| [E-commerce checkout choreography](iii-ecommerce-checkout-choreography.md) | Same checkout | **Choreography** — event bus; no central orchestrator |
| [E-commerce checkout local ACID](iv-ecommerce-checkout-local-acid.md) | Same checkout | **Local ACID** — modular monolith, one `@Transactional` |
| [E-commerce checkout transactional outbox](v-ecommerce-checkout-transactional-outbox.md) | Order → Payment handoff | **Transactional outbox** — atomic DB + event publish |
| [E-commerce checkout idempotency](vi-ecommerce-checkout-idempotency.md) | Checkout retries | **Idempotency keys** — API, Payment, Stripe, consumers |
| [Product catalog cache-aside](vii-product-catalog-cache-aside.md) | Product pages | **Cache-aside** — Redis in front of Postgres |
| [Order search CDC](viii-order-search-cdc.md) | “Find my orders” | **CDC / events → search index** — OpenSearch read model |
| [E-commerce checkout sharded](ix-ecommerce-checkout-sharded.md) | Checkout at scale | **Sharded DBs** — saga across Order, Payment, Inventory shards |
| [E-commerce checkout workflow engine](x-ecommerce-checkout-workflow-engine.md) | Long-running checkout | **Temporal / Step Functions** — durable workflow orchestration |

## Checkout pattern progression

```text
Local ACID (IV) → Outbox (V) → Choreography (III) or Saga (II) → Sharded saga (IX) → Workflow engine (X)
         ↑                              ↑
   Idempotency (VI) everywhere on retries and at-least-once delivery
```

| Question | Start here |
|----------|------------|
| One app, one DB? | [Local ACID](iv-ecommerce-checkout-local-acid.md) |
| Publish events reliably? | [Transactional outbox](v-ecommerce-checkout-transactional-outbox.md) |
| Split microservices? | [Saga](ii-ecommerce-checkout-saga.md) or [Choreography](iii-ecommerce-checkout-choreography.md) |
| Client retries / duplicate messages? | [Idempotency](vi-ecommerce-checkout-idempotency.md) |
| Reads before checkout? | [Catalog cache-aside](vii-product-catalog-cache-aside.md) |
| Search orders? | [Order search CDC](viii-order-search-cdc.md) |
| DB write scale? | [Sharded checkout](ix-ecommerce-checkout-sharded.md) |
| Durable timers / workflow UI? | [Workflow engine](x-ecommerce-checkout-workflow-engine.md) |

## How to read an example

| Section | What to look for |
|---------|------------------|
| **Requirements** | Functional scope and consistency expectations |
| **Services & data** | Who owns what; no shared database |
| **Happy path** | Step order and local transactions |
| **Failure path** | Rollback, compensations, or eventual repair |
| **Ops concerns** | Idempotency, outbox, monitoring, timeouts |

## Study order

```text
Part I → Scalable patterns (theory) → Examples (applied) → Classic designs → Bottleneck analysis
```

**Related:** [Distributed transactions](../scalable-patterns/vii-distributed-transactions.md), [Message queues & async](../scalable-patterns/iii-message-queues-and-async.md), [Database sharding](../scalable-patterns/ix-database-sharding.md).
