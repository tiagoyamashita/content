---
label: "V"
subtitle: "カスタムアシスタントとナレッジ"
group: "Using AI"
order: 5
---
Custom assistants and knowledge
Products let you attach **your** documents and **standing instructions** so AI answers like a teammate who read the handbook — without fine-tuning models yourself.

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

## 4. RAG without the jargon

**Retrieval-augmented generation (RAG)** = AI **searches your files** and **writes using those chunks**.

| You do | Product does |
|--------|--------------|
| Upload PDFs / connect drive | Chunk, embed, search on each question |
| Ask question | Inject relevant passages into prompt |

Tips for better answers:

| Tip | Why |
|-----|-----|
| **Descriptive filenames** | Helps retrieval and your sanity |
| **One topic per doc** | Reduces wrong chunks mixed in |
| **Ask “quote the source”** | Easier to verify |
| **Split huge PDFs** | By chapter if product allows |

Technical depth: [LLM RAG](../llms/v-rag-and-fine-tuning.md), [Order search example](../../swe101/sysdesign/examples/viii-order-search-cdc.md).

## 5. Team knowledge libraries

| Approach | Fit |
|----------|-----|
| **Single shared Project/GPT** | Small team, one domain |
| **Per-product assistants** | Different policies and tone |
| **Wiki + AI sidebar** | Notion AI, Confluence AI on existing wiki |

Governance: owner per assistant, changelog when policies update.

## 6. Memory features

Some products **remember** facts across chats (“user prefers bullet points”).

| Upside | Downside |
|--------|----------|
| Less repetition | Wrong memory persists — correct or delete |
| Personalisation | Privacy — know what vendor stores |

Turn off or clear memory for **shared machines** or **sensitive work**.

## 7. Rehearsal questions

- Custom GPT vs one-off chat — when is setup worth it?
- Why ask the model to quote sources?
- What belongs in instructions vs uploaded files?

**Related:** [Effective prompting](ii-effective-prompting.md), [Trust & verify](vii-trust-privacy-and-verify.md).
