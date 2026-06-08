---
label: "I"
subtitle: "Overview"
group: "Deep learning"
order: 1
---
Deep learning — overview
**Deep learning** uses **neural networks** with many layers to learn hierarchical representations — strong on **images**, **audio**, **text**, and other high-dimensional data. It is a **subset** of [machine learning](../machine-learning/i-overview.md) with heavier **compute** and **data** requirements.

## Map of this submenu

| Part | Topic |
|------|--------|
| **I — Overview** | How deep learning fits AI101 |
| **II — Neural networks & training** | Neurons, backprop, optimisers, batch training |
| **III — CNNs & RNNs** | Spatial and sequential architectures |
| **IV — Transformers & attention** | Self-attention, encoder/decoder, foundation for LLMs |

## When deep learning vs classical ML

| Prefer classical ML | Prefer deep learning |
|---------------------|----------------------|
| Small tabular datasets | Images, long text, audio |
| Need interpretable coefficients | Need representation learning |
| Limited GPU budget | Large data + compute |

Many production systems use **both** — gradient boosting on tabular features + neural net on text/images.

## Stack

| Layer | Common tools |
|-------|--------------|
| **Framework** | PyTorch (research/industry), TensorFlow/Keras |
| **Training** | GPU/TPU, mixed precision |
| **Serving** | TorchServe, ONNX, Triton |

## Next

Continue with [Neural networks & training](ii-neural-networks-and-training.md).

**Related:** [Machine learning overview](../machine-learning/i-overview.md), [LLMs overview](../llms/i-overview.md).
