---
label: "II"
subtitle: "Java — Spring"
group: "DTOs"
order: 2
---
DTO template — Java (Spring Boot)
Request and response **records** with Bean Validation. Used by `@RestController` handlers — see [Controllers](../controllers/ii-java-spring.md).

## Dependencies

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

## Template

```java
package com.example.api.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/** Incoming body for POST / PUT — client does not send id. */
public record CreateItemRequest(
    @NotBlank(message = "name is required")
    @Size(max = 200, message = "name must be at most 200 characters")
    String name) {}

/** Outgoing JSON for every Item endpoint. */
public record ItemResponse(long id, String name) {}
```

Usage in a controller:

```java
@PostMapping
public ResponseEntity<ItemResponse> create(@Valid @RequestBody CreateItemRequest body) {
  // map body → service → ItemResponse
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Separate package** | `dto/` vs `domain/` vs `entity/` — never put a `*Dao` in `dto/` |
| **DTO ≠ DAO** | Records here are wire shapes; persistence belongs in [Repositories](../repositories/ii-java-spring.md) |
| **Validation** | Annotations on the request DTO; `@Valid` on the parameter |
| **Immutability** | Records are a good default for DTOs |
| **Mapping** | MapStruct or manual `new ItemResponse(entity.getId(), entity.getName())` |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [DTOs overview](i-overview.md).
