#!/usr/bin/env python3
"""Bring src/content/jp to structural + prose parity with src/content/en.

Phases:
  1) restructure — rename JP paths to match EN layout
  2) copy-missing — copy EN files that have no JP counterpart
  3) translate — machine-translate English prose in JP notes to Japanese

Skips EN-only junk (Untitled.*, graphify-out, .obsidian, dated scratch notes).
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "src" / "content" / "en"
JP_ROOT = ROOT / "src" / "content" / "jp"

SKIP_DIR_NAMES = {"graphify-out", ".obsidian"}
SKIP_FILE_NAMES = {
    "Untitled.canvas",
    "Untitled 1.canvas",
    "Untitled.base",
    "opaa.base",
    "2026-07-07.md",
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
FENCE_RE = re.compile(r"```[\s\S]*?```")
FIGURE_RE = re.compile(r"<figure\b[\s\S]*?</figure>", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"__SEG(\d+)__")
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
CORRUPT_RE = re.compile(r"[\uE000-\uE003]|__SEG\d+__|__IT\d+__")

TRANSLATE_FM_KEYS = {"subtitle", "group"}

KEEP_GROUP_AS_IS = frozenset(
    {
        "CI/CD",
        "SRE",
        "Spring Boot",
        "CDN",
        "Git",
        "GitHub",
        "API Gateway",
        "MongoDB",
        "PL/SQL",
        "Postgres",
        "Redis",
        "Java",
        "Python",
        "Rust",
        "CS101",
        "SWE101",
        "SRE101",
        "AI101",
    }
)
GROUP_JA = {
    "System design": "システム設計",
    "System Design": "システム設計",
    "Data structures & algorithms": "データ構造とアルゴリズム",
    "Cloud architecture": "クラウドアーキテクチャ",
    "Databases": "データベース",
    "Startups": "スタートアップ",
    "Networking": "ネットワーク",
    "Getting started": "はじめに",
    "Artificial intelligence": "人工知能",
    "Machine learning": "機械学習",
    "Operating systems": "オペレーティングシステム",
    "Careers": "キャリア",
    "Digital marketing": "デジタルマーケティング",
    "Cryptocurrency101": "暗号資産101",
    "Languages": "言語",
    "Food": "フード",
    "Product Manager 101": "プロダクトマネージャ101",
    "Project Manager 101": "プロジェクトマネージャ101",
    "Quant SWE": "クオンツ SWE",
    "Cybersecurity": "サイバーセキュリティ",
}

IT_TERMS = sorted(
    {
        "API Gateway",
        "Spring Boot",
        "PL/SQL",
        "PostgreSQL",
        "GitHub",
        "MongoDB",
        "Postgres",
        "Kubernetes",
        "Alertmanager",
        "Prometheus",
        "Terraform",
        "Ansible",
        "Jenkins",
        "Grafana",
        "GraphQL",
        "OAuth",
        "OIDC",
        "HTTPS",
        "HTTP",
        "TCP",
        "UDP",
        "DNS",
        "SSL",
        "TLS",
        "JWT",
        "JSON",
        "YAML",
        "REST",
        "CI/CD",
        "NoSQL",
        "LLMs",
        "LLM",
        "GPT",
        "RAG",
        "SVM",
        "k-NN",
        "k-Means",
        "DBSCAN",
        "MSE",
        "Redis",
        "Docker",
        "Python",
        "Java",
        "Rust",
        "Git",
        "CDN",
        "GPU",
        "CPU",
        "ML",
        "AI",
        "SQL",
        "API",
        "Kafka",
        "Ollama",
        "MCP",
        "Cursor",
        "PlantUML",
        "Mermaid",
    },
    key=len,
    reverse=True,
)
IT_ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9/+.-]{1,12}\b")
IT_TOKEN_RE = re.compile(r"__IT(\d+)__")

# JP historical paths → EN-canonical relative paths (casefold keys).
RENAME_MAP: list[tuple[str, str]] = [
    ("cs101/i-core-concepts.md", "cs101/ii-core-concepts.md"),
    ("cs101/ii-foundations.md", "cs101/iii-foundations.md"),
    ("cs101/i-machines-and-memory.md", "cs101/iv-machines-and-memory.md"),
    ("cs101/iv-paradigms-and-limits.md", "cs101/v-paradigms-and-limits.md"),
]


def iter_content_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in p.parts):
            continue
        if p.name in SKIP_FILE_NAMES:
            continue
        if p.name == "_meta.json" or p.suffix == ".md":
            out.append(p)
    return sorted(out)


def rel_key(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix().casefold()


def google_translate_http(text: str, sl: str = "en", tl: str = "ja") -> str:
    url = "https://translate.googleapis.com/translate_a/single"
    params = urllib.parse.urlencode(
        {"client": "gtx", "sl": sl, "tl": tl, "dt": "t", "q": text},
        encoding="utf-8",
    )
    req = urllib.request.Request(
        f"{url}?{params}",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return "".join(part[0] for part in data[0] if part and part[0])


def get_translator():
    try:
        from deep_translator import GoogleTranslator

        t = GoogleTranslator(source="en", target="ja")
        return lambda s: t.translate(s)
    except ImportError:
        return google_translate_http


def looks_japanese(text: str) -> bool:
    if len(text) < 40:
        return False
    cjk = len(CJK_RE.findall(text))
    return cjk / max(len(text), 1) > 0.08


def needs_translation(text: str) -> bool:
    if CORRUPT_RE.search(text):
        return True
    return not looks_japanese(text)


def read_preserve(path: Path) -> tuple[str, str, bool]:
    raw = path.read_bytes()
    bom = ""
    if raw.startswith(b"\xef\xbb\xbf"):
        bom = "\ufeff"
        raw = raw[3:]
    uses_crlf = b"\r\n" in raw
    text = raw.decode("utf-8")
    if uses_crlf:
        text = text.replace("\r\n", "\n")
    return text, bom, uses_crlf


def write_preserve(path: Path, text: str, bom: str = "", uses_crlf: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    out = text
    if uses_crlf:
        out = out.replace("\n", "\r\n")
    path.write_bytes((bom + out).encode("utf-8"))


def protect_segments(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def stash(match: re.Match[str]) -> str:
        saved.append(match.group(0))
        return f"__SEG{len(saved) - 1}__"

    for pattern in (FENCE_RE, FIGURE_RE, INLINE_CODE_RE, HTML_TAG_RE):
        text = pattern.sub(stash, text)

    def link_sub(m: re.Match[str]) -> str:
        label, target = m.group(1), m.group(2)
        saved.append(target)
        idx = len(saved) - 1
        return f"[{label}](__SEG{idx}__)"

    text = LINK_RE.sub(link_sub, text)
    text = URL_RE.sub(stash, text)
    return text, saved


def restore_segments(text: str, saved: list[str]) -> str:
    def repl(m: re.Match[str]) -> str:
        return saved[int(m.group(1))]

    for _ in range(len(saved) + 1):
        updated = PLACEHOLDER_RE.sub(repl, text)
        if updated == text:
            break
        text = updated
    return text


def protect_it_terms(text: str) -> tuple[str, list[str]]:
    if PLACEHOLDER_RE.search(text):
        return text, []
    saved: list[str] = []

    def stash(term: str) -> str:
        saved.append(term)
        return f"__IT{len(saved) - 1}__"

    for term in IT_TERMS:
        if term in text:
            text = text.replace(term, stash(term))

    def acronym_sub(m: re.Match[str]) -> str:
        token = m.group(0)
        if token in {"I", "A", "V", "X"}:
            return token
        return stash(token)

    text = IT_ACRONYM_RE.sub(acronym_sub, text)
    return text, saved


def restore_it_terms(text: str, saved: list[str]) -> str:
    def repl(m: re.Match[str]) -> str:
        return saved[int(m.group(1))]

    return IT_TOKEN_RE.sub(repl, text)


def translate_group(label: str) -> str:
    if label in KEEP_GROUP_AS_IS:
        return label
    if label in GROUP_JA:
        return GROUP_JA[label]
    return label


def translate_chunk(translator_fn, text: str, retries: int = 5) -> str:
    text = text.strip()
    if not text:
        return text
    if looks_japanese(text):
        return text
    protected, it_saved = protect_it_terms(text)
    for attempt in range(retries):
        try:
            if len(protected) <= 4500:
                translated = translator_fn(protected)
            else:
                parts: list[str] = []
                buf = ""
                for line in protected.split("\n"):
                    if len(buf) + len(line) + 1 > 4000:
                        if buf.strip():
                            parts.append(translator_fn(buf.strip()))
                            time.sleep(0.05)
                        buf = line
                    else:
                        buf = f"{buf}\n{line}" if buf else line
                if buf.strip():
                    parts.append(translator_fn(buf.strip()))
                translated = "\n".join(parts)
            if translated is None:
                raise RuntimeError("translator returned None")
            return restore_it_terms(translated, it_saved)
        except Exception as e:  # noqa: BLE001 — network / rate-limit soft fail
            wait = min(2**attempt, 20)
            print(f"  retry {attempt + 1}/{retries}: {e}", file=sys.stderr)
            time.sleep(wait)
    return text


def translate_mixed_block(translator_fn, block: str) -> str:
    parts = re.split(r"(__SEG\d+__)", block)
    out: list[str] = []
    for part in parts:
        if PLACEHOLDER_RE.fullmatch(part):
            out.append(part)
        elif part.strip():
            out.append(translate_chunk(translator_fn, part))
            time.sleep(0.04)
        else:
            out.append(part)
    return "".join(out)


def translate_prose(translator_fn, text: str) -> str:
    protected, saved = protect_segments(text)
    blocks = re.split(r"(\n\n+)", protected)
    out: list[str] = []
    for block in blocks:
        if not block.strip() or re.fullmatch(r"\n+", block):
            out.append(block)
            continue
        if re.fullmatch(r"__SEG\d+__\s*", block.strip()):
            out.append(block)
            continue
        if PLACEHOLDER_RE.search(block):
            out.append(translate_mixed_block(translator_fn, block))
            continue
        out.append(translate_chunk(translator_fn, block))
        time.sleep(0.04)
    return restore_segments("".join(out), saved)


def translate_frontmatter(translator_fn, fm: str) -> str:
    lines = fm.split("\n")
    out: list[str] = []
    for line in lines:
        m = re.match(r"^(\s*)([a-zA-Z]+)(\s*:\s*)(.*?)(\s*)$", line)
        if not m or m.group(2) not in TRANSLATE_FM_KEYS:
            out.append(line)
            continue
        prefix, key, colon, val, suffix = m.groups()
        val = val.strip().strip('"').strip("'")
        if val:
            if key == "group":
                val = translate_group(val)
            else:
                val = translate_chunk(translator_fn, val)
            out.append(f'{prefix}{key}{colon}"{val}"{suffix}')
        else:
            out.append(line)
        time.sleep(0.05)
    return "\n".join(out)


def translate_markdown_text(translator_fn, raw: str) -> str:
    if not needs_translation(raw):
        return raw
    m = FRONTMATTER_RE.match(raw)
    if not m:
        result = translate_prose(translator_fn, raw)
        if CORRUPT_RE.search(result):
            raise ValueError("unrestored placeholders")
        return result

    fm = translate_frontmatter(translator_fn, m.group(1))
    body = raw[m.end() :]
    translated_body = translate_prose(translator_fn, body) if body.strip() else body
    result = f"---\n{fm}\n---\n{translated_body}"
    if body.endswith("\n") and not translated_body.endswith("\n"):
        result += "\n"
    if CORRUPT_RE.search(result):
        raise ValueError("unrestored placeholders")
    return result


def translate_meta_text(translator_fn, raw: str) -> str:
    data = json.loads(raw)
    if "label" in data and isinstance(data["label"], str):
        label = data["label"]
        if not looks_japanese(label) and label not in KEEP_GROUP_AS_IS:
            data["label"] = translate_chunk(translator_fn, label)
            time.sleep(0.05)
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def phase_restructure(dry_run: bool) -> int:
    """Rename JP folders/files to EN-canonical layout. Returns moves count."""
    moves = 0

    # 1) CS101 -> cs101
    cs_old = JP_ROOT / "CS101"
    cs_new = JP_ROOT / "cs101"
    if cs_old.exists() and not cs_new.exists():
        print(f"rename {cs_old.relative_to(ROOT)} -> {cs_new.relative_to(ROOT)}")
        if not dry_run:
            shutil.move(str(cs_old), str(cs_new))
        moves += 1
    elif cs_old.exists() and cs_new.exists():
        print("WARN: both CS101 and cs101 exist; merging CS101 into cs101")
        for p in iter_content_files(cs_old):
            rel = p.relative_to(cs_old)
            dest = cs_new / rel
            if not dest.exists():
                print(f"  move {p} -> {dest}")
                if not dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(p), str(dest))
                moves += 1
        if not dry_run:
            shutil.rmtree(cs_old, ignore_errors=True)

    # 2) ai-applied -> ai-engineering
    aa = JP_ROOT / "ai101" / "ai-applied"
    ae = JP_ROOT / "ai101" / "ai-engineering"
    if aa.exists() and not ae.exists():
        print(f"rename {aa.relative_to(ROOT)} -> {ae.relative_to(ROOT)}")
        if not dry_run:
            shutil.move(str(aa), str(ae))
        moves += 1
    elif aa.exists() and ae.exists():
        print("WARN: both ai-applied and ai-engineering exist; merging")
        for p in iter_content_files(aa):
            rel = p.relative_to(aa)
            dest = ae / rel
            if not dest.exists():
                print(f"  move {p} -> {dest}")
                if not dry_run:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(p), str(dest))
                moves += 1
        if not dry_run:
            shutil.rmtree(aa, ignore_errors=True)

    # 3) swe101/{mongodb,postgres,plsql} -> swe101/databases/...
    for db in ("mongodb", "postgres", "plsql"):
        src = JP_ROOT / "swe101" / db
        dest = JP_ROOT / "swe101" / "databases" / db
        if src.exists() and not dest.exists():
            print(f"rename {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dest))
            moves += 1
        elif src.exists() and dest.exists():
            for p in iter_content_files(src):
                rel = p.relative_to(src)
                d = dest / rel
                if not d.exists():
                    print(f"  move {p} -> {d}")
                    if not dry_run:
                        d.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(p), str(d))
                    moves += 1
            if not dry_run:
                shutil.rmtree(src, ignore_errors=True)

    # 4) CS101 root note renumbers
    for old_rel, new_rel in RENAME_MAP:
        src = JP_ROOT / Path(old_rel)
        # after CS101 rename, path is cs101/...
        if not src.exists():
            # try original casing path variants already handled
            continue
        dest = JP_ROOT / Path(new_rel)
        if dest.exists():
            continue
        print(f"rename {src.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(dest))
        moves += 1

    # 5) Fix common link prefixes inside JP markdown
    if not dry_run:
        replacements = [
            (r"(\]\(\.\./)CS101/", r"\1cs101/"),
            (r"(\]\(\.\./\.\./)CS101/", r"\1cs101/"),
            (r"(\]\(\.\./\.\./\.\./)CS101/", r"\1cs101/"),
            (r"ai-applied/", "ai-engineering/"),
            (r"\]\(\.\./mongodb/", "](../databases/mongodb/"),
            (r"\]\(\.\./postgres/", "](../databases/postgres/"),
            (r"\]\(\.\./plsql/", "](../databases/plsql/"),
            (r"\]\(mongodb/", "](databases/mongodb/"),
            (r"\]\(postgres/", "](databases/postgres/"),
            (r"\]\(plsql/", "](databases/plsql/"),
            (r"i-core-concepts\.md", "ii-core-concepts.md"),
            (r"(?<!/)ii-foundations\.md", "iii-foundations.md"),
            (r"i-machines-and-memory\.md", "iv-machines-and-memory.md"),
            (r"iv-paradigms-and-limits\.md", "v-paradigms-and-limits.md"),
        ]
        for path in iter_content_files(JP_ROOT):
            if path.suffix != ".md":
                continue
            text, bom, crlf = read_preserve(path)
            new = text
            for pat, repl in replacements:
                new = re.sub(pat, repl, new)
            if new != text:
                write_preserve(path, new, bom, crlf)
                moves += 1
                print(f"relink {path.relative_to(ROOT)}")

    print(f"restructure moves/edits: {moves}")
    return moves


def phase_copy_missing(dry_run: bool) -> int:
    en_files = {rel_key(p, EN_ROOT): p for p in iter_content_files(EN_ROOT)}
    jp_files = {rel_key(p, JP_ROOT): p for p in iter_content_files(JP_ROOT)}
    copied = 0
    for key, en_path in sorted(en_files.items()):
        if key in jp_files:
            continue
        rel = en_path.relative_to(EN_ROOT)
        dest = JP_ROOT / rel
        print(f"copy {rel}")
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(en_path, dest)
        copied += 1
    print(f"copied missing: {copied}")
    return copied


def phase_translate(
    dry_run: bool,
    limit: int | None,
    workers: int,
    force: bool,
) -> int:
    translator_fn = get_translator()
    targets: list[Path] = []
    for path in iter_content_files(JP_ROOT):
        text, _, _ = read_preserve(path)
        if force or needs_translation(text):
            targets.append(path)
    if limit:
        targets = targets[:limit]
    print(f"translate candidates: {len(targets)} workers={workers}")

    updated = 0

    def work(path: Path) -> tuple[Path, bool, str]:
        text, bom, crlf = read_preserve(path)
        try:
            if path.name == "_meta.json":
                new_text = translate_meta_text(translator_fn, text)
            else:
                new_text = translate_markdown_text(translator_fn, text)
        except Exception as e:  # noqa: BLE001
            return path, False, f"FAILED {e}"
        if new_text == text:
            return path, False, "unchanged"
        if not dry_run:
            write_preserve(path, new_text, bom, crlf)
        return path, True, "updated"

    if workers <= 1:
        for i, path in enumerate(targets, 1):
            print(f"[{i}/{len(targets)}] {path.relative_to(ROOT)}", flush=True)
            _, changed, status = work(path)
            print(f"  {status}", flush=True)
            if changed:
                updated += 1
    else:
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = {ex.submit(work, p): p for p in targets}
            done = 0
            for fut in as_completed(futs):
                done += 1
                path, changed, status = fut.result()
                print(
                    f"[{done}/{len(targets)}] {path.relative_to(ROOT)} {status}",
                    flush=True,
                )
                if changed:
                    updated += 1
    print(f"translated/updated: {updated}")
    return updated


def parity_report() -> None:
    en = {rel_key(p, EN_ROOT) for p in iter_content_files(EN_ROOT)}
    jp = {rel_key(p, JP_ROOT) for p in iter_content_files(JP_ROOT)}
    missing = sorted(en - jp)
    extra = sorted(jp - en)
    print(f"EN={len(en)} JP={len(jp)} missing={len(missing)} extra={len(extra)}")
    if missing[:20]:
        print("missing sample:")
        for m in missing[:20]:
            print(" ", m)
    if extra[:20]:
        print("extra sample:")
        for m in extra[:20]:
            print(" ", m)
    # translation coverage
    eng_heavy = 0
    for path in iter_content_files(JP_ROOT):
        if path.suffix != ".md":
            continue
        text, _, _ = read_preserve(path)
        if needs_translation(text):
            eng_heavy += 1
    print(f"JP md still needing translation heuristic: {eng_heavy}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--phase",
        choices=["restructure", "copy-missing", "translate", "all", "report"],
        default="all",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Translate even if already looks Japanese",
    )
    args = parser.parse_args()
    limit = args.limit if args.limit > 0 else None

    if args.phase in {"restructure", "all"}:
        phase_restructure(args.dry_run)
    if args.phase in {"copy-missing", "all"}:
        phase_copy_missing(args.dry_run)
    if args.phase in {"translate", "all"}:
        phase_translate(args.dry_run, limit, args.workers, args.force)
    if args.phase in {"report", "all"}:
        parity_report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
