---
label: "V"
subtitle: "Go — net/http"
group: "HTTP clients"
order: 5
---
HTTP client template — Go (net/http)
**`http.Client{Timeout}`** with JSON decode into a response DTO. Struct: [DTOs](../dtos/v-go-nethttp.md) · caller: [Services](../services/v-go-nethttp.md).

## Configuration

```go
package config

import (
	"os"
	"time"
)

type CatalogConfig struct {
	BaseURL string
	Timeout time.Duration
}

func LoadCatalogConfig() CatalogConfig {
	timeout := 3 * time.Second
	if v := os.Getenv("CATALOG_TIMEOUT_MS"); v != "" {
		if ms, err := time.ParseDuration(v + "ms"); err == nil {
			timeout = ms
		}
	}
	base := os.Getenv("CATALOG_BASE_URL")
	if base == "" {
		base = "https://catalog.example.com"
	}
	return CatalogConfig{BaseURL: base, Timeout: timeout}
}
```

## Template

```go
package catalog

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
)

type ItemResponse struct {
	ID   int64  `json:"id"`
	Name string `json:"name"`
}

type Client struct {
	baseURL string
	http    *http.Client
}

func NewClient(baseURL string, timeout time.Duration) *Client {
	return &Client{
		baseURL: strings.TrimRight(baseURL, "/"),
		http:    &http.Client{Timeout: timeout},
	}
}

func (c *Client) GetItem(ctx context.Context, id int64, requestID string) (*ItemResponse, error) {
	url := fmt.Sprintf("%s/items/%d", c.baseURL, id)
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Accept", "application/json")
	req.Header.Set("X-Request-Id", requestID)

	resp, err := c.http.Do(req)
	if err != nil {
		return nil, fmt.Errorf("catalog unreachable: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		return nil, nil
	}
	if resp.StatusCode >= 400 {
		return nil, fmt.Errorf("catalog error: status %d", resp.StatusCode)
	}

	body, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if err != nil {
		return nil, err
	}

	var item ItemResponse
	if err := json.Unmarshal(body, &item); err != nil {
		return nil, fmt.Errorf("invalid catalog response: %w", err)
	}
	return &item, nil
}
```

Use from a handler / service:

```go
item, err := catalogClient.GetItem(r.Context(), id, middleware.RequestIDFrom(r.Context()))
if err != nil {
	// map to 502 / log
}
if item == nil {
	// 404
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Client.Timeout** | Total deadline for the whole exchange — always set |
| **Context** | `NewRequestWithContext` — honor cancellation from inbound request |
| **404 → nil, nil** | Idiom for "not found" without treating as transport error |
| **LimitReader** | Cap response body size — partner sends 1 GB by mistake |
| **Request ID** | From context — [Middleware](../middleware/v-go-nethttp.md) |

## Next

[HTTP clients overview](i-overview.md) · [Filters](../filters/v-go-nethttp.md) · [Templates overview](../i-overview.md).
