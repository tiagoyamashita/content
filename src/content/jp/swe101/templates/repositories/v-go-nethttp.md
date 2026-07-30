---
label: "V"
subtitle: "Go — net/http"
group: "Repositories"
order: 5
---
Repository template — Go (net/http)
**`Repository` interface + in-memory impl** for `Item` (`id`, `name`). Handlers depend on the interface.

## Template

```go
package repo

import (
	"sync"

	"github.com/google/uuid"
)

type Item struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type Repository interface {
	FindAll() []Item
	FindByID(id string) (Item, bool)
	Save(item Item) Item
	DeleteByID(id string) bool
}

type MemoryRepository struct {
	mu    sync.RWMutex
	store map[string]Item
}

func NewMemoryRepository() *MemoryRepository {
	return &MemoryRepository{store: make(map[string]Item)}
}

func (r *MemoryRepository) FindAll() []Item {
	r.mu.RLock()
	defer r.mu.RUnlock()
	out := make([]Item, 0, len(r.store))
	for _, item := range r.store {
		out = append(out, item)
	}
	return out
}

func (r *MemoryRepository) FindByID(id string) (Item, bool) {
	r.mu.RLock()
	defer r.mu.RUnlock()
	item, ok := r.store[id]
	return item, ok
}

func (r *MemoryRepository) Save(item Item) Item {
	if item.ID == "" {
		item.ID = uuid.NewString()
	}
	r.mu.Lock()
	r.store[item.ID] = item
	r.mu.Unlock()
	return item
}

func (r *MemoryRepository) DeleteByID(id string) bool {
	r.mu.Lock()
	_, ok := r.store[id]
	if ok {
		delete(r.store, id)
	}
	r.mu.Unlock()
	return ok
}
```

Wire in `main`: `items := repo.NewMemoryRepository()` and pass `items` into handler structs.

## Notes

| Topic | Practice |
|-------|----------|
| **Interface at call site** | Define `Repository` where handlers live, or in a small `repo` package |
| **SQL swap** | `PostgresRepository` with `*sql.DB` — same method set |
| **Context** | Add `ctx context.Context` as first param when you add real I/O |
| **Errors** | Return `(Item, error)` with sentinel `ErrNotFound` — map to HTTP in handlers |

## Next

[Repositories overview](i-overview.md) · [Templates overview](../i-overview.md).
