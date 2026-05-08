---
label: "IV"
subtitle: "Types, testing & tooling"
group: "Python"
groupOrder: 1
order: 4
---
Python — Part IV
Static typing with **`typing`**, **`pathlib`**, virtual environments, **`pytest`**, and debugging habits.

## 1. Type hints & checking
- Annotations document contracts (**`def f(x: int) -> str:`**) — **ignored at runtime** unless libraries inspect them.
- **`list[str]`**, **`dict[str, Any]`**, **`Optional[T]`** (**`T | None`** in 3.10+), **`Protocol`**, **`TypedDict`**, **`Literal`** express structured shapes.
- Run **`mypy`**, **`pyright`**, or **`basedpyright`** in CI — catches whole classes of bugs before runtime.

```python
from typing import Any, Literal, Protocol, TypedDict


class HasArea(Protocol):
    def area(self) -> float: ...


class Square:
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2


def total_area(shapes: list[HasArea]) -> float:
    return sum(s.area() for s in shapes)


Mode = Literal["dev", "prod"]


class UserRow(TypedDict):
    id: int
    name: str
    meta: dict[str, Any]


def parse_mode(raw: str) -> Mode | None:
    if raw in ("dev", "prod"):
        return raw  # type checker narrows to Literal union
    return None
```


## 2. Files & `pathlib`
- **`Path("data").joinpath("cfg.json").read_text(encoding="utf-8")`** replaces fragile **`open`** string juggling.
- Prefer **`encoding="utf-8"`** explicitly on text I/O — platform defaults still bite on Windows.

```python
from pathlib import Path

root = Path("data")
cfg = root / "config.json"
root.mkdir(parents=True, exist_ok=True)

text = '{"timeout": 30}'
cfg.write_text(text, encoding="utf-8")

snapshot = cfg.read_text(encoding="utf-8")
print(snapshot)

for py_file in Path("src").rglob("*.py"):
    print(py_file.relative_to("src"))
```


## 3. Virtual environments
- **`python -m venv .venv`** then **`source .venv/bin/activate`** (POSIX) or **`.venv\Scripts\activate`** (Windows).
- **`pip install -r requirements.txt`** or **`pyproject.toml`** + **`uv pip`** / **`pip-tools`** lock transitive deps for reproducible builds.
- Never install project libs into the **global** interpreter — collisions guaranteed.

```text
# Create & activate (POSIX)
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install pytest

# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```


## 4. `pytest` fundamentals
- Discover **`test_*.py`** / **`Test*`** classes; assertions use plain **`assert`** with rewritten failure messages.
- **Fixtures** (`@pytest.fixture`) inject temporary dirs, servers, DB URLs — scope=`module`/`session` trades speed vs isolation.
- **`pytest.mark.parametrize`** replaces copy-paste tables of inputs.
- **`monkeypatch`** / **`tmp_path`** builtins replace ad-hoc hacks for env vars and filesystem sandboxes.

```python
# math_extra.py
def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


# test_clamp.py
import pytest

from math_extra import clamp


@pytest.mark.parametrize(
    "value,low,high,expected",
    [
        (1.5, 0.0, 1.0, 1.0),
        (-5.0, 0.0, 10.0, 0.0),
        (7.0, 0.0, 10.0, 7.0),
    ],
)
def test_clamp_ranges(value, low, high, expected):
    assert clamp(value, low, high) == expected


@pytest.fixture
def greeting(monkeypatch):
    monkeypatch.setenv("GREETING", "howdy")
    return __import__("os").environ["GREETING"]


def test_env_fixture(greeting):
    assert greeting == "howdy"


def test_tmp_writes(tmp_path):
    p = tmp_path / "log.txt"
    p.write_text("ok", encoding="utf-8")
    assert p.read_text(encoding="utf-8") == "ok"
```

### Passed / failed / skipped on every run

Default **`pytest -q`** hides **why** tests were skipped. Use **`pytest -ra`** so each run ends with a **summary**: skipped (`s`), xfailed (`x`), xpassed (`X`), deselected, etc.

```text
pytest -ra
pytest -v          # every test name + PASSED/FAILED/SKIPPED as it runs
pytest --tb=short  # shorter tracebacks; combine with -ra
```

Persist that behavior so you do not have to type flags:

```ini
# pytest.ini (repo root) or [tool.pytest.ini_options] in pyproject.toml
[pytest]
addopts = -ra
```

Example footer you should see after runs:

```text
=========================== short test summary info ============================
SKIPPED [1] test_api.py:15: need NETWORK=1
FAILED test_math.py::test_bad - AssertionError: ...
=========== 1 failed, 12 passed, 1 skipped, 1 warning in 0.42s ============
```

The last line’s counts (**passed / failed / skipped**) update **every time** you run **`pytest`**; nothing in Markdown auto-syncs unless CI commits reports.


## 5. Debugging workflow
- **`breakpoint()`** (**`pdb`**) drops into an interactive shell at a line — **`n`**, **`s`**, **`c`**, **`p expr`**.
- Log with **`logging`** module — structured **`extra={}`** fields feed centralized observability stacks.
- **`traceback.print_exc()`** / **`logging.exception`** capture stack traces after **`except`**.

```python
import logging
import traceback

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def flaky_div(a: float, b: float) -> float:
    # breakpoint()  # uncomment to explore locals interactively
    return a / b


try:
    print(flaky_div(1, 0))
except ZeroDivisionError:
    traceback.print_exc()
    log.exception("division failed")
    log.info("retry later", extra={"op": "flaky_div"})
```


## 6. Packaging & quality gates (overview)
- **`pyproject.toml`** centralizes build backend (**`hatchling`**, **`setuptools`**, **`poetry`**) and tool configs (**`ruff`**, **`black`**).
- **Formatters** stabilize diffs; **linters** catch unused imports and suspicious patterns — wire into pre-commit or CI.
- **`python -m compileall`** catches syntax errors cheaply before heavier suites.

```toml
# pyproject.toml (minimal sketch — adjust to your build backend)
[project]
name = "demo-app"
version = "0.1.0"
requires-python = ">=3.11"

[tool.ruff]
line-length = 100
select = ["E", "F", "I"]
```

```text
python -m compileall src
ruff check src
pytest -q -ra
```


## 7. When to reach beyond stdlib
- **HTTP clients**: **`httpx`** / **`requests`**; **async**: **`asyncio`** + **`aiohttp`** (complexity budget required).
- **Numerics**: **`numpy`** / **`pandas`** — ownership semantics differ from pure Python lists; profile hot loops.

```python
# urllib is stdlib-only GET (no extra pip dependency)
from urllib.request import urlopen

with urlopen("https://httpbin.org/get", timeout=5) as resp:
    body = resp.read(200)
    print(resp.status, body[:60])

# Typical pip workflow for richer clients:
# pip install httpx
# import httpx; httpx.get("https://example.com")