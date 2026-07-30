---
label: "II"
subtitle: "Java — Spring"
group: "Concurrency"
order: 2
---
Concurrency template — Java (Spring Boot)
Spring MVC is **thread-per-request** (Tomcat pool). Keep beans stateless, offload slow work to a bounded executor, and parallelize independent outbound calls with `CompletableFuture`.

## Template code

```java
package com.example.api.concurrency;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.Executor;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.scheduling.annotation.Async;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.stereotype.Service;

@Configuration
class ExecutorConfig {

  /** Bounded pool — never use an unbounded executor in production. */
  @Bean(name = "itemExecutor")
  Executor itemExecutor() {
    ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
    ex.setCorePoolSize(8);
    ex.setMaxPoolSize(16);
    ex.setQueueCapacity(100);        // backpressure: reject when full
    ex.setThreadNamePrefix("item-");
    ex.initialize();
    return ex;
  }
}

@Service
public class ItemConcurrencyService {

  private final Executor executor;

  public ItemConcurrencyService(Executor itemExecutor) {
    this.executor = itemExecutor;
  }

  /** Fan out independent calls in parallel, then join. */
  public CombinedView loadCombined(String id) {
    CompletableFuture<Item> item =
        CompletableFuture.supplyAsync(() -> fetchItem(id), executor);
    CompletableFuture<List<String>> tags =
        CompletableFuture.supplyAsync(() -> fetchTags(id), executor);

    // join() blocks the request thread until both finish (or timeout upstream)
    return item.thenCombine(tags, CombinedView::new).join();
  }

  private Item fetchItem(String id) { /* repository / HTTP client */ return new Item(id, "Widget"); }
  private List<String> fetchTags(String id) { return List.of("a", "b"); }

  public record Item(String id, String name) {}
  public record CombinedView(Item item, List<String> tags) {}
}
```

Shared counter done safely (atomics instead of `synchronized` for simple cases):

```java
@Service
class RequestMetrics {
  private final AtomicLong served = new AtomicLong();   // thread-safe, lock-free
  long increment() { return served.incrementAndGet(); }
}
```

`@Async` for fire-and-forget on the bounded pool:

```java
@Async("itemExecutor")
public void reindexAsync(String id) { /* runs off the request thread */ }
```

## Capacity by version

Your capacity ceiling depends heavily on the JDK and Spring Boot version — state the minimum you assume.

| JDK / Spring Boot | Concurrency model | Practical ceiling |
|-------------------|-------------------|-------------------|
| **JDK 8–20** (any Boot) | Platform threads only | Blocked requests each pin an OS thread (~1 MB stack). Tomcat `server.tomcat.threads.max` (default **200**) caps concurrent blocking requests |
| **JDK 21+ LTS, Boot 3.2+** | **Virtual threads** (Project Loom) | Blocking I/O no longer thread-bound — hundreds of thousands of in-flight requests; ceiling moves to heap + DB/connection pool |
| **JDK 25 LTS** | Loom refinements | Same model as 21; fewer pinning cases (e.g. `synchronized`) |

Enable virtual threads (Boot 3.2+ on JDK 21+):

```properties
spring.threads.virtual.enabled=true
```

Capacity math on platform threads:

```text
max concurrent blocking requests  ≈  server.tomcat.threads.max   (default 200)
extra requests  ->  wait in accept queue  ->  latency + timeouts
```

**Watch out:** virtual threads make **blocking** cheap, but they don't remove **downstream** limits. If your DB pool is 20 connections, 50 000 virtual threads still queue on those 20. Size [connection pools](../repositories/i-overview.md) and pair with [Resilience](../resilience/i-overview.md) bulkheads. Pre-21, don't `join()` huge fan-outs on the request thread — you exhaust the Tomcat pool.

## Notes

| Topic | Practice |
|-------|----------|
| **Stateless beans** | Singletons are shared across threads — no mutable instance fields |
| **Bounded executor** | Set `maxPoolSize` + `queueCapacity`; avoid `Executors.newCachedThreadPool()` |
| **Shared state** | `AtomicLong`/`ConcurrentHashMap` over `synchronized` for hot paths |
| **Don't block twice** | Parallel `CompletableFuture` still ties up a request thread on `join()` — WebFlux avoids this |
| **Virtual threads (21+)** | `spring.threads.virtual.enabled=true` scales blocking I/O cheaply |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Concurrency overview](i-overview.md).
