---
label: "V"
subtitle: "Go — net/http"
group: "Transactions"
order: 5
---
Transaction template — Go (net/http)
**`sql.Tx` with explicit Begin / Commit / Rollback** — scope transactions in the service (or repository) layer. Handlers call service methods; service owns the unit of work.

Service context: [Services](../services/v-go-nethttp.md).

## Template

```go
package service

import (
	"context"
	"database/sql"
	"errors"

	"github.com/google/uuid"

	"example.com/api/dto"
)

type ItemService struct {
	db *sql.DB
}

func NewItemService(db *sql.DB) *ItemService {
	return &ItemService{db: db}
}

func (s *ItemService) Create(ctx context.Context, req dto.CreateItemRequest) (dto.ItemResponse, error) {
	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return dto.ItemResponse{}, err
	}
	defer tx.Rollback() // no-op after Commit

	id := uuid.NewString()
	_, err = tx.ExecContext(ctx,
		`INSERT INTO items (id, name) VALUES ($1, $2)`,
		id, req.Name,
	)
	if err != nil {
		return dto.ItemResponse{}, err
	}

	// Related write in same TX:
	// _, err = tx.ExecContext(ctx, `INSERT INTO item_audit ...`, id)
	// if err != nil { return dto.ItemResponse{}, err }

	if err := tx.Commit(); err != nil {
		return dto.ItemResponse{}, err
	}

	return dto.ItemResponse{ID: id, Name: req.Name}, nil
}

func (s *ItemService) Get(ctx context.Context, id string) (dto.ItemResponse, error) {
	var resp dto.ItemResponse
	err := s.db.QueryRowContext(ctx,
		`SELECT id, name FROM items WHERE id = $1`, id,
	).Scan(&resp.ID, &resp.Name)
	if errors.Is(err, sql.ErrNoRows) {
		return dto.ItemResponse{}, ErrNotFound
	}
	return resp, err
}
```

Reusable helper (optional — keep call sites in service methods):

```go
func withTx(ctx context.Context, db *sql.DB, fn func(*sql.Tx) error) error {
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		return err
	}
	defer tx.Rollback()
	if err := fn(tx); err != nil {
		return err
	}
	return tx.Commit()
}

// Usage:
// err := withTx(ctx, s.db, func(tx *sql.Tx) error {
//     _, err := tx.ExecContext(ctx, `INSERT INTO items ...`, ...)
//     return err
// })
```

Handler — pass `r.Context()`, no TX in handler:

```go
item, err := svc.Create(r.Context(), req)
if err != nil {
	mapError(w, err)
	return
}
writeJSON(w, http.StatusCreated, item)
```

## Notes

| Topic | Practice |
|-------|----------|
| **defer Rollback** | Safe after Commit (Rollback on committed TX returns `sql.ErrTxDone`) |
| **Context** | `BeginTx(ctx, nil)` — cancel propagates to in-flight queries |
| **Isolation** | Pass `&sql.TxOptions{Isolation: sql.LevelSerializable}` only when needed |
| **Repository pattern** | Accept `*sql.Tx` or `Querier` interface so repos run inside caller's TX |
| **No long TX** | Don't call external HTTP inside `withTx` — commit first |

## Next

[Transactions overview](i-overview.md) · [Templates overview](../i-overview.md).
