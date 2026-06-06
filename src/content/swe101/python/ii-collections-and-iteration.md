---
label: "II"
subtitle: "Collections & iteration"
group: "Python"
groupOrder: 1
order: 2
---
Python — Part II
Lists, tuples, dictionaries, sets, comprehensions, iteration protocols, and practical text handling.

## 1. Lists & tuples
- **`list`** is mutable, ordered, heterogeneous — **`append`**, **`extend`**, slicing **`items[1:4]`**, **`items[:]`** shallow copy.
- **`tuple`** is immutable — use for fixed-shape records and **`dict`** keys (when hashable).
- **Shallow vs deep**: nested structures share inner objects until **`copy.deepcopy`**.

```python
import copy

row = [10, 20, 30]
window = row[1:3]          # [20, 30] — new list, shallow
row[1] = 99
print(window)             # [99, 30] — indices still alias original slots

grid = [[1], [2]]
grid_copy = copy.deepcopy(grid)
grid[0].append(8)
print(grid_copy)          # [[1], [2]] — inner lists decoupled

point = (3, 4)
xs = {(0, 0), point}      # tuples are hashable if contents are hashable
```


## 2. Dictionaries (`dict`)
- Insertion-ordered since 3.7 (language guarantee 3.8+); keys must be **hashable**.
- **`dict.get(k, default)`** avoids **`KeyError`**; **`collections.defaultdict`** supplies factories for missing keys.
- **Spread / merge**: **`{**a, **b}`** (3.9+ **`a | b`**), comprehension **`{k: v for ...}`**.
- **`collections.Counter`**, **`ChainMap`** solve frequent aggregation / layered lookup patterns.

```python
from collections import ChainMap, Counter, defaultdict

scores = {"ada": 98, "grace": 100}
print(scores.get("linus", 0))    # 0 — no KeyError

by_len: defaultdict[int, list[str]] = defaultdict(list)
for word in ("aa", "bbb", "cc", "d"):
    by_len[len(word)].append(word)

counts = Counter("abracadabra")
print(counts.most_common(2))     # [('a', 5), ('b', 2)]

defaults = {"theme": "dark"}
user = {"theme": "light", "locale": "BR"}
merged = defaults | user       # user wins on clash — Python 3.9+
overlay = ChainMap(user, defaults)
print(overlay["theme"])          # light — walks maps in order

squares = {n: n * n for n in range(5)}
```


## 3. Sets & multisets
- **`set`** — unordered unique elements; **`frozenset`** for immutable/hashable sets.
- Operations: **`|`** union, **`&`** intersection, **`-`** difference, **`^`** symmetric difference.
- **`collections.Counter`** counts hashable items — multiset semantics without a dedicated multiset type in the core language.

```python
admins = {"ada", "grace"}
mods = {"grace", "tim"}

print(admins | mods)     # union
print(admins & mods)     # intersection {grace}
print(admins - mods)     # difference {ada}

frozen = frozenset({1, 2})
registry = {frozen: "pair"}   # frozenset can be dict key

from collections import Counter

votes = Counter(["red", "blue", "red", "red"])
print(votes["green"])    # 0 — Counter returns 0 for missing keys
```


## 4. Comprehensions & generators
- List comp **`[expr for x in xs if cond]`** — readable one-liners; avoid deeply nested comps.
- Dict/set comps mirror syntax with **`{}`** braces and key/value forms.
- **Generator expressions** **`(...)`** stream values lazily — memory-friendly pipelines feeding **`sum`**, **`any`**, **`all`**.
- **`yield`** defines **generator functions** — cooperative iterators; **`yield from`** delegates to sub-iterators.

```python
nums = range(10)
evens_squared = [n * n for n in nums if n % 2 == 0]

unique_lengths = {len(w) for w in ("aa", "bbb", "aa")}

total = sum(n * n for n in range(1_000_000) if n % 2 == 0)  # no giant list in RAM


def countdown(start: int):
    while start >= 0:
        yield start
        start -= 1


def chained():
    yield from [1, 2]
    yield from countdown(2)


print(list(chained()))   # [1, 2, 2, 1, 0]
```


## 5. Iteration protocol
- **`for`** calls **`iter()`** → **`__next__`** until **`StopIteration`**.
- **`enumerate`**, **`zip`**, **`reversed`**, **`itertools`** compose iterators without materializing giant lists.

```python
names = ["Ada", "Grace"]
years = [1815, 1906]
for name, year in zip(names, years, strict=True):  # strict=… requires Python 3.10+
    print(name, year)

nums = [10, 20, 30, 40]
pairs = list(zip(nums, nums[1:]))                  # [(10, 20), (20, 30), (30, 40)]

# Chunk a list without itertools.batched (3.12+)
data = list(range(7))
chunk_size = 3
chunks = [data[i : i + chunk_size] for i in range(0, len(data), chunk_size)]
print(chunks)  # [[0, 1, 2], [3, 4, 5], [6]]
```


## 6. Strings & bytes
- **`str`** methods: **`split`**, **`join`**, **`strip`**, **`startswith`**, **`format`** / **f-strings** **`f"{name!r}"`** for repr.
- **`bytes`** ↔ **`str`** crossing uses explicit encodings: **`b.decode("utf-8")`**, **`s.encode("utf-8")`** — **never guess** at boundaries between text and octets.
- **Regex**: **`re`** module — compile patterns for hot loops; raw strings **`r"\d+"`** reduce escaping pain.

```python
import re

csv_line = " ada , linus , grace "
cols = [c.strip() for c in csv_line.split(",")]
joined = " | ".join(cols)

path = r"C:\new\files.txt"      # raw string — backslashes literal
print(len(re.findall(r"\d+", "Room 404 on floor 3")))  # 3 digit runs

blob = "café".encode("utf-8")
text = blob.decode("utf-8")
```


## 7. Sorting & key functions
- **`sorted(iterable, key=..., reverse=...)`** returns new list; **`.sort()`** sorts lists in place.
- **`key=lambda row: row[1]`** / **`operator.itemgetter`** keeps comparisons stable and fast.

```python
from operator import itemgetter

rows = [("ada", 98), ("grace", 100), ("linus", 95)]
by_score = sorted(rows, key=itemgetter(1), reverse=True)

words = ["pear", "apple", "kiwi"]
by_length_then_alpha = sorted(words, key=lambda w: (len(w), w))
```


## 8. Practical idioms
- **Unpacking**: **`a, *rest, b = seq`**; starred dict unpacking in calls.
- **`collections.namedtuple` / `typing.NamedTuple`** for lightweight records before reaching **`dataclasses`** (Part III).

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first, middle, last)   # 1 [2, 3, 4] 5

defaults = {"host": "localhost", "port": 5432}
override = {"port": 9000}
connect(**defaults, **override, user="reader")

from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float


p = Point(3.0, 4.0)
print(p.x, p._replace(y=-1.0))