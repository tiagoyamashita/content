---
label: "I"
subtitle: "Overview"
group: "Skills examples"
order: 1
---
Skills examples — overview

Four **copy-paste patterns** for skills, scripts, and hooks. Every example includes:

- A **`scripts/`** Python file (real code — not inside `SKILL.md`)
- **Structured runtime logs** (timestamp, duration, exit code, results) via the stdlib `json` module
- Instructions for the agent on **what to do with the log output**

Scripts are **not** embedded in markdown — see [Where scripts live](../i-overview.md#where-scripts-live-not-inside-the-md).

## Why Python (not bash)

| | **Python** | **bash** |
|---|------------|----------|
| JSON logs | `json.dump` — no `jq` | Heredocs + escaping bugs |
| Args | `argparse` | Manual `case` / `getopts` |
| Parsing diffs, AST, perf | `re`, `pathlib`, `ast` | Fragile `grep`/`awk` |
| Hooks | Read stdin JSON, return dict | Same, but easier to get wrong |
| Deps | **stdlib only** in these examples | Often needs `jq`, `curl` |

Use **Python 3.10+**. No pip packages required for the examples below.

## Map of examples

| Example | Pattern | Trigger |
|---------|---------|---------|
| [Parameterized script + clarify](ii-parameterized-script-clarify.md) | Pass args; ask if missing; confirm intent | Skill (user asks to run tool) |
| [Loop on script results](iii-loop-on-script-results.md) | Re-use same log data; refine across iterations | Skill + agent loop |
| [Hook — secrets & `.env` scan](iv-hook-secrets-env-scan.md) | Block or warn before commit / shell | Cursor hook |
| [Performance & bottlenecks](v-performance-bottleneck-scan.md) | Profile / scan; log findings | Skill |

## Shared logging helper (optional)

Copy once per skill/hook folder — keeps log shape consistent:

```python
# scripts/lib/run_log.py
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_path(log_dir: Path, prefix: str = "run") -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return log_dir / f"{prefix}-{stamp}.json"


def write_log(
    log_file: Path,
    *,
    script: str,
    started_at: str,
    duration_ms: int,
    exit_code: int,
    parameters: dict[str, Any],
    results: dict[str, Any],
    messages: list[str],
) -> Path:
    payload = {
        "script": script,
        "started_at": started_at,
        "finished_at": utc_now(),
        "duration_ms": duration_ms,
        "exit_code": exit_code,
        "parameters": parameters,
        "results": results,
        "messages": messages,
        "log_file": str(log_file),
    }
    log_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Log written: {log_file}")
    print(json.dumps(payload, indent=2))
    return log_file


class Timer:
    def __init__(self) -> None:
        self.started_at = utc_now()
        self._t0 = perf_counter()

    @property
    def duration_ms(self) -> int:
        return int((perf_counter() - self._t0) * 1000)
```

## Shared log shape

```text
.cursor/skills/<skill-name>/logs/
  run-20260710T120301Z.json
.cursor/hooks/logs/
  secrets-scan-20260710T120405Z.json
```

```json
{
  "script": "deploy_check.py",
  "started_at": "2026-07-10T12:03:01Z",
  "finished_at": "2026-07-10T12:03:04Z",
  "duration_ms": 3120,
  "exit_code": 0,
  "parameters": { "environment": "staging", "dry_run": true },
  "results": { "checks_failed": 0 },
  "messages": ["Health OK"],
  "log_file": ".cursor/skills/deploy-check/logs/run-20260710T120301Z.json"
}
```

Add `logs/` to `.gitignore` if runs are local-only; commit **scripts** and **SKILL.md**, not ephemeral log files.

## Skill vs hook (which example to copy)

| Need | Copy |
|------|------|
| User invokes workflow; may need parameters | [Parameterized script + clarify](ii-parameterized-script-clarify.md) |
| Iterate on same script output until good enough | [Loop on script results](iii-loop-on-script-results.md) |
| Automatic check on commit / git / shell | [Hook — secrets scan](iv-hook-secrets-env-scan.md) |
| On-demand performance review | [Performance scan](v-performance-bottleneck-scan.md) |

## Study order

Read [Parameterized script + clarify](ii-parameterized-script-clarify.md) first (parameters + logs), then [Loop on script results](iii-loop-on-script-results.md). Add [Hook — secrets scan](iv-hook-secrets-env-scan.md) when you need **automatic** gates.

## Related

- [Linking a fixed script](../iv-cursor-skills-rules-agents-md.md#linking-a-fixed-script)
- [Loop prompting](../../loop-prompting/i-overview.md)
- [How MCP works](../../how-mcp-works/i-overview.md) — live data vs static scripts
