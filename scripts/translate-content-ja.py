#!/usr/bin/env python3
"""Translate prose in src/content/*.md and _meta.json labels to Japanese."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONTENT_ROOT = Path(__file__).resolve().parent.parent / "src" / "content"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
FENCE_RE = re.compile(r"```[\s\S]*?```")
FIGURE_RE = re.compile(r"<figure\b[\s\S]*?</figure>", re.IGNORECASE)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
URL_RE = re.compile(r"https?://[^\s)>\]]+")
LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
HTML_TAG_RE = re.compile(r"<[^>]+>")
PLACEHOLDER_RE = re.compile(r"__SEG(\d+)__")

TRANSLATE_FM_KEYS = {"subtitle", "group"}
SKIP_MD = {
    Path("en/aboutme/cv.md"),
}

# Heuristic: already translated if many CJK chars in body
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")
CORRUPT_RE = re.compile(r"[\uE000-\uE003]|__SEG\d+__|__IT\d+__")

# Sidebar group values: match _meta.json choices; keep product/course names in English.
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
}

# Longest first so multi-word product names win over substrings.
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
    },
    key=len,
    reverse=True,
)
IT_ACRONYM_RE = re.compile(r"\b[A-Z][A-Z0-9/+.-]{1,12}\b")
IT_TOKEN_RE = re.compile(r"__IT(\d+)__")


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


def protect_segments(text: str) -> tuple[str, list[str]]:
    saved: list[str] = []

    def stash(match: re.Match[str]) -> str:
        saved.append(match.group(0))
        return f"__SEG{len(saved) - 1}__"

    for pattern in (FENCE_RE, FIGURE_RE, INLINE_CODE_RE, HTML_TAG_RE):
        text = pattern.sub(stash, text)
    # Links before bare URLs so `(https://…)` inside `[label](url)` is not pre-stashed.
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

    # Repeat until nested placeholders (e.g. stashed table containing __SEG4__) are resolved.
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


def translate_chunk(translator_fn, text: str, retries: int = 4) -> str:
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
                        buf = line
                    else:
                        buf = f"{buf}\n{line}" if buf else line
                if buf.strip():
                    parts.append(translator_fn(buf.strip()))
                translated = "\n".join(parts)
            return restore_it_terms(translated, it_saved)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            wait = 2**attempt
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
            time.sleep(0.08)
        else:
            out.append(part)
    return "".join(out)


def translate_prose(translator_fn, text: str) -> str:
    protected, saved = protect_segments(text)
    # Split on paragraph boundaries to avoid huge blocks
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
        time.sleep(0.08)
    return restore_segments("".join(out), saved)


def assert_no_placeholders(text: str, context: str) -> None:
    if CORRUPT_RE.search(text):
        raise ValueError(f"unrestored placeholders in {context}")


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
        time.sleep(0.1)
    return "\n".join(out)


def translate_markdown(translator_fn, path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if not needs_translation(raw):
        return raw
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return translate_prose(translator_fn, raw)

    fm = translate_frontmatter(translator_fn, m.group(1))
    body = raw[m.end() :]
    lines = body.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        lines[i] = translate_prose(translator_fn, lines[i])
        time.sleep(0.1)
    rest = "\n".join(lines[i + 1 :])
    translated_rest = translate_prose(translator_fn, rest) if rest.strip() else ""
    new_lines = lines[: i + 1]
    if translated_rest:
        if new_lines and new_lines[-1].strip():
            new_lines.append("")
        new_lines.extend(translated_rest.split("\n"))
    new_body = "\n".join(new_lines)
    if body.endswith("\n") and not new_body.endswith("\n"):
        new_body += "\n"
    result = f"---\n{fm}\n---\n{new_body}"
    assert_no_placeholders(result, str(path))
    return result


def translate_meta(translator_fn, path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "label" in data and isinstance(data["label"], str):
        label = data["label"]
        if not looks_japanese(label):
            data["label"] = translate_chunk(translator_fn, label)
            time.sleep(0.1)
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def collect_files(limit: int | None) -> tuple[list[Path], list[Path]]:
    md_files = sorted(
        p
        for p in CONTENT_ROOT.rglob("*.md")
        if p.relative_to(CONTENT_ROOT) not in SKIP_MD
    )
    meta_files = sorted(CONTENT_ROOT.rglob("_meta.json"))
    if limit:
        md_files = md_files[:limit]
    return md_files, meta_files


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=0, help="Max .md files (0 = all)")
    parser.add_argument("--meta-only", action="store_true")
    parser.add_argument(
        "--include-meta",
        action="store_true",
        help="Also translate _meta.json labels (off by default; main uses English sidebar labels)",
    )
    parser.add_argument("--md-only", action="store_true")
    args = parser.parse_args()

    limit = args.limit if args.limit > 0 else None
    md_files, meta_files = collect_files(limit)
    translator_fn = get_translator()

    updated = 0
    if not args.meta_only:
        for i, path in enumerate(md_files, 1):
            rel = path.relative_to(CONTENT_ROOT.parent.parent)
            print(f"[md {i}/{len(md_files)}] {rel}", flush=True)
            try:
                new_text = translate_markdown(translator_fn, path)
            except Exception as e:
                print(f"  FAILED: {e}", file=sys.stderr)
                continue
            if new_text != path.read_text(encoding="utf-8"):
                updated += 1
                if not args.dry_run:
                    path.write_text(new_text, encoding="utf-8")

    if not args.md_only and (args.meta_only or args.include_meta):
        for i, path in enumerate(meta_files, 1):
            rel = path.relative_to(CONTENT_ROOT.parent.parent)
            print(f"[meta {i}/{len(meta_files)}] {rel}", flush=True)
            try:
                old = path.read_text(encoding="utf-8")
                new_text = translate_meta(translator_fn, path)
            except Exception as e:
                print(f"  FAILED: {e}", file=sys.stderr)
                continue
            if new_text != old:
                updated += 1
                if not args.dry_run:
                    path.write_text(new_text, encoding="utf-8")

    print(f"Done. Updated {updated} file(s). dry_run={args.dry_run}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
