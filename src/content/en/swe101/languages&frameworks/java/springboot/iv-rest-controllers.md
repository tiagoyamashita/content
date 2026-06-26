---
label: "IV"
subtitle: "REST controllers"
group: "Spring Boot"
groupOrder: 2
order: 4
---
Spring Boot — Part IV
Expose HTTP APIs with **`@RestController`**, map paths and payloads, return **`ResponseEntity`** for status control, and centralize errors with **`@ControllerAdvice`**.

## 1. Controller skeleton
**`@RestController`** combines **`@Controller`** + **`@ResponseBody`** — return values serialize via Jackson by default.

```java
// Compile: javac --release 22 …
package com.example.demo.web;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import java.net.URI;
import java.util.Optional;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

@RestController
@RequestMapping("/api/customers")
public class CustomerController {

  private final CustomerService customers;

  public CustomerController(CustomerService customers) {
    this.customers = customers;
  }

  @GetMapping("/{id}")
  public ResponseEntity<CustomerResponse> get(@PathVariable UUID id) {
    return customers
        .find(id)
        .map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.notFound().build());
  }

  @PostMapping
  public ResponseEntity<CustomerResponse> create(@Valid @RequestBody CreateCustomerRequest body) {
    CustomerResponse created = customers.register(body.name(), body.email());
    URI location =
        ServletUriComponentsBuilder.fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(created.id())
            .toUri();
    return ResponseEntity.created(location).body(created);
  }

  @GetMapping
  public Iterable<CustomerResponse> search(@RequestParam(required = false) String q) {
    return customers.search(Optional.ofNullable(q).orElse(""));
  }
}
```

## 2. Request / response DTOs + validation
Keep entities out of the wire format — use dedicated records:

```java
// Compile: javac --release 22 …
public record CreateCustomerRequest(
    @NotBlank String name,
    @NotBlank String email
) {}

public record CustomerResponse(UUID id, String name, String email) {}
```

Enable **`jakarta.validation`** on incoming bodies with **`@Valid`** on the parameter (requires **`spring-boot-starter-validation`** on the classpath).

## 3. Mapping cheat sheet
| Annotation | Maps from |
|------------|-----------|
| **`@PathVariable`** | `/items/{id}` segment |
| **`@RequestParam`** | Query string `?page=1` |
| **`@RequestHeader`** | HTTP headers |
| **`@RequestBody`** | JSON / XML body |
| **`@RequestPart`** | **`multipart/form-data`** fields |

## 4. Status codes without exceptions
**`ResponseEntity`** wraps body + status + headers:

```java
// Compile: javac --release 22 …
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable UUID id) {
  boolean removed = customers.deleteIfExists(id);
  return removed ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
}
```

## 5. Global exception mapping
Return Problem Details–style payloads consistently:

```java
// Compile: javac --release 22 …
package com.example.demo.web.error;

import java.time.Instant;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
    String message =
        ex.getBindingResult().getFieldErrors().stream()
            .findFirst()
            .map(err -> err.getField() + ": " + err.getDefaultMessage())
            .orElse("Validation failed");
    return ResponseEntity.badRequest()
        .body(
            Map.of(
                "timestamp", Instant.now().toString(),
                "status", HttpStatus.BAD_REQUEST.value(),
                "error", "Bad Request",
                "message", message));
  }

  @ExceptionHandler(IllegalArgumentException.class)
  public ResponseEntity<Map<String, Object>> handleIllegalArgument(IllegalArgumentException ex) {
    return ResponseEntity.badRequest()
        .body(
            Map.of(
                "timestamp", Instant.now().toString(),
                "status", HttpStatus.BAD_REQUEST.value(),
                "message", ex.getMessage()));
  }
}
```

### Multiple `@RestControllerAdvice` beans
You may register **more than one** advice class in the same app — each is a normal Spring bean picked up by component scan. They do **not** scope per package unless you configure that explicitly.

**Default (no attributes)** — every **`@RestControllerAdvice`** applies **globally** to all controllers:

```java
// Compile: javac --release 22 …
@RestControllerAdvice
public class ApiExceptionHandler { /* … */ }

@RestControllerAdvice  // also global — not limited to its own package
public class LegacyExceptionHandler { /* … */ }
```

**Optional scoping** — limit an advice bean to certain controllers:

| Attribute | Effect |
|-----------|--------|
| **`basePackages`** | Controllers in that package and subpackages |
| **`basePackageClasses`** | Package of the given class |
| **`assignableTypes`** | Only listed controller types |
| **`annotations`** | Controllers carrying the annotation (e.g. **`RestController.class`**) |

```java
// Compile: javac --release 22 …
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice(basePackages = "com.example.demo.api")
@Order(Ordered.HIGHEST_PRECEDENCE)
public class ApiExceptionHandler { /* … */ }

@RestControllerAdvice(basePackages = "com.example.demo.admin")
public class AdminExceptionHandler { /* … */ }
```

