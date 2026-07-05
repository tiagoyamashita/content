---
label: "II"
subtitle: "Hallucinations & verification"
group: "AI Applied"
order: 2
---
Hallucinations & verification

## 1. Hallucinations

**Hallucination** = plausible-sounding output that is **wrong** — fake citations, wrong numbers, invented API names.

| High hallucination risk | Lower risk |
|-------------------------|------------|
| Obscure facts, recent events | Editing your pasted text |
| “Give me 10 papers on …” with links | Style/format transformation |
| Numeric detail from memory | Summarising **provided** doc |

| Habit | Action |
|-------|--------|
| **Verify facts** | Check primary source |
| **Require citations** | Click links; confirm paper exists |
| **Numbers** | Trace to spreadsheet or report |
| **Code** | Run tests; don’t merge unseen |

Treat AI like a **clever colleague who sometimes bluffs**.

## 4. Verification checklist (before you ship)

- [ ] Facts traced to a source **you** opened
- [ ] Numbers match spreadsheet / system of record
- [ ] Names, dates, URLs manually spot-checked
- [ ] Code compiled / tests run (if applicable)
- [ ] Tone and commitments acceptable to send under **your** name
- [ ] No confidential content in prompt history you’ll regret