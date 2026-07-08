---
label: "II"
subtitle: "Pre-training & tokenization"
group: "LLMs"
order: 2
---
Pre-training and tokenization
**Pre-training** teaches a transformer to model text by **next-token prediction**. **Tokenization** maps raw text to **subword ids** the model consumes.

## 1. Causal language modelling

Given tokens **[t₁, …, tₙ]**, predict **tₙ₊₁** (decoder-only, left-to-right).

```text
"The cat sat on the" → predict "mat"
```

Loss = cross-entropy over vocabulary at each position. Trained on **trillions of tokens** → emergent skills (reasoning, code, multilingual).

## 2. Scale laws

Performance improves predictably with:

| Knob | Effect |
|------|--------|
| **Parameters** | Capacity |
| **Data** | Coverage |
| **Compute** | Training steps |

Larger models need more data and FLOPs — training runs use thousands of GPUs for weeks.

## 3. Tokenization — BPE

**Byte-Pair Encoding:** merge frequent byte/character pairs → **subword** vocabulary (30k–100k tokens).

| Text | Tokens (example) |
|------|------------------|
| `"tokenization"` | `["token", "ization"]` |
| Rare words | Split into known pieces |

**Implications:**

| Topic | Detail |
|-------|--------|
| **Billing** | API cost often per **token**, not word |
| **Context limit** | Max **tokens** in window |
| **Typos / unicode** | May split oddly — affects robustness |

## 4. Context window

Max tokens model attends to at once — historically 2K–4K; modern models **128K–1M+** (with cost).

| Long context use | Pattern |
|------------------|---------|
| Whole document Q&A | Stuff doc + question in prompt |
| Very long docs | [RAG](v-rag-and-fine-tuning.md) — retrieve chunks |

## 5. Base vs instruct model

| Model | Behaviour |
|-------|-----------|
| **Base** | Continues text — not chat-safe |
| **Instruct / chat** | After SFT + alignment — follows user messages |

Always use **instruct** checkpoints for products unless you control prompting carefully.

## 6. Rehearsal questions

- What is the pre-training objective of GPT-style models?
- Why subword tokenization vs one token per word?
- Base vs instruct — which for a customer support bot?

**Related:** [Alignment](iii-alignment-sft-rlhf-dpo.md), [Transformers](../deep-learning/iv-transformers-and-attention.md).
