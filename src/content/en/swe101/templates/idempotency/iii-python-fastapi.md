---
label: "III"
subtitle: "Python — FastAPI"
group: "Idempotency"
order: 3
---
Idempotency template — Python (FastAPI)
**Dependency or middleware** enforces `Idempotency-Key` on `POST /items`. Service checks store, replays cached response, or creates Item once.

Errors: [Errors](../errors/iii-python-fastapi.md) · service: [Services](../services/iii-python-fastapi.md).

## Template

```python
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, Response


@dataclass
class IdempotencyRecord:
    body_hash: str
    status_code: int
    response_body: dict[str, Any]
    expires_at: datetime


class IdempotencyStore:
    """In-memory stub — replace with Redis / DB."""

    def __init__(self) -> None:
        self._data: dict[str, IdempotencyRecord] = {}

    def get(self, key: str) -> IdempotencyRecord | None:
        rec = self._data.get(key)
        if rec and rec.expires_at < datetime.now(timezone.utc):
            del self._data[key]
            return None
        return rec

    def put(self, key: str, record: IdempotencyRecord) -> None:
        self._data[key] = record


store = IdempotencyStore()


def hash_body(body: dict[str, Any]) -> str:
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode()).hexdigest()


class ItemService:
    def __init__(self, idempotency: IdempotencyStore) -> None:
        self._idempotency = idempotency
        self._items: dict[str, dict] = {}

    def create_idempotent(
        self, key: str, body: dict[str, Any]
    ) -> tuple[int, dict[str, Any], bool]:
        body_hash = hash_body(body)
        existing = self._idempotency.get(key)

        if existing:
            if existing.body_hash != body_hash:
                raise HTTPException(
                    status_code=409,
                    detail="Idempotency-Key reused with different body",
                )
            return existing.status_code, existing.response_body, True

        item_id = f"item-{len(self._items) + 1}"
        created = {"id": item_id, "name": body["name"]}
        self._items[item_id] = created

        self._idempotency.put(
            key,
            IdempotencyRecord(
                body_hash=body_hash,
                status_code=201,
                response_body=created,
                expires_at=datetime.now(timezone.utc) + timedelta(hours=24),
            ),
        )
        return 201, created, False


item_service = ItemService(store)
app = FastAPI()


def require_idempotency_key(
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> str:
    if not idempotency_key or not idempotency_key.strip():
        raise HTTPException(status_code=400, detail="Idempotency-Key required")
    return idempotency_key.strip()


@app.post("/items", status_code=201)
def create_item(
    body: dict[str, Any],
    key: str = Depends(require_idempotency_key),
) -> Response:
    status, payload, replayed = item_service.create_idempotent(key, body)
    response = JSONResponse(status_code=status, content=payload)
    if replayed:
        response.headers["Idempotency-Replayed"] = "true"
    return response
```

Optional ASGI middleware for path-scoped header enforcement:

```python
from starlette.middleware.base import BaseHTTPMiddleware

class IdempotencyKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST" and request.url.path == "/items":
            if not request.headers.get("Idempotency-Key"):
                return JSONResponse(
                    status_code=400, content={"detail": "Idempotency-Key required"}
                )
        return await call_next(request)

# app.add_middleware(IdempotencyKeyMiddleware)
```

## Notes

| Topic | Practice |
|-------|----------|
| **Canonical hash** | `sort_keys=True` — stable hash regardless of JSON key order |
| **Depends vs middleware** | Depends gives typed access; middleware for global path rules |
| **409 vs 400** | Missing key → 400; key reuse with new body → 409 |
| **Persistence** | Replace in-memory store before production — TTL index required |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Idempotency overview](i-overview.md).
