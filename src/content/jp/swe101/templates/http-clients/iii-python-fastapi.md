---
label: "III"
subtitle: "Python — FastAPI"
group: "HTTP clients"
order: 3
---
HTTP client template — Python (FastAPI)
**`httpx.AsyncClient`** with timeout and **`ItemResponse`** mapping. Schema: [DTOs](../dtos/iii-python-fastapi.md) · caller: [Services](../services/iii-python-fastapi.md).

## Configuration

```python
import os

CATALOG_BASE_URL = os.getenv("CATALOG_BASE_URL", "https://catalog.example.com")
CATALOG_TIMEOUT = float(os.getenv("CATALOG_TIMEOUT_SECONDS", "3.0"))
```

## Template

```python
import httpx
from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: int
    name: str


class CatalogClient:
    def __init__(self, base_url: str, timeout: float) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = httpx.Timeout(timeout)

    async def get_item(self, item_id: int, request_id: str) -> ItemResponse | None:
        url = f"{self._base_url}/items/{item_id}"
        headers = {
            "Accept": "application/json",
            "X-Request-Id": request_id,
        }

        async with httpx.AsyncClient(timeout=self._timeout) as client:
            try:
                response = await client.get(url, headers=headers)
            except httpx.TimeoutException as exc:
                raise CatalogError("catalog timeout") from exc
            except httpx.RequestError as exc:
                raise CatalogError("catalog unreachable") from exc

        if response.status_code == 404:
            return None
        if response.is_error:
            raise CatalogError(f"catalog error: {response.status_code}")

        return ItemResponse.model_validate(response.json())


class CatalogError(Exception):
    pass


# catalog = CatalogClient(CATALOG_BASE_URL, CATALOG_TIMEOUT)
# item = await catalog.get_item(42, request.state.request_id)
```

Reuse a **single long-lived client** in production (`lifespan` hook) instead of opening one per call.

## Lifespan pattern (production)

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

catalog_client: CatalogClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global catalog_client
    catalog_client = CatalogClient(CATALOG_BASE_URL, CATALOG_TIMEOUT)
    yield
    # httpx.AsyncClient close if you keep a shared instance


app = FastAPI(lifespan=lifespan)
```

## Notes

| Topic | Practice |
|-------|----------|
| **httpx.Timeout** | Covers connect + read — never use default infinite wait |
| **404 → None** | Service maps to HTTP 404 or fallback logic |
| **Request ID** | From `request.state.request_id` — [Middleware](../middleware/iii-python-fastapi.md) |
| **Pydantic validate** | Catches remote schema drift early |
| **Sync alternative** | `httpx.Client` for non-async services |

## Next

[JavaScript — Express](iv-javascript-express.md) · [HTTP clients overview](i-overview.md).
