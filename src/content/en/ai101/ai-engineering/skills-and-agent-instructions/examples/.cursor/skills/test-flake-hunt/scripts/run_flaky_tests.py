#!/usr/bin/env python3
"""Run tests and log structured output for agent iteration."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from lib.run_log import Timer, log_path, write_log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run flaky test hunt")
    parser.add_argument(
        "pattern",
        nargs="?",
        default="",
        help="Optional test path pattern (passed to npm test)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    timer = Timer()

    cmd = ["npm", "test"]
    if args.pattern:
        cmd.extend(["--", "--testPathPattern", args.pattern])

    completed = subprocess.run(cmd, capture_output=True, text=True)
    output = (completed.stdout or "") + (completed.stderr or "")
    excerpt = "\n".join(output.splitlines()[-40:])

    log_file = log_path(log_dir)
    write_log(
        log_file,
        script="run_flaky_tests.py",
        started_at=timer.started_at,
        duration_ms=timer.duration_ms,
        exit_code=completed.returncode,
        parameters={"pattern": args.pattern},
        results={"command": " ".join(cmd), "output_excerpt": excerpt},
        messages=[f"exit_code={completed.returncode}"],
    )
    print(excerpt)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
