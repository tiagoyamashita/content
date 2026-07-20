---
label: "III"
subtitle: "Python — FastAPI"
group: "Resilience"
order: 3
---
Resilience template — Python (FastAPI)
**httpx** client with timeout and retry (tenacity or manual). Outbound setup: [HTTP clients](../http-clients/iii-python-fastapi.md).

## Dependencies

```bash
pip install httpx tenacity
```

## Template code

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

BASE_URL = "https://catalog.example.com"
TIMEOUT = httpx.Timeout(connect=2.0, read=5.0, write=5.0, pool=2.0)


class CatalogClient:
    def __init__(self) -> None:
        self._client = httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)

    def close(self) -> None:
        self._client.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential_jitter(initial=0.1, max=1.0),
        retry=retry_if_exception_type((httpx.TransportError, httpx.TimeoutException)),
        reraise=True,
    )
    def list_items(self) -> list[dict]:
        """Idempotent GET — safe to retry."""
        response = self._client.get("/api/items")
        response.raise_for_status()
        return response.json()

    def create_item(self, name: str) -> dict:
        """POST — no retry unless you send an Idempotency-Key header."""
        response = self._client.post("/api/items", json={"name": name})
        response.raise_for_status()
        return response.json()


# Manual retry (no tenacity) — same rules: GET only, bounded attempts
def get_with_manual_retry(client: httpx.Client, path: str, attempts: int = 3) -> httpx.Response:
    last_exc: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            response = client.get(path)
            response.raise_for_status()
            return response
        except (httpx.TransportError, httpx.TimeoutException) as exc:
            last_exc = exc
            if attempt == attempts:
                break
    raise last_exc  # type: ignore[misc]


# Graceful degradation in a FastAPI route:
#
# @router.get("/items")
# def list_items():
#     try:
#         return catalog.list_items()
#     except httpx.HTTPError:
#         return {"items": [], "degraded": True}
```

## Notes

| Topic | Practice |
|-------|----------|
| **`httpx.Timeout`** | Set connect + read — default "no timeout" hangs forever |
| **Tenacity** | Retry transport/timeout errors only — not arbitrary `HTTPStatusError` |
| **429 / 503** | Add `retry_if_result` or custom predicate + respect `Retry-After` |
| **Lifecycle** | One `Client` per app — close on shutdown; don't create per request |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Resilience overview](i-overview.md).
