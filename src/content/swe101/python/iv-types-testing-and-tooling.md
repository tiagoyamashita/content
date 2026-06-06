---
label: "IV"
subtitle: "種類、テスト、ツール"
group: "パイソン"
groupOrder: 1
order: 4
---
Python — パート IV

**`typing`**、**`pathlib`**、仮想環境、**`pytest`**、およびデバッグ習慣による静的型付け。

## 1. 入力ヒントとチェック
- アノテーション ドキュメント コントラクト (**`def f(x: int) -> str:`**) — ライブラリが検査しない限り、**実行時に無視されます**。
- **`list[str]`**、**`dict[str, Any]`**、**`Optional[T]`** (**`T | None`** 3.10 以降)、**`Protocol`**、**`TypedDict`**、**`Literal`** は構造化された形状を表します。
- CI で **`mypy`**、**`pyright`**、または **`basedpyright`** を実行します。実行前にバグのクラス全体を捕捉します。

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


## 2. ファイルと `pathlib`
- **`Path("data").joinpath("cfg.json").read_text(encoding="utf-8")`** は壊れやすい **`open`** のストリング ジャグリングを置き換えます。
- テキスト I/O では **`encoding="utf-8"`** を明示的に優先します。プラットフォームのデフォルトは依然として Windows に影響します。

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


## 3. 仮想環境
- **`python -m venv .venv`**、次に **`source .venv/bin/activate`** (POSIX) または **`.venv\Scripts\activate`** (Windows)。
- **`pip install -r requirements.txt`** または **`pyproject.toml`** + **`uv pip`** / **`pip-tools`** は、再現可能なビルドのための推移的な DEP をロックします。
- プロジェクト ライブラリを **グローバル** インタプリタにインストールしないでください。衝突が保証されます。

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


## 4. `pytest` の基本
- **`test_*.py`** / **`Test*`** クラスを発見;アサーションは、書き換えられた失敗メッセージを含むプレーン **`assert`** を使用します。
- **フィクスチャ** (`@pytest.fixture`) 一時ディレクトリ、サーバー、DB URL を挿入します — スコープ=`module`/`session`は速度と分離性をトレードします。
- **`pytest.mark.parametrize`** は入力のコピー＆ペーストテーブルを置き換えます。
- **`monkeypatch`** / **`tmp_path`** ビルトインは、環境変数とファイルシステム サンドボックスのアドホック ハックを置き換えます。

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

### 実行ごとに成功/失敗/スキップ

デフォルトの **`pytest -q`** は、テストがスキップされた **理由** を非表示にします。 **`pytest -ra`** を使用すると、各実行が **概要** で終了します: スキップ (`s`)、x 失敗 (`x`)、x 合格 (`X`)、選択解除など。

```text
pytest -ra
pytest -v          # every test name + PASSED/FAILED/SKIPPED as it runs
pytest --tb=short  # shorter tracebacks; combine with -ra
```

フラグを入力する必要がないように、その動作を維持します。

```ini
# pytest.ini (repo root) or [tool.pytest.ini_options] in pyproject.toml
[pytest]
addopts = -ra
```

実行後に表示されるフッターの例:

```text
=========================== short test summary info ============================
SKIPPED [1] test_api.py:15: need NETWORK=1
FAILED test_math.py::test_bad - AssertionError: ...
=========== 1 failed, 12 passed, 1 skipped, 1 warning in 0.42s ============
```

最後の行のカウント (**成功 / 失敗 / スキップ**) は、***`pytest`** を実行するたびに**更新されます。 CI がレポートをコミットしない限り、Markdown では何も自動同期されません。


## 5. デバッグワークフロー
- **`breakpoint()`** (**`pdb`**) は、対話型シェルの **`n`**、**`s`**、**`c`**、**`p expr`** の行にドロップされます。
- **`logging`** モジュールを使用したログ — 構造化された **`extra={}`** フィールドは、一元的な可観測性スタックにフィードします。
- **`traceback.print_exc()`** / **`logging.exception`** は **`except`** 以降のスタック トレースをキャプチャします。

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


## 6. パッケージングと品質ゲート (概要)
- **`pyproject.toml`** は、ビルド バックエンド (**`hatchling`**、**`setuptools`**、**`poetry`**) とツール構成 (**`ruff`**、**`black`**) を一元化します。
- **フォーマッタ** は差分を安定させます。 **リンター** は、未使用のインポートと疑わしいパターンを捕捉します。コミット前または CI に接続します。
- **`python -m compileall`** は、重いスイートよりも前に、構文エラーを安価にキャッチします。

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


## 7. stdlib を超える場合
- **HTTP クライアント**: **`httpx`** / **`requests`**; **非同期**: **`asyncio`** + **`aiohttp`** (複雑さの予算が必要)。
- **数値**: **`numpy`** / **`pandas`** — 所有権のセマンティクスは純粋な Python リストとは異なります。プロファイルホットループ。

「」パイソン
# urllib は stdlib のみの GET (余分な pip 依存関係はありません)
urllib.request から urlopen をインポート

urlopen("https://httpbin.org/get", timeout=5) をそれぞれ次のように指定します。
    body = resp.read(200)
    print(resp.status, body[:60])

# リッチクライアントの典型的な pip ワークフロー:
# pip インストール httpx
# httpx をインポートします。 httpx.get("https://example.com")