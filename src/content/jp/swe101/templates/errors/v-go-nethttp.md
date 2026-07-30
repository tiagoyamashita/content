---
label: "V"
subtitle: "Go — net/http"
group: "Errors"
order: 5
---
Error template — Go (net/http)
**Sentinel / typed errors + helper** that maps domain failures to HTTP status and JSON in handlers.

## Template

```go
package api

import (
	"encoding/json"
	"errors"
	"net/http"
)

var ErrNotFound = errors.New("item not found")

type apiError struct {
	Error string `json:"error"`
	Code  string `json:"code"`
}

func writeError(w http.ResponseWriter, status int, code, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(apiError{Error: message, Code: code})
}

func mapError(w http.ResponseWriter, err error) {
	switch {
	case errors.Is(err, ErrNotFound):
		writeError(w, http.StatusNotFound, "NOT_FOUND", "Item not found")
	default:
		writeError(w, http.StatusInternalServerError, "INTERNAL_ERROR", "Internal server error")
	}
}

// Handler usage:
// item, err := svc.GetItem(r.Context(), id)
// if err != nil {
//     mapError(w, err)
//     return
// }
```

Wrap for context: `fmt.Errorf("load item %s: %w", id, ErrNotFound)`.

## Notes

| Topic | Practice |
|-------|----------|
| **Sentinel errors** | `var ErrNotFound = errors.New(...)` — compare with `errors.Is` |
| **Custom types** | `type ValidationError struct { Field string }` + type switch in `mapError` |
| **No panics for 404** | Return errors; reserve panic for truly broken invariants |
| **Middleware** | Optional wrapper that catches panics and returns 500 JSON |

## Next

[Errors overview](i-overview.md) · [Templates overview](../i-overview.md).
