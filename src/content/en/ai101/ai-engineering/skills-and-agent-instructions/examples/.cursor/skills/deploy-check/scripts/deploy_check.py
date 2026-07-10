#!/usr/bin/env python3
"""Deploy preflight checks — writes JSON log under ../logs/."""
from __future__ import annotations

import argparse
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

from lib.run_log import Timer, log_path, write_log


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Deploy preflight checks")
    parser.add_argument(
        "--environment",
        required=True,
        choices=("staging", "production"),
        help="Target environment",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate deploy (recommended for production)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    timer = Timer()
    messages: list[str] = []
    failures = 0

    if args.environment == "production" and not args.dry_run:
        messages.append("WARN: production deploy without dry-run")

    url = os.environ.get("STAGING_URL", "https://staging.example.com/health")
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            if 200 <= resp.status < 300:
                messages.append("Health OK")
            else:
                messages.append(f"Health FAILED: HTTP {resp.status}")
                failures += 1
    except (urllib.error.URLError, TimeoutError) as exc:
        messages.append(f"Health FAILED: {exc}")
        failures += 1

    log_file = log_path(log_dir)
    write_log(
        log_file,
        script="deploy_check.py",
        started_at=timer.started_at,
        duration_ms=timer.duration_ms,
        exit_code=failures,
        parameters={"environment": args.environment, "dry_run": args.dry_run},
        results={"checks_failed": failures},
        messages=messages,
    )
    return failures


if __name__ == "__main__":
    sys.exit(main())
