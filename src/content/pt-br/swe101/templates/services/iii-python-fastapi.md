---
label: "III"
subtitle: "Python — FastAPI"
group: "Services"
order: 3
---
Service template — Python (FastAPI)
**`ItemService`** class — no FastAPI imports inside. DTOs: [DTOs](../dtos/iii-python-fastapi.md) · router: [Controllers](../controllers/iii-python-fastapi.md).

## Template

```python
from dataclasses import dataclass
from uuid import uuid4

from dto import CreateItemRequest, ItemResponse  # adjust import path


@dataclass
class Item:
    id: str
    name: str


class ItemRepository:
    """Swap for SQLAlchemy / async driver in real apps."""

    def __init__(self) -> None:
        self._store: dict[str, Item] = {}

    def find_all(self) -> list[Item]:
        return list(self._store.values())

    def find_by_id(self, item_id: str) -> Item | None:
        return self._store.get(item_id)

    def save(self, item: Item) -> Item:
        self._store[item.id] = item
        return item

    def delete_by_id(self, item_id: str) -> bool:
        return self._store.pop(item_id, None) is not None


class ItemService:
    def __init__(self, repository: ItemRepository) -> None:
        self._repo = repository

    def list_items(self) -> list[ItemResponse]:
        return [self._to_response(i) for i in self._repo.find_all()]

    def get_item(self, item_id: str) -> ItemResponse | None:
        item = self._repo.find_by_id(item_id)
        return self._to_response(item) if item else None

    def create_item(self, body: CreateItemRequest) -> ItemResponse:
        item = Item(id=str(uuid4()), name=body.name)
        saved = self._repo.save(item)
        return self._to_response(saved)

    def update_item(self, item_id: str, body: CreateItemRequest) -> ItemResponse | None:
        if self._repo.find_by_id(item_id) is None:
            return None
        updated = self._repo.save(Item(id=item_id, name=body.name))
        return self._to_response(updated)

    def delete_item(self, item_id: str) -> bool:
        return self._repo.delete_by_id(item_id)

    @staticmethod
    def _to_response(item: Item) -> ItemResponse:
        return ItemResponse(id=item.id, name=item.name)
```

Wire in a router:

```python
repo = ItemRepository()
item_service = ItemService(repo)

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: str) -> ItemResponse:
    item = item_service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Not found")
    return item
```

## Notes

| Topic | Practice |
|-------|----------|
| **Depends()** | `def get_service(): return ItemService(ItemRepository())` for DI |
| **No HTTP in service** | Raise domain errors or return `None` — router picks status |
| **Async** | Mirror with `async def` + async repository when using async DB |
| **Testing** | Mock `ItemRepository` — no HTTP client needed |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Services overview](i-overview.md).
