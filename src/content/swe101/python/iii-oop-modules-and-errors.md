---
label: "III"
subtitle: "OOP、モジュールとエラー"
group: "Python"
groupOrder: 1
order: 3
---
Python — パート III

クラス、継承と合成、プロトコル、パッケージ、構造化例外処理。

## 1. クラスとインスタンス
- **`class Name:`** 型オブジェクトを導入します。インスタンスはオブジェクトごとに保持します **`__dict__`** （ない限り **`__slots__`**)。
- **`__init__`** 状態を初期化します — **C++ の意味でのコンストラクターではありません**。 **`__new__`** を割り当てます (まれなオーバーライド)。
- **インスタンス属性**は**を介してバインドされます`self`**; **クラス属性**は型オブジェクト上に存在し、シャドウされない限り共有されます。

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
- **インスタンス メソッド**は**を必要とします`self`**; **`@staticmethod`** 受信者を無視します。 **`@classmethod`** かかります **`cls`** 代替コンストラクター/ファクトリーフック用。
- **プロパティ** (**`@property`**) 属性構文を壊さずにゲッター/セッターをラップします。

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


## 3. 継承と`super()`- **MRO** (メソッド解決順序) は基底を線形化します — ** を理解してください`super()`** 協調階層、特に複数の継承ミックスインにおいて。
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
- **`typing.Protocol`** (構造サブタイピング) ドキュメントは ** をサポートします`read()`**」スタイルのインターフェイスは、継承を強制する必要はありません。
- **`collections.abc`** (**`Sequence`**、**`Mapping`**、**`Iterable`**) ガイド **`isinstance`** 本当に必要なときにチェックします。

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


## 5. データクラスと`slots`- **`@dataclass`** データキャリアの定型文を削減 — **`frozen=True`** 不変性、**`field(default_factory=list)`** 可変デフォルトの落とし穴を回避します。
- **`__slots__`** または **`dataclass(slots=True)`** メモリと属性の作成をトリミングします — 柔軟性とトレードオフの関係。

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
- **モジュール** へのマッピング`.py`ファイル（または拡張子）。 **パッケージ**は**を含むディレクトリです`__init__.py`** (名前空間パッケージはこれを緩和します)。
- **`from pkg import mod`** 対 **`import pkg.mod`** スペルとリロード セマンティクスに影響します。
- **`if typing.TYPE_CHECKING:`** 型のみの依存関係の循環インポートを回避します。

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
- **`try / except SpecificError as e:`** — 最初に **narrow** 型をキャッチします。裸**`except:`** ツバメ **`KeyboardInterrupt`** - 避ける。
- **`raise NewError("ctx") from e`** トレースバックを保持しながら例外を連鎖させます (**`__cause__`**)。
- **`finally`** すべての出口で実行されます。 **`else`** の場合に ** が実行されます`try`** 例外なく完了しました。
- **カスタム例外** サブクラス **`Exception`** — ドメイン固有のツリーにより簡素化 **`except`** 境界。

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
- **`with open(path) as fh:`** 保証 **`close()`** - 埋め込む **`__enter__`/`__exit__`** または ** を使用してください`contextlib.contextmanager`** デコレータ **`yield`**。
- ロック、トランザクション、タイマーのクリーンアップを作成します - 手動よりもリソースのリークが少なくなります **`try/finally`**。

「」パイソン
contextlibからcontextmanagerをインポートします


クラスタイマー:
    def __enter__(self) -> "タイマー":
        print("開始")
        自分を返す

def __exit__(self, exc_type, exc, tb) -> なし:
        print("終了 (例外でも実行)")


Timer() の使用:
    print("仕事")


@contextmanager
def トランザクション():
    print("BEGIN")
    試してみてください:
        収量
        print("COMMIT")
    例外を除く:
        print("ROLLBACK")
        上げる


そこで()を使用:
    print("行を挿入")