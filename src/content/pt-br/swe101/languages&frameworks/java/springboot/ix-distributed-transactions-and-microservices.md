---
label: "IX"
subtitle: "Distributed transactions & microservices"
group: "Spring Boot"
groupOrder: 2
order: 12
---
Spring Boot — Part IX: Distributed transactions & microservices
**`@Transactional`** wraps **one database** inside **one service**. In microservices, a single business action often spans several services (order → payment → inventory). There is no built-in ACID transaction across them unless you add something extra — and that extra is usually **not** what you want.

**Java baseline:** **Java SE 22** (`javac --release 22`); examples target **Spring Boot 3.x**.

## 1. The core problem

| Scope | What Spring gives you |
|-------|----------------------|
| **One service, one DB** | **`@Transactional`** — commit or rollback as one unit (see **Part V** — [JPA & @Transactional](v-jpa-and-transactional.md)) |
| **Several services, several DBs** | No single transaction by default; you design **eventual consistency** |

Each microservice should own **its own database** and a clear **bounded context**. Cross-service “all or nothing” ACID is expensive, brittle, and fights the independence microservices are meant to provide.

## 2. What to do instead (practical order)

### 2.1 Avoid distributed transactions when you can

- Keep each write inside **one local transaction**.
- Accept **eventual consistency** across services: each commits locally, then notifies others.
- This is the default pattern in production Spring Boot microservice setups.

### 2.2 Saga pattern (most common)

Break a workflow into **local transactions** plus **compensating actions** when a later step fails.

| Style | How it works |
|-------|--------------|
| **Choreography** | Services publish and consume events (Kafka, RabbitMQ). Each service knows what to do next. |
| **Orchestration** | One coordinator drives steps and triggers compensation on failure (custom service, **Temporal**, **Camunda**, etc.). |

**Example flow:** create order → reserve inventory → charge payment. If payment fails, **compensate** by releasing inventory and cancelling the order.

Spring pieces: **`@Transactional`** per step, messaging (**`spring-kafka`**), and explicit saga state (DB table or workflow engine).

```text
Client → Order Service (@Transactional: order + outbox)
              ↓ event
         Payment Service (@Transactional: payment)
              ↓ event
         Inventory Service (@Transactional: reserve)
              ↓ on failure
         Compensating events / orchestrator rollback
```

### 2.3 Transactional outbox (reliable cross-service messaging)

**Problem:** you update your DB and publish an event — one can succeed and the other fail.

**Outbox:** in the **same local transaction**, write business data **and** an **outbox row**. A separate process publishes from the outbox to Kafka or RabbitMQ. Consumers must be **idempotent** (processing the same message twice must be safe).

Tools: **Debezium** (CDC), **Spring Integration**, or libraries such as **Eventuate Tram**.

```java
// Compile: javac --release 22 …
import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "outbox_events")
public class OutboxEvent {

  @Id
  private UUID id;

  @Column(nullable = false, length = 120)
  private String aggregateType;

  @Column(nullable = false, length = 120)
  private String eventType;

  @Lob
  @Column(nullable = false)
  private String payloadJson;

  @Column(nullable = false)
  private Instant createdAt;

  @Column(nullable = false)
  private boolean published;

  protected OutboxEvent() {}

  public OutboxEvent(String aggregateType, String eventType, String payloadJson) {
    this.id = UUID.randomUUID();
    this.aggregateType = aggregateType;
    this.eventType = eventType;
    this.payloadJson = payloadJson;
    this.createdAt = Instant.now();
    this.published = false;
  }
}
```

```java
// Compile: javac --release 22 …
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OrderService {

  private final OrderRepository orders;
  private final OutboxRepository outbox;

  public OrderService(OrderRepository orders, OutboxRepository outbox) {
    this.orders = orders;
    this.outbox = outbox;
  }

  @Transactional
  public OrderEntity placeOrder(PlaceOrderCommand cmd) {
    OrderEntity order = orders.save(new OrderEntity(cmd.customerId(), cmd.total()));
    outbox.save(new OutboxEvent(
        "Order",
        "OrderPlaced",
        "{\"orderId\":\"" + order.getId() + "\"}"));
    return order;
  }
}
```

A scheduled job or CDC connector reads **`published = false`** rows, sends them to the broker, then marks them published — still **outside** the original transaction, but the event is never lost if the DB commit succeeded.

### 2.4 Idempotency and retries

Network calls fail mid-flight. Without safeguards, sagas and outbox break under retries.

