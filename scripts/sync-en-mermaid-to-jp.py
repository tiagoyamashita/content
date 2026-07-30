#!/usr/bin/env python3
"""Sync Mermaid diagrams from English notes into paired Japanese notes.

Pairs files under src/content/en and src/content/jp by case-insensitive path,
with ai-engineering ↔ ai-applied. For each EN ```mermaid``` block, either
replaces a diagram-like ```text``` / ```plantuml``` fence in the matching JP
section, or inserts the Mermaid block at an analogous position.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EN_ROOT = ROOT / "src" / "content" / "en"
JP_ROOT = ROOT / "src" / "content" / "jp"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.M)
FENCE_RE = re.compile(r"```([a-zA-Z0-9_+-]*)\n(.*?)```", re.S)
DIAGRAM_LANGS = {"text", "plantuml", "ascii"}


@dataclass
class MermaidBlock:
    body: str
    heading_index: int  # index among ##-###### headings (0-based); -1 if before any
    heading_level: int
    heading_text: str
    ordinal_in_section: int
    before_first_table: bool
    char_offset: int


def casefold_key(rel: str) -> str:
    return rel.casefold()


# Extra EN→JP path aliases when folder layout drifted between locales.
PATH_ALIASES: list[tuple[str, str]] = [
    ("swe101/databases/mongodb/", "swe101/mongodb/"),
    ("swe101/databases/postgres/", "swe101/postgres/"),
    ("swe101/databases/plsql/", "swe101/plsql/"),
    ("cs101/v-paradigms-and-limits.md", "cs101/iv-paradigms-and-limits.md"),
    ("cs101/ii-core-concepts.md", "cs101/i-core-concepts.md"),
    ("cs101/iii-foundations.md", "cs101/ii-foundations.md"),
    ("cs101/iv-machines-and-memory.md", "cs101/i-machines-and-memory.md"),
]


def alias_keys(key: str) -> list[str]:
    keys = [key]
    if "ai-engineering" in key:
        keys.append(key.replace("ai-engineering", "ai-applied"))
    if "ai-applied" in key:
        keys.append(key.replace("ai-applied", "ai-engineering"))
    for src, dst in PATH_ALIASES:
        if key.startswith(src) or key == src:
            keys.append(key.replace(src, dst, 1))
        if key.startswith(dst) or key == dst:
            keys.append(key.replace(dst, src, 1))
    # dedupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for k in keys:
        if k not in seen:
            seen.add(k)
            out.append(k)
    return out


def index_md(root: Path) -> dict[str, tuple[str, Path]]:
    out: dict[str, tuple[str, Path]] = {}
    for path in root.rglob("*.md"):
        rel = path.relative_to(root).as_posix()
        out[casefold_key(rel)] = (rel, path)
    return out


def heading_number_prefix(text: str) -> str | None:
    m = re.match(r"^(\d+)\.", text.strip())
    if m:
        return m.group(1)
    m = re.match(r"^([IVXLC]+)\b", text.strip(), re.I)
    if m:
        return m.group(1).upper()
    return None


def extract_mermaid_blocks(text: str) -> list[MermaidBlock]:
    headings = [(m.start(), len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(text)]
    blocks: list[MermaidBlock] = []
    section_counts: dict[int, int] = {}

    for m in FENCE_RE.finditer(text):
        lang = (m.group(1) or "").lower()
        if lang != "mermaid":
            continue
        pos = m.start()
        heading_index = -1
        heading_level = 0
        heading_text = ""
        for i, (hpos, level, htext) in enumerate(headings):
            if hpos < pos:
                heading_index = i
                heading_level = level
                heading_text = htext
            else:
                break
        ordinal = section_counts.get(heading_index, 0)
        section_counts[heading_index] = ordinal + 1

        # section end = next heading at same or higher level
        section_end = len(text)
        if heading_index >= 0:
            for j in range(heading_index + 1, len(headings)):
                if headings[j][1] <= heading_level:
                    section_end = headings[j][0]
                    break
        else:
            section_end = headings[0][0] if headings else len(text)

        section_prefix = text[headings[heading_index][0] if heading_index >= 0 else 0 : pos]
        before_first_table = "|" not in section_prefix or not re.search(
            r"^\|.+\|$", section_prefix, re.M
        )

        blocks.append(
            MermaidBlock(
                body=m.group(2),
                heading_index=heading_index,
                heading_level=heading_level,
                heading_text=heading_text,
                ordinal_in_section=ordinal,
                before_first_table=before_first_table
                and bool(re.search(r"^\|.+\|$", text[pos:section_end], re.M)),
                char_offset=pos,
            )
        )
    return blocks


def find_jp_heading_index(jp_text: str, en_block: MermaidBlock, en_headings: list[tuple[int, int, str]]) -> int:
    jp_headings = [(m.start(), len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(jp_text)]
    if en_block.heading_index < 0:
        return -1
    if not jp_headings:
        return -1

    en_text = en_block.heading_text
    en_num = heading_number_prefix(en_text)

    # 1) same numeric / roman prefix at same level
    if en_num is not None:
        candidates = [
            i
            for i, (_, level, text) in enumerate(jp_headings)
            if level == en_block.heading_level and heading_number_prefix(text) == en_num
        ]
        if len(candidates) == 1:
            return candidates[0]
        if candidates:
            # pick by ordinal among same-number? unlikely; use en heading index clamped
            return candidates[min(len(candidates) - 1, max(0, en_block.heading_index))]

    # 2) same heading index if counts are close
    if en_block.heading_index < len(jp_headings):
        return en_block.heading_index

    return len(jp_headings) - 1


def section_bounds(text: str, heading_index: int) -> tuple[int, int]:
    headings = [(m.start(), len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(text)]
    if heading_index < 0:
        end = headings[0][0] if headings else len(text)
        return 0, end
    start = headings[heading_index][0]
    level = headings[heading_index][1]
    end = len(text)
    for j in range(heading_index + 1, len(headings)):
        if headings[j][1] <= level:
            end = headings[j][0]
            break
    return start, end


def is_diagram_fence(lang: str, body: str) -> bool:
    lang = (lang or "").lower()
    if lang in DIAGRAM_LANGS:
        return True
    if lang in {"", "txt"} and re.search(r"(→|->|-->|┌|└|│|flowchart|sequenceDiagram)", body):
        return True
    return False


def mermaid_fence(body: str) -> str:
    body = body.strip("\n")
    return f"```mermaid\n{body}\n```"


def apply_blocks_to_jp(jp_text: str, en_text: str, blocks: list[MermaidBlock]) -> tuple[str, int, int]:
    """Return (new_jp, replaced_count, inserted_count)."""
    if not blocks:
        return jp_text, 0, 0

    en_headings = [(m.start(), len(m.group(1)), m.group(2).strip()) for m in HEADING_RE.finditer(en_text)]
    # Work with mutable string via list of operations from end to start, but inserts/replaces
    # interact — process section by section reconstructing the file.

    # Build map: jp_heading_index -> list of mermaid bodies in order
    planned: dict[int, list[MermaidBlock]] = {}
    for b in blocks:
        jh = find_jp_heading_index(jp_text, b, en_headings)
        planned.setdefault(jh, []).append(b)

    # Process headings from bottom to top so offsets stay valid
    new_text = jp_text
    replaced = 0
    inserted = 0

    for jh in sorted(planned.keys(), reverse=True):
        section_blocks = planned[jh]
        start, end = section_bounds(new_text, jh)
        section = new_text[start:end]

        # heading line end
        hm = HEADING_RE.match(section) if jh >= 0 else None
        heading_line_end = hm.end() if hm else 0

        # Find replaceable diagram fences in section (not mermaid/java/etc.)
        fence_matches = list(FENCE_RE.finditer(section))
        diagram_fences = [
            m
            for m in fence_matches
            if is_diagram_fence(m.group(1), m.group(2)) and (m.group(1) or "").lower() != "mermaid"
        ]
        existing_mermaid = [
            m for m in fence_matches if (m.group(1) or "").lower() == "mermaid"
        ]

        # How many mermaids already present — only add missing
        already = len(existing_mermaid)
        needed = section_blocks[already:]
        if not needed:
            continue

        # Prefer replacing diagram fences that are not yet "used"
        # Skip fences that appear before we've "accounted" for existing mermaid slots
        replace_targets = diagram_fences[:]

        # Rebuild section from pieces
        pieces: list[str] = []
        cursor = 0
        need_i = 0

        # If we need to insert before first table and no replace targets early, handle insert
        def insert_position_for(block: MermaidBlock) -> int:
            # After heading + blank line default
            pos = heading_line_end
            if section[pos : pos + 2] == "\n\n":
                pos = pos + 1  # stay after first newline; we'll add block with newlines
            elif section[pos : pos + 1] == "\n":
                pass

            if block.before_first_table:
                tm = re.search(r"^\|.+\|$", section[heading_line_end:], re.M)
                if tm:
                    return heading_line_end + tm.start()

            # After first blank line following heading content paragraph? Prefer before table else after heading
            # Look for a natural blank-line slot after first short intro paragraph
            after = section[heading_line_end:]
            # If section starts with blank then content, insert before first non-empty content block that is a table
            # Fallback: right after heading line
            mblank = re.match(r"\n+", after)
            return heading_line_end + (mblank.end() if mblank else 0)

        # Strategy: for each needed block, try to replace next diagram fence; else insert
        # Build operations as (start, end, replacement) on section
        ops: list[tuple[int, int, str]] = []
        used_fence_idxs: set[int] = set()

        for block in needed:
            # find next unused diagram fence
            target = None
            for fi, fm in enumerate(replace_targets):
                if fi in used_fence_idxs:
                    continue
                target = (fi, fm)
                break
            if target is not None:
                fi, fm = target
                used_fence_idxs.add(fi)
                ops.append((fm.start(), fm.end(), mermaid_fence(block.body)))
                replaced += 1
            else:
                ins_at = insert_position_for(block)
                # Avoid stacking multiple inserts at same exact point: offset by previous inserts at same pos
                same = sum(1 for a, b, _ in ops if a == b == ins_at)
                # Use sentinel end==start for insert
                ops.append((ins_at, ins_at, ("\n" if ins_at > 0 else "") + mermaid_fence(block.body) + "\n"))
                if same:
                    # shift by applying later; we'll sort stably
                    pass
                inserted += 1

        # Apply ops from end to start; for identical insert points, apply in reverse order of list
        # Sort by start desc, and for inserts at same point, later ops first so earlier blocks appear first
        def op_key(item: tuple[int, tuple[int, int, str]]) -> tuple[int, int]:
            idx, (a, b, _) = item
            # higher start first; for same start, higher idx first (so earlier inserts applied last → appear first)
            return (-a, -idx)

        for _, (a, b, rep) in sorted(enumerate(ops), key=op_key):
            section = section[:a] + rep + section[b:]

        # Normalize accidental triple blank lines
        section = re.sub(r"\n{4,}", "\n\n\n", section)
        new_text = new_text[:start] + section + new_text[end:]

    return new_text, replaced, inserted


def pair_files() -> list[tuple[Path, Path, str, str]]:
    en_idx = index_md(EN_ROOT)
    jp_idx = index_md(JP_ROOT)
    pairs: list[tuple[Path, Path, str, str]] = []
    used_jp: set[str] = set()
    for key, (en_rel, en_path) in sorted(en_idx.items()):
        jp_hit = None
        for a in alias_keys(key):
            if a in jp_idx and a not in used_jp:
                jp_hit = jp_idx[a]
                used_jp.add(a)
                break
        if jp_hit is None:
            continue
        jp_rel, jp_path = jp_hit
        pairs.append((en_path, jp_path, en_rel, jp_rel))
    return pairs


def read_text_preserve(path: Path) -> tuple[str, str, bool]:
    """Return (text_with_lf_newlines, bom, uses_crlf)."""
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


def write_text_preserve(path: Path, text: str, bom: str, uses_crlf: bool) -> None:
    out = text
    if uses_crlf:
        out = out.replace("\n", "\r\n")
    data = (bom + out).encode("utf-8")
    path.write_bytes(data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    changed_files = 0
    total_replaced = 0
    total_inserted = 0
    still_short: list[str] = []

    for en_path, jp_path, en_rel, jp_rel in pair_files():
        en_text, _, _ = read_text_preserve(en_path)
        if "```mermaid" not in en_text:
            continue
        en_count = len(re.findall(r"```mermaid", en_text))
        jp_text, bom, uses_crlf = read_text_preserve(jp_path)
        jp_before = len(re.findall(r"```mermaid", jp_text))
        if jp_before >= en_count:
            continue

        blocks = extract_mermaid_blocks(en_text)
        new_jp, replaced, inserted = apply_blocks_to_jp(jp_text, en_text, blocks)
        if new_jp == jp_text:
            still_short.append(f"{jp_rel} (en={en_count} jp={jp_before} no-change)")
            continue
        if not args.dry_run:
            # Normalize spacing around mermaid before write
            new_jp = re.sub(r"(```)\n(\|)", r"\1\n\n\2", new_jp)
            new_jp = re.sub(r"(```)\n(#{1,6} )", r"\1\n\n\2", new_jp)
            new_jp = re.sub(r"(#{1,6} [^\n]+)\n```mermaid", r"\1\n\n```mermaid", new_jp)
            write_text_preserve(jp_path, new_jp, bom, uses_crlf)
        jp_after = len(re.findall(r"```mermaid", new_jp))
        changed_files += 1
        total_replaced += replaced
        total_inserted += inserted
        status = f"updated {jp_rel}: +{jp_after - jp_before} mermaid (replaced={replaced}, inserted={inserted})"
        print(status)
        if jp_after < en_count:
            still_short.append(f"{jp_rel} (en={en_count} jp={jp_after})")

    print(
        f"\nDone. files_changed={changed_files} replaced={total_replaced} inserted={total_inserted}"
    )
    if still_short:
        print(f"Still short ({len(still_short)}):")
        for line in still_short:
            print(" ", line)


if __name__ == "__main__":
    main()
