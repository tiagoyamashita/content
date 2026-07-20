---
label: "III"
subtitle: "Python — FastAPI"
group: "Transactions"
order: 3
---
Transaction template — Python (FastAPI)
**SQLAlchemy session scope** — one session per request (or per use-case); `commit` on success, `rollback` on error. Keep transaction boundaries in the service layer, not in route handlers.

Service context: [Services](../services/iii-python-fastapi.md).

## Template

```python
from contextlib import contextmanager
from dataclasses import dataclass
from uuid import uuid4

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class ItemModel(Base):
    __tablename__ = "items"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)


engine = create_engine("postgresql+psycopg://user:pass@localhost/app", future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


@contextmanager
def session_scope() -> Session:
    """One transaction: commit or rollback, always close."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


@dataclass
class CreateItemRequest:
    name: str


class ItemService:
    def create_item(self, body: CreateItemRequest) -> dict:
        with session_scope() as session:
            item = ItemModel(id=str(uuid4()), name=body.name)
            session.add(item)
            session.flush()  # assign DB defaults / catch constraint errors before commit
            return {"id": item.id, "name": item.name}

    def get_item(self, item_id: str) -> dict | None:
        with session_scope() as session:
            row = session.get(ItemModel, item_id)
            return {"id": row.id, "name": row.name} if row else None
```

FastAPI dependency wiring (session per request — service still owns commit):

```python
from fastapi import Depends, FastAPI

app = FastAPI()
item_service = ItemService()


@app.post("/items", status_code=201)
def create_item(body: CreateItemRequest) -> dict:
    return item_service.create_item(body)
```

Read-only path: use the same `session_scope()` or a dedicated `get_db()` dependency with `session.execute(select(...))` and no `commit` until the end of the read-only unit.

## Notes

| Topic | Practice |
|-------|----------|
| **Scope in service** | Router calls service; service opens `session_scope()` for writes |
| **One session per TX** | Don't pass sessions across threads; don't share across unrelated requests |
| **flush vs commit** | `flush` sends SQL; `commit` makes durable — use flush to surface DB errors inside TX |
| **Async** | SQLAlchemy 2 async: `async with AsyncSession(...) as session` + same commit/rollback pattern |
| **Long work** | Never hold session open during external HTTP — commit first |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Transactions overview](i-overview.md).
