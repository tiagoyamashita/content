---
label: "II"
subtitle: "Java — Spring"
group: "Controllers"
order: 2
---
Controller template — Java (Spring Boot)
Minimal **`@RestController`** for a resource. Full track: [REST controllers](../../languages&frameworks/java/springboot/iv-rest-controllers.md).

## Dependencies

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

## Template

```java
package com.example.api;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import java.net.URI;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

record CreateItemRequest(@NotBlank String name) {}

record ItemResponse(long id, String name) {}

@RestController
@RequestMapping("/api/items")
public class ItemController {

  // Demo only — replace with a service + repository
  private final AtomicLong seq = new AtomicLong(1);
  private final Map<Long, ItemResponse> store = new ConcurrentHashMap<>();

  @GetMapping
  public List<ItemResponse> list() {
    return List.copyOf(store.values());
  }

  @GetMapping("/{id}")
  public ResponseEntity<ItemResponse> get(@PathVariable long id) {
    ItemResponse item = store.get(id);
    return item == null ? ResponseEntity.notFound().build() : ResponseEntity.ok(item);
  }

  @PostMapping
  public ResponseEntity<ItemResponse> create(@Valid @RequestBody CreateItemRequest body) {
    long id = seq.getAndIncrement();
    ItemResponse created = new ItemResponse(id, body.name());
    store.put(id, created);
    return ResponseEntity.created(URI.create("/api/items/" + id)).body(created);
  }

  @PutMapping("/{id}")
  public ResponseEntity<ItemResponse> update(
      @PathVariable long id, @Valid @RequestBody CreateItemRequest body) {
    if (!store.containsKey(id)) {
      return ResponseEntity.notFound().build();
    }
    ItemResponse updated = new ItemResponse(id, body.name());
    store.put(id, updated);
    return ResponseEntity.ok(updated);
  }

  @DeleteMapping("/{id}")
  public ResponseEntity<Void> delete(@PathVariable long id) {
    return store.remove(id) == null
        ? ResponseEntity.notFound().build()
        : ResponseEntity.noContent().build();
  }
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Thin controller** | Move `store` into `ItemService` in real apps |
| **Validation** | `@Valid` + `@ControllerAdvice` for consistent 400s |
| **IDs** | Prefer UUID or DB-generated keys over `AtomicLong` |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Controllers overview](i-overview.md).
