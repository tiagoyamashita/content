#!/usr/bin/env python3
"""Apply curated Japanese sidebar labels from scripts/ja-menu-labels.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "src" / "content"
GLOSSARY = Path(__file__).resolve().parent / "ja-menu-labels.json"


def main() -> int:
    mapping = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    updated = 0
    for rel, label in mapping.items():
        path = ROOT / rel.replace("/", "\\") if "\\" in str(ROOT) else ROOT / rel
        if not path.exists():
            print(f"skip missing: {rel}")
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("label") == label:
            continue
        data["label"] = label
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"updated: {rel}")
        updated += 1
    print(f"Done. {updated} label(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
