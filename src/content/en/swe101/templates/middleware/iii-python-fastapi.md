---
label: "III"
subtitle: "Python — FastAPI"
group: "Middleware"
order: 3
---
Middleware template — Python (FastAPI)
**ASGI middleware** for request ID + logging, or **`Depends`** when you only need per-route context.

## Template (middleware)

```python
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        request.state.request_id = request_id

        # Auth stub
        request.state.user_id = request.headers.get("X-User-Id")

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        response.headers["X-Request-Id"] = request_id
        print(f"{request_id} {request.method} {request.url.path} {response.status_code} {duration_ms:.1f}ms")
        return response


# app.add_middleware(RequestContextMiddleware)
```

## Template (Depends alternative)

```python
import uuid

from fastapi import Header, Request


def get_request_context(
    request: Request,
    x_request_id: str | None = Header(default=None, alias="X-Request-Id"),
    x_user_id: str | None = Header(default=None, alias="X-User-Id"),
) -> dict:
    request_id = x_request_id or str(uuid.uuid4())
    request.state.request_id = request_id
    return {"request_id": request_id, "user_id": x_user_id}
```

## Notes

| Topic | Practice |
|-------|----------|
| **Middleware vs Depends** | Middleware for global ID/logging; Depends for typed injection |
| **Pure ASGI** | For streaming bodies, use raw ASGI middleware instead of `BaseHTTPMiddleware` |
| **CORS** | Add `CORSMiddleware` before custom middleware |
| **Production logging** | Replace `print` with `structlog` / `logging` + request ID |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Middleware overview](i-overview.md).
