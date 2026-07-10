#!/usr/bin/env python3
"""Heuristic performance scan — writes JSON log."""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

from lib.run_log import Timer, log_path, write_log

SKIP_DIRS = {"node_modules", ".next", "dist", ".git", "__pycache__"}
CODE_GLOB = ("*.ts", "*.tsx", "*.js", "*.py")
SYNC_IO_RE = re.compile(r"readFileSync|writeFileSync|execSync|open\([^)]*\)\.read\(")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Performance heuristic scan")
    parser.add_argument("target", nargs="?", default=".", help="Path to scan")
    return parser.parse_args()


def iter_code_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in CODE_GLOB:
        for path in root.rglob(pattern):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            files.append(path)
            if len(files) >= 200:
                return files
    return files


def scan(target: Path, perf_url: str | None) -> list[str]:
    findings: list[str] = []

    for path in iter_code_files(target):
        try:
            line_count = sum(1 for _ in path.open(encoding="utf-8", errors="ignore"))
        except OSError:
            continue
        if line_count > 500:
            findings.append(f"LARGE_FILE: {path} ({line_count} lines)")

    for path in iter_code_files(target):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for match in SYNC_IO_RE.finditer(text):
            findings.append(f"SYNC_IO_CANDIDATE: {path} ({match.group(0)})")
            if len(findings) >= 25:
                break

    analyze = subprocess.run(
        ["npm", "run", "-s", "analyze"],
        capture_output=True,
        text=True,
        cwd=target if target.is_dir() else target.parent,
    )
    if analyze.returncode == 0:
        findings.append("BUNDLE_ANALYZE: npm run analyze completed — check report")

    if perf_url:
        try:
            with urllib.request.urlopen(perf_url, timeout=15) as resp:
                findings.append(f"HTTP_TIMING: {perf_url} status={resp.status}")
        except (urllib.error.URLError, TimeoutError) as exc:
            findings.append(f"HTTP_TIMING: {perf_url} failed: {exc}")

    return findings


def main() -> int:
    args = parse_args()
    target = Path(args.target).resolve()
    perf_url = os.environ.get("PERF_URL") or None
    log_dir = Path(__file__).resolve().parent.parent / "logs"
    timer = Timer()

    findings = scan(target, perf_url)
    count = len(findings)
    severity = "high" if count > 10 else "medium"

    log_file = log_path(log_dir)
    write_log(
        log_file,
        script="perf_scan.py",
        started_at=timer.started_at,
        duration_ms=timer.duration_ms,
        exit_code=0,
        parameters={"target_path": str(target), "perf_url": perf_url},
        results={"findings_count": count, "severity_hint": severity},
        messages=findings,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
