---
label: "I"
subtitle: "基本と構文"
group: "パイソン"
groupOrder: 1
order: 1
---
Python — パート I

コードの実行方法、コア構文、組み込み型、制御フロー、関数、小さなプログラムの構成。

## 1. インタプリタのモデルとツール
- Python は **ソース → バイトコード → VM** を実行します (Java の JVM と同様の考え方ですが、特殊な JIT を使用しない限り、通常はプロセスごとに解釈されます)。
- **`python script.py`** はファイルを実行します。 **`python -m module`** はパッケージ/モジュールを **`__main__`** として実行します。
- **REPL** (`python`、**`ipython`**) は、簡単な実験に最適です。複数行のブロックを慎重に貼り付けるか、重要な作業にはファイルを使用します。

```text
# Terminal examples (same folder as greet.py)
python greet.py                    # run a script file
python -m http.server 8000         # run stdlib module as a tiny static file server
python -c "print(2 ** 10)"         # one-liner without a file
```


<figure class="notes-diagram"><svg xmlns="63 viewBox="0 0 420 108" role="img" aria-label="Python source to execution">
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


## 2. インデントとブロック
- **インデントは、`if`、`for`、`def`、`class` などの後のスイートを定義します。タブとスペースを組み合わせる場合は、自己責任でのみ行ってください (**PEP 8**: スペース 4 つ)。
- **`pass`** は、構文が本体を必要とする no-op プレースホルダーです。

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


## 3. 名前、割り当て、変更可能性
- **名前**はオブジェクトにバインドされます。代入 **`a = b`** は **`a`** を再バインドします。要求しない限り、オブジェクトをコピーすることはありません (`copy.copy`、`copy.deepcopy`、該当する場合はスライス)。
- **`id()`** / **`is`** オブジェクトのアイデンティティを公開します。 **`==`** は **`__eq__`** を介して **value** を比較します。
- **数値**: 任意精度の整数。 **`float`** は IEEE バイナリです。通貨形式のルールには **`decimal.Decimal`** を使用します。

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


## 4. コアの組み込み型
- **`str`** (不変 Unicode)、生のオクテットの場合は **`bytes`** / **`bytearray`**。
- **`None`**、**`bool`**、**`int`**、**`float`**、**`complex`**。
- **真実性**: 空のコンテナと **`None`** / **`0`** / **`""`** はカスタマイズされていない限り偽です。

```python
label: str = "hello"
raw: bytes = b"\xff\xfe"
mutable_raw = bytearray(b"abc")
mutable_raw[0] = ord("z")

values = ["", [1], 0, None]
print([bool(v) for v in values])   # [False, True, False, False]
```


## 5. 制御フロー
- **`if / elif / else`**、**`match / case`** (構造パターン マッチング、3.10 以降)。
- **`for x in iterable:`** はループを駆動します。必要な場合を除き、インデックスを手動で管理しないでください。 **`enumerate`** インデックス + 値のペア。
- ループ上の **`while`**、**`break`**、**`continue`**、**`else`** (**`break`** なしでループが完了した場合に実行)。

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


## 6. 機能
- **`def`** は関数を定義します。 **`return`** 実行を終了します。 **`return`** ⇒ **`None`** は省略します。
- **パラメータ**: 位置、キーワードのみ (`*` 区切り文字)、可変長引数 **`*args`**、キーワード辞書 **`**kwargs`**。
- **デフォルト引数**は定義時に**1回**評価されます。変更可能なデフォルトを回避します(`def f(x=[])`バグパターン)。代わりに **`None`** + 内部初期化を使用してください。
- **内部関数**は、外側のスコープを超えて閉じます。デフォルトの引数が値を取得しない限り、ラムダを作成するループで遅延バインディングの問題が発生します。

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


## 7. 輸入と`__name__`
- **`import math`** 対 **`from math import sqrt`** — 名前の衝突を避けるために、より大きなモジュールの修飾されたインポートを優先します。
- **`if __name__ == "__main__":`** は、ライブラリとしてインポートされるときに実行可能なスクリプトを保護します。

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


## 8. ドキュメント文字列とスタイル
- モジュール/クラス/関数 **docstrings** (`""" ... """`) パワー **`help()`** および Sphinx/MkDoc - 最初の行の概要、空行、詳細。
- **`python -m pip`** は、アクティブなインタープリターにパッケージをインストールします — 仮想環境とペアリングします (パート IV)。

「」パイソン
def クランプ(値: 浮動小数点、低値: 浮動小数点、高値: 浮動小数点) -> 浮動小数点:
    """値を包括的な範囲 [低、高] に制限します。

例:
        >>> クランプ(1.5、0.0、1.0)
        1.0
    「」
    最大(低値, 最小(高値, 値))を返します
