---
label: "II"
subtitle: "Java — Spring"
group: "Logging"
order: 2
---
Logging template — Java (Spring Boot)
Use **MDC** for automatic request context, a servlet filter for one access log, and a custom annotation + **Spring AOP** for reusable service-operation logs. Business methods stay free of repetitive entry/exit logging.

## `@LoggedOperation`

```java
package com.example.logging;

import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface LoggedOperation {
  String value();
}
```

## Operation aspect

```java
package com.example.logging;

import java.util.concurrent.TimeUnit;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class OperationLoggingAspect {
  private static final Logger log = LoggerFactory.getLogger(OperationLoggingAspect.class);

  @Around("@annotation(logged)")
  public Object logOperation(ProceedingJoinPoint joinPoint, LoggedOperation logged)
      throws Throwable {
    long started = System.nanoTime();
    try {
      Object result = joinPoint.proceed();
      log.info("event=operation.completed operation={} outcome=success durationMs={}",
          logged.value(), elapsedMs(started));
      return result;
    } catch (Throwable error) {
      log.error(
          "event=operation.completed operation={} outcome=error errorType={} durationMs={}",
          logged.value(), error.getClass().getSimpleName(), elapsedMs(started), error);
      throw error; // preserve transaction rollback and global error handling
    }
  }

  private static long elapsedMs(long started) {
    return TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - started);
  }
}
```

Use stable operation names and log safe domain events explicitly:

```java
@LoggedOperation("item.create")
@Transactional
public ItemResponse create(CreateItemRequest request) {
  Item saved = repository.save(new Item(request.name()));
  log.info("event=item.created itemId={}", saved.id());
  return ItemResponse.from(saved);
}
```

## Request context and access log

```java
package com.example.logging;

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
public class AccessLogFilter extends OncePerRequestFilter {
  private static final Logger log = LoggerFactory.getLogger(AccessLogFilter.class);

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {
    String requestId = request.getHeader("X-Request-Id");
    if (requestId == null || requestId.isBlank()) {
      requestId = UUID.randomUUID().toString();
    }

    long started = System.nanoTime();
    response.setHeader("X-Request-Id", requestId);
    try (MDC.MDCCloseable ignored = MDC.putCloseable("requestId", requestId)) {
      try {
        chain.doFilter(request, response);
      } finally {
        long durationMs =
            TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - started);
        log.info(
            "event=http.request.completed method={} path={} status={} durationMs={}",
            request.getMethod(), request.getRequestURI(),
            response.getStatus(), durationMs);
      }
    }
  }
}
```

## Dependencies

Add `spring-boot-starter-aop`. Spring Boot already provides SLF4J + Logback.

## Notes

| Topic | Practice |
|-------|----------|
| **No arguments/results** | Aspects must not dump DTOs, entities, or secrets |
| **MDC cleanup** | `MDC.putCloseable` prevents leakage across reused threads |
| **Exception ownership** | Aspect logs the stack once and rethrows |
| **JSON output** | Configure Logback JSON once; code continues emitting fields |
| **Async work** | MDC does not automatically cross executors—use a `TaskDecorator` or OTel context |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Logging overview](i-overview.md).