A controller in **`com.example.demo.api.web`** uses **`ApiExceptionHandler`** (scoped) plus any **global** advice with no **`basePackages`**. Overlapping scopes are allowed — use **`@Order`** (lower number = higher priority) when two beans both handle the same exception type.

**How Spring picks a handler** when an exception leaves a controller:

1. **Filter** — keep advice beans whose scope includes the throwing controller (global advice always applies).
2. **Match** — collect **`@ExceptionHandler`** methods whose exception parameter type fits (subtypes count).
3. **Resolve** — more specific exception types beat generic ones; **`@Order`** breaks ties between advice classes.

| Pattern | When to use |
|---------|-------------|
| **One global advice** | Most apps — single handler for validation, domain errors, and a catch-all |
| **Global + scoped** | Shared defaults plus a module that needs a different error envelope |
| **Multiple globals + `@Order`** | Layered handlers (e.g. domain-specific at **`HIGHEST_PRECEDENCE`**, fallback at **`LOWEST_PRECEDENCE`**) |

**Multiple globals without `@Order`** — each advice bean defaults to **`Ordered.LOWEST_PRECEDENCE`**, so they all tie at the same priority. That is fine when each bean handles **different** exception types (Spring routes by type match). If two global beans both declare **`@ExceptionHandler`** for the **same** exception type, Spring picks one handler — not both, and not a chain — but **which** bean wins depends on registration order (often component-scan / classpath order) and can change after refactors. Do not rely on that; use **`@Order`** or remove duplicate handlers.

| Situation | Without `@Order` |
|-----------|------------------|
| Different exception types per advice | Safe |
| Same exception type in multiple globals | Unstable — assign **`@Order`** or consolidate |
| Overlapping global + scoped handlers | Scoped alone does not break the tie — still need **`@Order`** or dedupe |

**`@RestControllerAdvice`** vs **`@ControllerAdvice`** — **`@RestControllerAdvice`** adds **`@ResponseBody`** to every handler return value (JSON via Jackson). Use plain **`@ControllerAdvice`** when handlers return view names or **`ModelAndView`**.

## 6. CORS (when browsers call your API)
For simple demos only — tighten origins in production:

```java
// Compile: javac --release 22 …
@RestController
@CrossOrigin(origins = "http://localhost:5173")
@RequestMapping("/api/public")
public class PublicFeedController { /* … */ }
```

Prefer **`WebMvcConfigurer.addCorsMappings`** or gateway-level CORS for multiple controllers.

```java
// Compile: javac --release 22 …
package com.example.demo.web;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class CorsConfig implements WebMvcConfigurer {

  @Override
  public void addCorsMappings(CorsRegistry registry) {
    registry
        .addMapping("/api/**")
        .allowedOrigins("http://localhost:5173", "https://app.example.com")
        .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
        .allowedHeaders("*")
        .maxAge(3600);
  }
}
```

One config class covers every controller under **`/api/**`** — no per-controller **`@CrossOrigin`**. In production with many services, apply the same rules at an [API gateway](../../api-gateway/i-overview.md) so CORS is enforced once at the edge.

## 7. Related notes

- **Security basics & filter chain** — [Basics & filter chain](security-basics-and-filter-chain.md) (JWT, HTTP Basic for dev, method security)
- **Global errors with Problem Details** — pair **`@ControllerAdvice`** with **`ProblemDetail`** (Spring 6+) for RFC 7807 responses in new APIs

