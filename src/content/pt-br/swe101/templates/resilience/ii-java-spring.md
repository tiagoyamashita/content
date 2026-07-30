---
label: "II"
subtitle: "Java — Spring"
group: "Resilience"
order: 2
---
Resilience template — Java (Spring Boot)
**RestClient** with explicit timeouts and retry guidance. Outbound setup: [HTTP clients](../http-clients/ii-java-spring.md).

## Dependencies

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<!-- Optional production resilience -->
<!--
<dependency>
  <groupId>io.github.resilience4j</groupId>
  <artifactId>resilience4j-spring-boot3</artifactId>
</dependency>
-->
```

## Template code

```java
package com.example.api.client;

import java.time.Duration;
import java.util.List;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

@Component
public class CatalogClient {

  private final RestClient restClient;

  public CatalogClient(RestClient.Builder builder) {
    SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
    factory.setConnectTimeout(Duration.ofSeconds(2));
    factory.setReadTimeout(Duration.ofSeconds(5));

    this.restClient = builder
        .baseUrl("https://catalog.example.com")
        .requestFactory(factory)
        .build();
  }

  /** Idempotent GET — safe to retry on transient failure. */
  public List<ItemDto> listItems() {
    return withSimpleRetry(
        () -> restClient.get()
            .uri("/api/items")
            .retrieve()
            .body(new org.springframework.core.ParameterizedTypeReference<List<ItemDto>>() {}),
        3);
  }

  /** POST — do NOT retry blindly; use idempotency keys in production. */
  public ItemDto createItem(CreateItemDto body) {
    return restClient.post()
        .uri("/api/items")
        .body(body)
        .retrieve()
        .body(ItemDto.class);
  }

  /**
   * Teaching stub — prefer Resilience4j @Retry / @CircuitBreaker in production.
   *
   * resilience4j.retry:
   *   instances:
   *     catalog:
   *       maxAttempts: 3
   *       waitDuration: 200ms
   *
   * @Retry(name = "catalog")
   * public List<ItemDto> listItems() { ... }
   *
   * resilience4j.circuitbreaker:
   *   instances:
   *     catalog:
   *       slidingWindowSize: 10
   *       failureRateThreshold: 50
   *
   * @CircuitBreaker(name = "catalog", fallbackMethod = "listItemsFallback")
   */
  private <T> T withSimpleRetry(RetryableCall<T> call, int maxAttempts) {
    RestClientException last = null;
    for (int attempt = 1; attempt <= maxAttempts; attempt++) {
      try {
        return call.run();
      } catch (RestClientException ex) {
        last = ex;
        if (attempt == maxAttempts) break;
        sleepBackoff(attempt);
      }
    }
    throw last;
  }

  private static void sleepBackoff(int attempt) {
    try {
      Thread.sleep(100L * (1L << (attempt - 1))); // 100ms, 200ms, ...
    } catch (InterruptedException ie) {
      Thread.currentThread().interrupt();
    }
  }

  /** Graceful degradation when circuit is open or upstream is down. */
  public List<ItemDto> listItemsFallback(Throwable t) {
    return List.of(); // or cached snapshot
  }

  @FunctionalInterface
  private interface RetryableCall<T> {
    T run();
  }

  public record ItemDto(String id, String name) {}
  public record CreateItemDto(String name) {}
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Timeouts** | `connectTimeout` + `readTimeout` on the request factory — mandatory |
| **Retry scope** | Only idempotent reads — never default-retry POST |
| **Resilience4j** | Use `@Retry`, `@CircuitBreaker`, `@TimeLimiter` instead of hand-rolled loops |
| **Fallback** | Return empty/cached data — don't mask errors silently in admin paths |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Resilience overview](i-overview.md).
