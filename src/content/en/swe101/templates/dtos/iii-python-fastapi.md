---
label: "III"
subtitle: "Python — FastAPI"
group: "DTOs"
order: 3
---
DTO template — Python (FastAPI)
**Pydantic** models for request validation and response serialization. Router usage: [Controllers](../controllers/iii-python-fastapi.md).

## Dependencies

```bash
pip install pydantic
```

## Template

```python
from pydantic import BaseModel, ConfigDict, Field


class CreateItemRequest(BaseModel):
    """Incoming body for POST / PUT — client does not send id."""

    name: str = Field(min_length=1, max_length=200)


class ItemResponse(BaseModel):
    """Outgoing JSON for every Item endpoint."""

    model_config = ConfigDict(from_attributes=True)  # ORM → DTO mapping

    id: str
    name: str
```

Usage in a router:

```python
@router.post("", response_model=ItemResponse, status_code=201)
def create_item(body: CreateItemRequest) -> ItemResponse:
    ...
```

## Notes

| Topic | Practice |
|-------|----------|
| **DTO ≠ DAO** | Pydantic models are wire shapes; DB access lives in [Repositories](../repositories/iii-python-fastapi.md) — see [overview](i-overview.md#dto-vs-dao-do-not-mix-these-up) |
| **Request vs response** | Separate models — don't reuse one class for both |
| **`from_attributes`** | Lets you build `ItemResponse` from ORM rows |
| **Extra fields** | `model_config = ConfigDict(extra="forbid")` rejects unknown JSON keys |
| **Partial updates** | Use a `UpdateItemRequest` with optional fields for PATCH |

## Next

[JavaScript — Express](iv-javascript-express.md) · [DTOs overview](i-overview.md).
