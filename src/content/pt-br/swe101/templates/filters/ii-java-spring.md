---
label: "II"
subtitle: "Java — Spring"
group: "Filters"
order: 2
---
Filter template — Java (Spring Boot)
**Servlet filters** for edge policy — rate limiting and security headers. Basic request ID / logging stays in [Middleware](../middleware/ii-java-spring.md).

## Template (security headers + body limit)

```java
package com.example.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 10)
public class EdgePolicyFilter extends OncePerRequestFilter {

  private static final long MAX_BYTES = 1_048_576; // 1 MiB

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {

    applySecurityHeaders(response);

    if (isMutating(request) && exceedsMaxBody(request)) {
      response.sendError(HttpServletResponse.SC_REQUEST_ENTITY_TOO_LARGE, "payload too large");
      return;
    }

    if (isMutating(request) && !isJson(request)) {
      response.sendError(HttpServletResponse.SC_UNSUPPORTED_MEDIA_TYPE, "application/json required");
      return;
    }

    chain.doFilter(request, response);
  }

  private void applySecurityHeaders(HttpServletResponse response) {
    response.setHeader("X-Content-Type-Options", "nosniff");
    response.setHeader("X-Frame-Options", "DENY");
    response.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
    // response.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
  }

  private boolean isMutating(HttpServletRequest request) {
    String method = request.getMethod();
    return "POST".equals(method) || "PUT".equals(method) || "PATCH".equals(method);
  }

  private boolean exceedsMaxBody(HttpServletRequest request) {
    long length = request.getContentLengthLong();
    return length > MAX_BYTES;
  }

  private boolean isJson(HttpServletRequest request) {
    String contentType = request.getContentType();
    return contentType != null && contentType.startsWith(MediaType.APPLICATION_JSON_VALUE);
  }
}
```

## Template (rate limit stub)

```java
package com.example.filter;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import org.springframework.boot.web.servlet.FilterRegistrationBean;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.filter.OncePerRequestFilter;

@Configuration
public class RateLimitFilterConfig {

  private static final int MAX_PER_MINUTE = 60;

  @Bean
  public FilterRegistrationBean<OncePerRequestFilter> rateLimitFilter() {
    ConcurrentHashMap<String, AtomicInteger> counts = new ConcurrentHashMap<>();

    OncePerRequestFilter filter = new OncePerRequestFilter() {
      @Override
      protected void doFilterInternal(
          HttpServletRequest request, HttpServletResponse response, FilterChain chain)
          throws ServletException, IOException {
        String key = request.getRemoteAddr();
        int count = counts.computeIfAbsent(key, k -> new AtomicInteger(0)).incrementAndGet();
        if (count > MAX_PER_MINUTE) {
          response.setStatus(429);
          response.setHeader("Retry-After", "60");
          response.getWriter().write("{\"error\":\"rate limit exceeded\"}");
          return;
        }
        chain.doFilter(request, response);
      }
    };

    FilterRegistrationBean<OncePerRequestFilter> bean = new FilterRegistrationBean<>(filter);
    bean.addUrlPatterns("/api/*");
    bean.setOrder(20);
    return bean;
  }
}
```

Use **`FilterRegistrationBean`** when you need explicit URL patterns and order — not every filter needs `@Component` auto-registration.

## HandlerInterceptor (controller-scoped timing)

```java
package com.example.filter;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

@Component
public class ControllerTimingInterceptor implements HandlerInterceptor {
  private static final Logger log = LoggerFactory.getLogger(ControllerTimingInterceptor.class);
  private static final String START = "controllerStartMs";

  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
    request.setAttribute(START, System.currentTimeMillis());
    return true;
  }

  @Override
  public void afterCompletion(
      HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
    Long start = (Long) request.getAttribute(START);
    if (start != null) {
      log.info("controller {} ms", System.currentTimeMillis() - start);
    }
  }
}
```

Register via `WebMvcConfigurer#addInterceptors` — runs **after** servlet filters, only for dispatched controller handlers.

## Notes

| Topic | Practice |
|-------|----------|
| **OncePerRequestFilter** | Prefer over raw `Filter` — one execution per request |
| **Order** | `@Order` or `FilterRegistrationBean#setOrder` — document the chain |
| **Filter vs interceptor** | Body size / rate limit = servlet filter; per-handler timing = interceptor |
| **Spring Security** | Security filter chain is separate — don't duplicate auth here |
| **Production limits** | Replace in-memory map with Redis + sliding window |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Filters overview](i-overview.md) · [Middleware](../middleware/i-overview.md).
