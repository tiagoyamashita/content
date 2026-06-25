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
