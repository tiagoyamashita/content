---
label: "II"
subtitle: "Deep Learning & LLMs"
group: "Artificial intelligence"
order: 2
---
Artificial Intelligence — Part II: Deep Learning & LLMs
Neural nets, transformers, large language models, prompting.

## 1. Neural networks
Inspired loosely by biological neurons.

Neuron (perceptron):
output = activation( w·x + b )
- w = weights, b = bias — the learnable parameters.
- activation introduces non-linearity.

Common activation functions:
- ReLU(x)    = max(0, x)     — default for hidden layers; fast, sparse.
- Sigmoid(x) = 1/(1+e⁻ˣ)   — squashes to (0,1); used in binary output.
- Softmax    = eˣᵢ/Σeˣʲ     — multi-class probabilities (sum to 1).
- GELU       ≈ x·Φ(x)       — smooth ReLU; used in transformers.

Fully-connected (dense) layer: every input connected to every output neuron.
Stack layers: input → [hidden ×N] → output.
More layers = deeper network = richer representations.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Neural network diagram">
  <text x="30" y="18" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Input</text>
  <circle cx="30" cy="35" r="8" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
  <circle cx="30" cy="65" r="8" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
  <circle cx="30" cy="95" r="8" fill="#27272a" stroke="#52525b" stroke-width="1.5"/>
  <text x="160" y="18" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Hidden</text>
  <circle cx="130" cy="45" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="130" cy="75" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="130" cy="105" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="190" cy="45" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="190" cy="75" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <circle cx="190" cy="105" r="8" fill="#27272a" stroke="#86efac" stroke-width="1.5"/>
  <text x="360" y="18" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Output</text>
  <circle cx="360" cy="55" r="8" fill="#27272a" stroke="#fbbf24" stroke-width="1.5"/>
  <circle cx="360" cy="85" r="8" fill="#27272a" stroke="#fbbf24" stroke-width="1.5"/>
  <line x1="38" y1="35" x2="122" y2="45" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="38" y1="35" x2="122" y2="75" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="38" y1="65" x2="122" y2="45" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="38" y1="65" x2="122" y2="75" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="38" y1="95" x2="122" y2="75" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="38" y1="95" x2="122" y2="105" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="198" y1="45" x2="352" y2="55" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="198" y1="75" x2="352" y2="55" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="198" y1="75" x2="352" y2="85" stroke="#3f3f46" stroke-width="0.8"/>
  <line x1="198" y1="105" x2="352" y2="85" stroke="#3f3f46" stroke-width="0.8"/>
</svg></figure>


## 2. Training deep networks
Backpropagation: chain rule applied layer by layer to compute ∂Loss/∂w.
Gradient descent: w ← w − η·∂Loss/∂w  (η = learning rate).

Optimisers:
- SGD + momentum: smooths gradient noise; needs careful lr tuning.
- Adam: adaptive per-parameter lr; combines momentum + RMSProp; default choice.
- AdamW: Adam + weight decay (fixes L2 regularization in Adam).

Mini-batch training:
- Full batch: stable but slow on large data.
- Mini-batch (32–512 samples): GPU-efficient; noisy gradient is actually helpful.
- 1 epoch = one full pass through the training data.

Learning rate schedule:
- Warm-up: start small → ramp up → decay (cosine or step).
- Too high lr → diverge; too low → very slow convergence.

## 3. CNNs & RNNs
CNN (Convolutional Neural Network) — images & spatial data:
- Convolution: slide a filter (kernel) over the input → detect local patterns.
- Pooling: downsample (max pool) → translation invariance, fewer params.
- Architecture: [Conv→ReLU→Pool] × N → Flatten → Dense → Output.
- Landmark models: LeNet, VGG, ResNet (skip connections cure vanishing gradient).

RNN (Recurrent Neural Network) — sequences:
- Hidden state hₜ = f(hₜ₋₁, xₜ) — carries memory across time steps.
- Vanishing gradient problem: gradients shrink over long sequences.
- LSTM: gated cells (forget, input, output gates) → learn long-range deps.
- GRU: simplified LSTM (2 gates); faster; often comparable accuracy.
- Largely replaced by transformers for NLP tasks.

