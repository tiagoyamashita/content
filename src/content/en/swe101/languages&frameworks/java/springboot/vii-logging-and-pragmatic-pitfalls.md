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

  **Example:**
  ```java
  @Transactional
  public void updateOrder(OrderDto dto) {
    try {
      // ... update some entities ...
    } catch (Exception e) {
      log.error("Failed to update order {}", dto.id(), e);
      // BUG: Exception is logged, but not rethrown!
      // Transaction may commit despite the error.
      // throw e; // <-- SHOULD be here!
    }
  }
  ```

  **Rollback on any exception:**
  ```java
  @Transactional(rollbackFor = Exception.class)
  public void updateOrderStrongly(OrderDto dto) throws Exception {
    // ... update some entities ...
    // any Exception (checked or unchecked) will trigger rollback
  }
  ```
- **Secure Actuator and admin paths** — see **Security basics & filter chain** and **Part VI (Testing & operations)**.

## 4. Centralized Logging for @Transactional Methods with Spring AOP

You can centralize logging for methods annotated with **`@Transactional`** using Spring's **AOP (Aspect-Oriented Programming)** capabilities. This allows you to log the entry, exit, and execution time of any transactional method—without cluttering your service classes with repetitive code.

**How it works:**
- Define an **`@Aspect`** class with a pointcut that targets methods annotated with **`@Transactional`**.
- Implement `@Around` advice to perform logging before and after method execution, capturing information such as method name, arguments, result, and execution duration.

**Advantages:**
- No need to add manual logging to each method.
- Consistent logging for all transactional operations.
- Easy to extend or modify logging behavior in one place.

### Example: Logging Aspect for @Transactional Methods

```java
package com.example.demo.logging;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.reflect.MethodSignature;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Aspect
@Component
public class TransactionalLoggingAspect {

  private static final Logger log = LoggerFactory.getLogger(TransactionalLoggingAspect.class);

  // Pointcut: any method annotated with @Transactional
  @Around("@annotation(transactional)")
  public Object logTransactionalMethod(ProceedingJoinPoint pjp, Transactional transactional) throws Throwable {
    MethodSignature signature = (MethodSignature) pjp.getSignature();
    String methodName = signature.getDeclaringType().getSimpleName() + "." + signature.getName();
    long start = System.nanoTime();

    log.info("START @Transactional: {} with args {}", methodName, pjp.getArgs());
    try {
      Object result = pjp.proceed();
      long ms = (System.nanoTime() - start) / 1_000_000;
      log.info("END @Transactional: {} -> {} ({} ms)", methodName, result, ms);
      return result;
    } catch (Throwable t) {
      long ms = (System.nanoTime() - start) / 1_000_000;
      log.error("EXCEPTION @Transactional: {} threw {} ({} ms)", methodName, t.getClass().getSimpleName(), ms);
      throw t; // Spring's exception handling (@RestControllerAdvice) can handle it globally so make sure to implement it the appropriate exception or catch it from the method its calling it.
     }
  }
}
```

**How to use:**
1. Make sure you have [spring-boot-starter-aop](https://mvnrepository.com/artifact/org.springframework.boot/spring-boot-starter-aop) on your classpath.
2. The aspect above will automatically log entry/exit for all `@Transactional` methods in your application.

**Sample log output:**
```
INFO  ... START @Transactional: CustomerService.register with args [Alice, alice@email.com]
INFO  ... END @Transactional: CustomerService.register -> CustomerResponse{id=...} (28 ms)
```

This way, you gain insight into all transactional operations, their inputs, outputs, and performance, with no clutter in your business logic.

## 4. Related notes

- **JPA & transactions** — [JPA & @Transactional](v-jpa-and-transactional.md)
- **REST validation & errors** — [REST controllers](iv-rest-controllers.md)
- **YAML logging levels** — [YAML & external config](ii-yaml-and-external-config.md)
