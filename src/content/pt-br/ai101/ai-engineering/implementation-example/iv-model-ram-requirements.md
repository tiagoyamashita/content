---
label: "IV"
subtitle: "Model RAM requirements"
group: "AI Applied"
order: 4
---
Model RAM requirements

Local inference needs RAM (and VRAM on GPU) for **weights** plus **KV cache** for the context window. Undersizing causes OOM kills, swapping, or refusal to load.

## 1. Quick rules

| Component | What it is | Rough sizing |
|-----------|------------|--------------|
| **Weights** | Frozen parameters on disk / in memory | Depends on parameter count × bytes per weight |
| **KV cache** | Attention state for prompt + generation | Grows with **context length** and batch size |
| **Overhead** | Runtime, tokenizer, graph | Often **1–3 GB** extra on GPU; less on pure CPU GGUF |

**Parameters → weight memory (unquantized):**

```text
GB ≈ (parameters in billions) × (bytes per parameter) × 1.07
```

| Precision | Bytes/param | 7B model | 13B | 70B |
|-----------|-------------|----------|-----|-----|
| FP16 | 2 | ~14 GB | ~26 GB | ~140 GB |
| INT8 | 1 | ~7 GB | ~13 GB | ~70 GB |
| INT4 | 0.5 | ~3.5 GB | ~6.5 GB | ~35 GB |

The **1.07** factor accounts for small overhead; real GGUF quants vary by scheme (Q4_K_M vs Q8_0).

## 2. GGUF quant cheat sheet (7B-class model)

Approximate **weight-only** RAM for a ~7B model:

| Quant | ~Weight RAM | Quality | Typical use |
|-------|-------------|---------|-------------|
| Q8_0 | ~7.5 GB | Near FP16 | 16 GB machines, quality-sensitive |
| Q6_K | ~6 GB | Excellent | Sweet spot on 16 GB |
| **Q4_K_M** | **~4.5 GB** | Good default | **8–16 GB** laptops |
| Q3_K_M | ~3.5 GB | Noticeable loss | Tight RAM only |
| Q2_K | ~2.5 GB | Degraded | Experimentation only |

Scale linearly by parameter count: a **3B** Q4_K_M is ~**2 GB** weights; **13B** Q4_K_M is ~**8 GB**.

## 3. Context length adds RAM

KV cache dominates at long contexts:

```text
KV cache grows with: layers × hidden_dim × context_tokens × 2 (K+V) × dtype
```

| Practical takeaway | Guidance |
|--------------------|----------|
| Default 4k context | Usually fine on top of weight table |
| 8k–32k context | Add **2–8+ GB** depending on model size |
| 128k context | Often needs **dedicated GPU** or aggressive offload |

If the app lets you set **context length**, lower it when you hit OOM before downsizing the model.

## 4. Model size → minimum practical RAM

Assumes **Q4_K_M**, **4k context**, small overhead. Add **4 GB** for OS + browser if this is your daily driver laptop.

| Model (params) | Weight RAM (Q4_K_M) | **System RAM minimum** | Comfortable |
|----------------|---------------------|------------------------|-------------|
| 1–3B | 1–2 GB | **8 GB** | 16 GB |
| 7–8B | 4–5 GB | **8 GB** (tight) | **16 GB** |
| 13–14B | 8–9 GB | **16 GB** | **32 GB** |
| 32B | ~18 GB | **32 GB** | **48–64 GB** |
| 70B | ~35 GB | **64 GB** + GPU or heavy offload | **96 GB+** |

**GPU VRAM:** weights + KV usually must fit on card for full-speed GPU inference. A **12 GB** card runs **7B Q4** comfortably; **24 GB** handles **13B Q4** or **7B** at long context.

## 5. CPU vs GPU memory

| Mode | Behavior |
|------|----------|
| **Full GPU** | Weights + KV on VRAM; fastest |
| **Partial offload** (llama.cpp `-ngl`) | Some layers on GPU, rest in RAM — flexible but slower |
| **CPU only** | All in system RAM — works with GGUF; expect low tokens/sec |
| **airLLM-style layer streaming** | Layers pulled to GPU in waves — fits huge models on small VRAM (see [CPU & lightweight runners](v-cpu-and-lightweight-runners.md)) |

## 6. Example picks by machine

| Your hardware | Reasonable starting models |
|---------------|----------------------------|
| 8 GB RAM, no GPU | 1–3B Q4 (`qwen2.5-coder:1.5b`, Llama 3.2 1B/3B) |
| 16 GB RAM, no GPU | 7B Q4_K_M (`qwen2.5-coder:7b`) |
| **8 GB VRAM (RTX 1080)** | **`qwen2.5-coder:7b`** — best open coder for the tier |
| 16 GB RAM + 8 GB VRAM | 7B Q4/Q8 on GPU (`qwen2.5-coder:7b`); or 13B partial offload |
| 32 GB RAM + 24 GB VRAM | `qwen2.5-coder:32b` full GPU; or 13B Q4 with headroom |
| 64 GB+ RAM | 32B–70B with mix of CPU/GPU offload |

### Qwen2.5-Coder family (weight RAM at Q4_K_M)

| Model | ~Weight RAM | Min VRAM (4k ctx) | Notes |
|-------|-------------|-------------------|-------|
| 0.5B / 1.5B | under 1 GB | 4 GB | Toy / autocomplete |
| 3B | ~2 GB | 6 GB | Fast coding on old GPUs |
| **7B** | **~4.5 GB** | **8 GB** | **Sweet spot for RTX 1080** |
| 14B | ~8.5 GB | 12 GB | Needs 12 GB+ card or offload |
| 32B | ~18 GB | 24 GB | Top open coder; matches GPT-4o class on many code benches |

## 7. Check before you commit

1. Note **parameter count** and **quant** on the HF or Ollama model card.
2. Add weight estimate from tables above.
3. Add **2–4 GB** KV + overhead for your target context.
4. Leave **20% headroom** — OS and desktop apps need RAM too.

## Next

[CPU & lightweight runners](v-cpu-and-lightweight-runners.md) — when you cannot fit weights fully on GPU.
