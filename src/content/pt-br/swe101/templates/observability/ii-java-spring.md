---
label: "II"
subtitle: "Java — Spring"
group: "Observability"
order: 2
---
Observability template — Java (Spring Boot)
**Micrometer timer** for request duration + **MDC** for `requestId` in structured logs. Spring Boot Actuator exposes `/actuator/prometheus` when configured.

## Template

```java
package com.example.observability;

import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;
import java.util.concurrent.TimeUnit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
public class ObservabilityFilter extends OncePerRequestFilter {
  private static final Logger log = LoggerFactory.getLogger(ObservabilityFilter.class);
  private final Timer requestTimer;

  public ObservabilityFilter(MeterRegistry registry) {
    this.requestTimer = Timer.builder("http.server.requests")
        .description("HTTP request duration")
        .tag("application", "items-api")
        .register(registry);
  }

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {
    long start = System.nanoTime();
    String requestId = request.getHeader("X-Request-Id");
    if (requestId == null || requestId.isBlank()) {
      requestId = UUID.randomUUID().toString();
    }
    response.setHeader("X-Request-Id", requestId);
    MDC.put("requestId", requestId);

    try {
      chain.doFilter(request, response);
    } finally {
      long ns = System.nanoTime() - start;
      requestTimer.record(ns, TimeUnit.NANOSECONDS);
      log.info("request completed method={} path={} status={} durationMs={}",
          request.getMethod(), request.getRequestURI(), response.getStatus(), ns / 1_000_000);
      MDC.clear();
    }
  }
}
```

Controller usage — log with MDC already populated:

```java
@GetMapping("/{id}")
public ResponseEntity<ItemResponse> get(@PathVariable long id) {
  log.debug("fetching item id={}", id);
  // ...
}
```

OpenTelemetry (optional): add `opentelemetry-spring-boot-starter` — spans auto-wrap MVC dispatch; MDC can include `traceId` via OTel log bridge.

## Notes

| Topic | Practice |
|-------|----------|
| **Micrometer** | Use route tags via `@Timed` or `WebMvcTagsProvider` — avoid per-id labels |
| **MDC** | Always `MDC.clear()` in `finally` — thread pools reuse threads |
| **Actuator** | `management.endpoints.web.exposure.include=health,prometheus` |
| **Logback JSON** | `logstash-logback-encoder` for ELK / Cloud Logging |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Observability overview](i-overview.md).
