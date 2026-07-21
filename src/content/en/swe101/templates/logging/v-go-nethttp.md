---
label: "V"
subtitle: "Go — net/http"
group: "Logging"
order: 5
---
Logging template — Go (net/http)
Use the standard library **`log/slog`**, put a request-scoped child logger in `context.Context`, wrap handlers for access logs, and wrap operations with a generic function.

## Logger context

```go
package logging

import (
	"context"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"time"

	"github.com/google/uuid"
)

type loggerKey struct{}

var root = slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
	Level: slog.LevelInfo,
}))

func FromContext(ctx context.Context) *slog.Logger {
	if logger, ok := ctx.Value(loggerKey{}).(*slog.Logger); ok {
		return logger
	}
	return root
}
```

## Access-log middleware

```go
type statusRecorder struct {
	http.ResponseWriter
	status int
}

func (w *statusRecorder) WriteHeader(status int) {
	w.status = status
	w.ResponseWriter.WriteHeader(status)
}

func AccessLog(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		requestID := r.Header.Get("X-Request-Id")
		if requestID == "" {
			requestID = uuid.NewString()
		}

		logger := root.With("requestId", requestID)
		ctx := context.WithValue(r.Context(), loggerKey{}, logger)
		recorder := &statusRecorder{ResponseWriter: w, status: http.StatusOK}
		started := time.Now()

		w.Header().Set("X-Request-Id", requestID)
		defer func() {
			logger.InfoContext(ctx, "http request completed",
				"event", "http.request.completed",
				"method", r.Method,
				"path", r.URL.Path,
				"status", recorder.status,
				"durationMs", time.Since(started).Milliseconds(),
			)
		}()

		next.ServeHTTP(recorder, r.WithContext(ctx))
	})
}
```

## Generic operation wrapper

```go
func Operation[T any](
	ctx context.Context,
	name string,
	run func(context.Context) (T, error),
) (T, error) {
	started := time.Now()
	result, err := run(ctx)
	logger := FromContext(ctx)

	if err != nil {
		logger.ErrorContext(ctx, "operation failed",
			"event", "operation.completed",
			"operation", name,
			"outcome", "error",
			"errorType", typeName(err),
			"durationMs", time.Since(started).Milliseconds(),
		)
		return result, err
	}

	logger.InfoContext(ctx, "operation completed",
		"event", "operation.completed",
		"operation", name,
		"outcome", "success",
		"durationMs", time.Since(started).Milliseconds(),
	)
	return result, nil
}

func typeName(err error) string {
	return fmt.Sprintf("%T", err)
}
```

Usage:

```go
func (s *ItemService) Create(
	ctx context.Context,
	request CreateItemRequest,
) (ItemResponse, error) {
	return Operation(ctx, "item.create", func(ctx context.Context) (ItemResponse, error) {
		item, err := s.repository.Save(ctx, Item{Name: request.Name})
		if err != nil {
			return ItemResponse{}, err
		}
		FromContext(ctx).InfoContext(ctx, "item created",
			"event", "item.created",
			"itemId", item.ID,
		)
		return toResponse(item), nil
	})
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Context logger** | Pass `context.Context`; do not use package-global request fields |
| **Safe fields** | `slog` has no built-in deep redactor—only attach allowlisted values |
| **Error field** | Prefer typed safe attributes; avoid returning sensitive driver text |
| **One wrapper** | Middleware owns access events; `Operation` owns use-case timing |
| **Cancellation** | Use `InfoContext`/`ErrorContext` so handlers can observe request context |

## Next

[Logging overview](i-overview.md) · [Observability](../observability/i-overview.md).