- **Idempotency keys** on APIs (`Idempotency-Key` header): An idempotency key is a unique value provided by the client (typically via a request header) that allows the server to recognize and ignore duplicate requests, ensuring that the same action is not performed multiple times if a request is retried due to network errors or timeouts. This helps prevent double processing (like charging a credit card twice) in unreliable environments.
- **At-least-once** delivery with deduplication
- Clear status fields (`PENDING`, `COMPLETED`, `FAILED`)

```java
// Compile: javac --release 22 …
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class PaymentService {

  private final PaymentRepository payments;

  public PaymentService(PaymentRepository payments) {
    this.payments = payments;
  }

  @Transactional
  public PaymentResult charge(String idempotencyKey, ChargeRequest request) {
    return payments.findByIdempotencyKey(idempotencyKey)
        .map(PaymentEntity::toResult)
        .orElseGet(() -> {
          PaymentEntity saved = payments.save(
              PaymentEntity.charge(idempotencyKey, request.orderId(), request.amount()));
          return saved.toResult();
        });
  }
}
```

### 2.5 Two-phase commit / XA (usually avoid)

True **two-phase commit** across multiple databases (**JTA**, Atomikos, Narayana) or protocols like **Seata AT**.

| Pros | Cons |
|------|------|
| Strong consistency | Tight coupling between services |
| | Higher latency and operational fragility |
| | Poor fit for heterogeneous systems and independent deploys |

Use only when regulation or legacy constraints force it — **not** as the default microservices pattern.

## 3. How to manage it in Spring Boot

A practical stack:

1. **Local `@Transactional`** per service (Part V).
2. **Messaging** for async steps (**`spring-kafka`**, Spring AMQP).
3. **Outbox** for atomic “DB + event” within one service.
4. **Saga orchestration or choreography** for multi-step flows with compensation.
5. **Observability**: correlation IDs, saga instance IDs, structured logs.

**Kafka dependency (Maven — use your BOM versions):**

```xml
<dependency>
  <groupId>org.springframework.kafka</groupId>
  <artifactId>spring-kafka</artifactId>
</dependency>
```

**Minimal consumer with idempotent handling:**

```java
// Compile: javac --release 22 …
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
public class InventoryEventListener {

  private final InventoryService inventory;
  private final ProcessedEventRepository processed;

  public InventoryEventListener(InventoryService inventory, ProcessedEventRepository processed) {
    this.inventory = inventory;
    this.processed = processed;
  }

  @KafkaListener(topics = "order-placed", groupId = "inventory")
  @Transactional
  public void onOrderPlaced(OrderPlacedEvent event) {
    if (processed.existsByEventId(event.eventId())) {
      return; // already handled — safe retry
    }
    inventory.reserve(event.orderId(), event.lines());
    processed.save(new ProcessedEvent(event.eventId()));
  }
}
```

## 4. Rule of thumb

| Need | Approach |
|------|----------|
| One service, one DB | **`@Transactional`** |
| Multiple services, normal microservices | **Saga + outbox + idempotency** |
| Must be strongly consistent everywhere | Reconsider architecture; **2PC** is a last resort |

**Mental model:** do not try to make microservices **one big transaction**. Manage consistency with **sagas**, **outbox**, and **compensations**.

## 5. Operations checklist

1. **One DB per service** — no shared tables across bounded contexts.
2. **Outbox or CDC** — never “DB commit then fire-and-forget HTTP” as your only integration path.
3. **Compensations are business logic** — define them up front (cancel order, release stock, refund).
4. **Correlation IDs** — propagate through HTTP headers and Kafka message headers for tracing.
5. **Monitor** stuck sagas (`PENDING` too long), outbox backlog, and duplicate-processing rates.
6. **Cache** (Part VIII) sits outside DB transactions — evict **after** successful commit when consistency matters.

## 6. Related notes

- **JPA & transactions** — Part V [JPA & @Transactional](v-jpa-and-transactional.md) — local transaction boundaries and propagation
- **Distributed cache** — Part VIII [Distributed cache](viii-distributed-cache.md) — cache invalidation vs cross-service consistency
- **YAML & config** — Part II [YAML & external config](ii-yaml-and-external-config.md) — broker URLs, env-specific profiles
- **Testing** — Part VI [Testing & operations](vi-testing-and-operations.md) — contract tests between services
- **Logging** — Part VII [Logging & pragmatic pitfalls](vii-logging-and-pragmatic-pitfalls.md) — structured logs for saga tracing
