---
label: "III"
subtitle: "Python — FastAPI"
group: "Observability"
order: 3
---
Observability template — Python (FastAPI)
**Structured logging** (`structlog` or stdlib `logging`) + middleware that records **duration** and a stub **Prometheus-style counter/histogram** hook.

## Template

```python
import time
import uuid
from collections.abc import Callable

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

log = structlog.get_logger()


class RequestMetrics:
    """Stub — swap for prometheus_client.Histogram in production."""

    def observe(self, method: str, path: str, status: int, duration_sec: float) -> None:
        pass  # metrics.http_duration.labels(method, path, status).observe(duration_sec)


metrics = RequestMetrics()


class ObservabilityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        request.state.request_id = request_id
        start = time.perf_counter()

        response = await call_next(request)
        duration_sec = time.perf_counter() - start

        response.headers["X-Request-Id"] = request_id
        metrics.observe(request.method, request.url.path, response.status_code, duration_sec)
        log.info(
            "request completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration_sec * 1000, 1),
        )
        return response


# app.add_middleware(ObservabilityMiddleware)
```

Route example (Item resource):

```python
@router.get("/{item_id}")
async def get_item(item_id: int, request: Request) -> ItemResponse:
    log.debug("fetching item", request_id=request.state.request_id, item_id=item_id)
    item = await repo.find_by_id(item_id)
    if item is None:
        raise NotFoundError()
    return item
```

OpenTelemetry stub: `opentelemetry-instrumentation-fastapi` auto-creates spans; bind `trace_id` in structlog processors.

## Notes

| Topic | Practice |
|-------|----------|
| **structlog** | Bind `request_id` once in middleware; merge in all downstream logs |
| **Path labels** | Normalize `/api/items/42` → `/api/items/{id}` for metric cardinality |
| **Async context** | Use `contextvars` if logging outside request middleware scope |
| **Production** | Replace `RequestMetrics` stub with `prometheus_client` or OTel metrics |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Observability overview](i-overview.md).
