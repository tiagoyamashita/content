---
label: "III"
subtitle: "Python — FastAPI"
group: "Caching"
order: 3
---
Caching template — Python (FastAPI)
Set **`Cache-Control`** and **`ETag`** on GET item; return **304** when **`If-None-Match`** matches.

## Template

```python
import hashlib
from typing import Annotated

from fastapi import APIRouter, Header, Response, status
from pydantic import BaseModel

router = APIRouter(prefix="/api/items", tags=["items"])


class ItemResponse(BaseModel):
    id: int
    name: str
    updated_at: str


def compute_etag(item: ItemResponse) -> str:
    payload = f"{item.id}|{item.name}|{item.updated_at}".encode()
    digest = hashlib.sha256(payload).hexdigest()[:16]
    return f'"{digest}"'


@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    response: Response,
    if_none_match: Annotated[str | None, Header(alias="If-None-Match")] = None,
) -> ItemResponse | Response:
    item = await load_item(item_id)  # repo + optional Redis
    if item is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    etag = compute_etag(item)
    response.headers["Cache-Control"] = "public, max-age=60"
    response.headers["ETag"] = etag

    if if_none_match == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers=response.headers)

    return item


async def load_item(item_id: int) -> ItemResponse | None:
    # TODO: redis.get(f"item:{item_id}") → on miss, repo.find_by_id
    return ItemResponse(id=item_id, name="Widget", updated_at="2026-07-20T12:00:00Z")
```

Invalidate on write:

```python
# await redis.delete(f"item:{item_id}")
# return Response(status_code=204, headers={"Cache-Control": "no-store"})
```

## Notes

| Topic | Practice |
|-------|----------|
| **304 body** | Must be empty — return `Response` directly, not the model |
| **Weak vs strong ETags** | Strong (`"abc"`) for byte-identical; weak (`W/"abc"`) for semantic equivalence |
| **Starlette caching** | `from starlette.middleware.gzip import GZipMiddleware` — gzip after ETag is fine |
| **Redis layer** | HTTP headers for clients; Redis for server-side repeat reads |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Caching overview](i-overview.md).
