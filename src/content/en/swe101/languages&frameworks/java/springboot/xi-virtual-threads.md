---
label: "XI"
subtitle: "Virtual threads"
group: "Spring Boot"
groupOrder: 2
order: 7
---
Spring Boot — Part XI: Virtual threads
Run blocking MVC code on **virtual threads** so Tomcat can handle many concurrent I/O-bound requests without sizing a large platform-thread pool.

**Java baseline:** **Java SE 21+** (virtual threads); examples use **Java SE 22** (`javac --release 22`) and **Spring Boot 3.2+**. Language-level basics — **`Executors.newVirtualThreadPerTaskExecutor()`** — are in [Lambdas & modern Java](../intro/vi-lambdas-and-modern-java.md).

## 1. Platform threads vs virtual threads

| | **Platform thread** | **Virtual thread** |
|--|---------------------|-------------------|
| **Backed by** | One OS thread | JVM-managed, mounted on a small pool of carrier threads |
| **Cost** | Heavy (MB stack, kernel scheduling) | Lightweight (many thousands per JVM) |
| **Best for** | CPU-bound work, pinned `synchronized` hot paths | **I/O-bound** blocking code (HTTP client, JDBC, file I/O) |
| **Typical MVC app** | Default Tomcat pool (~200 threads) | One virtual thread per request when enabled |

Virtual threads are **not** reactive programming — your controller still **blocks** on JDBC and `RestTemplate`. The JVM parks a virtual thread while it waits instead of holding a scarce platform thread.

## 2. Where virtual threads help most

These are the Spring Boot shapes that benefit most — all **blocking**, all **I/O-bound**, often already written without WebFlux:

| Scenario | What blocks | Why virtual threads fit |
|----------|-------------|-------------------------|
| **CRUD REST + JPA** | JDBC round-trips per request | Thousands of requests can wait on the DB without exhausting Tomcat’s ~200 platform threads |
| **BFF / API aggregation** | Serial or parallel calls to other services (`RestClient`, `RestTemplate`, Feign) | Each outbound HTTP wait parks a virtual thread; fan-out per request stays simple blocking code |
| **Auth-heavy APIs** | JWT validation + DB user lookup + permission checks | Security filters and services block on cache/DB — same thread model, higher concurrency ceiling |
| **Third-party integrations** | Payment, shipping, KYC APIs with seconds of latency | Slow partners no longer tie up scarce platform threads for the whole pod |
| **Read-heavy traffic spikes** | Cache miss → DB, or search index round-trip | Burst traffic that used to queue at the servlet pool often improves p99 with one YAML toggle |
| **`@Async` side effects** | Fire-and-forget email, webhooks, audit export to object storage | Many concurrent outbound I/O tasks without tuning `corePoolSize` / `maxPoolSize` |
| **Long-lived HTTP** | SSE, long-polling, slow streaming downloads | Many idle or slow connections; virtual threads are cheaper to hold than platform threads |
| **Batch / scheduled jobs** | N parallel JDBC or HTTP fetches inside one job | `Executors.newVirtualThreadPerTaskExecutor()` for per-record I/O inside `@Scheduled` work |

**Common migration story:** a **blocking MVC** monolith or microservice that hit **thread-pool exhaustion** (503s, Tomcat accept queue growth) while CPU and DB pool were still healthy — enable virtual threads before rewriting to reactive stacks.

**Usually not the first lever:** low-traffic internal tools, CPU-bound endpoints (image/PDF generation, large in-memory transforms), or apps already on **WebFlux** with non-blocking drivers end-to-end.

### Example: BFF fan-out (blocking, I/O-bound)

```java
// Compile: javac --release 22 …
@Service
public class OrderDetailsService {

  private final OrderRepository orders;
  private final RestClient inventory;
  private final RestClient shipping;

  public OrderDetailsService(OrderRepository orders, RestClient inventory, RestClient shipping) {
    this.orders = orders;
    this.inventory = inventory;
    this.shipping = shipping;
  }

  public OrderDetailsDto load(UUID orderId) {
    var order = orders.findById(orderId).orElseThrow();
    // Each call blocks — on virtual threads, waits are cheap
    var stock = inventory.get().uri("/api/stock/{sku}", order.sku()).retrieve().body(StockDto.class);
    var tracking = shipping.get().uri("/api/tracking/{id}", orderId).retrieve().body(TrackingDto.class);
    return OrderDetailsDto.from(order, stock, tracking);
  }
}
```

