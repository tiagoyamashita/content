---
label: "IV"
subtitle: "種類、テスト、ツール"
group: "Python"
groupOrder: 1
order: 4
---
Python — パート IV






** を使用した静的型付け`typing`**、**`pathlib`**、仮想環境、**`pytest`**、およびデバッグの習慣。

## 1. 入力ヒントとチェック
- 注釈文書契約 (**`def f(x: int) -> str:`**) — ライブラリが検査しない限り、**実行時に無視されます**。
- **`list[str]`**、**`dict[str, Any]`**、**`Optional[T]`** (**`T | None`** 3.10 以降)、**`Protocol`**、**`TypedDict`**、**`Literal`** 構造化された形状を表現します。
- 走る **`mypy`**、**`pyright`**、 または **`basedpyright`** CI 内 — 実行前にバグのクラス全体を捕捉します。

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


## 2. ファイルと`pathlib`- **`Path("data").joinpath("cfg.json").read_text(encoding="utf-8")`** 壊れやすいものを置き換えます **`open`** ストリングジャグリング。
- 好む **`encoding="utf-8"`** テキスト I/O で明示的に — プラットフォームのデフォルトは依然として Windows に影響を及ぼします。

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
- **`python -m venv .venv`** それから **`source .venv/bin/activate`** (POSIX) または **`.venv\Scripts\activate`** (Windows)。
- **`pip install -r requirements.txt`** または **`pyproject.toml`** + **`uv pip`** / **`pip-tools`** 再現可能なビルドのために推移的なdepsをロックします。
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


＃＃４。`pytest`基本的なこと
- 発見**`test_*.py`** / **`Test*`** クラス;アサーションはプレーン ** を使用します`assert`** 書き換えられた失敗メッセージ付き。
- **備品** (`@pytest.fixture`) 一時ディレクトリ、サーバー、DB URL を挿入します — スコープ=`module`/`session`スピードと分離性をトレードします。
- **`pytest.mark.parametrize`** は入力のコピー＆ペーストテーブルを置き換えます。
- **`monkeypatch`** / **`tmp_path`** 組み込みは、環境変数とファイルシステム サンドボックスのアドホック ハックを置き換えます。

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

デフォルト **`pytest -q`** テストがスキップされた **理由** を非表示にします。使用 **`pytest -ra`** したがって、各実行は **概要** で終了します: スキップされました (`s`)、x 失敗 (`x`)、xpassed (`X`)、選択解除など。

```text
pytest -ra
pytest -v          # every test name + PASSED/FAILED/SKIPPED as it runs
pytest --tb=short  # shorter tracebacks; combine with -ra
```

部分を入力する必要がないように、その動作を維持します。

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

** を実行するたびに**、最後の行のカウント (**成功/失敗/スキップ**) が更新されます。`pytest`**; CI がレポートをコミットしない限り、Markdown では何も自動同期されません。


## 5. デバッグワークフロー
- **`breakpoint()`** (**`pdb`**) 行でインタラクティブ シェルにドロップします — **`n`**、**`s`**、**`c`**、**`p expr`**。
- ** を使用してログを記録します`logging`** モジュール — 構造化 **`extra={}`** フィールドは一元化された可観測性スタックにフィードを提供します。
- **`traceback.print_exc()`** / **`logging.exception`** 後のスタック トレースをキャプチャします **`except`**。

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
- **`pyproject.toml`** ビルド バックエンドを一元化します (**`hatchling`**、**`setuptools`**、**`poetry`**) およびツール構成 (**)`ruff`**、**`black`**)。
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

URLopen("を使用してhttps://httpbin.org/get",timeout=5) として、それぞれ:
    body = resp.read(200)
    print(resp.status, body[:60])

# リッチクライアントの典型的な pip ワークフロー:
# pip インストール httpx
# httpx をインポートします。 httpx.get("https://example.com")