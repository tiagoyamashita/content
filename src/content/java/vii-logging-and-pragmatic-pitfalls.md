---
label: "VII"
subtitle: "Logging & pragmatic pitfalls"
group: "Spring Boot"
groupOrder: 2
order: 8
---
Spring Boot — Part VII
Structured logging with **SLF4J**, sensible defaults for development, and where **`@Transactional`** actually belongs (usually **not** on **`@RestController`**).

## 1. Logging with SLF4J

Spring Boot wires **SLF4J** + **Logback** by default. Declare a **static** logger per class:

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class OrderController {

  private static final Logger log = LoggerFactory.getLogger(OrderController.class);

  @PostMapping("/orders")
  public OrderDto create(@RequestBody CreateOrderDto body) {
    log.debug("create order customer={}", body.customerId());
    // ...
  }
}
```

- Use **`{}` placeholders** — **`log.info("id={}", id)`** — avoid **`string + id`** so work is skipped when that level is disabled.
- **Levels**: **`ERROR`** / **`WARN`** need human attention; **`INFO`** lifecycle events; **`DEBUG`** / **`TRACE`** noisy inspection — tune via **`application.yml`** (`logging.level.com.example=DEBUG`).
- **Never log passwords, tokens, full PANs** — redact or log identifiers only.
- **`logging.pattern.correlation`** / **MDC** (`MDC.put("traceId", …)`) tie logs across threads when you add tracing filters later.

## 2. `@Transactional`: rollback vs layer hygiene

**Mental model you want:** if persistence work fails, the DB transaction **rolls back** so nothing half-written stays committed.

**Where Spring applies it:** **`@Transactional`** uses proxies around Spring-managed beans. Unchecked exceptions **`RuntimeException`** and **`Error`** **rollback** by default; checked exceptions **commit** unless you set **`rollbackFor`**.

**Avoid `@Transactional` on `@RestController`** as your default pattern:

- The **controller** should map HTTP ↔ DTOs and delegate; the **service** owns **business consistency** and **transaction boundaries**.
- A transaction opened on the controller stays open while you serialize JSON, call helpers, etc.—longer DB connections and muddy boundaries if multiple services participate.
- `@Transactional` on **`private`** methods or **self-invocation** inside the same class **does not** start a new proxy transaction — another reason thin controllers + **`@Service`** methods matter.

**Preferred shape:**

```java
@Service
@RequiredArgsConstructor
public class OrderService {

  private final OrderRepository orders;

  @Transactional
  public OrderDto create(CreateOrderDto dto) {
    var entity = new OrderEntity(/* … */);
    orders.save(entity);
    return OrderDto.from(entity); // same transaction; rollback if anything throws
  }
}
```

```java
@RestController
@RequiredArgsConstructor
public class OrderController {

  private final OrderService orderService;

  @PostMapping("/orders")
  public OrderDto create(@Valid @RequestBody CreateOrderDto body) {
    return orderService.create(body); // transaction boundary in service
  }
}
```

Putting **`@Transactional`** on the controller **might** appear to “fix” issues in tiny demos, but it hides layering problems and scales poorly—keep rollback semantics **next to the repository work**.

## 3. Pragmatic development caveats

- **`@Valid`** on request bodies + **`@ControllerAdvice`** / **`ProblemDetail`** — consistent **400** responses beat silent **`500`** from constraint violations.
- **`spring.jpa.show-sql=true`** — tolerable in dev only; prefer **`logging.level.org.hibernate.SQL=DEBUG`** + parameter logging sparingly — noisy and easy to leak data in shared logs.
- **DevTools** optional auto-restart — fast feedback; turn off in perf-sensitive profiling.
- **Don’t swallow exceptions** — **`catch (Exception e) { log.error(...); }`** without **`throw`** may **commit** a transaction you thought failed.
- **`readOnly = true`** on **`@Transactional`** for pure queries — helps some providers optimize and documents intent.

Cross-check **Part V (JPA & `@Transactional`)** for propagation, **`REQUIRES_NEW`**, and repository placement.
