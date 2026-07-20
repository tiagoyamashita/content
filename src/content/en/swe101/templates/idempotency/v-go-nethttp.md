---
label: "V"
subtitle: "Go — net/http"
group: "Idempotency"
order: 5
---
Idempotency template — Go (net/http)
**Middleware** requires `Idempotency-Key` on `POST /items`; **service** deduplicates before creating an Item.

Errors: [Errors](../errors/v-go-nethttp.md) · service: [Services](../services/v-go-nethttp.md).

## Template

```go
package api

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"net/http"
	"strings"
	"time"

	"github.com/google/uuid"

	"example.com/api/dto"
)

var (
	ErrIdempotencyConflict = errors.New("idempotency key reused with different body")
	ErrMissingIdempotencyKey = errors.New("idempotency-key required")
)

type IdempotencyRecord struct {
	BodyHash     string
	StatusCode   int
	ResponseBody []byte
	ExpiresAt    time.Time
}

type IdempotencyStore interface {
	Get(ctx context.Context, key string) (*IdempotencyRecord, error)
	Put(ctx context.Context, key string, rec IdempotencyRecord) error
}

type ItemService struct {
	store IdempotencyStore
	// repo ItemRepository — wire real persistence
}

type IdempotentResult struct {
	StatusCode int
	Body       []byte
	Replayed   bool
}

func hashBody(body []byte) string {
	sum := sha256.Sum256(body)
	return hex.EncodeToString(sum[:])
}

func (s *ItemService) CreateIdempotent(
	ctx context.Context, key string, rawBody []byte, req dto.CreateItemRequest,
) (IdempotentResult, error) {
	bodyHash := hashBody(rawBody)

	existing, err := s.store.Get(ctx, key)
	if err != nil {
		return IdempotentResult{}, err
	}
	if existing != nil {
		if existing.BodyHash != bodyHash {
			return IdempotentResult{}, ErrIdempotencyConflict
		}
		return IdempotentResult{
			StatusCode: existing.StatusCode,
			Body:       existing.ResponseBody,
			Replayed:   true,
		}, nil
	}

	item := dto.ItemResponse{ID: uuid.NewString(), Name: req.Name}
	respBody, err := json.Marshal(item)
	if err != nil {
		return IdempotentResult{}, err
	}

	if err := s.store.Put(ctx, key, IdempotencyRecord{
		BodyHash:     bodyHash,
		StatusCode:   http.StatusCreated,
		ResponseBody: respBody,
		ExpiresAt:    time.Now().Add(24 * time.Hour),
	}); err != nil {
		return IdempotentResult{}, err
	}

	return IdempotentResult{
		StatusCode: http.StatusCreated,
		Body:       respBody,
		Replayed:   false,
	}, nil
}

func RequireIdempotencyKey(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost && strings.HasSuffix(r.URL.Path, "/items") {
			key := strings.TrimSpace(r.Header.Get("Idempotency-Key"))
			if key == "" {
				writeError(w, http.StatusBadRequest, "MISSING_KEY", "Idempotency-Key required")
				return
			}
			ctx := context.WithValue(r.Context(), idempotencyKeyCtx, key)
			next.ServeHTTP(w, r.WithContext(ctx))
			return
		}
		next.ServeHTTP(w, r)
	})
}

type ctxKey string

const idempotencyKeyCtx ctxKey = "idempotencyKey"

func idempotencyKeyFrom(ctx context.Context) string {
	v, _ := ctx.Value(idempotencyKeyCtx).(string)
	return v
}
```

Handler — read body once for hashing:

```go
func (h *ItemHandler) Create(w http.ResponseWriter, r *http.Request) {
	raw, err := io.ReadAll(r.Body) // import "io"
	if err != nil {
		writeError(w, http.StatusBadRequest, "BAD_BODY", "invalid body")
		return
	}

	var req dto.CreateItemRequest
	if err := json.Unmarshal(raw, &req); err != nil {
		writeError(w, http.StatusBadRequest, "BAD_BODY", "invalid json")
		return
	}

	key := idempotencyKeyFrom(r.Context())
	result, err := h.svc.CreateIdempotent(r.Context(), key, raw, req)
	if errors.Is(err, ErrIdempotencyConflict) {
		writeError(w, http.StatusConflict, "IDEMPOTENCY_CONFLICT", err.Error())
		return
	}
	if err != nil {
		mapError(w, err)
		return
	}

	if result.Replayed {
		w.Header().Set("Idempotency-Replayed", "true")
	}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(result.StatusCode)
	_, _ = w.Write(result.Body)
}
```

Wire middleware:

```go
mux := http.NewServeMux()
mux.Handle("POST /items", RequireIdempotencyKey(http.HandlerFunc(h.Create)))
```

## Notes

| Topic | Practice |
|-------|----------|
| **Read body once** | Hash raw bytes — don't re-marshal from struct (field order drift) |
| **Context key** | Pass idempotency key via `context.Context`, not globals |
| **Concurrent POST** | Use DB unique constraint on key or Redis `SETNX` to prevent double-create |
| **TTL cleanup** | Background job or Redis EXPIRE on idempotency keys |

## Next

[Idempotency overview](i-overview.md) · [Templates overview](../i-overview.md).
