#!/usr/bin/env python3
"""Translate remaining jp/ English notes in batches; commit and push each batch."""

from __future__ import annotations

import subprocess
import sys
import time

BATCH = 30
WORKERS = 3
MAX_ROUNDS = 50


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True)


def main() -> int:
    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n===== BATCH ROUND {round_no} =====", flush=True)
        report = run([sys.executable, "scripts/sync-en-locale-to-jp.py", "--phase", "report"])
        print(report.stdout.strip(), flush=True)
        if "still needing translation heuristic: 0" in report.stdout:
            print("DONE — no md left needing translation", flush=True)
            return 0

        proc = subprocess.run(
            [
                sys.executable,
                "scripts/sync-en-locale-to-jp.py",
                "--phase",
                "translate",
                "--workers",
                str(WORKERS),
                "--limit",
                str(BATCH),
            ]
        )
        if proc.returncode != 0:
            print(f"translate exit {proc.returncode}", flush=True)

        subprocess.run(["git", "add", "src/content/jp", "scripts/sync-en-locale-to-jp.py"])
        st = run(["git", "status", "--porcelain"])
        if not st.stdout.strip():
            print("No file changes this round; backing off", flush=True)
            time.sleep(10)
            continue

        msg = f"docs(jp): translate batch {round_no} of remaining English notes"
        subprocess.run(
            [
                "git",
                "commit",
                "--author=Tiago Yamashita <yamashiita@gmail.com>",
                "-m",
                msg,
            ],
            check=False,
        )
        for delay in (4, 8, 16, 32):
            push = run(["git", "push", "-u", "origin", "HEAD"])
            if push.returncode == 0:
                print("pushed", flush=True)
                break
            print("push failed:", push.stderr, flush=True)
            time.sleep(delay)
        time.sleep(1)

    print("Reached max rounds", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
