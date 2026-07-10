---
label: "VI"
subtitle: "Agent orchestration"
group: "Using skills, agents & hooks"
order: 6
---
Agent orchestration

**Agent orchestration** is how you **coordinate** multiple pieces — briefing, skills, hooks, scripts, MCP, loops — so the agent does the right thing at the right time without you re-explaining every chat.

This folder is a **project-level orchestration** guide. For product-wide patterns (Zapier, connectors), see [Orchestration patterns](../../tools-and-orchestration/iii-orchestration-patterns.md). For multi-step reasoning, see [Agents & agentic workflows](../../agents-and-agentic-workflows/i-overview.md).

## Orchestration stack (bottom → top)

```text
┌─────────────────────────────────────────────────────────────┐
│  Human — goal, approval, parameters                          │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  AGENTS.md — always-on context (stack, tests, skill index)   │
└────────────────────────────┬────────────────────────────────┘
                             │ every session
┌────────────────────────────▼────────────────────────────────┐
│  Hooks — event gates (commit, shell, edit, stop)             │
│  Deterministic; no LLM required                              │
└────────────────────────────┬────────────────────────────────┘
                             │ allow / deny / follow-up
┌────────────────────────────▼────────────────────────────────┐
│  Skills — route workflows by user intent (description match) │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│  Scripts + MCP — act on repo / external systems              │
│  JSON logs back to agent for summarize / loop                │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Orchestrates | Example |
|-------|--------------|---------|
| **AGENTS.md** | *What repo is* | “Tests: `npm test`” |
| **Hooks** | *When actions may run* | Block `git commit` if `.env` staged |
| **Skills** | *Which playbook* | PR review vs deploy check |
| **Scripts** | *Repeatable side effects* | `deploy_check.py` → JSON log |
| **MCP** | *Live external data* | Query Sentry, not static skill text |

## Orchestration patterns in Cursor

### 1. Briefing + on-demand skill (default)

```text
Session start → AGENTS.md
User task     → matching skill
Agent         → tools + skill procedure
```

No hook. User drives timing. See [Skills alone](ii-use-skills-alone.md).

### 2. Gate then explain (hook + companion skill)

```text
git commit → hook DENY → log written
User asks  → hook-failure-help / secrets-scan-help skill
User fixes → retry commit → hook ALLOW
```

Hook enforces; skill narrates. See [Hooks on commit](iv-use-hooks-on-commit.md).

### 3. Script loop (skill + JSON log)

```text
Skill runs script → log file
Agent reads log   → proposes fix
User approves     → skill re-runs script → compare logs
```

Same data refined across turns. See [Loop on script results](../examples/iii-loop-on-script-results.md).

### 4. Stop / subagent loops (advanced hooks)

| Hook event | Orchestration use |
|------------|-------------------|
| `stop` + `loop_limit` | Agent finishes → hook injects follow-up (“re-read log, iteration 2”) |
| `subagentStart` | Approve or deny Task/subagent spawns |
| `subagentStop` | Chain subagent with `followup_message` |
| `preToolUse` | Block or rewrite dangerous tool calls |

Use when a **skill loop** is not enough — you need the **product** to continue without a new user message.

### 5. MCP + skills (live + static)

| Piece | Role |
|-------|------|
| Skill | *How we triage production errors* |
| MCP (Sentry) | *Current stack trace* |

Skill without MCP = stale runbook. MCP without skill = agent improvises process.

## Who orchestrates what

| Actor | Responsibility |
|-------|----------------|
| **You** | Goals, parameters, approve destructive actions |
| **AGENTS.md** | Stable repo facts |
| **Hooks** | Hard gates and automation edges |
| **Skills** | Named workflows and output shape |
| **Agent (LLM)** | Reasoning inside skill boundaries |
| **Scripts** | Deterministic checks and logs |
| **CI / git** | Post-push truth (hooks are not a substitute) |

## Design rules

| Rule | Why |
|------|-----|
| **Hooks stay dumb** | Fast, auditable; no model latency on every commit |
| **Skills stay procedural** | “Ask → confirm → run → read log” |
| **AGENTS.md stays short** | Index skills; don’t duplicate checklists |
| **One log path per iteration** | Agent cites `current_log_file` — [loop example](../examples/iii-loop-on-script-results.md) |
| **Human approval before externals** | Email customers, prod deploy, history rewrite |

## Example orchestration map (this repo’s samples)

```text
AGENTS.md
  ├── index → pr-review-lite skill      (user: "review PR")
  ├── index → deploy-check skill        (user: "deploy check")
  └── note  → secrets hook on commit

hooks.json
  └── beforeShellExecution → secrets_scan.py

On block → secrets-scan-help / hook-failure-help skill
On deploy → deploy_check.py → logs/ → agent summarizes
```

Copy layout: [sample/](sample/.cursor/README.md) + [examples/.cursor/](../examples/.cursor/README.md).

## vs “just chat”

| Just chat | Orchestrated project |
|-----------|----------------------|
| Re-paste test commands | `AGENTS.md` |
| “Remember to check secrets” | Hook on commit |
| Inconsistent PR reviews | `pr-review` skill |
| Agent guesses deploy steps | `deploy-check` script + skill |
| No audit trail | JSON logs under `logs/` |

## Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| One giant `AGENTS.md` with every workflow | Split into skills; index in briefing |
| Hook that calls the LLM for policy | `preToolUse` prompt hook only when needed; prefer script |
| Skill that tries to block git | Use hook for enforce |
| Orchestration without logs | Scripts write JSON; agent reads path |
| 10 skills with overlapping descriptions | Narrow `description`; one job per folder |

## Rehearsal questions

- Name the four layers from briefing down to scripts.
- Why should a commit gate be a hook, not a skill?
- When would you add a `stop` hook instead of relying on the skill loop text?

## Related

- [Combine skills, agents & hooks](v-combine-skills-agents-hooks.md)
- [Orchestration patterns](../../tools-and-orchestration/iii-orchestration-patterns.md)
- [Agents & agentic workflows](../../agents-and-agentic-workflows/i-overview.md)
- [Loop prompting](../../loop-prompting/i-overview.md)
- [How MCP works](../../how-mcp-works/i-overview.md)
