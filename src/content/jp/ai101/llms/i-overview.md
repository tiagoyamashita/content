---
label: "I"
subtitle: "概要"
group: "LLMs"
order: 1
---
LLMs — 概要
**Large language models (LLMs)** are **very large decoder-only transformers** trained on massive text to **predict the next token**. After pre-training, **alignment** and **prompting** make them useful assistants; **RAG** and **fine-tuning** add domain knowledge.

Prerequisites: [Transformers & attention](../deep-learning/iv-transformers-and-attention.md), [Machine learning evaluation](../machine-learning/iv-model-evaluation-and-metrics.md).

## このサブメニューのマップ

| Part | Topic |
|------|--------|
| **I — Overview** | LLM lifecycle in one page |
| **II — Pre-training & tokenization** | Causal LM objective, scale, BPE, context window |
| **III — Alignment (SFT, RLHF, DPO)** | Helpful, harmless, honest behaviour |
| **IV — Prompt engineering** | Zero/few-shot, CoT, roles, structured output |
| **V — RAG & fine-tuning** | Domain knowledge without full retrain |
| **VI — Safety & production** | Injection, monitoring, serving |

## LLM lifecycle

```text
Pre-train (next token) → SFT (instructions) → RLHF/DPO (preferences) → Deploy (+ RAG / LoRA)
```

| Stage | Data | Output |
|-------|------|--------|
| **Pre-training** | Web-scale text | Base model — completion, not chat |
| **SFT** | Curated Q&A pairs | Follows instructions |
| **RLHF / DPO** | Human preference rankings | Safer, more helpful tone |
| **Production** | Your docs + prompts | Domain-specific answers |

## Open vs closed models

| | Open weights (Llama, Mistral) | API-only (GPT-4, Claude) |
|---|------------------------------|---------------------------|
| **Deploy** | Self-host, fine-tune | Vendor hosts |
| **Cost** | Infra + ops | Per-token |
| **Control** | Full | Limited |

## Next

Continue with [Pre-training & tokenization](ii-pretraining-and-tokenization.md).

**Related:** [Deep learning overview](../deep-learning/i-overview.md), [Order search CDC](../../swe101/sysdesign/examples/viii-order-search-cdc.md) (RAG index pattern).
