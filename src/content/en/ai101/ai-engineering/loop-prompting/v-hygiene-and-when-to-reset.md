---
label: "V"
subtitle: "Hygiene & when to reset"
group: "AI Applied"
order: 5
---
Hygiene & when to reset
Loop prompting fails when **stored context lies** or **threads rot**. Maintain persistent layers like code: review, version, and reset deliberately.

## 1. Context rot symptoms

| Symptom | Likely cause |
|---------|--------------|
| Model “forgets” rules mid-thread | Context window filled with old turns |
| Contradictory answers | Polluted thread + outdated skill |
| Wrong file patterns | Rules glob mismatch after refactor |
| Loop keeps reporting stale status | Watcher not reset after deploy |

## 2. When to reset

| Reset **thread** | Reset **instructions / skill** |
|------------------|--------------------------------|
| Model stuck repeating mistake | Process or stack changed |
| Topic pivot | Instructions have wrong facts |
| Confidential bleed | Skill copied from old job |
| Long thread > ~20 heavy turns | Quarterly review either way |

**New chat + same project** often fixes thread rot without losing persistent instructions.

## 3. Maintenance cadence

| Artifact | Review |
|----------|--------|
| Custom GPT / Project instructions | When output quality slips |
| `SKILL.md` | After workflow or CLI changes |
| `.cursor/rules` | After major refactor |
| `AGENTS.md` | When test commands or layout change |
| Automation loops | After repo rename, branch policy change |

Add **last reviewed** date in skill footer if your team forgets.

## 4. Trust and verification in loops

Loops amplify mistakes — the same wrong check runs every 5 minutes.

| Habit | Apply to |
|-------|----------|
| **Verify sources** | Research loops, data summaries |
| **Diff before accept** | Code loops, agent edits |
| **Human gate** | External sends, merges, spend |
| **Log loop output** | Audit what auto-ran |

See [Trust, privacy & verify](../trust-privacy-and-verify/i-overview.md).

## 5. Security boundaries

| Never loop unattended… | Without… |
|------------------------|----------|
| Send email / Slack to customers | Approval step |
| Merge to main | CI + human review |
| Use production credentials | Scoped read-only tokens |
| Paste secrets into instructions | Redaction and env vars |

Recurring prompts in shared terminals or logs can **leak** task details — scope loops to trusted environments.

## 6. Team rollout

| Step | Action |
|------|--------|
| 1 | Identify top 3 repeated prompts → skills or project |
| 2 | Document in repo (`AGENTS.md`, team wiki) |
| 3 | Short internal examples of **delta** messages |
| 4 | Shared review of skills like code |
| 5 | Measure time saved; drop unused loops |

## 7. Decision checklist

Before starting a loop workflow:

```text
[ ] Persistent layer holds stable rules (not retyped each time)
[ ] Each turn / tick prompt is a clear delta or self-contained check
[ ] I know when to start a fresh chat
[ ] Instructions updated for current stack
[ ] Verification step for high-stakes output
[ ] Stop condition defined for recurring loops
```

## 8. Rehearsal questions

- What is context rot and one fix?
- When should you update a skill vs start a new chat?
- Why are unattended loops risky for customer email?

**Next:** [Agents & agentic workflows](../agents-and-agentic-workflows/i-overview.md) or [Skills & agent instructions](../skills-and-agent-instructions/i-overview.md).
