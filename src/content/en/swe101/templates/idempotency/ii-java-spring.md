---
label: "II"
subtitle: "Java — Spring"
group: "Idempotency"
order: 2
---
Idempotency template — Java (Spring Boot)
**Filter or service guard** checks `Idempotency-Key` on `POST /items` before creating an Item. Store key → response; replay on retry; 409 on body mismatch.

Errors: [Errors](../errors/ii-java-spring.md) · service: [Services](../services/ii-java-spring.md).

## Template

Idempotency store (interface — swap Redis / JDBC impl):

```java
package com.example.api.idempotency;

import java.time.Instant;
import java.util.Optional;

public record IdempotencyRecord(
    String bodyHash,
    int statusCode,
    String responseBody,
    Instant expiresAt) {}

public interface IdempotencyStore {
  Optional<IdempotencyRecord> find(String key);
  void save(String key, IdempotencyRecord record);
}
```

Service — check before create:

```java
package com.example.api.service;

import com.example.api.domain.Item;
import com.example.api.dto.CreateItemRequest;
import com.example.api.dto.ItemResponse;
import com.example.api.idempotency.IdempotencyRecord;
import com.example.api.idempotency.IdempotencyStore;
import com.example.api.repository.ItemRepository;
import com.example.api.idempotency.IdempotencyStore;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.HexFormat;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

public class IdempotencyConflictException extends RuntimeException {
  public IdempotencyConflictException(String message) {
    super(message);
  }
}

@Service
public class ItemService {

  private final ItemRepository repository;
  private final IdempotencyStore idempotencyStore;

  public ItemService(ItemRepository repository, IdempotencyStore idempotencyStore) {
    this.repository = repository;
    this.idempotencyStore = idempotencyStore;
  }

  public record IdempotentResult(int statusCode, String body, boolean replayed) {}

  @Transactional
  public IdempotentResult createIdempotent(
      String idempotencyKey, CreateItemRequest request) {

    String bodyHash = hash(request.name());
    var existing = idempotencyStore.find(idempotencyKey);

    if (existing.isPresent()) {
      IdempotencyRecord rec = existing.get();
      if (!rec.bodyHash().equals(bodyHash)) {
        throw new IdempotencyConflictException("Idempotency-Key reused with different body");
      }
      return new IdempotentResult(rec.statusCode(), rec.responseBody(), true);
    }

    Item saved = repository.save(new Item(null, request.name()));
    ItemResponse created = new ItemResponse(saved.id(), saved.name());
    String json = toJson(created); // Jackson ObjectMapper in real app

    idempotencyStore.save(idempotencyKey, new IdempotencyRecord(
        bodyHash, 201, json, Instant.now().plusSeconds(86_400)));

    return new IdempotentResult(201, json, false);
  }

  private static String hash(String canonicalBody) {
    try {
      MessageDigest md = MessageDigest.getInstance("SHA-256");
      byte[] digest = md.digest(canonicalBody.getBytes(StandardCharsets.UTF_8));
      return HexFormat.of().formatHex(digest);
    } catch (Exception e) {
      throw new IllegalStateException(e);
    }
  }

  private String toJson(ItemResponse item) {
    return "{\"id\":" + item.id() + ",\"name\":\"" + item.name() + "\"}";
  }
}
```

Filter stub (read header, short-circuit only if you prefer HTTP-edge handling):

```java
@Component
@Order(Ordered.HIGHEST_PRECEDENCE + 10)
public class IdempotencyKeyFilter extends OncePerRequestFilter {

  @Override
  protected void doFilterInternal(
      HttpServletRequest request, HttpServletResponse response, FilterChain chain)
      throws ServletException, IOException {

    if ("POST".equalsIgnoreCase(request.getMethod())
        && request.getRequestURI().endsWith("/items")) {
      String key = request.getHeader("Idempotency-Key");
      if (key == null || key.isBlank()) {
        response.sendError(400, "Idempotency-Key required");
        return;
      }
      request.setAttribute("idempotencyKey", key);
    }
    chain.doFilter(request, response);
  }
}
```

Controller passes key to service:

```java
@PostMapping("/items")
public ResponseEntity<String> create(
    @RequestAttribute("idempotencyKey") String key,
    @RequestBody CreateItemRequest body) {

  var result = itemService.createIdempotent(key, body);
  return ResponseEntity.status(result.statusCode()).body(result.body());
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **TX + store** | Save idempotency record in same TX as insert — or use outbox pattern |
| **409 mapping** | `IdempotencyConflictException` → 409 in `@RestControllerAdvice` |
| **Header validation** | Reject empty keys; optional max length |
| **Filter vs service** | Filter validates presence; service owns lookup/replay logic |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Idempotency overview](i-overview.md).
