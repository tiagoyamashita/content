---
label: "III"
subtitle: "RAG & knowledge libraries"
group: "AI Applied"
order: 3
---
RAG & knowledge libraries

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

Technical depth: [LLM RAG](../../llms/v-rag-and-fine-tuning.md), [Order search example](../../swe101/sysdesign/examples/viii-order-search-cdc.md).

## 5. Team knowledge libraries

| Approach | Fit |
|----------|-----|
| **Single shared Project/GPT** | Small team, one domain |
| **Per-product assistants** | Different policies and tone |
| **Wiki + AI sidebar** | Notion AI, Confluence AI on existing wiki |

Governance: owner per assistant, changelog when policies update.