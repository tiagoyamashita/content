---
label: "III"
subtitle: "Directing agents"
group: "AI Applied"
order: 3
---
Directing agents

## 3. When agents help vs hurt

| Good for agents | Better as plain chat |
|-----------------|----------------------|
| Multi-file coding tasks | One-off definition |
| Research across many sources | Short rewrite |
| Repetitive ops with checks | Sensitive irreversible actions without review |
| “Figure out how this repo works” | Factual lookup you can verify in one doc |

| Risk | Mitigation |
|------|------------|
| Wrong file edited | Small tasks; review diffs |
| Invented citations | Require links; verify |
| Runaway scope | “Stop after step 3 and show plan” |
| Cost / time | Set limits; use smaller model for drafts |

## 4. How to direct an agent well

Use the same building blocks as [Effective prompting](../effective-prompting/i-overview.md), plus:

| Add | Example |
|-----|---------|
| **Clear done state** | “Done when: PR-ready diff + test command output.” |
| **Boundaries** | “Do not change files under `/legacy`.” |
| **Tools allowed** | “Use repo search only; no web.” |
| **Checkpoints** | “After plan, wait for my OK before edits.” |
| **Verification** | “Run tests and paste summary.” |

**Cursor / IDE agents:** point at folders, mention stack, reference existing patterns (“match `UserService` style”).

**Research agents:** specify date range, preferred sources, and output schema (table, memo, slides).