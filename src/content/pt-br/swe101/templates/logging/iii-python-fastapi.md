---
label: "III"
subtitle: "Python — FastAPI"
group: "Logging"
order: 3
---
Logging template — Python (FastAPI)
Bind request context once with **`contextvars`**, emit one access event in middleware, and wrap service operations with an async-aware decorator. Structured fields flow through nested calls without passing a logger everywhere.

## Logger and context

```python
import contextvars
import functools
import inspect
import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any, ParamSpec, TypeVar, cast

import structlog
from fastapi import FastAPI, Request

P = ParamSpec("P")
R = TypeVar("R")

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
)

log = structlog.get_logger()
app = FastAPI()
```

## Access-log middleware

```python
@app.middleware("http")
async def access_log(request: Request, call_next: Callable) -> Any:
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    token = request_id_var.set(request_id)
    structlog.contextvars.bind_contextvars(request_id=request_id)
    started = time.perf_counter()

    try:
        response = await call_next(request)
        response.headers["X-Request-Id"] = request_id
        log.info(
            "http.request.completed",
            event="http.request.completed",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            outcome="success",
            duration_ms=round((time.perf_counter() - started) * 1000, 1),
        )
        return response
    except Exception:
        log.exception(
            "http.request.failed",
            event="http.request.completed",
            method=request.method,
            path=request.url.path,
            outcome="error",
            duration_ms=round((time.perf_counter() - started) * 1000, 1),
        )
        raise
    finally:
        structlog.contextvars.clear_contextvars()
        request_id_var.reset(token)
```

## Reusable operation decorator

```python
def logged_operation(
    operation: str,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        if inspect.iscoroutinefunction(function):
            @functools.wraps(function)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
                return await _run_async(operation, function, args, kwargs)

            return cast(Callable[P, R], async_wrapper)

        @functools.wraps(function)
        def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
            return _run_sync(operation, function, args, kwargs)

        return cast(Callable[P, R], sync_wrapper)
    return decorate


async def _run_async(
    operation: str,
    function: Callable[..., Awaitable[R]],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> R:
    started = time.perf_counter()
    try:
        result = await function(*args, **kwargs)
        _completed(operation, "success", started)
        return result
    except Exception as error:
        _failed(operation, error, started)
        raise


def _run_sync(
    operation: str,
    function: Callable[..., R],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> R:
    started = time.perf_counter()
    try:
        result = function(*args, **kwargs)
        _completed(operation, "success", started)
        return result
    except Exception as error:
        _failed(operation, error, started)
        raise


def _completed(operation: str, outcome: str, started: float) -> None:
    log.info(
        "operation.completed",
        event="operation.completed",
        operation=operation,
        outcome=outcome,
        duration_ms=round((time.perf_counter() - started) * 1000, 1),
    )


def _failed(operation: str, error: Exception, started: float) -> None:
    log.exception(
        "operation.failed",
        event="operation.completed",
        operation=operation,
        outcome="error",
        error_type=type(error).__name__,
        duration_ms=round((time.perf_counter() - started) * 1000, 1),
    )
```

Usage:

```python
@logged_operation("item.create")
async def create_item(request: CreateItemRequest) -> ItemResponse:
    item = await repository.save(request)
    log.info("item.created", event="item.created", item_id=item.id)
    return ItemResponse.model_validate(item)
```

## Notes

| Topic | Practice |
|-------|----------|
| **Context propagation** | `contextvars` follows asyncio tasks; clear it after every request |
| **No args/results** | Decorator logs metadata only—never dump request objects |
| **One stack trace** | Choose decorator or global exception boundary as stack owner |
| **Sync + async** | Wrapper handles both without forcing callers to change |
| **Configuration** | Keep processors, levels, JSON rendering, and redaction in one module |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Logging overview](i-overview.md).
