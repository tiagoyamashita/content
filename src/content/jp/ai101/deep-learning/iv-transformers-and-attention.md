---
label: "IV"
subtitle: "Transformer と attention"
group: "Deep learning"
order: 4
---
Transformers and attention
**"Attention is All You Need"** (Vaswani et al., 2017) — the architecture behind modern **LLMs**, **BERT**, and most NLP/vision transformers.

## 1. Self-attention

Each token builds a representation by **attending** to all other tokens in the sequence.

```text
Q = X·Wq    K = X·Wk    V = X·Wv
Attention(Q,K,V) = softmax(QKᵀ / √dₖ) · V
```

| Symbol | Meaning |
|--------|---------|
| **Q** (query) | What am I looking for? |
| **K** (key) | What do I offer? |
| **V** (value) | What information do I pass if selected? |

Output = **weighted sum** of values; weights = similarity of query to each key.

## 2. Multi-head attention

Run **h** attention heads in parallel with **different** learned projections — capture different relationship types (syntax, coreference, etc.).

Concatenate heads → linear projection.

## 3. Transformer block

```text
x → Multi-Head Attention → Add & Norm → Feed-Forward → Add & Norm → output
```

| Piece | Role |
|-------|------|
| **Add & Norm** | Residual + layer normalisation — stable deep training |
| **Feed-forward** | Per-token MLP — extra capacity |

Stack **N** blocks → deep transformer.

## 4. Positional encoding

Attention alone is **permutation-invariant** — order must be injected:

| Style | Used in |
|-------|---------|
| **Sinusoidal** (fixed) | Original transformer |
| **Learned embeddings** | GPT, BERT |

## 5. Encoder vs decoder

| Architecture | Attention mask | Examples |
|--------------|----------------|----------|
| **Encoder-only** | Bidirectional — all tokens see all | BERT (classification, embeddings) |
| **Decoder-only** | Causal — token t sees ≤ t | GPT, LLaMA ([LLMs](../llms/i-overview.md)) |
| **Encoder-decoder** | Encoder bidirectional; decoder causal cross-attn | T5, original translation |

**LLMs** for chat are almost always **decoder-only** causal LMs.

## 6. Complexity note

Self-attention is **O(n²)** in sequence length **n** — context window and compute drive cost. Techniques: **FlashAttention**, sparse attention, sliding window (some long-context models).

## 7. Rehearsal questions

- What problem does positional encoding solve?
- Decoder-only vs encoder-only — which for next-token prediction?
- Why √dₖ in the attention scale?

**Related:** [LLMs — pre-training](../llms/ii-pretraining-and-tokenization.md), [Neural networks & training](ii-neural-networks-and-training.md).
