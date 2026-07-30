---
label: "V"
subtitle: "Performance & bottlenecks"
group: "Skills examples"
order: 5
---
Performance & bottlenecks

**Goal:** A **skill-triggered** bot that scans for **performance issues** — large files, sync I/O heuristics, optional HTTP timing — and logs **runtime + findings** for the agent to summarize and suggest fixes.

## Live files (copy-ready)

| File | Path |
|------|------|
| Skill instructions | [`.cursor/skills/perf-scan/SKILL.md`](.cursor/skills/perf-scan/SKILL.md) |
| Script | [`.cursor/skills/perf-scan/scripts/perf_scan.py`](.cursor/skills/perf-scan/scripts/perf_scan.py) |

## Folder layout

```text
.cursor/skills/perf-scan/
  SKILL.md
  scripts/perf_scan.py
  logs/
```

## Run

```bash
PERF_URL="${PERF_URL:-}" python3 .cursor/skills/perf-scan/scripts/perf_scan.py "."
```

Agent flow: ask scope → confirm → run → read log → prioritize top 3 findings.

## Combine with loop example

[Loop on script results](iii-loop-on-script-results.md) — baseline log, fix, re-run, compare `findings_count`.

## Related

- [Parameterized script + clarify](ii-parameterized-script-clarify.md)
- [Examples overview](i-overview.md)
