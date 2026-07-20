---
label: "III"
subtitle: "Python — FastAPI"
group: "Repositories"
order: 3
---
Repository template — Python (FastAPI)
**Protocol + in-memory class** for `Item` (`id`, `name`). Inject via FastAPI `Depends` in routers.

## Template

```python
from typing import Protocol
from uuid import uuid4

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str
    name: str


class CreateItem(BaseModel):
    name: str = Field(min_length=1)


class ItemRepository(Protocol):
    def find_all(self) -> list[Item]: ...
    def find_by_id(self, item_id: str) -> Item | None: ...
    def save(self, item: Item) -> Item: ...
    def delete_by_id(self, item_id: str) -> bool: ...


class InMemoryItemRepository:
    def __init__(self) -> None:
        self._store: dict[str, Item] = {}

    def find_all(self) -> list[Item]:
        return list(self._store.values())

    def find_by_id(self, item_id: str) -> Item | None:
        return self._store.get(item_id)

    def save(self, item: Item) -> Item:
        item_id = item.id or str(uuid4())
        saved = Item(id=item_id, name=item.name)
        self._store[item_id] = saved
        return saved

    def delete_by_id(self, item_id: str) -> bool:
        return self._store.pop(item_id, None) is not None


# FastAPI wiring:
# def get_item_repo() -> ItemRepository:
#     return InMemoryItemRepository()
```

## Notes

| Topic | Practice |
|-------|----------|
| **Protocol vs ABC** | `Protocol` for duck typing; `ABC` if you want `@abstractmethod` enforcement |
| **Async repos** | Use `async def` + SQLAlchemy/asyncpg when I/O-bound |
| **Session scope** | One DB session per request via `Depends` — not a global dict in production |
| **Not found** | Return `None`; raise domain/HTTP errors in the service or router |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Repositories overview](i-overview.md).
