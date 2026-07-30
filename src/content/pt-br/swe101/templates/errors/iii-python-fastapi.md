---
label: "III"
subtitle: "Python — FastAPI"
group: "Errors"
order: 3
---
Error template — Python (FastAPI)
**Custom exception + registered handler** — domain code raises; FastAPI maps to HTTP.

## Template

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


class NotFoundError(Exception):
    def __init__(self, message: str = "Item not found") -> None:
        self.message = message
        super().__init__(message)


@app.exception_handler(NotFoundError)
async def not_found_handler(_request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": exc.message, "code": "NOT_FOUND"},
    )


# Usage in a route or service:
# item = repo.find_by_id(item_id)
# if item is None:
#     raise NotFoundError()
```

Optional: register handlers on a router factory or use `HTTPException` only at the HTTP edge — prefer domain exceptions in services for reuse.

## Notes

| Topic | Practice |
|-------|----------|
| **Central handlers** | One place for 404, 400, 500 shapes |
| **Request context** | Read `request.state.request_id` in handlers for logging |
| **Pydantic validation** | FastAPI auto-returns 422; customize with `@app.exception_handler(RequestValidationError)` |
| **Testing** | `pytest.raises(NotFoundError)` in service tests; `TestClient` for HTTP |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Errors overview](i-overview.md).
