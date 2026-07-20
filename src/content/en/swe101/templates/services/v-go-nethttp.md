---
label: "V"
subtitle: "Go — net/http"
group: "Services"
order: 5
---
Service template — Go (net/http)
**`ItemService`** struct with repository interface — handlers stay thin. DTOs: [DTOs](../dtos/v-go-nethttp.md) · handlers: [Controllers](../controllers/v-go-nethttp.md).

## Template

```go
package service

import (
	"errors"

	"github.com/google/uuid"

	"example.com/api/domain"
	"example.com/api/dto"
	"example.com/api/repository"
)

var ErrNotFound = errors.New("not found")

type ItemService struct {
	repo repository.ItemRepository
}

func NewItemService(repo repository.ItemRepository) *ItemService {
	return &ItemService{repo: repo}
}

func (s *ItemService) List() ([]dto.ItemResponse, error) {
	items, err := s.repo.FindAll()
	if err != nil {
		return nil, err
	}
	out := make([]dto.ItemResponse, len(items))
	for i, item := range items {
		out[i] = toResponse(item)
	}
	return out, nil
}

func (s *ItemService) Get(id string) (dto.ItemResponse, error) {
	item, err := s.repo.FindByID(id)
	if err != nil {
		return dto.ItemResponse{}, err
	}
	if item == nil {
		return dto.ItemResponse{}, ErrNotFound
	}
	return toResponse(*item), nil
}

func (s *ItemService) Create(req dto.CreateItemRequest) (dto.ItemResponse, error) {
	item := domain.Item{ID: uuid.NewString(), Name: req.Name}
	saved, err := s.repo.Save(item)
	if err != nil {
		return dto.ItemResponse{}, err
	}
	return toResponse(saved), nil
}

func (s *ItemService) Update(id string, req dto.CreateItemRequest) (dto.ItemResponse, error) {
	existing, err := s.repo.FindByID(id)
	if err != nil {
		return dto.ItemResponse{}, err
	}
	if existing == nil {
		return dto.ItemResponse{}, ErrNotFound
	}
	updated := domain.Item{ID: id, Name: req.Name}
	saved, err := s.repo.Save(updated)
	if err != nil {
		return dto.ItemResponse{}, err
	}
	return toResponse(saved), nil
}

func (s *ItemService) Delete(id string) error {
	ok, err := s.repo.DeleteByID(id)
	if err != nil {
		return err
	}
	if !ok {
		return ErrNotFound
	}
	return nil
}

func toResponse(item domain.Item) dto.ItemResponse {
	return dto.ItemResponse{ID: item.ID, Name: item.Name}
}
```

Repository interface:

```go
package repository

import "example.com/api/domain"

type ItemRepository interface {
	FindAll() ([]domain.Item, error)
	FindByID(id string) (*domain.Item, error)
	Save(item domain.Item) (domain.Item, error)
	DeleteByID(id string) (bool, error)
}
```

Domain type:

```go
package domain

type Item struct {
	ID   string
	Name string
}
```

Handler wiring:

```go
svc := service.NewItemService(memory.NewItemRepository())

item, err := svc.Get(id)
if errors.Is(err, service.ErrNotFound) {
	writeJSON(w, http.StatusNotFound, map[string]string{"error": "Not found"})
	return
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Interface injection** | `ItemRepository` in constructor — mock in tests |
| **Sentinel errors** | `ErrNotFound` — map to 404 in handlers |
| **No `http` imports** | Keep service package free of net/http |
| **Context** | Add `context.Context` as first param when calling DB |

## Next

[Services overview](i-overview.md) · [Templates overview](../i-overview.md).
