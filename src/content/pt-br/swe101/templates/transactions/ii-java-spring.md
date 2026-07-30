---
label: "II"
subtitle: "Java — Spring"
group: "Transactions"
order: 2
---
Transaction template — Java (Spring Boot)
**`@Transactional` on service methods** — Spring opens/commits/rolls back around repository calls. Controllers never manage transactions.

Service context: [Services](../services/ii-java-spring.md) · repository: [Repositories](../repositories/ii-java-spring.md).

## Template

```java
package com.example.api.service;

import com.example.api.domain.Item;
import com.example.api.dto.CreateItemRequest;
import com.example.api.dto.ItemResponse;
import com.example.api.repository.ItemRepository;
import java.util.List;
import java.util.Optional;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class ItemService {

  private final ItemRepository repository;

  public ItemService(ItemRepository repository) {
    this.repository = repository;
  }

  @Transactional(readOnly = true)
  public List<ItemResponse> list() {
    return repository.findAll().stream().map(this::toResponse).toList();
  }

  @Transactional(readOnly = true)
  public Optional<ItemResponse> get(long id) {
    return repository.findById(id).map(this::toResponse);
  }

  @Transactional
  public ItemResponse create(CreateItemRequest request) {
    Item saved = repository.save(new Item(null, request.name()));
    return toResponse(saved);
  }

  @Transactional
  public Optional<ItemResponse> update(long id, CreateItemRequest request) {
    return repository.findById(id)
        .map(existing -> repository.save(new Item(id, request.name())))
        .map(this::toResponse);
  }

  @Transactional
  public boolean delete(long id) {
    return repository.deleteById(id);
  }

  private ItemResponse toResponse(Item item) {
    return new ItemResponse(item.id(), item.name());
  }
}
```

Multi-step write in one TX (extend `create` when you add related tables):

```java
@Transactional
public ItemResponse createWithAudit(CreateItemRequest request) {
  Item saved = repository.save(new Item(null, request.name()));
  auditRepository.insert(saved.id(), "created"); // same TX — rolls back together
  return toResponse(saved);
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Service only** | `@Transactional` on `@Service`, not `@RestController` |
| **readOnly = true** | Use on queries — hints Hibernate/JPA to skip unnecessary writes |
| **Rollback** | Unchecked exceptions roll back by default; checked exceptions need `rollbackFor` |
| **Self-invocation** | Calling `@Transactional` method from same class bypasses proxy — extract to another bean |
| **Propagation** | Default `REQUIRED` — nested service calls join one TX |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Transactions overview](i-overview.md).
