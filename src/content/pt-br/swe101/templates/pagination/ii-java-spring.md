---
label: "II"
subtitle: "Java — Spring"
group: "Pagination"
order: 2
---
Pagination template — Java (Spring Boot)
**Query params** + **response envelope** for listing `Item` (`id`, `name`). Controller wiring: [Controllers](../controllers/ii-java-spring.md) · DTOs: [DTOs](../dtos/ii-java-spring.md).

## Template code

```java
package com.example.api.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import java.util.List;

/** Offset-style query: GET /api/items?page=1&size=20 */
public record PageQuery(
    @Min(1) int page,
    @Min(1) @Max(100) int size) {

  public PageQuery {
    if (page < 1) page = 1;
    if (size < 1) size = 20;
    if (size > 100) size = 100;
  }

  public int offset() {
    return (page - 1) * size;
  }
}

/** Cursor-style query: GET /api/items?cursor=abc&limit=20 */
public record CursorQuery(
    String cursor,
    @Min(1) @Max(100) int limit) {

  public CursorQuery {
    if (limit < 1) limit = 20;
    if (limit > 100) limit = 100;
  }
}

public record ItemResponse(long id, String name) {}

/** Shared list envelope — include total only when cheap to compute. */
public record PagedItemResponse(
    List<ItemResponse> items,
    String nextCursor,
    Long total) {}
```

Controller stub:

```java
@GetMapping
public PagedItemResponse list(@Valid PageQuery query) {
  // service.listPage(query.offset(), query.size()) → PagedItemResponse
  return new PagedItemResponse(List.of(), null, 0L);
}

@GetMapping(params = "cursor")
public PagedItemResponse listByCursor(@Valid CursorQuery query) {
  // service.listAfterCursor(query.cursor(), query.limit())
  return new PagedItemResponse(List.of(), null, null);
}
```

Repository signature (bounded — never `findAll()` on the wire path):

```java
public interface ItemRepository {
  List<Item> findPage(int offset, int limit);
  long count(); // optional — omit from response when expensive

  List<Item> findAfterCursor(String cursor, int limit);
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Clamp `size`** | Defaults in the record compact constructor — don't trust the client |
| **`nextCursor`** | Encode last seen sort key (Base64 JSON or signed token) — opaque to clients |
| **`total`** | Use `Long` (nullable) — skip field when you don't run `COUNT(*)` |
| **Spring Data** | `Pageable` + `Page<T>` map cleanly to this envelope |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Pagination overview](i-overview.md).
