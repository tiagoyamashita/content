---
label: "III"
subtitle: "OOP、モジュール、エラー"
group: "パイソン"
groupOrder: 1
order: 3
---
Python — パート III

クラス、継承と合成、プロトコル、パッケージ、構造化例外処理。

## 1. クラスとインスタンス
- **`class Name:`** は型オブジェクトを導入します。インスタンスはオブジェクトごとに **`__dict__`** を保持します (**`__slots__`** を除く)。
- **`__init__`** は状態を初期化します。**C++ の意味でのコンストラクターではありません**。 **`__new__`** は割り当てます (まれなオーバーライド)。
- **インスタンス属性**は**`self`**を介してバインドされます。 **クラス属性**は型オブジェクト上に存在し、シャドウされない限り共有されます。

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


## 2. メソッドと記述子
- **インスタンス メソッド**は **`self`** かかります。 **`@staticmethod`** は受信者を無視します。 **`@classmethod`** は、代替コンストラクタ/ファクトリ フックに **`cls`** を必要とします。
- **プロパティ** (**`@property`**) は、属性の構文を壊さずにゲッター/セッターをラップします。

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


## 3. 継承と `super()`
- **MRO** (メソッド解決順序) は塩基を線形化します。協調階層、特に多重継承ミックスインにおける **`super()`** を理解します。
- 動作が個別に異なる場合は **composition** (has-a) を優先します。継承は **is-a** 分類法をエンコードします。

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


## 4. アヒルタイピングとプロトコル
- **`typing.Protocol`** (構造サブタイピング) ドキュメントは、継承を強制せずに「**`read()`**」スタイルのインターフェイスをサポートします。
- **`collections.abc`** (**`Sequence`**、**`Mapping`**、**`Iterable`**) は、本当に必要なときに **`isinstance`** チェックをガイドします。

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


## 5. データクラスと `slots`
- **`@dataclass`** はデータ キャリアのボイラープレートを削減します。 — **`frozen=True`** は不変であり、**`field(default_factory=list)`** は可変デフォルトの落とし穴を回避します。
- **`__slots__`** または **`dataclass(slots=True)`** はメモリと属性の作成をトリミングします。これは柔軟性とトレードオフの関係です。

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


## 6. モジュールとパッケージ
- **モジュール**は `.py` ファイル (または拡張子) にマップされます。 **packages** は **`__init__.py`** のディレクトリです (名前空間パッケージはこれを緩和します)。
- **`from pkg import mod`** と **`import pkg.mod`** は、スペルとリロード セマンティクスに影響します。
- **`if typing.TYPE_CHECKING:`** は、型のみの依存関係の循環インポートを回避します。

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


## 7. 例外
- **`try / except SpecificError as e:`** — **狭い**型を最初にキャッチします。裸の **`except:`** を飲み込む **`KeyboardInterrupt`** — 避けてください。
- **`raise NewError("ctx") from e`** トレースバックを保持しながら例外を連鎖させます (**`__cause__`**)。
- **`finally`** はすべての出口で実行されます。 **`try`** が例外なく完了した場合、**`else`** が実行されます。
- **カスタム例外** サブクラス **`Exception`** — ドメイン固有のツリーにより **`except`** 境界が簡素化されます。

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


## 8. コンテキストマネージャー
- **`with open(path) as fh:`** は **`close()`** を保証します — **`__enter__` / `__exit__`** を実装するか、**`contextlib.contextmanager`** デコレータを **`yield`** とともに使用します。
- ロック、トランザクション、タイマーのクリーンアップを作成します。手動 **`try/finally`** よりもリソースのリークが少なくなります。

「」パイソン
contextlibからcontextmanagerをインポートします


クラスタイマー:
    def __enter__(self) -> "タイマー":
        print("開始")
        自分を返す

def __exit__(self, exc_type, exc, tb) -> なし:
        print("終了 (例外でも実行)")


Timer() を使用:
    print("仕事")


@contextmanager
def トランザクション():
    print("開始")
    試してみてください:
        収量
        print("コミット")
    例外を除く:
        print("ロールバック")
        上げる


トランザクション()を使用:
    print("行を挿入")