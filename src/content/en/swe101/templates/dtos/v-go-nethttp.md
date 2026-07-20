---
label: "V"
subtitle: "Go — net/http"
group: "DTOs"
order: 5
---
DTO template — Go (net/http)
Request and response **structs** with `json` tags. Handler usage: [Controllers](../controllers/v-go-nethttp.md).

## Template

```go
package dto

// CreateItemRequest is the incoming body for POST / PUT — client does not send id.
type CreateItemRequest struct {
	Name string `json:"name"`
}

// ItemResponse is the outgoing JSON for every Item endpoint.
type ItemResponse struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}
```

Decode in a handler:

```go
var body dto.CreateItemRequest
if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.Name == "" {
	writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name is required"})
	return
}
```

Optional validation helper (stdlib only):

```go
func (r CreateItemRequest) Validate() error {
	if strings.TrimSpace(r.Name) == "" {
		return errors.New("name is required")
	}
	if len(r.Name) > 200 {
		return errors.New("name must be at most 200 characters")
	}
	return nil
}
```

## Notes

| Topic | Practice |
|-------|----------|
| **DTO ≠ DAO** | `dto` package = JSON structs; DB access is [Repositories](../repositories/v-go-nethttp.md) — see [overview](i-overview.md#dto-vs-dao-do-not-mix-these-up) |
| **Package layout** | `dto/` separate from `domain/` and `handler/` — no `Save` methods on DTO types |
| **Unexported vs exported** | Capitalize field names for JSON encoding |
| **Omit empty** | `json:"name,omitempty"` on optional PATCH fields |
| **Validation libs** | `go-playground/validator` when annotations aren't enough |

## Next

[DTOs overview](i-overview.md) · [Templates overview](../i-overview.md).
