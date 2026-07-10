---
label: "IV"
subtitle: "Hook — secrets & env scan"
group: "Skills examples"
order: 4
---
Hook — secrets & `.env` scan

**Goal:** A **bot** that runs on **hooks** — before shell runs `git commit` — and scans for exposed secrets, `.env` files staged, API keys in diffs. Writes a **log**; can **block** the action when `failClosed` is set.

Hooks run **automatically**; skills run when the user asks. See [Linking a fixed script](../../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script).

## Folder layout

```text
.cursor/
  hooks.json
  hooks/
    secrets_scan.py
    lib/
      scan_staged_secrets.py   ← shared scan logic
    logs/
      secrets-scan-20260710T150001Z.json
```

Add to `.gitignore`:

```gitignore
.cursor/hooks/logs/
.cursor/skills/*/logs/
```

## Hook config — `.cursor/hooks.json`

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "python3 .cursor/hooks/secrets_scan.py",
        "matcher": "git\\s+commit",
        "timeout": 30,
        "failClosed": true
      }
    ]
  }
}
```

| Event | When it fires |
|-------|----------------|
| `beforeShellExecution` + matcher `git\s+commit` | User/agent tries to commit (JS regex — escape backslashes in JSON) |

The script also filters on `git commit` internally so you can omit the matcher while testing.

## Scan logic — `hooks/lib/scan_staged_secrets.py`

Reusable from the Cursor hook and from git `pre-commit`:

```python
"""Scan staged files for .env and obvious secrets."""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field


SECRET_RE = re.compile(
    r"(api[_-]?key|secret|password|private[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{8,}",
    re.IGNORECASE,
)


@dataclass
class ScanResult:
    findings: list[str] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return bool(self.findings)

    def add(self, message: str) -> None:
        self.findings.append(message)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    ).stdout


def scan_staged() -> ScanResult:
    result = ScanResult()
    names = _git("diff", "--cached", "--name-only").splitlines()

    for name in names:
        if re.search(r"\.env(\.|$)", name):
            result.add(f"STAGED_ENV_FILE: {name}")
        if name == ".env":
            result.add("DOT_ENV_IN_COMMIT")

    diff = _git("diff", "--cached", "-U0")
    if SECRET_RE.search(diff):
        result.add("POSSIBLE_SECRET_IN_STAGED_DIFF")

    return result
```

## Hook wrapper — `hooks/secrets_scan.py`

`beforeShellExecution` hooks receive JSON on **stdin** and return JSON on **stdout** (`permission`: `allow` | `deny`).

```python
#!/usr/bin/env python3
"""Cursor beforeShellExecution hook — block commits with staged secrets."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

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
```

```bash
chmod +x .cursor/hooks/secrets_scan.py
```

## Optional: git pre-commit (runs outside Cursor too)

```bash
# .git/hooks/pre-commit
#!/bin/sh
cd "$(git rev-parse --show-toplevel)" || exit 1
python3 .cursor/hooks/lib/scan_staged_secrets_cli.py
```

Minimal CLI wrapper:

```python
#!/usr/bin/env python3
# .cursor/hooks/lib/scan_staged_secrets_cli.py
import sys
from scan_staged_secrets import scan_staged

result = scan_staged()
if result.blocked:
    for line in result.findings:
        print(line, file=sys.stderr)
    sys.exit(1)
print("secrets scan OK")
```

## SKILL.md companion (optional)

```markdown
---
name: secrets-scan-help
description: Explain secrets-scan hook failures and how to fix staged .env or leaked keys. Use when commit blocked, secrets scan failed, or .env staged.
---

# Secrets scan failures

1. Read latest log in `.cursor/hooks/logs/secrets-scan-*.json`.
2. For `STAGED_ENV_FILE`: unstage with `git reset HEAD -- <file>`; ensure `.env` is in `.gitignore`.
3. For `POSSIBLE_SECRET_IN_STAGED_DIFF`: rotate the secret; remove from code; use env vars.
4. Never tell the user to commit secrets to "fix" the hook.
```

## Agent / user flow

```text
User or agent: git commit -m "…"
  → beforeShellExecution fires
  → secrets_scan.py runs → writes log
  → exit 2 → commit blocked (if failClosed)
  → Agent reads log → suggests fixes
```

## Next

[Performance & bottlenecks](v-performance-bottleneck-scan.md) — on-demand profiling skill.
