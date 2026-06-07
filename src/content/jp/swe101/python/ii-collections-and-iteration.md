---
label: "II"
subtitle: "コレクションと繰り返し"
group: "Python"
groupOrder: 1
order: 2
---
Python — パート II

リスト、タプル、辞書、セット、内包表記、反復プロトコル、および実用的なテキスト処理。

## 1. リストとタプル
- **`list`** は変更可能、順序付けられ、異種混合です — **`append`**、**`extend`**、スライス**`items[1:4]`**、**`items[:]`** 浅いコピー。
- **`tuple`** は不変です。固定形状のレコードと ** に使用します。`dict`** キー (ハッシュ可能な場合)。
- **浅いものと深いもの**: ネストされた構造は ** まで内部オブジェクトを共有します。`copy.deepcopy`**。

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


## 2. 辞書 (`dict`)
- 3.7 以降の挿入オーダー (言語保証 3.8+)。キーは**ハッシュ可能**である必要があります。
- **`dict.get(k, default)`**は避けます**`KeyError`**; **`collections.defaultdict`** 紛失したキーを工場に供給します。
- **スプレッド/マージ**: **`{**a, **b}`** (3.9+ **`a | b`**)、理解**`{k: v for ...}`**。
- **`collections.Counter`**、**`ChainMap`** 頻繁な集約/階層化された検索パターンを解決します。

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


## 3. セットとマルチセット
- **`set`** - 順序付けされていない一意の要素。 **`frozenset`** 不変/ハッシュ可能セットの場合。
- 操作: **`|`** 組合、**`&`** 交差点、**`-`** 違い、 **`^`** 対称的な違い。
- **`collections.Counter`** ハッシュ可能なアイテムをカウントします - コア言語に専用のマルチセット タイプを持たないマルチセット セマンティクス。

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


## 4. 内包表記とジェネレーター
- リストコンプ **`[expr for x in xs if cond]`** — 読みやすいワンライナー。深くネストされたコンプは避けてください。
- dict/set comps は ** を使用した構文をミラーリングします`{}`** 中括弧とキー/値の形式。
- **ジェネレータ式** **`(...)`** 値を遅延ストリーム — メモリに優しいパイプラインの供給 **`sum`**、**`any`**、**`all`**。
- **`yield`** は **ジェネレーター関数** を定義します。つまり、協調的な反復子です。 **`yield from`** サブ反復子へのデリゲート。

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


## 5. 反復プロトコル
- **`for`** 通話 **`iter()`** → **`__next__`** それまで **`StopIteration`**。
- **`enumerate`**、**`zip`**、**`reversed`**、**`itertools`** 巨大なリストを具体化せずにイテレータを構成します。

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


## 6. 文字列とバイト
- **`str`** メソッド: **`split`**、**`join`**、**`strip`**、**`startswith`**、**`format`** / **f-strings** **`f"{name!r}"`** 代表者用
- **`bytes`** ↔ **`str`** 交差は明示的なエンコーディングを使用します: **`b.decode("utf-8")`**、**`s.encode("utf-8")`** — テキストとオクテットの間の境界を **決して推測しないでください**。
- **正規表現**: **`re`** モジュール — ホット ループのパターンをコンパイルします。生の文字列 **`r"\d+"`** 逃げる痛みを軽減します。

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


## 7. 並べ替えとキー機能
- **`sorted(iterable, key=..., reverse=...)`** 新しいリストを返します。 **`.sort()`** リストを所定の位置に並べ替えます。
- **`key=lambda row: row[1]`** / **`operator.itemgetter`** 比較を安定かつ高速に保ちます。

```python
from operator import itemgetter

rows = [("ada", 98), ("grace", 100), ("linus", 95)]
by_score = sorted(rows, key=itemgetter(1), reverse=True)

words = ["pear", "apple", "kiwi"]
by_length_then_alpha = sorted(words, key=lambda w: (len(w), w))
```


## 8. 実用的なイディオム
- **開梱**: **`a, *rest, b = seq`**;呼び出し時にスター付きの辞書を解凍します。
- **`collections.namedtuple`/`typing.NamedTuple`** に達する前の軽量レコードの場合`dataclasses`** (パート III)。

「」パイソン
最初、*真ん中、最後 = [1、2、3、4、5]
print(先頭、中間、最後) # 1 [2, 3, 4] 5

デフォルト = {"ホスト": "ローカルホスト", "ポート": 5432}
オーバーライド = {"ポート": 9000}
connect(**デフォルト、**オーバーライド、user="reader")

import NamedTuple の入力から


クラスポイント(NamedTuple):
    x: 浮動小数点
    y: 浮動小数点


p = ポイント(3.0, 4.0)
print(p.x, p._replace(y=-1.0))