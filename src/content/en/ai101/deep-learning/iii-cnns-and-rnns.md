---
label: "III"
subtitle: "CNNs & RNNs"
group: "Deep learning"
order: 3
---
CNNs and RNNs
Two specialised architectures before **transformers** dominated: **CNNs** for **spatial** data (images), **RNNs** for **sequences** (text, time series).

## 1. CNN — Convolutional Neural Network

**Idea:** slide a **filter (kernel)** over the input to detect **local patterns** (edges, textures, parts).

| Layer | Role |
|-------|------|
| **Conv** | Local feature detection; shared weights → parameter efficient |
| **ReLU** | Non-linearity |
| **Pooling** (max/avg) | Downsample; translation tolerance |
| **Flatten + Dense** | Classify from high-level maps |

```text
[Conv → ReLU → Pool] × N → Flatten → Dense → logits
```

### Why CNNs for images

| Property | Benefit |
|----------|---------|
| **Local connectivity** | Nearby pixels matter together |
| **Weight sharing** | Same edge detector everywhere |
| **Hierarchy** | Early layers edges → late layers objects |

**Landmarks:** LeNet, AlexNet, VGG, **ResNet** (skip connections fix vanishing gradient).

### Data augmentation

Random flip, crop, colour jitter — cheap regularisation for vision.

## 2. RNN — Recurrent Neural Network

**Idea:** maintain **hidden state** **hₜ** updated at each time step:

```text
hₜ = f(hₜ₋₁, xₜ)
yₜ = g(hₜ)
```

Memory of prior inputs — for language, sensor streams.

| Variant | Fix |
|---------|-----|
| **Vanilla RNN** | Vanishing gradient on long sequences |
| **LSTM** | Gates (forget, input, output) — long-range deps |
| **GRU** | Simpler LSTM (2 gates) — often similar accuracy |

## 3. CNN vs RNN vs Transformer

| Architecture | Inductive bias | Dominant today |
|--------------|----------------|----------------|
| **CNN** | Local spatial | Vision backbones (often + transformer head) |
| **RNN** | Sequential recurrence | Mostly replaced in NLP |
| **Transformer** | Global attention | NLP, vision (ViT), multimodal |

RNNs still appear in **small on-device** or **streaming** models; most new NLP uses [Transformers](iv-transformers-and-attention.md).

## 4. Rehearsal questions

- What does pooling buy you?
- Why do LSTMs beat vanilla RNNs on long text?
- Name one modern vision model family.

**Related:** [Transformers & attention](iv-transformers-and-attention.md), [LLMs overview](../llms/i-overview.md).
