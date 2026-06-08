---
label: "II"
subtitle: "Neural networks & training"
group: "Deep learning"
order: 2
---
Neural networks and training
A **neural network** stacks **layers** of neurons — each computes **activation(weights · input + bias)**. **Training** adjusts weights via **backpropagation** and **gradient descent** to minimise **loss**.

## 1. Single neuron

```text
output = activation( w · x + b )
```

| Piece | Role |
|-------|------|
| **w** | Weights — learnable |
| **b** | Bias — learnable |
| **activation** | Non-linearity — without it, stack of layers collapses to linear |

### Activation functions

| Function | Use |
|----------|-----|
| **ReLU** max(0,x) | Default hidden layers |
| **Sigmoid** | Binary output (legacy hidden) |
| **Softmax** | Multi-class probabilities (sum to 1) |
| **GELU** | Smooth; common in transformers |

## 2. Network architecture

**Dense (fully connected):** every input connects to every output in the layer.

```text
input → [hidden × N] → output
```

More layers = **deeper** network = richer (hierarchical) features.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Neural network layers">
  <text x="30" y="18" fill="#71717a" font-size="10" text-anchor="middle">Input</text>
  <circle cx="30" cy="55" r="8" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
  <circle cx="30" cy="85" r="8" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
  <text x="160" y="18" fill="#71717a" font-size="10" text-anchor="middle">Hidden</text>
  <circle cx="130" cy="45" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="130" cy="75" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="190" cy="45" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="190" cy="75" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <text x="360" y="18" fill="#71717a" font-size="10" text-anchor="middle">Output</text>
  <circle cx="360" cy="65" r="8" fill="#27272a" stroke="#fbbf24" stroke-width="1.5"/>
  <line x1="38" y1="55" x2="122" y2="45" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="38" y1="85" x2="122" y2="75" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="198" y1="45" x2="352" y2="65" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="198" y1="75" x2="352" y2="65" stroke="#3f3f46" stroke-width="0.8"/>
</svg></figure>

## 3. Backpropagation

**Forward pass:** compute predictions and loss.
**Backward pass:** chain rule → **∂Loss/∂w** for each weight.
**Update:** **w ← w − η · gradient** (η = learning rate).

Automatic differentiation (PyTorch `autograd`, TF) implements this.

## 4. Optimisers

| Optimiser | Notes |
|-----------|-------|
| **SGD + momentum** | Classic; needs lr tuning |
| **Adam** | Adaptive per-parameter lr — common default |
| **AdamW** | Adam + decoupled weight decay |

## 5. Mini-batch training

| Mode | Trade-off |
|------|-----------|
| **Full batch** | Stable gradient; memory heavy |
| **Mini-batch** (32–512) | GPU-efficient; noisy gradient helps generalisation |
| **SGD batch=1** | Noisy; rarely used alone at scale |

**Epoch** = one full pass over training set.

### Learning rate schedule

| Issue | Fix |
|-------|-----|
| Loss diverges | Lower lr |
| Loss flat | Warm-up + cosine decay; check data |

## 6. Regularisation in deep nets

| Method | See also |
|--------|----------|
| **Dropout** | Randomly zero activations during train |
| **Weight decay** | L2 on weights (AdamW) |
| **Early stopping** | Stop on val loss |
| **Data augmentation** | Images — random crop/flip |

[Overfitting](../machine-learning/v-overfitting-regularization-and-tuning.md) applies the same bias-variance intuition.

## 7. PyTorch sketch

```python
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, d_in, d_hidden, d_out):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_in, d_hidden),
            nn.ReLU(),
            nn.Linear(d_hidden, d_out),
        )
    def forward(self, x):
        return self.net(x)
```

## 8. Rehearsal questions

- Why are non-linear activations required?
- One sentence: what does backprop compute?
- Mini-batch size affects what two things?

**Related:** [CNNs & RNNs](iii-cnns-and-rnns.md), [Transformers](iv-transformers-and-attention.md).
