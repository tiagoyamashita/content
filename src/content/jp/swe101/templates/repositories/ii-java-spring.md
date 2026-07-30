---
label: "II"
subtitle: "Java — Spring"
group: "Repositories"
order: 2
---
Repository template — Java (Spring Boot)
**Interface + in-memory impl** for `Item` (`id`, `name`). In production, swap the impl for Spring Data **`JpaRepository`**.

## Template

```java
package com.example.repo;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;
import org.springframework.stereotype.Repository;

public record Item(long id, String name) {}

public interface ItemRepository {
  List<Item> findAll();

  Optional<Item> findById(long id);

  Item save(Item item);

  boolean deleteById(long id);
}

@Repository
class InMemoryItemRepository implements ItemRepository {
  private final AtomicLong seq = new AtomicLong(1);
  private final ConcurrentHashMap<Long, Item> store = new ConcurrentHashMap<>();

  @Override
  public List<Item> findAll() {
    return List.copyOf(store.values());
  }

  @Override
  public Optional<Item> findById(long id) {
    return Optional.ofNullable(store.get(id));
  }

  @Override
  public Item save(Item item) {
    long id = item.id() == 0 ? seq.getAndIncrement() : item.id();
    Item saved = new Item(id, item.name());
    store.put(id, saved);
    return saved;
  }

  @Override
  public boolean deleteById(long id) {
    return store.remove(id) != null;
  }
}

// Production swap — keep the same method names on a JPA entity:
// public interface ItemJpaRepository extends JpaRepository<ItemEntity, Long> {}
// Wire ItemJpaRepository (or an adapter) where ItemRepository is injected.
```

## Notes

| Topic | Practice |
|-------|----------|
| **Injection** | `@Service` depends on `ItemRepository`, not `InMemoryItemRepository` |
| **JPA swap** | Entity + `JpaRepository<ItemEntity, Long>`; map entity ↔ domain in an adapter |
| **Transactions** | `@Transactional` on the service, not the repository interface |
| **Testing** | In-memory impl or `@DataJpaTest` with Testcontainers |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [Repositories overview](i-overview.md).
