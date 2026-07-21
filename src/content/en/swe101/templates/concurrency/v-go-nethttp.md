---
label: "V"
subtitle: "Go — net/http"
group: "Concurrency"
order: 5
---
Concurrency template — Go (net/http)
Go serves each request on its own **goroutine** — cheap and preemptible. Concurrency is easy; **safety** is the work: protect shared state, bound fan-out, and always carry a `context` for cancellation and timeouts.

## Template code

```go
package concurrency

import (
	"context"
	"net/http"
	"sync"
	"time"

	"golang.org/x/sync/errgroup"
)

type Item struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

type CombinedView struct {
	Item Item     `json:"item"`
	Tags []string `json:"tags"`
}

// Parallel fan-out with errgroup: first error cancels the rest.
func LoadCombined(ctx context.Context, id string) (CombinedView, error) {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()

	var (
		item Item
		tags []string
	)
	g, ctx := errgroup.WithContext(ctx)

	g.Go(func() error {
		var err error
		item, err = fetchItem(ctx, id)
		return err
	})
	g.Go(func() error {
		var err error
		tags, err = fetchTags(ctx, id)
		return err
	})

	if err := g.Wait(); err != nil {
		return CombinedView{}, err
	}
	return CombinedView{Item: item, Tags: tags}, nil
}
```

Bound fan-out with a semaphore channel so N goroutines don't become 10,000:

```go
func FetchMany(ctx context.Context, ids []string) ([]Item, error) {
	const maxParallel = 10
	sem := make(chan struct{}, maxParallel)

	out := make([]Item, len(ids))
	g, ctx := errgroup.WithContext(ctx)

	for i, id := range ids {
		i, id := i, id // capture
		g.Go(func() error {
			sem <- struct{}{}        // acquire
			defer func() { <-sem }() // release
			item, err := fetchItem(ctx, id)
			if err != nil {
				return err
			}
			out[i] = item // distinct index — no lock needed
			return nil
		})
	}
	return out, g.Wait()
}
```

Protect genuinely shared state with a mutex:

```go
type Metrics struct {
	mu     sync.Mutex
	served int64
}

func (m *Metrics) Inc() {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.served++
}
```

`http.Request` already carries a per-request context — honor cancellation:

```go
func handler(w http.ResponseWriter, r *http.Request) {
	view, err := LoadCombined(r.Context(), r.PathValue("id"))
	if err != nil {
		http.Error(w, "upstream failed", http.StatusBadGateway)
		return
	}
	_ = view // encode JSON...
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Pass `context`** | Propagate `r.Context()` for cancellation + deadlines everywhere |
| **`errgroup`** | Cleaner than raw `WaitGroup` when goroutines can fail |
| **Bound goroutines** | Semaphore channel or worker pool — unbounded spawning is a leak |
| **Race detector** | Run tests with `go test -race` — catches data races early |
| **Share by communicating** | Prefer channels over shared memory; use `sync.Mutex`/atomics when you must share |

## Next

[Concurrency overview](i-overview.md) · [Resilience](../resilience/i-overview.md).
