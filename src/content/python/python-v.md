---
label: "V"
subtitle: "File I/O"
group: "Python"
groupOrder: 1
order: 5
---
Python — Part V
Reading and writing files safely: text vs binary, encodings, streaming lines, structured formats, and common failure modes.

## 1. Two kinds of file content
- **Text mode** (`"r"`, `"w"`, `"a"`, …): Python decodes bytes → **`str`** using an **encoding** (default is locale-dependent — **always pass `encoding="utf-8"`** for portable apps).
- **Binary mode** (`"rb"`, `"wb"`): you read/write **`bytes`** — use for images, zip blobs, pickle (careful), or unknown encodings you’ll handle manually.


## 2. `pathlib` vs `open()`
**`pathlib.Path`** is usually clearer for whole-file reads/writes; **`open()`** shines when you stream or need fine-grained control.

```python
from pathlib import Path

out = Path("build") / "note.txt"
out.parent.mkdir(parents=True, exist_ok=True)

out.write_text("hello\nworld\n", encoding="utf-8")

text = out.read_text(encoding="utf-8")
blob = out.read_bytes()

print(text.splitlines())
```

Same operations with **`open`**:

```python
path = Path("build/note.txt")

with path.open("w", encoding="utf-8", newline="") as fh:
    fh.write("line1\n")
    fh.writelines(["line2\n", "line3\n"])

with path.open("r", encoding="utf-8") as fh:
    body = fh.read()
```


## 3. Always control newlines & encoding on text files
- **`newline=""`** when using **`csv`** module — lets the reader/writer control `\r\n` vs `\n` translation (**CSV docs recommend this on Windows**).
- **`errors="replace"` / `"strict"` / `"ignore"`** tunes decoder behavior when bytes are not valid UTF-8.

```python
from pathlib import Path

legacy = Path("latin1.bin")
legacy.write_bytes("café".encode("latin-1"))

text = legacy.read_text(encoding="latin-1")
utf8_path = Path("utf8copy.txt")
utf8_path.write_text(text, encoding="utf-8")
```


## 4. Streaming instead of slurping
Large logs or datasets: iterate lines without loading the whole file into RAM.

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


## 5. CSV & delimited text
Use the **`csv`** module — don’t split on commas by hand (quotes, embedded commas).

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


## 6. JSON lines & pretty JSON
**`json.load`/`dump`** pairs with file objects; **`indent`** helps humans; **`default=str`** is a blunt fallback for non-JSON types.

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


## 7. Binary layouts & `struct`
When you must parse packed binary (network payloads, legacy files), **`struct.unpack`** maps bytes → numbers.

```python
import struct

payload = struct.pack(">IH", 65_535, 9)    # big-endian uint32 + uint16
full_word, short_word = struct.unpack(">IH", payload)
```


## 8. Temporary & atomic patterns
- **`tempfile.TemporaryDirectory`** / **`NamedTemporaryFile`** for scratch space auto-cleaned on **`with`** exit.
- **Atomic replace**: write to **`path.tmp`** then **`Path.replace`** (POSIX rename semantics) — reduces torn files if the process crashes mid-write.

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


## 9. Exceptions you should catch deliberately
| Exception | Typical cause |
|-----------|----------------|
| **`FileNotFoundError`** | Missing path on read/open |
| **`PermissionError`** | ACLs, read-only media, antivirus locks |
| **`IsADirectoryError`** / **`NotADirectoryError`** | Wrong path kind |
| **`UnicodeDecodeError`** | Bytes don’t match declared encoding |

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


## 10. Quick checklist
- Prefer **`pathlib`** for path arithmetic; pair with **`encoding="utf-8"`** on every text open.
- Wrap IO in **`with`** so handles close on exceptions.
- For CSV: **`newline=""`** + **`csv`** module.
- For huge files: iterate line-by-line; avoid **`read()` unless size-bounded**.
- For concurrent writers: use locks, databases, or append-only logs — naive simultaneous **`write_text`** races corrupt data.
