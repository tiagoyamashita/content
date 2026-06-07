---
label: "V"
subtitle: "ファイルI/O"
group: "Python"
groupOrder: 1
order: 5
---
Python — パート V

ファイルの安全な読み取りと書き込み: テキストとバイナリ、エンコーディング、ストリーミング ライン、構造化フォーマット、一般的な障害モード。

## 1. 2 種類のファイルの内容
- **テキストモード** (`"r"`、`"w"`、`"a"`, …): Python はバイトをデコードします → **`str`** **エンコーディング**を使用します (デフォルトはロケールに依存します — **常にパスします)`encoding="utf-8"`** ポータブル アプリの場合)。
- **バイナリモード** (`"rb"`、`"wb"`): あなたは読み取り/書き込み **`bytes`** — 画像、zip BLOB、pickle (注意)、または手動で処理する未知のエンコーディングに使用します。


＃＃２。`pathlib`対`open()`**`pathlib.Path`通常、ファイル全体の読み取り/書き込みの場合は ** の方が明確です。 **`open()`** ストリーミングしている場合や、きめ細かい制御が必要な場合に点灯します。

```python
from pathlib import Path

out = Path("build") / "note.txt"
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text("hello\nworld\n", encoding="utf-8")

text = out.read_text(encoding="utf-8")
blob = out.read_bytes()

print(text.splitlines())
```

**と同じ操作`open`**:

```python
path = Path("build/note.txt")

with path.open("w", encoding="utf-8", newline="") as fh:
    fh.write("line1\n")
    fh.writelines(["line2\n", "line3\n"])

with path.open("r", encoding="utf-8") as fh:
    body = fh.read()
```


## 3. テキスト ファイルの改行とエンコーディングを常に制御する
- **`newline=""`**使用する場合**`csv`** モジュール — リーダー/ライターの制御を可能にします`\r\n`対`\n`翻訳 (**CSV ドキュメントでは、Windows ではこれを推奨しています**)。
- **`errors="replace"`/`"strict"`/`"ignore"`** バイトが有効でない場合のデコーダの動作を調整します UTF-8。

```python
from pathlib import Path

legacy = Path("latin1.bin")
legacy.write_bytes("café".encode("latin-1"))

text = legacy.read_text(encoding="latin-1")
utf8_path = Path("utf8copy.txt")
utf8_path.write_text(text, encoding="utf-8")
```


## 4. 丸呑みする代わりにストリーミングする
大きなログまたはデータセット: ファイル全体を RAM にロードせずに行を繰り返します。

```python
from pathlib import Path


def count_matching_lines(path: Path, needle: str) -> int:
    n = 0
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            if needle in line:
                n += 1
    return n


def tail_bytes(path: Path, max_bytes: int = 4096) -> bytes:
    with path.open("rb") as fh:
        fh.seek(0, 2)                      # end of file
        size = fh.tell()
        fh.seek(max(0, size - max_bytes))
        return fh.read()
```


## 5. CSV と区切り文字で区切られたテキスト
**を使用してください`csv`** モジュール — カンマで手動で分割しないでください (引用符、埋め込みカンマ)。

```python
import csv
from pathlib import Path

src = Path("users.csv")
with src.open("r", encoding="utf-8", newline="") as fh:
    reader = csv.DictReader(fh)
    rows = list(reader)

dst = Path("users.tsv")
with dst.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=["name", "email"], delimiter="\t")
    writer.writeheader()
    writer.writerows(rows)
```


## 6. JSON 行と美しい JSON
**`json.load`/`dump`** ファイル オブジェクトとペアになります。 **`indent`** 人間を助けます。 **`default=str`** は、非 JSON 型の単純なフォールバックです。

```python
import json
from pathlib import Path

cfg = {"timeout": 30, "hosts": ["a", "b"]}
Path("cfg.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")

loaded = json.loads(Path("cfg.json").read_text(encoding="utf-8"))

# newline-delimited JSON (one object per line)
nd_path = Path("events.ndjson")
with nd_path.open("w", encoding="utf-8") as fh:
    fh.write(json.dumps({"id": 1}) + "\n")
    fh.write(json.dumps({"id": 2}) + "\n")

with nd_path.open("r", encoding="utf-8") as fh:
    events = [json.loads(line) for line in fh]
```


## 7. バイナリ レイアウトと`struct`パックされたバイナリ (ネットワーク ペイロード、レガシー ファイル) を解析する必要がある場合、**`struct.unpack`** バイト → 数値をマッピングします。

```python
import struct

payload = struct.pack(">IH", 65_535, 9)    # big-endian uint32 + uint16
full_word, short_word = struct.unpack(">IH", payload)
```


## 8. 一時的および原子的パターン
- **`tempfile.TemporaryDirectory`** / **`NamedTemporaryFile`** スクラッチ スペースの場合は ** で自動クリーニングされます`with`** 出口。
- **アトミック置換**: ** に書き込みます`path.tmp`** それから **`Path.replace`** (POSIX 名前変更セマンティクス) — 書き込み中にプロセスがクラッシュした場合に破損したファイルを削減します。

```python
import tempfile
from pathlib import Path


def write_atomic(target: Path, data: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        delete=False,
        dir=target.parent,
    ) as fh:
        fh.write(data)
        tmp_path = Path(fh.name)
    tmp_path.replace(target)  # atomic rename on same filesystem (POSIX semantics)
```


## 9. 意図的にキャッチする必要がある例外
|例外 |典型的な原因 |
|----------|----------------|
| **`FileNotFoundError`** |読み取り/オープン時にパスがありません |
| **`PermissionError`** | ACL、読み取り専用メディア、ウイルス対策ロック |
| **`IsADirectoryError`** / **`NotADirectoryError`** |パスの種類が間違っています |
| **`UnicodeDecodeError`** |バイトが宣言されたエンコーディングと一致しません |

```python
from pathlib import Path


def safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
```


## 10. 簡単なチェックリスト
- 優先 **`pathlib`** パス算術の場合。 **とペアにする`encoding="utf-8"`** テキストを開くたびに。
- IO を ** で囲む`with`** したがって、ハンドルは例外時に閉じます。
- CSV の場合: **`newline=""`** + **`csv`**モジュール。
- 巨大なファイルの場合: 行ごとに繰り返します。避ける **`read()`サイズ制限がある場合を除きます**。
- 同時ライターの場合: ロック、データベース、または追加専用ログを使用します — 単純な同時 **`write_text`** レースによりデータが破損します。