## 4. Transformers & attention
"Attention is All You Need" (Vaswani et al., 2017) — foundation of modern NLP.

Self-attention:
- Each token attends to every other token in the sequence.
- Q (query), K (key), V (value) projections of the input.
- Attention(Q,K,V) = softmax(QKᵀ/√dₖ) · V
- Output: weighted sum of values; weight = similarity of query to each key.

Multi-head attention:
- Run h attention heads in parallel with different projections.
- Captures different relationship types simultaneously.

Transformer block:
Multi-head attention → Add & Norm → Feed-forward → Add & Norm

Positional encoding:
- Attention has no built-in sequence order → inject position info.
- Fixed sine/cosine (original) or learned positional embeddings (GPT).

Encoder-decoder (BERT / T5 style) vs decoder-only (GPT style).

## 5. Large language models
LLM = very large decoder-only transformer trained on massive text corpora.

Pre-training objective — next token prediction (causal LM):
Given tokens [t₁, t₂, …, tₙ], predict tₙ₊₁.
Trained on trillions of tokens → emergent capabilities.

Scale laws (Kaplan et al.):
Performance improves predictably with more params, data, and compute.

Alignment — making the model helpful & safe:
- SFT (Supervised Fine-Tuning): fine-tune on curated instruction-response pairs.
- RLHF (Reinforcement Learning from Human Feedback):
– Human raters rank model outputs.
– Train a reward model on rankings.
– Fine-tune LLM with PPO to maximise reward.
- DPO (Direct Preference Optimisation): simpler RLHF alternative; trains on
(chosen, rejected) pairs without a separate reward model.

Tokenisation:
- BPE (Byte-Pair Encoding): merge frequent byte pairs → subword vocabulary.
- Context window: max tokens the model can attend to at once (4K–1M+).

## 6. Prompt engineering
The model is frozen; we steer behaviour through the input prompt alone.

Basic techniques:
- Zero-shot: just describe the task. Works for simple, well-known tasks.
- Few-shot:  provide 2–5 examples in the prompt before the query.
- Chain-of-thought (CoT): ask the model to 'think step by step'.
→ Dramatically improves multi-step reasoning & math.

Structured output:
- Ask for JSON / Markdown tables; use system prompt to enforce format.
- Constrained decoding (grammar sampling) guarantees valid structure.

System / user / assistant roles:
- System prompt: persistent instruction (persona, format, guardrails).
- User: the human turn.
- Assistant: the model's previous response (in multi-turn chat).

Prompt injection risk: untrusted user input embedded in a prompt can
override system instructions. Sanitise and isolate untrusted content.

## 7. RAG & fine-tuning
Two main ways to add domain knowledge to an LLM:

RAG (Retrieval-Augmented Generation):
1. Embed documents into a vector store (pgvector, Pinecone, Weaviate).
2. At query time: embed the question → nearest-neighbour search.
3. Inject retrieved chunks into the prompt as context.
+ No model retraining; knowledge is updated by changing the store.
+ Source citations are natural.
− Quality depends on retrieval quality.

Fine-tuning:
- Continue training on domain-specific (instruction, response) pairs.
- LoRA (Low-Rank Adaptation): inject small trainable rank-decomposition
matrices into attention layers — trains <1% of params; cheap & fast.
+ Bakes knowledge / style into weights; no retrieval latency.
− Requires curated dataset; can forget general knowledge (catastrophic forgetting).

When to use which:
- Dynamic knowledge / long documents → RAG.
- Fixed style / format / domain vocabulary → fine-tuning.
- Both combined is often the best approach for production systems.

## 8. Remember & rehearse
- What does a single neuron compute? What is the role of the activation function?
- Explain backpropagation in one sentence.
- What problem do LSTMs solve compared to vanilla RNNs?
- Describe self-attention: what are Q, K, and V?
- What is the pre-training objective of a GPT-style LLM?
- What is RLHF and why is it used?
- Compare RAG vs fine-tuning — when would you choose each?
- What is prompt injection and how do you mitigate it?
