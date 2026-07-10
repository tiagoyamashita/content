---
name: perf-scan
description: Scan codebase for performance smells, large files, sync I/O, and bottlenecks. Use when user asks about performance, slow app, optimization, or profiling.
---

# Performance scan

## Before running

Ask if missing:

- **Scope:** whole repo `.` or path (e.g. `src/api/`)?
- **Runtime check:** optional URL for `PERF_URL` smoke timing?

Confirm:

> I will run perf-scan on `<path>` and summarize findings from the JSON log. Proceed?

## Run

```bash
PERF_URL="${PERF_URL:-}" python3 examples/.cursor/skills/perf-scan/scripts/perf_scan.py "<path>"
```

## After run

1. Open the log file path from script output.
2. Group findings: **large files**, **sync I/O**, **HTTP timing**, **bundle**.
3. Prioritize top 3 by likely user impact — not every hit needs a fix.
4. For each: suggest **one** concrete change (async I/O, split module, cache, index).

## Loop (optional)

After user applies a fix, re-run the **same path** and compare `findings_count` and `duration_ms` to the previous log. Keep both log paths in the reply.

## Do not

- Claim production metrics without data — this is a **static/heuristic** scan
- Run load tests against prod URLs without explicit user approval
