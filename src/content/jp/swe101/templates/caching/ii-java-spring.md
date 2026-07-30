---
label: "II"
subtitle: "Java — Spring"
group: "Caching"
order: 2
---
Caching template — Java (Spring Boot)
**`ETag` + `Cache-Control`** on GET item; return **304** when `If-None-Match` matches. Spring's `ShallowEtagHeaderFilter` can automate ETags — shown here explicitly for clarity.

## Template

```java
package com.example.caching;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.HexFormat;
import org.springframework.http.CacheControl;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

record ItemResponse(long id, String name, String updatedAt) {}

@RestController
@RequestMapping("/api/items")
public class ItemController {

  @GetMapping("/{id}")
  public ResponseEntity<ItemResponse> get(
      @PathVariable long id,
      @RequestHeader(value = HttpHeaders.IF_NONE_MATCH, required = false) String ifNoneMatch) {
    ItemResponse item = loadItem(id); // service + optional Redis
    if (item == null) {
      return ResponseEntity.notFound().build();
    }

    String etag = computeEtag(item);
    if (etag.equals(ifNoneMatch)) {
      return ResponseEntity.status(HttpStatus.NOT_MODIFIED)
          .eTag(etag)
          .cacheControl(CacheControl.maxAge(60).cachePublic())
          .build();
    }

    return ResponseEntity.ok()
        .eTag(etag)
        .cacheControl(CacheControl.maxAge(60).cachePublic())
        .body(item);
  }

  private ItemResponse loadItem(long id) {
    // TODO: redis.get("item:" + id) → on miss, repository.findById
    return new ItemResponse(id, "Widget", "2026-07-20T12:00:00Z");
  }

  private static String computeEtag(ItemResponse item) {
    String payload = item.id() + "|" + item.name() + "|" + item.updatedAt();
    try {
      byte[] hash = MessageDigest.getInstance("SHA-256")
          .digest(payload.getBytes(StandardCharsets.UTF_8));
      return "\"" + HexFormat.of().formatHex(hash, 0, 8) + "\"";
    } catch (Exception e) {
      throw new IllegalStateException(e);
    }
  }
}
```

On `PUT` / `DELETE`: `@CacheEvict` (Spring Cache) or manual `redis.delete("item:" + id)`.

## Notes

| Topic | Practice |
|-------|----------|
| **Quoted ETags** | HTTP spec expects `"value"` — Spring's `.eTag()` handles quoting |
| **ShallowEtagHeaderFilter** | Auto-ETag on response body — good default for simple APIs |
| **Conditional GET only** | ETags on GET; mutations return `no-store` |
| **Personalized items** | `CacheControl.maxAge(0).cachePrivate()` or skip caching |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Caching overview](i-overview.md).
