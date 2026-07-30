---
label: "III"
subtitle: "Loop on script results"
group: "Skills examples"
order: 3
---
Loop on script results

**Goal:** Run a script, read its **log file**, and **iterate** on the same data — refine fixes or analysis without re-fetching from scratch each time. Keeps `current_log_file` in the conversation as the source of truth.

## Live files (copy-ready)

| File | Path |
|------|------|
| Skill instructions | [`.cursor/skills/test-flake-hunt/SKILL.md`](.cursor/skills/test-flake-hunt/SKILL.md) |
| Script | [`.cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py`](.cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py) |

## Folder layout

```text
.cursor/skills/test-flake-hunt/
  SKILL.md
  scripts/run_flaky_tests.py
  logs/
```

## Loop pattern (from SKILL.md)

1. **Round 1** — run `python3 .cursor/skills/test-flake-hunt/scripts/run_flaky_tests.py "[pattern]"`
2. Store `current_log_file` from script output.
3. **Round 2+** — read same log; propose fix; re-run only to verify.
4. **Stop** at `exit_code == 0`, user stop, or 5 iterations without progress.

## Optional: Cursor `stop` hook

For automatic “keep going” loops, use a `stop` hook with `loop_limit` — see [Hook — secrets scan](iv-hook-secrets-env-scan.md). Skills alone rely on the agent following the loop in `SKILL.md`.

## Tie-in

[Loop prompting](../../loop-prompting/i-overview.md) — short deltas each turn (“iteration 3: read last log, fix `auth.test.ts`”).

## Next

[Hook — secrets & `.env` scan](iv-hook-secrets-env-scan.md) — automatic checks without user asking.
