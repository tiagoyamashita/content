---
label: "II"
subtitle: "Java — Spring"
group: "Middleware"
order: 2
---
Middleware template — Java (Spring Boot)
**`OncePerRequestFilter`** adding **`X-Request-Id`**, optional logging, and a stub user id on the request.

## Template

```java
package com.example.middleware;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
public class RequestContextFilter extends OncePerRequestFilter {
  private static final Logger log = LoggerFactory.getLogger(RequestContextFilter.class);
  public static final String REQUEST_ID = "requestId";

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {
    long start = System.currentTimeMillis();
    String requestId = request.getHeader("X-Request-Id");
    if (requestId == null || requestId.isBlank()) {
      requestId = UUID.randomUUID().toString();
    }
    request.setAttribute(REQUEST_ID, requestId);
    response.setHeader("X-Request-Id", requestId);

    // Auth stub — replace with SecurityContext / JWT
    String userId = request.getHeader("X-User-Id");
    if (userId != null) {
      request.setAttribute("userId", userId);
    }

    try {
      chain.doFilter(request, response);
    } finally {
      long ms = System.currentTimeMillis() - start;
      log.info("{} {} {} {} {}ms", requestId, request.getMethod(), request.getRequestURI(),
          response.getStatus(), ms);
    }
  }
}
```

Spring Boot auto-registers `@Component` filters. Read `request.getAttribute(REQUEST_ID)` in controllers.

## Notes

| Topic | Practice |
|-------|----------|
| **OncePerRequestFilter** | Runs once per dispatch — safe for forwards/includes |
| **MDC logging** | `MDC.put("requestId", requestId)` for structured logs |
| **Spring Security** | Replace header stub with `JwtAuthenticationFilter` |
| **Order** | `@Order(Ordered.HIGHEST_PRECEDENCE)` if multiple filters |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Middleware overview](i-overview.md).