## 8. Problem Details (RFC 7807)
Section **5** builds error bodies with **`Map<String, Object>`** — fine for demos, but every handler invents its own field names. **[RFC 7807](https://www.rfc-editor.org/rfc/rfc7807)** defines a standard problem JSON shape clients can rely on: **`type`**, **`title`**, **`status`**, **`detail`**, and optional **`instance`**. Spring 6+ provides **`org.springframework.http.ProblemDetail`** so **`@RestControllerAdvice`** handlers return that shape without manual maps.

Typical response for a validation failure:

```json
{
  "type": "https://api.example.com/errors/validation",
  "title": "Invalid request",
  "status": 400,
  "detail": "email: must not be blank"
}
```

Spring sets **`Content-Type: application/problem+json`** when a handler method returns **`ProblemDetail`** directly.

### Throw in the service; advice maps to HTTP
The controller **never** calls the advice handler directly. Throw a domain exception from the **service** when business rules fail, call the service from the controller **without** **`try/catch`**, and let the exception bubble up — Spring MVC finds the matching **`@ExceptionHandler`** in any **`@RestControllerAdvice`** bean and turns it into the response.

That differs from §1’s **`Optional` → `ResponseEntity.notFound()`** pattern, which handles “not found” inside the controller. Both work; use exceptions + advice when you want the same **`ProblemDetail`** shape across many endpoints.

| Approach | Best for |
|----------|----------|
| **`Optional` → `ResponseEntity.notFound()`** | Simple reads; no shared error envelope |
| **Throw domain exception → `@ExceptionHandler`** | Consistent RFC 7807 bodies; extra context (`customerId`, …) |

Define the exception in the domain layer (not the web package) so services can throw it without depending on Spring MVC. Add your own **`CustomerNotFoundException.java`** source file — a plain **`RuntimeException`** subclass, not a Spring bean (full listing under **Validation errors** below).

The service decides “not found” and throws; the repository usually returns **`Optional.empty()`**:

```java
// Compile: javac --release 22 …
package com.example.demo.service;

import com.example.demo.domain.CustomerNotFoundException;
import java.util.UUID;
import org.springframework.stereotype.Service;

@Service
public class CustomerService {

  private final CustomerRepository customers;

  public CustomerService(CustomerRepository customers) {
    this.customers = customers;
  }

  public CustomerResponse find(UUID id) {
    return customers
        .findById(id)
        .map(c -> new CustomerResponse(c.getId(), c.getName(), c.getEmail()))
        .orElseThrow(() -> new CustomerNotFoundException(id));
  }
}
```

The controller stays thin — no **`try/catch`**, no manual 404 mapping:

```java
// Compile: javac --release 22 …
@GetMapping("/{id}")
public CustomerResponse get(@PathVariable UUID id) {
  return customers.find(id);  // may throw — ApiProblemHandler below handles it
}
```

### Validation errors: Spring throws; you shape the response
**`MethodArgumentNotValidException`** is a **Spring class** (`org.springframework.web.bind`) — you do **not** write it or register it as a bean. When a controller parameter has **`@Valid`** (§2) and Jakarta Validation fails (e.g. blank **`email`** on **`CreateCustomerRequest`**), Spring MVC throws this exception **before** your method body runs. Your **`@ExceptionHandler`** only customizes the **400** response body — validation itself is already built in (constraints on the DTO + **`@Valid`** + **`spring-boot-starter-validation`** on the classpath).

| Exception | Who throws it | You write a `.java` file? |
|-----------|---------------|---------------------------|
| **`MethodArgumentNotValidException`** | Spring automatically on **`@Valid`** failure | No — Spring provides the class |
| **`CustomerNotFoundException`** | Your service (`throw new …`) | Yes — your domain exception |

For validation, put **`@Valid`** on the controller parameter (§2) — Spring throws **`MethodArgumentNotValidException`** when constraints fail; no exception file needed:

```java
// Compile: javac --release 22 …
@PostMapping
public ResponseEntity<CustomerResponse> create(@Valid @RequestBody CreateCustomerRequest body) {
  CustomerResponse created = customers.register(body.name(), body.email());
  // …
}
```

For “not found”, create **`CustomerNotFoundException.java`** yourself — plain class, not a Spring bean. Spring Boot **does not** generate or register it: no **`@Component`**, no **`@Bean`**, no interface. You **`throw new CustomerNotFoundException(id)`** in the service; **`@ExceptionHandler(CustomerNotFoundException.class)`** matches that type when it bubbles up.

```java
// Compile: javac --release 22 …
// src/main/java/com/example/demo/domain/CustomerNotFoundException.java
package com.example.demo.domain;

import java.util.UUID;

public class CustomerNotFoundException extends RuntimeException {

  private final UUID id;

  public CustomerNotFoundException(UUID id) {
    super("Customer not found: " + id);
    this.id = id;
  }

  public UUID getId() {
    return id;
  }
}
```

Then throw it from the service: **`throw new CustomerNotFoundException(id)`** (see **`CustomerService.find`** above).

**`@RestControllerAdvice`** catches both — validation failures from Spring and domain exceptions you throw:

```java
// Compile: javac --release 22 …
package com.example.demo.web.error;

import com.example.demo.domain.CustomerNotFoundException;
import java.net.URI;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiProblemHandler {

  // Spring threw MethodArgumentNotValidException — map it to ProblemDetail
  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
    String detail =
        ex.getBindingResult().getFieldErrors().stream()
            .findFirst()
            .map(err -> err.getField() + ": " + err.getDefaultMessage())
            .orElse("Validation failed");
    ProblemDetail problem = ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, detail);
    problem.setTitle("Invalid request");
    problem.setType(URI.create("https://api.example.com/errors/validation"));
    return problem;
  }

  // Your service threw CustomerNotFoundException — map it to ProblemDetail
  @ExceptionHandler(CustomerNotFoundException.class)
  public ProblemDetail handleNotFound(CustomerNotFoundException ex) {
    ProblemDetail problem =
        ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    problem.setTitle("Customer not found");
    problem.setType(URI.create("https://api.example.com/errors/not-found"));
    problem.setProperty("customerId", ex.getId());
    return problem;
  }
}
```

Use **`ResponseEntity<ProblemDetail>`** when you need the request path in **`instance`** or extra response headers:

```java
// Compile: javac --release 22 …
import com.example.demo.domain.CustomerNotFoundException;
import jakarta.servlet.http.HttpServletRequest;

@ExceptionHandler(CustomerNotFoundException.class)
public ResponseEntity<ProblemDetail> handleNotFound(
    CustomerNotFoundException ex, HttpServletRequest request) {
  ProblemDetail problem =
      ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
  problem.setTitle("Customer not found");
  problem.setInstance(URI.create(request.getRequestURI()));
  return ResponseEntity.status(HttpStatus.NOT_FOUND).body(problem);
}
```

**`problem.setProperty("customerId", …)`** adds custom fields beside the RFC core keys — useful for machine-readable error codes without breaking the standard envelope. Prefer stable **`type`** URIs (or registered codes) over free-text **`title`** values when clients branch on error kind.

## 9. Automatic request logging
Do not add **`log.info`** to every controller method — register a **servlet filter** once and log method, path, status, and duration for **all** HTTP requests. Controllers from §1 stay unchanged.

```java
// Compile: javac --release 22 …
package com.example.demo.web;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class RequestLoggingFilter extends OncePerRequestFilter {

  private static final Logger log = LoggerFactory.getLogger(RequestLoggingFilter.class);

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {
    long start = System.nanoTime();
    try {
      chain.doFilter(request, response);
    } finally {
      long ms = (System.nanoTime() - start) / 1_000_000;
      log.info("{} {} -> {} ({} ms)",
          request.getMethod(), request.getRequestURI(), response.getStatus(), ms);
    }
  }
}
```

**`OncePerRequestFilter`** runs once per dispatch (including forwards) — safer than a raw **`Filter`**. **`@Component`** registers the bean; **`@Order(Ordered.HIGHEST_PRECEDENCE)`** runs it early so the elapsed time covers the full controller + service stack.

### Alternative: `@WebFilter` (Servlet API)
Spring Boot has **no** general **`@Filter`** annotation for HTTP filters. **`@WebFilter`** comes from **Jakarta Servlet** — it marks the class as a filter and sets URL patterns. Boot does **not** pick it up unless you add **`@ServletComponentScan`** on the application class. Do **not** also annotate the same class with **`@Component`** — that can register the filter twice.

```java
// Compile: javac --release 22 …
package com.example.demo.web;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebFilter;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.filter.OncePerRequestFilter;

@WebFilter(urlPatterns = "/api/*")
public class RequestLoggingFilter extends OncePerRequestFilter {

  private static final Logger log = LoggerFactory.getLogger(RequestLoggingFilter.class);

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {
    long start = System.nanoTime();
    try {
      chain.doFilter(request, response);
    } finally {
      long ms = (System.nanoTime() - start) / 1_000_000;
      log.info("{} {} -> {} ({} ms)",
          request.getMethod(), request.getRequestURI(), response.getStatus(), ms);
    }
  }
}
```

```java
// Compile: javac --release 22 …
package com.example.demo;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.web.servlet.ServletComponentScan;

@SpringBootApplication
@ServletComponentScan
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
```

| | **`@Component` + `@Order`** | **`@WebFilter` + `@ServletComponentScan`** |
|--|------------------------------|--------------------------------------------|
| **Registered by** | Spring Boot | Servlet container scan |
| **URL patterns** | All requests by default; narrow with **`FilterRegistrationBean`** | **`urlPatterns`** on **`@WebFilter`** |
| **Dependency injection** | Constructor injection works cleanly | Awkward — filter may be created before the Spring context |
| **Typical in Boot apps** | Preferred | Legacy / WAR-style deployments |

Do not confuse **`@WebFilter`** with **`@ComponentScan(… includeFilters …)`** — that controls which **classes become beans**, not HTTP request filtering. Spring Security filters are registered separately via a **`SecurityFilterChain`** bean.

Sample line in the console:

```text
GET /api/customers/550e8400-e29b-41d4-a716-446655440000 -> 200 (12 ms)
```

- Log at **`INFO`** for request summaries; tune **`logging.level.com.example.demo.web.RequestLoggingFilter`** in YAML if it is too chatty.
- Do **not** log bodies, headers, or query strings here — easy to leak tokens and PII. For correlation across service logs, add a trace ID to **`MDC`** in the same filter (see [Logging & pragmatic pitfalls](vii-logging-and-pragmatic-pitfalls.md)).

For **non-blocking** APIs (`Mono` / `Flux`, streaming, R2DBC), see [WebFlux & reactive APIs](xii-webflux.md).
