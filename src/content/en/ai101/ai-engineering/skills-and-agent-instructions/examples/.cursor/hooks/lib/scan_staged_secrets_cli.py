#!/usr/bin/env python3
"""CLI entry for git pre-commit — scan staged secrets."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scan_staged_secrets import scan_staged


def main() -> int:
    result = scan_staged()
    if result.blocked:
        for line in result.findings:
            print(line, file=sys.stderr)
        return 1
    print("secrets scan OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
