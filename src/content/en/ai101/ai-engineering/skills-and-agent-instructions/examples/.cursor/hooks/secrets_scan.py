#!/usr/bin/env python3
"""Cursor beforeShellExecution hook — block commits with staged secrets."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.scan_staged_secrets import scan_staged


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> int:
    raw = sys.stdin.read()
    payload = json.loads(raw) if raw.strip() else {}
    command = payload.get("command", "")

    if not re.search(r"git\s+commit", command):
        print(json.dumps({"permission": "allow"}))
        return 0

    started_at = utc_now()
    t0 = perf_counter()
    scan = scan_staged()
    duration_ms = int((perf_counter() - t0) * 1000)

    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    log_file = log_dir / f"secrets-scan-{stamp}.json"

    log_payload = {
        "script": "secrets_scan.py",
        "command": command,
        "started_at": started_at,
        "finished_at": utc_now(),
        "duration_ms": duration_ms,
        "exit_code": 1 if scan.blocked else 0,
        "results": {
            "findings_count": len(scan.findings),
            "blocked": scan.blocked,
        },
        "messages": scan.findings,
        "log_file": str(log_file),
    }
    log_file.write_text(json.dumps(log_payload, indent=2) + "\n", encoding="utf-8")

    if scan.blocked:
        msg = "; ".join(scan.findings)
        print(
            json.dumps(
                {
                    "permission": "deny",
                    "user_message": f"Commit blocked — secrets scan failed. See {log_file}",
                    "agent_message": f"Fix before commit: {msg}",
                }
            )
        )
        return 2

    print(
        json.dumps(
            {
                "permission": "allow",
                "agent_message": f"Secrets scan passed. Log: {log_file}",
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
