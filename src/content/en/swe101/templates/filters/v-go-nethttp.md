---
label: "V"
subtitle: "Go — net/http"
group: "Filters"
order: 5
---
Filter template — Go (net/http)
**Middleware** for edge policy — 429 rate limiting and security headers. Request ID / logging: [Middleware](../middleware/v-go-nethttp.md).

## Template

```go
package filter

import (
	"encoding/json"
	"net"
	"net/http"
	"strings"
	"sync"
	"time"
)

const maxBodyBytes = 1 << 20 // 1 MiB

type hitWindow struct {
	mu    sync.Mutex
	times []time.Time
}

var (
	windowDuration = time.Minute
	maxRequests    = 60
	clients        sync.Map // key string -> *hitWindow
)

func EdgePolicy(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		applySecurityHeaders(w)

		if limited := checkRateLimit(clientKey(r)); limited {
			w.Header().Set("Retry-After", "60")
			writeJSON(w, http.StatusTooManyRequests, map[string]string{"error": "rate limit exceeded"})
			return
		}

		if isMutating(r.Method) {
			if ct := r.Header.Get("Content-Type"); !strings.HasPrefix(ct, "application/json") {
				writeJSON(w, http.StatusUnsupportedMediaType, map[string]string{"error": "application/json required"})
				return
			}
			r.Body = http.MaxBytesReader(w, r.Body, maxBodyBytes)
		}

		next.ServeHTTP(w, r)
	})
}

func applySecurityHeaders(w http.ResponseWriter) {
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("X-Frame-Options", "DENY")
	w.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
}

func clientKey(r *http.Request) string {
	host, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return r.RemoteAddr
	}
	return host
}

func checkRateLimit(key string) bool {
	v, _ := clients.LoadOrStore(key, &hitWindow{})
	hw := v.(*hitWindow)
	hw.mu.Lock()
	defer hw.mu.Unlock()

	cutoff := time.Now().Add(-windowDuration)
	alive := hw.times[:0]
	for _, t := range hw.times {
		if t.After(cutoff) {
			alive = append(alive, t)
		}
	}
	hw.times = alive
	if len(hw.times) >= maxRequests {
		return true
	}
	hw.times = append(hw.times, time.Now())
	return false
}

func isMutating(method string) bool {
	switch method {
	case http.MethodPost, http.MethodPut, http.MethodPatch:
		return true
	default:
		return false
	}
}

func writeJSON(w http.ResponseWriter, status int, body any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(body)
}
```

Wire **inside** request-context middleware:

```go
mux := http.NewServeMux()
// register handlers ...
handler := middleware.RequestContext(filter.EdgePolicy(mux))
_ = http.ListenAndServe(":8080", handler)
```

`http.MaxBytesReader` returns **413** automatically when the body exceeds the limit.

## Notes

| Topic | Practice |
|-------|----------|
| **Wrap order** | `RequestContext(EdgePolicy(mux))` — ID on all responses including 429 |
| **MaxBytesReader** | Prefer over manual `Content-Length` checks for streamed bodies |
| **sync.Map** | Demo-only rate limit store — use Redis in production |
| **Chi / Echo** | Same handlers as `r.Use(EdgePolicy)` |
| **Reverse proxy** | Rate-limit on `X-Forwarded-For` only when you trust the proxy |

## Next

[Filters overview](i-overview.md) · [Middleware](../middleware/v-go-nethttp.md) · [HTTP clients](../http-clients/v-go-nethttp.md).
