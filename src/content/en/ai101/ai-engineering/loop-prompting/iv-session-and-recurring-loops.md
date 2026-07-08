---
label: "IV"
subtitle: "Session & recurring loops"
group: "AI Applied"
order: 4
---
Session & recurring loops
Beyond stored instructions, you can **loop inside one session** (refine the same work) or **loop on a schedule / event** (rerun without opening a new chat). Both are loop prompting — the trigger differs.

## 1. Session loop (same thread)

```text
Turn 1: produce draft
Turn 2: fix specific section
Turn 3: change format
Turn 4: verify against source
```

| Practice | Why |
|----------|-----|
| Reference prior output (“section 2 only”) | Model uses thread context |
| One change per message | Easier to undo mentally |
| Pin files with `@` in IDE | Context stays attached |
| Say “stop and summarize state” before break | Easier resume |

**Resume later:** same project/thread if the tool keeps history; otherwise paste **state summary** + last good artifact — not the whole thread.

## 2. Recurring loop (time-based)

**Cursor `/loop`** runs a prompt on an interval — you define the task once, the agent reruns on a schedule.

```text
/loop 5m check if main CI is green; if failed paste last error
/loop 30s watch deploy log until "healthy" or 10 min timeout
/loop 1d summarize overnight Sentry errors
```

| Pattern | Use |
|---------|-----|
| **Fixed interval** | Poll CI, inbox, metrics dashboard |
| **Dynamic interval** | Agent picks next delay after each run (busy vs quiet) |
| **Run once immediately** | Confirm setup before waiting for first tick |

Syntax varies by product; the idea is universal: **arm → wake → act → re-arm** until you stop.

## 3. Event-driven loop (watcher)

Instead of blind polling, wake when something **changes**:

```text
Watch: git branch updates, log line matches, file saved, webhook fires
  → run prompt
  → optional fallback heartbeat if no event
```

| Event | Example prompt |
|-------|----------------|
| PR opened | “Review diff; comment checklist only” |
| Build failed | “Parse log; suggest fix; link doc” |
| New CSV in folder | “Same weekly report template as last Friday” |

Event loops reduce noise vs `sleep 30s` forever.

## 4. Automation platforms (no IDE)

Same loop shape outside Cursor:

```text
Trigger (schedule / form / webhook)
  → AI step (summarise, classify, draft)
  → Action (Notion, Slack, email)
  → (optional) human approval gate
```

| Platform | Good for |
|----------|----------|
| **Zapier / Make** | SaaS glue, non-developers |
| **n8n** | Self-hosted, complex branches |
| **GitHub Actions + AI** | CI-adjacent loops on repo events |

See [Orchestration patterns](../tools-and-orchestration/iii-orchestration-patterns.md). Put **approval** before customer-facing sends.

## 5. Designing a good loop prompt

Recurring prompts must be **self-contained** each tick — the model may not remember yesterday.

| Include every run | Omit (store elsewhere) |
|-------------------|------------------------|
| What to check / read | Long style guide → skill |
| Pass / fail criteria | Full repo map → `AGENTS.md` |
| Output format | Historical context unless needed |
| Stop conditions | “Be helpful” fluff |

```text
Loop: Every 5m
Task: Read CI status for branch main.
If green: reply "OK" only.
If red: paste failing job name + last 20 log lines + one-line likely cause.
Do not fix code unless I say FIX.
```

## 6. Stopping and supervision

| Risk | Mitigation |
|------|------------|
| Runaway polling / cost | Max duration; exponential backoff |
| Repeated wrong “fixes” | Loop = report only; separate FIX command |
| Alert fatigue | Only notify on state **change** |
| Stale loop after task done | Explicit “stop loop” or kill command |

**Human-in-the-loop** for loops that edit production, send email, or spend money.

## 7. Loop vs agent run

| | Session refine loop | Recurring `/loop` |
|---|---------------------|-------------------|
| **Trigger** | You send next message | Timer or event |
| **Scope** | One deliverable | Monitoring / batch |
| **Context** | Thread history | Fresh read each tick |
| **Best** | Writing, coding, analysis | Ops, CI, digests |

Full **agents** combine tools inside one triggered run — [Directing agents](../agents-and-agentic-workflows/iii-directing-agents.md).

## 8. Rehearsal questions

- How does a session loop differ from a time-based loop?
- Why should recurring prompts be self-contained each tick?
- Name one stop condition you would add to a CI watch loop.

**Next:** [Hygiene & when to reset](v-hygiene-and-when-to-reset.md).
