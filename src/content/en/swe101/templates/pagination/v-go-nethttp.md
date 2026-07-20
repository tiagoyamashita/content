---
label: "V"
subtitle: "Go — net/http"
group: "Pagination"
order: 5
---
Pagination template — Go (net/http)
**Query helpers** + **JSON envelope** for listing `Item` (`id`, `name`). Handler wiring: [Controllers](../controllers/v-go-nethttp.md).

## Template code

```go
package pagination

import (
	"net/http"
	"strconv"
)

const (
	DefaultLimit = 20
	MaxLimit     = 100
)

type ItemResponse struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

// PagedResponse is the shared list envelope.
type PagedResponse struct {
	Items      []ItemResponse `json:"items"`
	NextCursor *string        `json:"nextCursor,omitempty"`
	Total      *int64         `json:"total,omitempty"`
}

type PageParams struct {
	Page   int
	Size   int
	Offset int
}

type CursorParams struct {
	Cursor string
	Limit  int
}

func ParsePageQuery(r *http.Request) PageParams {
	page := clampInt(queryInt(r, "page", 1), 1, 1<<30)
	size := clampInt(queryInt(r, "size", DefaultLimit), 1, MaxLimit)
	return PageParams{
		Page:   page,
		Size:   size,
		Offset: (page - 1) * size,
	}
}

func ParseCursorQuery(r *http.Request) CursorParams {
	return CursorParams{
		Cursor: r.URL.Query().Get("cursor"),
		Limit:  clampInt(queryInt(r, "limit", DefaultLimit), 1, MaxLimit),
	}
}

func queryInt(r *http.Request, key string, fallback int) int {
	raw := r.URL.Query().Get(key)
	if raw == "" {
		return fallback
	}
	n, err := strconv.Atoi(raw)
	if err != nil {
		return fallback
	}
	return n
}

func clampInt(n, min, max int) int {
	if n < min {
		return min
	}
	if n > max {
		return max
	}
	return n
}
```

Handler stub:

```go
func (h *ItemHandler) List(w http.ResponseWriter, r *http.Request) {
	if r.URL.Query().Has("cursor") {
		params := pagination.ParseCursorQuery(r)
		items, next := h.repo.FindAfterCursor(r.Context(), params.Cursor, params.Limit)
		writeJSON(w, http.StatusOK, pagination.PagedResponse{
			Items:      items,
			NextCursor: next,
		})
		return
	}
	params := pagination.ParsePageQuery(r)
	items := h.repo.FindPage(r.Context(), params.Offset, params.Size)
	total := h.repo.Count(r.Context()) // omit Total when expensive
	writeJSON(w, http.StatusOK, pagination.PagedResponse{
		Items: items,
		Total: &total,
	})
}
```

Repository interface (bounded):

```go
type ItemRepository interface {
	FindPage(ctx context.Context, offset, limit int) ([]pagination.ItemResponse, error)
	Count(ctx context.Context) (int64, error)
	FindAfterCursor(ctx context.Context, cursor string, limit int) ([]pagination.ItemResponse, *string, error)
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Pointer fields** | `*string` / `*int64` with `omitempty` — omit nulls from JSON |
| **Clamp limits** | Always enforce max in `ParsePageQuery` / `ParseCursorQuery` |
| **Context** | Pass `r.Context()` into repo for timeouts and cancellation |
| **No unbounded slice** | Repo methods always take `limit` |

## Next

[Pagination overview](i-overview.md) · [Templates overview](../i-overview.md).
