#!/usr/bin/env python3
"""Translate pt-br locale in batches; commit and push each batch."""
from __future__ import annotations
import subprocess, sys, time

BATCH = 30
WORKERS = 3
MAX_ROUNDS = 40

def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True)

def main():
    for round_no in range(1, MAX_ROUNDS + 1):
        print(f"\n===== PT-BR BATCH {round_no} =====", flush=True)
        report = run([sys.executable, "scripts/sync-en-locale.py", "--locale", "pt-br", "--lang", "pt", "--phase", "report"])
        print(report.stdout.strip(), flush=True)
        if "still needing translation heuristic: 0" in report.stdout:
            print("DONE", flush=True)
            return 0
        subprocess.run([
            sys.executable, "scripts/sync-en-locale.py",
            "--locale", "pt-br", "--lang", "pt",
            "--phase", "translate", "--workers", str(WORKERS), "--limit", str(BATCH),
        ])
        subprocess.run(["git", "add", "src/content/pt-br", "scripts", "README.md"])
        st = run(["git", "status", "--porcelain"])
        if not st.stdout.strip():
            print("No changes; backoff", flush=True)
            time.sleep(8)
            continue
        subprocess.run([
            "git", "commit",
            "--author=Tiago Yamashita <yamashiita@gmail.com>",
            "-m", f"docs(pt-br): translate batch {round_no} of Portuguese (Brazil) notes",
        ], check=False)
        for delay in (4, 8, 16, 32):
            push = run(["git", "push", "-u", "origin", "HEAD"])
            if push.returncode == 0:
                print("pushed", flush=True)
                break
            print("push failed", push.stderr, flush=True)
            time.sleep(delay)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
