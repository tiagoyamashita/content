---
label: "V"
subtitle: "Go — net/http"
group: "Observability"
order: 5
---
Observability template — Go (net/http)
**`log/slog`** structured logging + middleware that records **duration**. Brief OpenTelemetry hook for traces.

## Template

```go
package api

import (
	"context"
	"log/slog"
	"net/http"
	"time"

	"github.com/google/uuid"
)

type ctxKey int

const requestIDKey ctxKey = iota

func RequestIDFromContext(ctx context.Context) string {
	if id, ok := ctx.Value(requestIDKey).(string); ok {
		return id
	}
	return ""
}

func ObservabilityMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID := r.Header.Get("X-Request-Id")
		if requestID == "" {
			requestID = uuid.NewString()
		}
		w.Header().Set("X-Request-Id", requestID)
		ctx := context.WithValue(r.Context(), requestIDKey, requestID)

		start := time.Now()
		rec := &statusRecorder{ResponseWriter: w, status: http.StatusOK}
		next.ServeHTTP(rec, r.WithContext(ctx))

		slog.InfoContext(ctx, "request completed",
			"method", r.Method,
			"path", r.URL.Path,
			"status", rec.status,
			"durationMs", time.Since(start).Milliseconds(),
		)
	})
}

type statusRecorder struct {
	http.ResponseWriter
	status int
}

func (r *statusRecorder) WriteHeader(code int) {
	r.status = code
	r.ResponseWriter.WriteHeader(code)
}

// Handler usage:
// func getItem(w http.ResponseWriter, r *http.Request) {
//     slog.DebugContext(r.Context(), "fetching item", "itemId", id)
//     ...
// }
```

OpenTelemetry (brief): `go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp` wraps handlers — `otelhttp.NewHandler(next, "GET /api/items/{id}")` emits spans; propagate `trace_id` into slog with a `LogHandler` wrapper.

## Notes

| Topic | Practice |
|-------|----------|
| **slog** | Use `InfoContext` — carries request ID from context |
| **Status capture** | Default `Write` is 200; wrap `ResponseWriter` to record real status |
| **Metrics** | `prometheus.NewHistogramVec` labeled by method + route pattern |
| **OTel** | One span per request; child spans around `repo.GetItem` calls |

## Next

[Observability overview](i-overview.md) · [Templates overview](../i-overview.md).
