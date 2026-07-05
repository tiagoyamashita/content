---
label: "II"
subtitle: "Products & building assistants"
group: "AI Applied"
order: 2
---
Products & building assistants

## 1. Product equivalents

| Product | Feature | What you configure |
|---------|---------|-------------------|
| **ChatGPT** | Custom GPTs, Memory (optional) | Instructions, files, actions |
| **Claude** | Projects | Project knowledge + instructions |
| **Gemini** | Gems | Persona + optional files |
| **Copilot** | Copilot Studio / M365 Copilot | Tenant data, plugins |
| **NotebookLM** | Notebooks | Sources → grounded Q&A, audio overview |
| **Cursor** | Rules, docs index | Repo + `.cursor/rules` |

Same idea everywhere: **instructions + knowledge + (optional) tools**.

## 2. What to put in “knowledge”

| Good sources | Poor sources |
|--------------|--------------|
| Policy PDFs, playbooks, FAQs | Random outdated exports |
| Product specs, API docs you own | Confidential you’re not allowed to upload |
| Meeting notes **you** curate | Entire email archive unfiltered |
| Style guide, brand voice | Competitor docs you don’t have rights to |

**Refresh:** stale knowledge → confident wrong answers. Date your uploads; replace quarterly.

## 3. Building a useful custom assistant

```text
1. One sentence purpose   ("Answers support tier-1 about Billing v2")
2. Audience               (customers vs internal)
3. Tone & format          (short, links, escalate when …)
4. Boundaries             (no legal advice; no discounts)
5. 3–5 example Q&As       (few-shot in instructions)
6. Knowledge files        (indexed docs)
7. Test with edge cases   (unknown product, angry user, non-English)
```

### Instruction template

```text
Purpose: …
Always: cite doc section; say "I don't know" if not in knowledge.
Never: promise refunds; invent SKU prices.
Format: numbered steps for how-to; table for comparisons.
Escalate: billing disputes → human@company.com
```