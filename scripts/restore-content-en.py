#!/usr/bin/env python3
"""Restore English prose in src/content/*.md from git history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

CONTENT_ROOT = Path(__file__).resolve().parent.parent / "src" / "content"
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")


def path_variants(rel_posix: str) -> list[str]:
    p = PurePosixPath(rel_posix)
    rel = p.as_posix()
    parts = rel.split("/")
    variants: set[str] = {rel}

    def add(s: str) -> None:
        variants.add(s)

    add(rel.replace("CS101/", "cs101/"))
    add(rel.replace("cs101/", "CS101/"))
    add(rel.replace("/algorithms/", "/Algorithms/"))
    add(rel.replace("/Algorithms/", "/algorithms/"))

    if parts:
        head, *tail = parts
        for head_variant in {head, head.lower(), head.upper()}:
            if tail:
                add("/".join([head_variant, *tail]))
        if len(parts) >= 2:
            section = parts[1]
            for section_variant in {
                section,
                section.lower(),
                section.title(),
                section.capitalize(),
            }:
                add("/".join([parts[0], section_variant, *parts[2:]]))
            add("/".join(["cs101", "Algorithms", *parts[2:]]))
            add("/".join(["CS101", "Algorithms", *parts[2:]]))
            add("/".join(["cs101", "algorithms", *parts[2:]]))

    return list(variants)


def git_file_at(commit: str, rel_posix: str) -> str | None:
    for variant in path_variants(rel_posix):
        git_path = f"src/content/{variant}"
        try:
            return subprocess.check_output(
                ["git", "show", f"{commit}:{git_path}"],
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError:
            continue
    return None


def git_history(rel_posix: str, limit: int = 200) -> list[str]:
    for variant in path_variants(rel_posix):
        git_path = f"src/content/{variant}"
        try:
            out = subprocess.check_output(
                ["git", "log", "--follow", f"--max-count={limit}", "--format=%H", "--", git_path],
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
            )
            commits = [line.strip() for line in out.splitlines() if line.strip()]
            if commits:
                return commits
        except subprocess.CalledProcessError:
            continue
    return []


def is_english(text: str) -> bool:
    return not CJK_RE.search(text)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    restored = 0
    missing: list[str] = []

    for path in sorted(CONTENT_ROOT.rglob("*.md")):
        rel = path.relative_to(CONTENT_ROOT).as_posix()
        current = path.read_text(encoding="utf-8")
        if is_english(current):
            continue

        english: str | None = None
        source_commit: str | None = None
        for commit in git_history(rel):
            candidate = git_file_at(commit, rel)
            if candidate and is_english(candidate):
                english = candidate
                source_commit = commit[:8]
                break

        if not english:
            missing.append(rel)
            print(f"MISSING {rel}", file=sys.stderr)
            continue

        if english != current:
            print(f"{rel} <- {source_commit}")
            restored += 1
            if not args.dry_run:
                if not english.endswith("\n"):
                    english += "\n"
                path.write_text(english, encoding="utf-8")

    print(f"Done. Restored {restored} file(s). missing={len(missing)} dry_run={args.dry_run}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
