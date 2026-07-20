---
label: "V"
subtitle: "Go — net/http"
group: "Middleware"
order: 5
---
Middleware template — Go (net/http)
**Middleware function** wrapping `http.Handler` — request ID, logging, auth stub on context.

## Template

```go
package middleware

import (
	"context"
	"log"
	"net/http"
	"time"

	"github.com/google/uuid"
)

type ctxKey string

const requestIDKey ctxKey = "requestId"

func RequestContext(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID := r.Header.Get("X-Request-Id")
		if requestID == "" {
			requestID = uuid.NewString()
		}
		w.Header().Set("X-Request-Id", requestID)

		ctx := context.WithValue(r.Context(), requestIDKey, requestID)

		// Auth stub
		if userID := r.Header.Get("X-User-Id"); userID != "" {
			ctx = context.WithValue(ctx, ctxKey("userId"), userID)
		}

		start := time.Now()
		next.ServeHTTP(w, r.WithContext(ctx))
		log.Printf("%s %s %s %s", requestID, r.Method, r.URL.Path, time.Since(start))
	})
}

func RequestIDFrom(ctx context.Context) string {
	id, _ := ctx.Value(requestIDKey).(string)
	return id
}
```

Wire in `main`:

```go
mux := http.NewServeMux()
// register handlers on mux ...
handler := middleware.RequestContext(mux)
_ = http.ListenAndServe(":8080", handler)
```

## Notes

| Topic | Practice |
|-------|----------|
| **Wrap outermost** | `RequestContext(mux)` — ID available to all handlers |
| **Typed context keys** | Unexported `ctxKey` type avoids collisions |
| **Chi / Echo** | Same pattern: `r.Use(RequestContext)` or equivalent |
| **Panic recovery** | Optional outer middleware: `defer recover()` → 500 JSON |

## Next

[Middleware overview](i-overview.md) · [Templates overview](../i-overview.md).
