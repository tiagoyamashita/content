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
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable UUID id) {
  boolean removed = customers.deleteIfExists(id);
  return removed ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
}
```

## 5. Global exception mapping
Return Problem Details–style payloads consistently:

```java
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
@RestController
@CrossOrigin(origins = "http://localhost:5173")
@RequestMapping("/api/public")
public class PublicFeedController { /* … */ }
```

Prefer **`WebMvcConfigurer.addCorsMappings`** or gateway-level CORS for multiple controllers.
