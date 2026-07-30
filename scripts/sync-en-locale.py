#!/usr/bin/env python3
"""Copy and translate src/content/en into another locale folder.

Examples:
  python scripts/sync-en-locale.py --locale pt-br --lang pt --phase all
  python scripts/sync-en-locale.py --locale pt-br --lang pt --phase translate --workers 3 --limit 30
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
CONTENT = ROOT / "src" / "content"
EN_ROOT = CONTENT / "en"

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
CORRUPT_RE = re.compile(r"[\uE000-\uE003]|__SEG\d+__|__IT\d+__")
# Latin letters with Portuguese-common diacritics + Japanese CJK for multi-locale checks
PT_MARK_RE = re.compile(
    r"[ãõáéíóúâêôàçüÃÕÁÉÍÓÚÂÊÔÀÇÜ]|\b(não|você|são|também|através|seção|visão|configuração|visão|visão)\b",
    re.IGNORECASE,
)
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")

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
        "Kafka",
        "MCP",
        "Ollama",
    }
)

GROUP_PT = {
    "System design": "Design de sistemas",
    "System Design": "Design de sistemas",
    "Data structures & algorithms": "Estruturas de dados e algoritmos",
    "Cloud architecture": "Arquitetura em nuvem",
    "Databases": "Bancos de dados",
    "Startups": "Startups",
    "Networking": "Redes",
    "Getting started": "Primeiros passos",
    "Artificial intelligence": "Inteligência artificial",
    "Machine learning": "Aprendizado de máquina",
    "Operating systems": "Sistemas operacionais",
    "Careers": "Carreiras",
    "Digital marketing": "Marketing digital",
    "Cryptocurrency101": "Criptomoedas 101",
    "Languages": "Idiomas",
    "Food": "Comida",
    "Product Manager 101": "Product Manager 101",
    "Project Manager 101": "Project Manager 101",
    "Quant SWE": "Quant SWE",
    "Cybersecurity": "Cibersegurança",
    "Notes": "Notas",
}

LOCALE_ROOT_LABELS = {
    "pt-br": "Notas",
    "pt": "Notas",
    "jp": "ノート",
    "ja": "ノート",
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


def google_translate_http(text: str, sl: str = "en", tl: str = "pt") -> str:
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


def get_translator(lang: str):
    # Google uses "pt" for Portuguese; prefer Brazilian phrasing via pt
    tl = "pt" if lang.lower() in {"pt", "pt-br", "pt_br"} else lang
    backends = []
    try:
        from deep_translator import GoogleTranslator

        gt = GoogleTranslator(source="en", target=tl)

        def _deep(s: str) -> str:
            out = gt.translate(s)
            if out is None:
                raise RuntimeError("deep returned None")
            return out

        backends.append(("deep", _deep))
    except ImportError:
        pass
    try:
        from deep_translator import MyMemoryTranslator

        # MyMemory Brazilian Portuguese
        mm_target = "pt-BR" if tl == "pt" else tl
        mm = MyMemoryTranslator(source="en-US", target=mm_target)

        def _mm(s: str) -> str:
            out = mm.translate(s)
            if out is None:
                raise RuntimeError("mymemory returned None")
            return out

        backends.append(("mymemory", _mm))
    except Exception:
        pass
    backends.append(("http", lambda s: google_translate_http(s, tl=tl)))

    def translate(s: str) -> str:
        last_err: Exception | None = None
        for name, fn in backends:
            try:
                return fn(s)
            except Exception as e:  # noqa: BLE001
                last_err = e
                continue
        raise RuntimeError(f"all translators failed: {last_err}")

    return translate


def looks_target_language(text: str, lang: str) -> bool:
    if len(text) < 40:
        return False
    lang = lang.lower()
    if lang in {"ja", "jp"}:
        return len(CJK_RE.findall(text)) / max(len(text), 1) > 0.08
    if lang in {"pt", "pt-br", "pt_br"}:
        marks = len(PT_MARK_RE.findall(text))
        # Accent / PT-word density; English copies score near zero
        return marks >= 8 or marks / max(len(text), 1) > 0.004
    # Fallback: treat as already translated if little ASCII letters remain
    letters = len(re.findall(r"[A-Za-z]", text))
    return letters < 80


def needs_translation(text: str, lang: str) -> bool:
    if CORRUPT_RE.search(text):
        return True
    return not looks_target_language(text, lang)


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
    out = text.replace("\n", "\r\n") if uses_crlf else text
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
        return f"[{label}](__SEG{len(saved) - 1}__)"

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


def translate_group(label: str, lang: str) -> str:
    if label in KEEP_GROUP_AS_IS:
        return label
    if lang.lower() in {"pt", "pt-br", "pt_br"} and label in GROUP_PT:
        return GROUP_PT[label]
    return label


def translate_chunk(translator_fn, text: str, lang: str, retries: int = 5) -> str:
    text = text.strip()
    if not text:
        return text
    if looks_target_language(text, lang):
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
                            time.sleep(0.01)
                        buf = line
                    else:
                        buf = f"{buf}\n{line}" if buf else line
                if buf.strip():
                    parts.append(translator_fn(buf.strip()))
                translated = "\n".join(parts)
            if translated is None:
                raise RuntimeError("translator returned None")
            return restore_it_terms(translated, it_saved)
        except Exception as e:  # noqa: BLE001
            wait = min(2**attempt, 20)
            print(f"  retry {attempt + 1}/{retries}: {e}", file=sys.stderr)
            time.sleep(wait)
    return text


def translate_mixed_block(translator_fn, block: str, lang: str) -> str:
    parts = re.split(r"(__SEG\d+__)", block)
    out: list[str] = []
    for part in parts:
        if PLACEHOLDER_RE.fullmatch(part):
            out.append(part)
        elif part.strip():
            out.append(translate_chunk(translator_fn, part, lang))
            time.sleep(0.01)
        else:
            out.append(part)
    return "".join(out)


def translate_prose(translator_fn, text: str, lang: str) -> str:
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
            out.append(translate_mixed_block(translator_fn, block, lang))
            continue
        out.append(translate_chunk(translator_fn, block, lang))
        time.sleep(0.01)
    return restore_segments("".join(out), saved)


def translate_frontmatter(translator_fn, fm: str, lang: str) -> str:
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
                val = translate_group(val, lang)
            else:
                val = translate_chunk(translator_fn, val, lang)
            out.append(f'{prefix}{key}{colon}"{val}"{suffix}')
        else:
            out.append(line)
        time.sleep(0.01)
    return "\n".join(out)


def translate_markdown_text(translator_fn, raw: str, lang: str) -> str:
    if not needs_translation(raw, lang):
        return raw
    m = FRONTMATTER_RE.match(raw)
    if not m:
        result = translate_prose(translator_fn, raw, lang)
        if CORRUPT_RE.search(result):
            raise ValueError("unrestored placeholders")
        return result
    fm = translate_frontmatter(translator_fn, m.group(1), lang)
    body = raw[m.end() :]
    translated_body = translate_prose(translator_fn, body, lang) if body.strip() else body
    result = f"---\n{fm}\n---\n{translated_body}"
    if body.endswith("\n") and not translated_body.endswith("\n"):
        result += "\n"
    if CORRUPT_RE.search(result):
        raise ValueError("unrestored placeholders")
    return result


def translate_meta_text(translator_fn, raw: str, lang: str) -> str:
    data = json.loads(raw)
    if "label" in data and isinstance(data["label"], str):
        label = data["label"]
        if label not in KEEP_GROUP_AS_IS and not looks_target_language(label, lang):
            if lang.lower() in {"pt", "pt-br", "pt_br"} and label in GROUP_PT:
                data["label"] = GROUP_PT[label]
            elif len(label) > 24 or len(PT_MARK_RE.findall(label)) == 0:
                # translate longer labels; keep short English product names
                if len(label) > 24:
                    data["label"] = translate_chunk(translator_fn, label, lang)
                    time.sleep(0.01)
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def phase_copy(locale_root: Path, dry_run: bool) -> int:
    en_files = {rel_key(p, EN_ROOT): p for p in iter_content_files(EN_ROOT)}
    loc_files = (
        {rel_key(p, locale_root): p for p in iter_content_files(locale_root)}
        if locale_root.exists()
        else {}
    )
    copied = 0
    for key, en_path in sorted(en_files.items()):
        if key in loc_files:
            continue
        rel = en_path.relative_to(EN_ROOT)
        dest = locale_root / rel
        print(f"copy {rel}")
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(en_path, dest)
        copied += 1
    # Root locale label
    meta = locale_root / "_meta.json"
    if not dry_run:
        locale_name = locale_root.name
        label = LOCALE_ROOT_LABELS.get(locale_name, "Notes")
        meta.write_text(
            json.dumps({"label": label, "order": 0}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    print(f"copied missing: {copied}")
    return copied


def phase_translate(
    locale_root: Path,
    lang: str,
    dry_run: bool,
    limit: int | None,
    workers: int,
    force: bool,
) -> int:
    translator_fn = get_translator(lang)
    targets: list[Path] = []
    for path in iter_content_files(locale_root):
        text, _, _ = read_preserve(path)
        if not (force or needs_translation(text, lang)):
            continue
        if path.name == "_meta.json" and not force:
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                targets.append(path)
                continue
            label = data.get("label")
            if isinstance(label, str) and (
                label in KEEP_GROUP_AS_IS
                or looks_target_language(label, lang)
                or (len(label) <= 24 and not PT_MARK_RE.search(label))
            ):
                continue
        targets.append(path)
    targets.sort(key=lambda p: (0 if p.suffix == ".md" else 1, str(p)))
    if limit:
        targets = targets[:limit]
    print(f"translate candidates: {len(targets)} workers={workers}")

    updated = 0

    def work(path: Path) -> tuple[Path, bool, str]:
        text, bom, crlf = read_preserve(path)
        try:
            if path.name == "_meta.json":
                new_text = translate_meta_text(translator_fn, text, lang)
            else:
                new_text = translate_markdown_text(translator_fn, text, lang)
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


def parity_report(locale_root: Path, lang: str) -> None:
    en = {rel_key(p, EN_ROOT) for p in iter_content_files(EN_ROOT)}
    loc = (
        {rel_key(p, locale_root) for p in iter_content_files(locale_root)}
        if locale_root.exists()
        else set()
    )
    missing = sorted(en - loc)
    extra = sorted(loc - en)
    print(
        f"EN={len(en)} {locale_root.name}={len(loc)} missing={len(missing)} extra={len(extra)}"
    )
    if missing[:15]:
        print("missing sample:")
        for m in missing[:15]:
            print(" ", m)
    needing = 0
    if locale_root.exists():
        for path in iter_content_files(locale_root):
            if path.suffix != ".md":
                continue
            text, _, _ = read_preserve(path)
            if needs_translation(text, lang):
                needing += 1
    print(f"{locale_root.name} md still needing translation heuristic: {needing}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True, help="Target folder under src/content/")
    parser.add_argument(
        "--lang",
        required=True,
        help="Target language code for translation (e.g. pt, ja)",
    )
    parser.add_argument(
        "--phase",
        choices=["copy", "translate", "all", "report"],
        default="all",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    locale_root = CONTENT / args.locale
    limit = args.limit if args.limit > 0 else None

    if args.phase in {"copy", "all"}:
        phase_copy(locale_root, args.dry_run)
    if args.phase in {"translate", "all"}:
        if not locale_root.exists():
            print(f"locale root missing: {locale_root}", file=sys.stderr)
            return 1
        phase_translate(
            locale_root, args.lang, args.dry_run, limit, args.workers, args.force
        )
    if args.phase in {"report", "all"}:
        parity_report(locale_root, args.lang)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
