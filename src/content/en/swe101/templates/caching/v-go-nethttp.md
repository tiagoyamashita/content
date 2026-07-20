---
label: "V"
subtitle: "Go — net/http"
group: "Caching"
order: 5
---
Caching template — Go (net/http)
**`Cache-Control` + `ETag`** on GET item; **304** when **`If-None-Match`** matches.

## Template

```go
package api

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"net/http"
)

type ItemResponse struct {
	ID        int64  `json:"id"`
	Name      string `json:"name"`
	UpdatedAt string `json:"updatedAt"`
}

func computeEtag(item ItemResponse) string {
	payload := fmt.Sprintf("%d|%s|%s", item.ID, item.Name, item.UpdatedAt)
	sum := sha256.Sum256([]byte(payload))
	return `"` + hex.EncodeToString(sum[:8]) + `"`
}

func getItem(w http.ResponseWriter, r *http.Request) {
	id := parseItemID(r) // e.g. from chi/mux path param
	item, err := loadItem(r.Context(), id) // repo + optional Redis
	if err != nil {
		http.Error(w, `{"error":"Item not found"}`, http.StatusNotFound)
		return
	}

	etag := computeEtag(item)
	w.Header().Set("Cache-Control", "public, max-age=60")
	w.Header().Set("ETag", etag)

	if match := r.Header.Get("If-None-Match"); match == etag {
		w.WriteHeader(http.StatusNotModified)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(item)
}

func loadItem(ctx context.Context, id int64) (ItemResponse, error) {
	// TODO: redis.Get(ctx, "item:"+strconv.FormatInt(id,10))
	return ItemResponse{ID: id, Name: "Widget", UpdatedAt: "2026-07-20T12:00:00Z"}, nil
}

// Invalidate on write:
// redis.Del(ctx, "item:"+id)
// w.Header().Set("Cache-Control", "no-store")
```

Implement `parseItemID(r *http.Request) int64` for your router. Normalize weak ETags if clients send `W/"..."`.

## Notes

| Topic | Practice |
|-------|----------|
| **WriteHeader once** | Set headers before `WriteHeader(304)` — body must stay empty |
| **Strong ETags** | Hash canonical JSON if field order varies |
| **http.FileServer** | Built-in `If-Modified-Since` / ETag for static assets |
| **Redis** | Separate concern — cache DB rows server-side; HTTP headers for clients |

## Next

[Caching overview](i-overview.md) · [Templates overview](../i-overview.md).
