---
label: "II"
subtitle: "Java — Spring"
group: "Services"
order: 2
---
Service template — Java (Spring Boot)
**`@Service`** with constructor-injected repository. DTOs: [DTOs](../dtos/ii-java-spring.md) · controller: [Controllers](../controllers/ii-java-spring.md).

## Template

```java
package com.example.api.service;

import com.example.api.dto.CreateItemRequest;
import com.example.api.dto.ItemResponse;
import com.example.api.domain.Item;
import com.example.api.repository.ItemRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class ItemService {

  private final ItemRepository repository;

  public ItemService(ItemRepository repository) {
    this.repository = repository;
  }

  public List<ItemResponse> list() {
    return repository.findAll().stream().map(this::toResponse).toList();
  }

  public Optional<ItemResponse> get(long id) {
    return repository.findById(id).map(this::toResponse);
  }

  public ItemResponse create(CreateItemRequest request) {
    Item saved = repository.save(new Item(null, request.name()));
    return toResponse(saved);
  }

  public Optional<ItemResponse> update(long id, CreateItemRequest request) {
    return repository.findById(id)
        .map(existing -> repository.save(new Item(id, request.name())))
        .map(this::toResponse);
  }

  public boolean delete(long id) {
    return repository.deleteById(id);
  }

  private ItemResponse toResponse(Item item) {
    return new ItemResponse(item.id(), item.name());
  }
}
```

Repository interface (inject this — swap impl for DB later):

```java
package com.example.api.repository;

import com.example.api.domain.Item;
import java.util.List;
import java.util.Optional;

public interface ItemRepository {
  List<Item> findAll();
  Optional<Item> findById(long id);
  Item save(Item item);
  boolean deleteById(long id);
}
```

Domain record (internal — not exposed on the wire):

```java
package com.example.api.domain;

public record Item(Long id, String name) {}
```

## Notes

| Topic | Practice |
|-------|----------|
| **No HTTP types** | Return `Optional` / throw domain exceptions — map in controller |
| **Constructor injection** | Prefer over `@Autowired` fields |
| **Transactions** | `@Transactional` on service methods that write |
| **Demo repo** | In-memory `@Repository` impl is fine for learning |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Services overview](i-overview.md).
