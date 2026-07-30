---
label: "III"
subtitle: "Python — FastAPI"
group: "Filters"
order: 3
---
Filter template — Python (FastAPI)
**ASGI middleware** for edge policy — security headers and a 429 rate-limit stub. Request ID / logging: [Middleware](../middleware/iii-python-fastapi.md).

## Template

```python
import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

# In-memory stub — use Redis / API gateway in production
WINDOW_SECONDS = 60
MAX_REQUESTS = 60
_hits: dict[str, list[float]] = defaultdict(list)


class EdgePolicyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        client = request.client.host if request.client else "unknown"

        if _is_rate_limited(client):
            return JSONResponse(
                status_code=429,
                content={"error": "rate limit exceeded"},
                headers={"Retry-After": str(WINDOW_SECONDS)},
            )

        if request.method in {"POST", "PUT", "PATCH"}:
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith("application/json"):
                return JSONResponse(
                    status_code=415,
                    content={"error": "application/json required"},
                )

            content_length = request.headers.get("content-length")
            if content_length and int(content_length) > 1_048_576:
                return JSONResponse(
                    status_code=413,
                    content={"error": "payload too large"},
                )

        response = await call_next(request)
        _apply_security_headers(response)
        return response


def _is_rate_limited(client: str) -> bool:
    now = time.monotonic()
    window = _hits[client]
    _hits[client] = [t for t in window if now - t < WINDOW_SECONDS]
    if len(_hits[client]) >= MAX_REQUESTS:
        return True
    _hits[client].append(now)
    return False


def _apply_security_headers(response: Response) -> None:
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")


# app.add_middleware(EdgePolicyMiddleware)  # after RequestContextMiddleware
```

Register **after** request-context middleware so rejected responses still carry `X-Request-Id`.

## Notes

| Topic | Practice |
|-------|----------|
| **Middleware order** | First added = outermost — add edge policy inside logging middleware |
| **BaseHTTPMiddleware** | Fine for teaching; pure ASGI middleware for streaming/large bodies |
| **429 body** | Return JSON consistent with [Errors](../errors/iii-python-fastapi.md) |
| **Security headers** | `setdefault` so downstream handlers can override when needed |
| **Rate limit key** | IP for demos; API key or user id in production |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Filters overview](i-overview.md).
