---
label: "V"
subtitle: "Go — net/http"
group: "Resilience"
order: 5
---
Resilience template — Go (net/http)
**context.WithTimeout** on every outbound call and a simple retry loop for idempotent GETs. Outbound setup: [HTTP clients](../http-clients/v-go-nethttp.md).

## Template code

```go
package resilience

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"time"
)

const (
	defaultTimeout = 5 * time.Second
	maxAttempts    = 3
)

type CatalogClient struct {
	baseURL string
	http    *http.Client
}

func NewCatalogClient(baseURL string) *CatalogClient {
	return &CatalogClient{
		baseURL: baseURL,
		http: &http.Client{
			Timeout: defaultTimeout, // entire request deadline (connect + read)
		},
	}
}

type Item struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

// ListItems — idempotent GET; safe to retry on transient errors.
func (c *CatalogClient) ListItems(ctx context.Context) ([]Item, error) {
	var lastErr error
	for attempt := 1; attempt <= maxAttempts; attempt++ {
		items, err := c.listItemsOnce(ctx)
		if err == nil {
			return items, nil
		}
		if !isRetryable(err) {
			return nil, err
		}
		lastErr = err
		if attempt < maxAttempts {
			time.Sleep(backoff(attempt))
		}
	}
	return nil, fmt.Errorf("catalog list failed after %d attempts: %w", maxAttempts, lastErr)
}

func (c *CatalogClient) listItemsOnce(ctx context.Context) ([]Item, error) {
	reqCtx, cancel := context.WithTimeout(ctx, defaultTimeout)
	defer cancel()

	req, err := http.NewRequestWithContext(reqCtx, http.MethodGet, c.baseURL+"/api/items", nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Accept", "application/json")

	res, err := c.http.Do(req)
	if err != nil {
		return nil, err
	}
	defer res.Body.Close()

	if res.StatusCode >= 500 || res.StatusCode == http.StatusTooManyRequests {
		body, _ := io.ReadAll(io.LimitReader(res.Body, 512))
		return nil, fmt.Errorf("upstream %d: %s", res.StatusCode, body)
	}
	if res.StatusCode >= 400 {
		return nil, fmt.Errorf("client error %d", res.StatusCode)
	}

	var items []Item
	if err := json.NewDecoder(res.Body).Decode(&items); err != nil {
		return nil, err
	}
	return items, nil
}

// CreateItem — POST; do not retry without an idempotency key.
func (c *CatalogClient) CreateItem(ctx context.Context, name string) (Item, error) {
	reqCtx, cancel := context.WithTimeout(ctx, defaultTimeout)
	defer cancel()
	// build POST body, single attempt — see HTTP clients template
	_ = reqCtx
	return Item{}, errors.New("implement single-attempt POST")
}

func isRetryable(err error) bool {
	if errors.Is(err, context.DeadlineExceeded) {
		return true
	}
	// extend: net.Error Timeout/Temporary, specific status codes
	return true
}

func backoff(attempt int) time.Duration {
	return time.Duration(100*(1<<(attempt-1))) * time.Millisecond
}

// Handler graceful degradation:
//
// func (h *Handler) List(w http.ResponseWriter, r *http.Request) {
//   items, err := h.catalog.ListItems(r.Context())
//   if err != nil {
//     writeJSON(w, http.StatusOK, map[string]any{"items": []Item{}, "degraded": true})
//     return
//   }
//   writeJSON(w, http.StatusOK, map[string]any{"items": items})
// }
```

## Notes

| Topic | Practice |
|-------|----------|
| **Context timeout** | Per-request `WithTimeout` even when `Client.Timeout` is set — honors caller cancellation |
| **Retry GET only** | Loop belongs on reads; POST is single-flight unless idempotent |
| **Transport errors** | Retry `Temporary()` network errors; don't retry context.Canceled from client |
| **Circuit breaker** | Use `sony/gobreaker` when failure rate triggers bulkhead isolation |

## Next

[Resilience overview](i-overview.md) · [Templates overview](../i-overview.md).
