#!/usr/bin/env python3
"""Convert internal .md references to markdown links across src/content."""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

CONTENT_ROOT = Path(__file__).resolve().parent.parent / "src" / "content"

REF_PATTERN = re.compile(
    r"(?<!\[)"
    r"`("
    r"(?:(?:\.\./)+|\./)?"
    r"(?:[A-Za-z0-9_.-]+/)*"
    r"[A-Za-z0-9_.-]+\.md"
    r")`"
)

PAREN_REF_PATTERN = re.compile(
    r"(?<!\])\("
    r"("
    r"(?:(?:\.\./)+|\./)?"
    r"(?:[A-Za-z0-9_.-]+/)*"
    r"[A-Za-z0-9_.-]+\.md"
    r")\)"
)

PAREN_BACKTICK_REF_PATTERN = re.compile(
    r"(?<!\])\(\`("
    r"(?:(?:\.\./)+|\./)?"
    r"(?:[A-Za-z0-9_.-]+/)*"
    r"[A-Za-z0-9_.-]+\.md"
    r")\`\)"
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
SUBTITLE_RE = re.compile(r'^subtitle:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)

SKIP_FILES = {
    CONTENT_ROOT / "getting-started" / "guide-topics-and-folders.md",
}


def parse_subtitle(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    sm = SUBTITLE_RE.search(m.group(1))
    return sm.group(1).strip() if sm else None


def humanize_filename(name: str) -> str:
    stem = name.removesuffix(".md")
    stem = re.sub(r"^[ivxlc]+-", "", stem, flags=re.IGNORECASE)
    return stem.replace("-", " ").strip().title()


def build_index() -> dict:
    by_rel: dict[str, Path] = {}
    by_name: dict[str, list[Path]] = {}
    by_suffix: dict[str, list[Path]] = {}
    for path in CONTENT_ROOT.rglob("*.md"):
        rel = path.relative_to(CONTENT_ROOT).as_posix()
        key = rel.lower()
        by_rel[key] = path
        by_name.setdefault(path.name.lower(), []).append(path)
        by_suffix.setdefault(path.name.lower(), []).append(path)
        parts = key.split("/")
        for i in range(len(parts)):
            suffix = "/".join(parts[i:])
            by_suffix.setdefault(suffix, []).append(path)
    return {"by_rel": by_rel, "by_name": by_name, "by_suffix": by_suffix}


def resolve_target(ref: str, source: Path, index: dict) -> Path | None:
    ref = ref.replace("\\", "/").strip()
    if ref.lower() == "readme.md":
        return None

    candidate = (source.parent / ref).resolve()
    try:
        candidate.relative_to(CONTENT_ROOT.resolve())
        if candidate.is_file():
            return candidate
    except ValueError:
        pass

    rel_key = ref.lstrip("./").lower()
    if rel_key in index["by_rel"]:
        return index["by_rel"][rel_key]

    suffix_matches = index["by_suffix"].get(rel_key, [])
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if len(suffix_matches) > 1:
        source_top = source.relative_to(CONTENT_ROOT).parts[0].lower()
        same_topic = [
            m
            for m in suffix_matches
            if m.relative_to(CONTENT_ROOT).parts[0].lower() == source_top
        ]
        if len(same_topic) == 1:
            return same_topic[0]
        # prefer shortest relative path from source
        same_topic = same_topic or suffix_matches
        return min(
            same_topic,
            key=lambda p: len(os.path.relpath(p, start=source.parent)),
        )

    name = Path(ref).name.lower()
    matches = index["by_name"].get(name, [])
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        source_top = source.relative_to(CONTENT_ROOT).parts[0].lower()
        for m in matches:
            if m.relative_to(CONTENT_ROOT).parts[0].lower() == source_top:
                return m
    return None


def link_text(target: Path, cache: dict[Path, str]) -> str:
    if target not in cache:
        sub = parse_subtitle(target)
        cache[target] = sub if sub else humanize_filename(target.name)
    return cache[target]


def split_fences(text: str) -> list[tuple[bool, str]]:
    """Split prose vs fenced code blocks (toggle on ``` lines)."""
    parts: list[tuple[bool, str]] = []
    pos = 0
    in_fence = False
    fence_start = 0
    for m in re.finditer(r"^```[\w.-]*\s*$", text, re.MULTILINE):
        if not in_fence:
            if m.start() > pos:
                parts.append((False, text[pos : m.start()]))
            in_fence = True
            fence_start = m.start()
        else:
            end_pos = m.end()
            parts.append((True, text[fence_start:end_pos]))
            pos = end_pos
            in_fence = False
    if pos < len(text):
        parts.append((False, text[pos:]))
    return parts


def make_link(ref: str, source: Path, index: dict, cache: dict[Path, str]) -> str | None:
    target = resolve_target(ref, source, index)
    if not target:
        return None
    rel_href = Path(os.path.relpath(target, start=source.parent)).as_posix()
    text = link_text(target, cache)
    return f"[{text}]({rel_href})"


def replace_refs(
    segment: str,
    source: Path,
    index: dict,
    cache: dict[Path, str],
    *,
    paren: bool = True,
) -> str:
    def repl(match: re.Match[str]) -> str:
        link = make_link(match.group(1), source, index, cache)
        return link if link else match.group(0)

    segment = PAREN_BACKTICK_REF_PATTERN.sub(repl, segment)
    segment = REF_PATTERN.sub(repl, segment)
    if paren:
        segment = PAREN_REF_PATTERN.sub(repl, segment)
    return segment


def process_file(path: Path, index: dict, cache: dict[Path, str]) -> bool:
    if path.resolve() in {p.resolve() for p in SKIP_FILES}:
        return False

    original = path.read_text(encoding="utf-8")
    chunks = split_fences(original)
    out_parts: list[str] = []
    changed = False
    for in_fence, chunk in chunks:
        if in_fence:
            out_parts.append(chunk)
        else:
            new_chunk = replace_refs(chunk, path, index, cache)
            if new_chunk != chunk:
                changed = True
            out_parts.append(new_chunk)
    if changed:
        path.write_text("".join(out_parts), encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    index = build_index()
    cache: dict[Path, str] = {}
    changed_files = 0
    for path in sorted(CONTENT_ROOT.rglob("*.md")):
        if process_file(path, index, cache):
            changed_files += 1
            print(f"updated: {path.relative_to(CONTENT_ROOT.parent.parent)}")
    print(f"Done. {changed_files} file(s) updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
