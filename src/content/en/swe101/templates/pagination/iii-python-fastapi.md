---
label: "III"
subtitle: "Python — FastAPI"
group: "Pagination"
order: 3
---
Pagination template — Python (FastAPI)
**Pydantic query models** + **response envelope** for listing `Item` (`id`, `name`). Router wiring: [Controllers](../controllers/iii-python-fastapi.md).

## Template code

```python
from typing import Generic, Protocol, TypeVar

from fastapi import Query
from pydantic import BaseModel, Field

T = TypeVar("T")


class ItemResponse(BaseModel):
    id: str
    name: str


class PagedResponse(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None = None
    total: int | None = None  # omit or None when COUNT(*) is too expensive


class PageParams(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size


class CursorParams(BaseModel):
    cursor: str | None = None
    limit: int = Field(default=20, ge=1, le=100)


def page_params(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PageParams:
    return PageParams(page=page, size=size)


def cursor_params(
    cursor: str | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
) -> CursorParams:
    return CursorParams(cursor=cursor, limit=limit)


# Router stubs:
#
# @router.get("/items", response_model=PagedResponse[ItemResponse])
# def list_items(params: PageParams = Depends(page_params)) -> PagedResponse[ItemResponse]:
#     rows = repo.find_page(params.offset, params.size)
#     return PagedResponse(items=rows, next_cursor=None, total=repo.count())
#
# @router.get("/items/by-cursor", response_model=PagedResponse[ItemResponse])
# def list_items_cursor(params: CursorParams = Depends(cursor_params)) -> PagedResponse[ItemResponse]:
#     rows, next_cursor = repo.find_after_cursor(params.cursor, params.limit)
#     return PagedResponse(items=rows, next_cursor=next_cursor, total=None)
```

Repository protocol (bounded):

```python
class ItemRepository(Protocol):
    def find_page(self, offset: int, limit: int) -> list[ItemResponse]: ...
    def count(self) -> int: ...
    def find_after_cursor(
        self, cursor: str | None, limit: int
    ) -> tuple[list[ItemResponse], str | None]: ...
```

## Notes

| Topic | Practice |
|-------|----------|
| **`Field(le=100)`** | Enforce max page size in the schema — OpenAPI documents it |
| **`Generic[T]`** | Reuse `PagedResponse` for other resources |
| **`total=None`** | Prefer omitting expensive counts on hot list endpoints |
| **Cursor encoding** | URL-safe base64 of `(sort_key, id)` — validate before querying |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Pagination overview](i-overview.md).
