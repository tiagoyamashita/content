---
label: "VI"
subtitle: "E-commerce checkout idempotency"
group: "System design"
order: 6
---
E-commerce checkout idempotency
Mobile and browser clients **retry** `POST /checkout` on timeouts. Without **idempotency**, retries **double-charge** or create duplicate orders. This example shows keys at the **API**, **Payment service**, and **Stripe** for the same checkout domain as [Saga](ii-ecommerce-checkout-saga.md) / [Choreography](iii-ecommerce-checkout-choreography.md).

Theory: [Distributed transactions](../scalable-patterns/vii-distributed-transactions.md) §4, [API design](../scalable-patterns/ii-api-design.md).

## 1. Layers of idempotency

```text
Client Idempotency-Key
    → Checkout / Order API (store key → response)
        → Payment service (key → payment_id)
            → Stripe API (Idempotency-Key header)
```

| Layer | Dedupes |
|-------|---------|
| **API gateway / Checkout** | Entire checkout attempt |
| **Payment service** | Capture for same `order_id` |
| **Stripe** | Same money movement for 24h window |
| **Event consumer** | Same `OrderCreated` message twice |

## 2. Client → API

```http
POST /v1/checkout
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
Content-Type: application/json
```

| Request | Server behavior |
|---------|-----------------|
| **First** key | Process checkout; store `key → {status, order_id, body}` |
| **Retry** same key, in progress | `409` + `Retry-After` or wait and return same result |
| **Retry** same key, completed | Return **cached** `201` / `200` body |
| **New** key | New checkout |

```java
public CheckoutResponse checkout(String idempotencyKey, Cart cart) {
    return idempotencyStore.find(idempotencyKey)
        .map(CheckoutResponse::fromStored)
        .orElseGet(() -> {
            CheckoutResponse result = doCheckout(cart);
            idempotencyStore.save(idempotencyKey, result);
            return result;
        });
}
```

Store in Redis or Postgres with TTL (e.g. 24h). Key scope: **per customer** or **per API key** to prevent cross-user collision.

## 3. Payment service + Stripe

```java
public Payment capture(UUID orderId, Money amount, String idempotencyKey) {
    Optional<Payment> existing = paymentRepo.findByOrderId(orderId);
    if (existing.isPresent()) return existing.get();

    PaymentIntent intent = stripe.paymentIntents().create(
        CreateParams.builder()
            .setAmount(amount.cents())
            .setIdempotencyKey(idempotencyKey)  // Stripe dedupes
            .build()
    );
    return paymentRepo.save(new Payment(orderId, intent.getId()));
}
```

| Failure | Safe retry? |
|---------|-------------|
| Timeout after Stripe succeeded | Yes — same key returns same intent |
| Timeout before Stripe called | Yes — capture runs once |
| Client sends **new** key for same cart | **New** charge — user error or abuse |

## 4. At-least-once messaging

[Outbox relay](v-ecommerce-checkout-transactional-outbox.md) may deliver `OrderCreated` twice:

```java
@KafkaListener(topics = "OrderCreated")
public void onOrderCreated(OrderCreatedEvent e) {
    if (paymentRepo.existsByOrderId(e.orderId())) return;
    capture(e.orderId(), e.amount(), e.idempotencyKey());
}
```

Natural key: `order_id`. Alternative: `event_id` in processed-events table.

## 5. Saga orchestrator retries

[Orchestrated saga](ii-ecommerce-checkout-saga.md) retries HTTP steps on network blips. Each participant must treat:

| Call | Idempotent on |
|------|---------------|
| `create order` | `idempotency_key` or `checkout_id` |
| `capture` | `order_id` |
| `reserve` | `order_id` + line items |
| `refund` | `payment_id` |
| `cancel` | `order_id` |

Orchestrator resumes from `checkout_sagas.current_step` — downstream calls must not duplicate side effects.

## 6. HTTP semantics (sketch)

| Status | Meaning |
|--------|---------|
| `201` | Checkout completed (first or cached) |
| `202` | Accepted, still processing — client polls `GET /checkout/{id}` |
| `409` | Same key, another request in flight |

## 7. Rehearsal questions

- Client retries with same key but **different** cart body — what should server do?
- Why idempotency at both Payment service **and** Stripe?
- How does idempotency interact with [Choreography](iii-ecommerce-checkout-choreography.md) duplicate events?

**Related:** [Checkout saga](ii-ecommerce-checkout-saga.md), [Transactional outbox](v-ecommerce-checkout-transactional-outbox.md).
