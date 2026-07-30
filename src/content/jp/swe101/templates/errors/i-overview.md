---
label: "I"
subtitle: "Overview"
group: "Errors"
order: 1
---
Errors — overview
Separate **domain errors** (what went wrong in your app) from **HTTP mapping** (which status code and JSON body the client sees). Services and repositories raise or return typed failures; one boundary layer translates them to responses.

## Mental model

```mermaid
flowchart LR
  Repo[Repository] -->|not found| Service
  Service -->|NotFoundError| Controller
  Controller --> Mapper[Error mapper / advice]
  Mapper -->|404 JSON| Client
```

| Layer | Responsibility |
|-------|----------------|
| **Domain / service** | `NotFoundError`, validation failures — no `ResponseEntity` |
| **Controller / handler** | Catch or propagate; avoid duplicating mapping logic |
| **Global handler** | Map error type → status + body (`ProblemDetail`, `{ error }`, etc.) |

## Common mappings (Item resource)

| Domain signal | HTTP | Body (example) |
|---------------|------|----------------|
| Missing item | 404 | `{ "error": "Item not found" }` |
| Invalid input | 400 | `{ "error": "name is required" }` |
| Unexpected failure | 500 | `{ "error": "Internal server error" }` (log details server-side) |

## Language templates

| Note | Stack |
|------|--------|
| [Java — Spring](ii-java-spring.md) | `NotFoundException` + `@RestControllerAdvice` |
| [Python — FastAPI](iii-python-fastapi.md) | Custom exception + `@app.exception_handler` |
| [JavaScript — Express](iv-javascript-express.md) | `AppError` + error middleware |
| [Go — net/http](v-go-nethttp.md) | Sentinel errors + status helper |

## Notes

| Topic | Practice |
|-------|----------|
| **One mapper** | Centralize status/body shape — clients stay consistent |
| **No stack traces to clients** | Log internally; return safe messages |
| **Stable codes** | Optional `code` field (`ITEM_NOT_FOUND`) for programmatic clients |
| **Validation vs domain** | 400 for bad input; 404 for missing resource; 409 for conflicts |

## Next

Pick your stack — start with [Java — Spring](ii-java-spring.md) or [Python — FastAPI](iii-python-fastapi.md).
