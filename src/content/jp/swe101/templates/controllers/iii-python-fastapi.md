---
label: "III"
subtitle: "Python — FastAPI"
group: "Controllers"
order: 3
---
Controller template — Python (FastAPI)
Minimal **router** for a resource. Language basics: [Python](../../languages&frameworks/python/i-basics-and-syntax.md).

## Dependencies

```bash
pip install fastapi uvicorn pydantic
```

## Template

```python
from uuid import uuid4

from fastapi import APIRouter, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI()
router = APIRouter(prefix="/api/items", tags=["items"])

# Demo only — replace with a service + DB
_store: dict[str, dict] = {}


class CreateItemRequest(BaseModel):
    name: str = Field(min_length=1)


class ItemResponse(BaseModel):
    id: str
    name: str


@router.get("", response_model=list[ItemResponse])
def list_items() -> list[ItemResponse]:
    return [ItemResponse(**row) for row in _store.values()]


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: str) -> ItemResponse:
    row = _store.get(item_id)
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return ItemResponse(**row)


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(body: CreateItemRequest) -> ItemResponse:
    item_id = str(uuid4())
    row = {"id": item_id, "name": body.name}
    _store[item_id] = row
    return ItemResponse(**row)


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: str, body: CreateItemRequest) -> ItemResponse:
    if item_id not in _store:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    row = {"id": item_id, "name": body.name}
    _store[item_id] = row
    return ItemResponse(**row)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str) -> None:
    if _store.pop(item_id, None) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")


app.include_router(router)
```

Run: `uvicorn main:app --reload`

## Notes

| Topic | Practice |
|-------|----------|
| **Thin router** | Inject a service via FastAPI `Depends` |
| **Validation** | Pydantic models on the edge |
| **Async** | Use `async def` + async DB drivers when I/O-bound |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Controllers overview](i-overview.md).
