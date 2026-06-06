---
label: "I"
subtitle: "Basics & syntax"
group: "Python"
groupOrder: 1
order: 1
---
Python — Part I
How code runs, core syntax, built-in types, control flow, functions, and organizing small programs.

## 1. Interpreter model & tooling
- Python executes **source → bytecode → VM** (similar idea to Java’s JVM, but typically interpreted per process unless using specialized JITs).
- **`python script.py`** runs a file; **`python -m module`** executes a package/module as **`__main__`**.
- **REPL** (`python`, **`ipython`**) is ideal for quick experiments — paste multi-line blocks carefully or use files for anything non-trivial.

```text
# Terminal examples (same folder as greet.py)
python greet.py                    # run a script file
python -m http.server 8000         # run stdlib module as a tiny static file server
python -c "print(2 ** 10)"         # one-liner without a file
```


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 108" role="img" aria-label="Python source to execution">
  <text x="92" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Typical run path</text>
  <rect x="24" y="34" width="92" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="42" y="56" fill="#e4e4e7" font-size="10">app.py</text>
  <path d="M116 52 H158" stroke="#a1a1aa" stroke-width="2"/>
  <text x="162" y="56" fill="#71717a" font-size="10">compile</text>
  <path d="M224 52 H262" stroke="#a1a1aa" stroke-width="2"/>
  <rect x="264" y="34" width="96" height="36" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="278" y="56" fill="#e4e4e7" font-size="10">bytecode</text>
  <path d="M362 52 H392" stroke="#a1a1aa" stroke-width="2"/>
  <text x="44" y="96" fill="#71717a" font-size="9">CPython bytecode (.pyc caches) — semantics follow language reference + version you run</text>
</svg></figure>


## 2. Indentation & blocks
- **Indentation defines suites** after `if`, `for`, `def`, `class`, etc. — mix tabs and spaces only at your own risk (**PEP 8**: 4 spaces).
- **`pass`** is a no-op placeholder where syntax demands a body.

```python
def toggle(enabled: bool) -> str:
    if enabled:
        return "on"
    elif not enabled:
        return "off"
    else:
        pass  # unreachable here — bool is only True/False


class Placeholder:
    pass  # class body cannot be empty without pass
```


## 3. Names, assignment, and mutability
- **Names** bind to objects; assignment **`a = b`** rebinds **`a`** — it never copies objects unless you ask (`copy.copy`, `copy.deepcopy`, slicing where applicable).
- **`id()`** / **`is`** expose object identity; **`==`** compares **value** via **`__eq__`**.
- **Numbers**: arbitrary-precision integers; **`float`** is IEEE binary — use **`decimal.Decimal`** for money-style rules.

```python
import copy

xs = [1, 2, 3]
ys = xs              # same list object — mutate xs, ys changes too
zs = xs[:]           # shallow copy — top-level list is new
nested = [[1], [2]]
clone = copy.deepcopy(nested)
nested[0].append(99)
print(clone)         # [[1], [2]] — inner lists not shared with nested after deepcopy

a = 256
b = 256
print(a is b)        # often True for small integers cached by CPython — don't rely on identity for ints

from decimal import Decimal
price = Decimal("19.99") * 3   # exact decimal arithmetic vs float rounding surprises
```


## 4. Core built-in types
- **`str`** (immutable Unicode), **`bytes`** / **`bytearray`** for raw octets.
- **`None`**, **`bool`**, **`int`**, **`float`**, **`complex`**.
- **Truthiness**: empty containers and **`None`** / **`0`** / **`""`** are falsy unless customized.

```python
label: str = "hello"
raw: bytes = b"\xff\xfe"
mutable_raw = bytearray(b"abc")
mutable_raw[0] = ord("z")

values = ["", [1], 0, None]
print([bool(v) for v in values])   # [False, True, False, False]
```


## 5. Control flow
- **`if / elif / else`**, **`match / case`** (structural pattern matching, 3.10+).
- **`for x in iterable:`** drives loops — never manually manage indices unless needed; **`enumerate`** pairs index + value.
- **`while`**, **`break`**, **`continue`**, **`else`** on loops (runs if loop completed without **`break`**).

```python
users = ["ada", "linus", "grace"]

for i, name in enumerate(users, start=1):
    print(i, name.upper())

# loop else: runs only if break never fired
for n in range(2, 10):
    if 91 % n == 0:
        print("factor found", n)
        break
else:
    print("91 had no divisor in range — it's prime here")

def http_status_label(code: int) -> str:
    match code:
        case 200:
            return "OK"
        case 404:
            return "Not Found"
        case _:
            return "other"
```


## 6. Functions
- **`def`** defines functions; **`return`** ends execution; omitting **`return`** ⇒ **`None`**.
- **Parameters**: positional, keyword-only (`*` separator), variadic **`*args`**, keyword dict **`**kwargs`**.
- **Default arguments** are evaluated **once** at definition time — avoid mutable defaults (`def f(x=[])` bug pattern); use **`None`** + inner initialization instead.
- **Inner functions** close over enclosing scopes — late-binding gotchas appear with loops creating lambdas unless default args capture values.

```python
def greet(title: str, name: str, *, shout: bool = False) -> str:
    msg = f"{title} {name}"
    return msg.upper() if shout else msg


print(greet("Ms.", "Hopper", shout=True))


def trace(prefix: str, *parts: int, **meta: str) -> None:
    print(prefix, parts, meta)


trace("nums", 1, 2, 3, user="ada")   # nums (1, 2, 3) {'user': 'ada'}


# BAD: shared mutable default
def append_bug(item, bucket=[]):  # noqa: deliberately wrong for demo
    bucket.append(item)
    return bucket


# GOOD: fresh list each call
def append_ok(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket


# Lambda closure: default arg binds i at definition time (fixes late binding)
funcs = [(lambda x, i=i: x + i) for i in range(3)]
print([f(10) for f in funcs])   # [10, 11, 12] not [12, 12, 12]
```


## 7. Imports & `__name__`
- **`import math`** vs **`from math import sqrt`** — prefer qualified imports for larger modules to avoid name clashes.
- **`if __name__ == "__main__":`** guards runnable scripts when imported as libraries.

```python
# stats.py — safe to import AND runnable as a script
from __future__ import annotations

import statistics


def summarize(nums: list[float]) -> tuple[float, float]:
    return statistics.mean(nums), statistics.stdev(nums)


if __name__ == "__main__":
    sample = [1.2, 2.4, 3.1, 4.0]
    mean, stdev = summarize(sample)
    print(f"mean={mean:.2f} stdev={stdev:.2f}")
```


## 8. Docstrings & style
- Module/class/function **docstrings** (`""" ... """`) power **`help()`** and Sphinx/MkDoc — first line summary, blank line, details.
- **`python -m pip`** installs packages into the active interpreter — pair with virtual environments (Part IV).

```python
def clamp(value: float, low: float, high: float) -> float:
    """Restrict value to the inclusive range [low, high].

    Examples:
        >>> clamp(1.5, 0.0, 1.0)
        1.0
    """
    return max(low, min(high, value))