For **parallel** fan-out, use **`ExecutorService`** with **`newVirtualThreadPerTaskExecutor()`** and **`Future`** / **`invokeAll`** — same pattern as [Lambdas & modern Java](../intro/vi-lambdas-and-modern-java.md), now with Tomcat also on virtual threads.

## 3. Turn on virtual threads in Boot

One property enables virtual threads for the embedded web server (Tomcat by default) and for Boot’s auto-configured async executor:

```yaml
spring:
  threads:
    virtual:
      enabled: true
```

**Maven / Gradle:** no extra starter — you need **JDK 21+** and a recent **Boot 3.2+** BOM. Confirm at runtime: log lines and thread dumps show names like **`tomcat-handler-0`** on virtual threads.

## 4. What stays the same

- **`@Transactional`** / JPA — transaction boundaries attach to the request thread; virtual threads participate like platform threads.
- **Blocking JDBC** — still blocks; you just block a virtual thread. Size **`spring.datasource.hikari.maximum-pool-size`** for **database** concurrency, not Tomcat thread count.
- **Spring Security filter chain** — runs on the same request thread model.

```java
// Compile: javac --release 22 …
@RestController
@RequestMapping("/api/orders")
public class OrderController {

  private final OrderService orders;

  public OrderController(OrderService orders) {
    this.orders = orders;
  }

  @GetMapping("/{id}")
  public OrderDto get(@PathVariable UUID id) {
    // Blocks on JDBC inside @Transactional service — fine on a virtual thread
    return orders.findById(id);
  }
}
```

## 5. `@Async` and custom executors

With **`spring.threads.virtual.enabled=true`**, Boot’s default **`applicationTaskExecutor`** uses virtual threads for **`@Async`** methods.

For explicit control:

```java
// Compile: javac --release 22 …
package com.example.demo.config;

import java.util.concurrent.Executors;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.task.TaskExecutor;
import org.springframework.core.task.support.TaskExecutorAdapter;
import org.springframework.scheduling.annotation.EnableAsync;

@Configuration
@EnableAsync
public class AsyncConfig {

  @Bean
  TaskExecutor applicationTaskExecutor() {
    return new TaskExecutorAdapter(Executors.newVirtualThreadPerTaskExecutor());
  }
}
```

Fire-and-forget work (email, webhooks) can scale concurrency without a fixed **`corePoolSize`** — still cap outbound rate to external systems.

## 6. Pitfalls (pragmatic)

- **Pinning:** long **`synchronized`** blocks or native code on the hot path can **pin** a virtual thread to its carrier and reduce gains. Prefer **`ReentrantLock`** for new code on hot paths; fix libraries that pin when profiling shows it.
- **Connection pools:** 10k concurrent virtual threads ≠ 10k DB connections. Pool size stays a **capacity** knob; virtual threads remove the **thread** bottleneck, not datastore limits.
- **`ThreadLocal` / MDC:** modern SLF4J + Logback propagate **MDC** across virtual threads when you set correlation IDs in a servlet filter — same pattern as platform threads (see [Logging & pragmatic pitfalls](vii-logging-and-pragmatic-pitfalls.md)).
- **CPU-bound `@Async`:** route CPU-heavy tasks to a **bounded platform-thread** `ExecutorService`, not **`newVirtualThreadPerTaskExecutor()`**.
- **Not WebFlux:** need backpressure and non-blocking end-to-end? **WebFlux** / reactive drivers are still the right tool. Virtual threads are for **keeping blocking code** at scale.

## 7. Observability

Thread names in logs help confirm the model:

```yaml
logging:
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n"
```

Under load, **`jcmd <pid> Thread.dump_to_file - -`** should show many **virtual** threads parked in socket or JDBC waits — expected for I/O-bound traffic.

Load-test before/after: compare p99 latency and error rate at the same RPS, not just “more threads.”

## 8. Related notes

- **Language-level virtual threads** — [Lambdas & modern Java](../intro/vi-lambdas-and-modern-java.md)
- **REST & filters** — [REST controllers](iv-rest-controllers.md)
- **Transactions on services** — [JPA & @Transactional](v-jpa-and-transactional.md)
- **YAML toggles per profile** — [YAML & external config](ii-yaml-and-external-config.md)
- **Pool exhaustion at scale** — [Application-level bottlenecks](../../../sysdesign/bottleneck-analysis/vii-application-level.md)
