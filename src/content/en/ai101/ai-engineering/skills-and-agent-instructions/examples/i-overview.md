---
label: "I"
subtitle: "Overview"
group: "Skills examples"
order: 1
---
Skills examples — overview

Four **copy-paste patterns** for skills, scripts, and hooks. Every example includes:

- A **`scripts/`** file (real code — not inside `SKILL.md`)
- **Structured runtime logs** (timestamp, duration, exit code, results)
- Instructions for the agent on **what to do with the log output**

Scripts are **not** embedded in markdown — see [Where scripts live](../i-overview.md#where-scripts-live-not-inside-the-md).

## Map of examples

| Example | Pattern | Trigger |
|---------|---------|---------|
| [Parameterized script + clarify](ii-parameterized-script-clarify.md) | Pass args; ask if missing; confirm intent | Skill (user asks to run tool) |
| [Loop on script results](iii-loop-on-script-results.md) | Re-use same log data; refine across iterations | Skill + agent loop |
| [Hook — secrets & `.env` scan](iv-hook-secrets-env-scan.md) | Block or warn before commit / shell | Cursor hook |
| [Performance & bottlenecks](v-performance-bottleneck-scan.md) | Profile / scan; log findings | Skill |

## Shared logging pattern

All example scripts write logs under the skill or hook folder:

```text
.cursor/skills/<skill-name>/logs/
  run-20260710T120301Z.json
.cursor/hooks/logs/
  secrets-scan-20260710T120405Z.json
```

**Log shape (JSON):**

```json
{
  "script": "deploy-check.sh",
  "started_at": "2026-07-10T12:03:01Z",
  "finished_at": "2026-07-10T12:03:04Z",
  "duration_ms": 3120,
  "exit_code": 0,
  "parameters": { "environment": "staging", "dry_run": true },
  "results": { "checks_passed": 3, "checks_failed": 0 },
  "messages": ["Health OK", "Migrations current"]
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
