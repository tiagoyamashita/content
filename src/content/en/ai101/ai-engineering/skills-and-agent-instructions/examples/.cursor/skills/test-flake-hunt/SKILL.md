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

Record `current_log_file` from script output (e.g. `.cursor/skills/test-flake-hunt/logs/run-20260710T143022Z.json`).

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
- **Log:** `.cursor/skills/test-flake-hunt/logs/run-….json`
- **Duration:** … ms | **Exit:** …
- **Finding:** …
- **Next:** fix X / re-run / ask user
```

## Do not

- Re-run full suite every message without reading the existing log
- Lose the log path between turns — cite `current_log_file` in each reply
