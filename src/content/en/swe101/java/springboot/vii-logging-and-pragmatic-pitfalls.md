---
label: "VII"
subtitle: "Logging & pragmatic pitfalls"
group: "Spring Boot"
groupOrder: 2
order: 9
---
Spring Boot — Part VII
Structured logging with **SLF4J**, sensible defaults for development, and common mistakes that look like framework bugs but are layering or config issues.

## 1. Logging with SLF4J

Spring Boot wires **SLF4J** + **Logback** by default. Declare a **static** logger per class:

```java
// Compile: javac --release 22 …
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class OrderController {

  private static final Logger log = LoggerFactory.getLogger(OrderController.class);

  private final OrderService orderService;

  public OrderController(OrderService orderService) {
    this.orderService = orderService;
  }

  @PostMapping("/orders")
  public OrderDto create(@RequestBody CreateOrderDto body) {
    log.debug("create order customer={}", body.customerId());
    return orderService.create(body);
  }
}
```

- Use **`{}` placeholders** — **`log.info("id={}", id)`** — avoid **`string + id`** so work is skipped when that level is disabled.
- **Levels**: **`ERROR`** / **`WARN`** need human attention; **`INFO`** lifecycle events; **`DEBUG`** / **`TRACE`** noisy inspection — tune via **`application.yml`** (`logging.level.com.example=DEBUG`).
- **Never log passwords, tokens, full PANs** — redact or log identifiers only.
- **`logging.pattern.correlation`** / **MDC** (`MDC.put("traceId", …)`) tie logs across threads when you add tracing filters later.

## 2. Transaction boundaries belong in services

Keep **`@Transactional`** on **`@Service`** methods that touch repositories — **not** on **`@RestController`**. Controllers should map HTTP ↔ DTOs; services own consistency and rollback semantics.

Common surprises (full detail in **Part V — JPA & `@Transactional`**):

- Unchecked exceptions **rollback** by default; checked exceptions **commit** unless you set **`rollbackFor`**.
- **`@Transactional`** on **`private`** methods or **self-invocation** inside the same class **does not** start a proxy transaction.
- **`readOnly = true`** on query-only service methods documents intent and can help the provider optimize.

## 3. Pragmatic development caveats

- **`@Valid`** on request bodies + **`@ControllerAdvice`** / **`ProblemDetail`** — consistent **400** responses beat silent **`500`** from constraint violations.
- **`spring.jpa.show-sql=true`** — tolerable in dev only; prefer **`logging.level.org.hibernate.SQL=DEBUG`** + parameter logging sparingly — noisy and easy to leak data in shared logs.
- **DevTools** optional auto-restart — fast feedback; turn off in perf-sensitive profiling.
- **Don’t swallow exceptions** — **`catch (Exception e) { log.error(...); }`** without **`throw`** may **commit** a transaction you thought failed.
- **Secure Actuator and admin paths** — see **Security basics & filter chain** and **Part VI (Testing & operations)**.

## 4. Related notes

- **JPA & transactions** — [JPA & @Transactional](v-jpa-and-transactional.md)
- **REST validation & errors** — [REST controllers](iv-rest-controllers.md)
- **YAML logging levels** — [YAML & external config](ii-yaml-and-external-config.md)
