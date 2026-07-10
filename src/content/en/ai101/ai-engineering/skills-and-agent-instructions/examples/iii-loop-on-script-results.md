---
label: "III"
subtitle: "Loop on script results"
group: "Skills examples"
order: 3
---
Loop on script results

**Goal:** Run a script, read its **log file**, and **iterate** on the same data — refine fixes or analysis without re-fetching from scratch each time. Keeps `current_log_file` in the conversation as the source of truth.

## Folder layout

```text
.cursor/skills/test-flake-hunt/
  SKILL.md
  scripts/
    lib/
      run_log.py
    run_flaky_tests.py
  logs/
    run-20260710T143022Z.json
```

## Script — `scripts/run_flaky_tests.py`

```python
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
```

## SKILL.md — loop on the same log

```markdown
---
name: test-flake-hunt
description: Run tests, analyze failures from log files, and iterate fixes. Use when user mentions flaky tests, failing CI, or re-run tests after a fix.
---

# Test flake hunt (loop on results)

## Iteration loop (max 5 rounds)

Keep **`current_log_file`** — path from the latest script run. Do not discard prior log content until the user starts a new hunt.

### Round 1 — run

```bash
python3 .cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py "[optional-test-pattern]"
```

Record `current_log_file` from script output (e.g. `logs/run-20260710T143022Z.json`).

### Round 2+ — refine (same data)

1. **Read** `current_log_file` (do not re-run tests yet if analyzing the same failure).
2. Parse `exit_code`, `results.output_excerpt`, `duration_ms`.
3. Propose a **specific fix** (file + line if visible in output).
4. After user approves edit OR you apply a fix, ask: **"Re-run tests?"**
5. Only re-run script when verifying a fix → new log becomes `current_log_file`.

### Stop when

- `exit_code` is 0, or
- User says stop, or
- 5 iterations without progress → summarize blockers from **last log**

## Output format each round

```markdown
## Iteration N
- **Log:** `logs/run-….json`
- **Duration:** … ms | **Exit:** …
- **Finding:** …
- **Next:** fix X / re-run / ask user
```

## Do not

- Re-run full suite every message without reading the existing log
- Lose the log path between turns — cite `current_log_file` in each reply
```

## Optional: Cursor `stop` hook for follow-up

For **automatic** “keep going” loops (agent continues after stop), use a `stop` hook with `loop_limit` in `.cursor/hooks.json` — see [Hook — secrets scan](iv-hook-secrets-env-scan.md) for hook layout. Skills alone rely on the **agent following the loop** in `SKILL.md`; hooks enforce automation.

## Tie-in: loop prompting

Store this skill once; each chat turn is a **short delta** (“iteration 3: read last log, fix `auth.test.ts`”) — see [Loop prompting](../../loop-prompting/i-overview.md).

## Next

[Hook — secrets & `.env` scan](iv-hook-secrets-env-scan.md) — automatic checks without user asking.
