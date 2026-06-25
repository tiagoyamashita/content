---
label: "III"
subtitle: "OOP, modules & errors"
group: "Python"
groupOrder: 1
order: 3
---
Python — Part III
Classes, inheritance versus composition, protocols, packages, and structured exception handling.

## 1. Classes & instances
- **`class Name:`** introduces a type object; instances carry per-object **`__dict__`** (unless **`__slots__`**).
- **`__init__`** initializes state — **not** a constructor in the C++ sense; **`__new__`** allocates (rare override).
- **Instance attributes** bind via **`self`**; **class attributes** live on the type object and are shared unless shadowed.

```python
class Greeter:
    default_lang = "en"          # class attribute — shared

    def __init__(self, name: str) -> None:
        self.name = name         # instance attribute

    def hello(self) -> str:
        return f"[{self.default_lang}] hello {self.name}"


g = Greeter("Ada")
Greeter.default_lang = "pt"
print(g.hello())                # [pt] hello Ada
```


## 2. Methods & descriptors
- **Instance methods** take **`self`**; **`@staticmethod`** ignores receiver; **`@classmethod`** takes **`cls`** for alternate constructors/factory hooks.
- **Properties** (**`@property`**) wrap getters/setters without breaking attribute syntax.

```python
class Temperature:
    def __init__(self, kelvin: float) -> None:
        self._k = kelvin

    @property
    def kelvin(self) -> float:
        return self._k

    @kelvin.setter
    def kelvin(self, value: float) -> None:
        if value < 0:
            raise ValueError("Kelvin cannot be negative")
        self._k = value

    @classmethod
    def from_celsius(cls, c: float) -> Temperature:
        return cls(c + 273.15)

    @staticmethod
    def is_boiling_water_k(k: float) -> bool:
        return k >= 373.15
```


## 3. Inheritance & `super()`
- **MRO** (method resolution order) linearizes bases — understand **`super()`** in cooperative hierarchies, especially multiple inheritance mix-ins.
- Prefer **composition** (has-a) when behavior varies independently — inheritance encodes **is-a** taxonomies.

```python
class LoggerMixin:
    def log(self, msg: str) -> None:
        print(f"[{self.__class__.__name__}] {msg}")


class Worker(LoggerMixin):
    def run(self) -> None:
        self.log("starting")
        self.log("finished")


class Base:
    def ping(self) -> str:
        return "base"


class Child(Base):
    def ping(self) -> str:
        return super().ping() + "+child"


print(Child().ping())            # base+child — super follows MRO


class Engine:
    def start(self) -> None:
        print("vroom")


class Car:
    def __init__(self) -> None:
        self._engine = Engine()   # composition — swap engines without subclassing

    def drive(self) -> None:
        self._engine.start()
```


## 4. Duck typing & protocols
- **`typing.Protocol`** (structural subtyping) documents “supports **`read()`**” style interfaces without forcing inheritance.
- **`collections.abc`** (**`Sequence`**, **`Mapping`**, **`Iterable`**) guides **`isinstance`** checks when you truly need them.

```python
from collections.abc import Mapping
from typing import Protocol


class Readable(Protocol):
    def read(self, n: int = -1) -> str: ...


def slugify(source: Readable) -> str:
    return source.read().strip().lower().replace(" ", "-")


class FakeFile:
    def read(self, n: int = -1) -> str:
        return "Hello World"


print(slugify(FakeFile()))       # structural match — no inheritance from Readable

cfg = {"timeout": 30}
print(isinstance(cfg, Mapping))  # True
```


## 5. Dataclasses & `slots`
- **`@dataclass`** reduces boilerplate for data carriers — **`frozen=True`** immutability, **`field(default_factory=list)`** dodges mutable-default pitfalls.
- **`__slots__`** or **`dataclass(slots=True)`** trims memory and attribute creation — trade-offs vs flexibility.

```python
from dataclasses import dataclass, field


@dataclass(slots=True)
class Order:
    id: int
    items: list[str] = field(default_factory=list)
    paid: bool = False


@dataclass(frozen=True)
class Point:
    x: float
    y: float


o = Order(1)
o.items.append("keyboard")
p = Point(1.0, 2.0)
# p.x = 0  # dataclass.FrozenInstanceError
```


## 6. Modules & packages
- **Modules** map to `.py` files (or extensions); **packages** are directories with **`__init__.py`** (namespace packages relax this).
- **`from pkg import mod`** vs **`import pkg.mod`** affects spelling and reload semantics.
- **`if typing.TYPE_CHECKING:`** avoids circular imports for type-only dependencies.

```python
# Two import styles for the same standard-library module
import pathlib
from pathlib import Path

root = Path.cwd()
readme = pathlib.Path.joinpath(root, "README.md")
print(readme.name)


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Example: import symbols only for static type checkers, not at runtime
    from collections.abc import Mapping  # noqa: F401 — illustrative import
```


## 7. Exceptions
- **`try / except SpecificError as e:`** — catch **narrow** types first; bare **`except:`** swallows **`KeyboardInterrupt`** — avoid.
- **`raise NewError("ctx") from e`** chains exceptions preserving tracebacks (**`__cause__`**).
- **`finally`** runs on all exits; **`else`** runs if **`try`** completed without exception.
- **Custom exceptions** subclass **`Exception`** — domain-specific trees simplify **`except`** boundaries.

```python
class DomainError(Exception):
    """Base for business-rule violations."""


class NegativeBalance(DomainError):
    pass


def withdraw(balance: float, amount: float) -> float:
    if amount < 0:
        raise ValueError("amount must be non-negative")
    if amount > balance:
        raise NegativeBalance("insufficient funds")
    return balance - amount


try:
    withdraw(10.0, 20.0)
except NegativeBalance as err:
    raise RuntimeError("payment failed") from err
```


## 8. Context managers
- **`with open(path) as fh:`** guarantees **`close()`** — implement **`__enter__` / `__exit__`** or use **`contextlib.contextmanager`** decorator with **`yield`**.
- Compose cleanup for locks, transactions, timers — fewer leaked resources than manual **`try/finally`**.

```python
from contextlib import contextmanager


class Timer:
    def __enter__(self) -> "Timer":
        print("start")
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        print("end (runs even on exception)")


with Timer():
    print("work")


@contextmanager
def transactional():
    print("BEGIN")
    try:
        yield
        print("COMMIT")
    except Exception:
        print("ROLLBACK")
        raise


with transactional():
    print("insert rows")