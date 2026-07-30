---
label: "II"
subtitle: "Java — Spring"
group: "Errors"
order: 2
---
Error template — Java (Spring Boot)
**Domain exception + `@RestControllerAdvice`** mapping to HTTP. Uses Spring 6 **`ProblemDetail`** (RFC 7807); swap to a simple JSON map if you prefer.

## Template

```java
package com.example.error;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

public class NotFoundException extends RuntimeException {
  public NotFoundException(String message) {
    super(message);
  }
}

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(NotFoundException.class)
  public ProblemDetail handleNotFound(NotFoundException ex) {
    ProblemDetail detail = ProblemDetail.forStatusAndDetail(
        HttpStatus.NOT_FOUND, ex.getMessage());
    detail.setTitle("Not Found");
    detail.setProperty("code", "NOT_FOUND");
    return detail;
  }

  // Simple JSON alternative:
  // @ExceptionHandler(NotFoundException.class)
  // public ResponseEntity<Map<String, String>> handleNotFound(NotFoundException ex) {
  //   return ResponseEntity.status(404).body(Map.of("error", ex.getMessage()));
  // }
}
```

Usage in a service or controller:

```java
Item item = itemRepository.findById(id)
    .orElseThrow(() -> new NotFoundException("Item not found"));
```

## Notes

| Topic | Practice |
|-------|----------|
| **Throw in service** | Keep controllers free of `ResponseEntity.notFound()` branches |
| **ProblemDetail** | Built-in since Spring 6; good default for APIs |
| **Validation** | `@ExceptionHandler(MethodArgumentNotValidException.class)` → 400 |
| **Catch-all** | Log + generic 500 handler — never expose internals |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Errors overview](i-overview.md).
