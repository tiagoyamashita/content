---
label: "I"
subtitle: "Overview"
group: "AI Applied"
order: 1
---
Implementation examples — overview
Hands-on notes for **running open models locally** — downloading weights from Hugging Face, picking a runtime, sizing RAM, and using CPU-friendly runners when you do not have a large GPU.

This track is for **practitioners** who want to go beyond hosted chat apps. For how models work conceptually, see [LLMs](../../llms/i-overview.md).

## Map of this submenu

| Note | Focus |
|------|--------|
| [Downloading from Hugging Face](ii-downloading-from-huggingface.md) | CLI, Git LFS, auth, and what you actually get |
| [Local run platforms](iii-local-run-platforms.md) | Ollama, llama.cpp, LM Studio, vLLM, and more — pros and cons |
| [Model RAM requirements](iv-model-ram-requirements.md) | Quantization, context length, and sizing tables |
| [CPU & lightweight runners](v-cpu-and-lightweight-runners.md) | airLLM, llama.cpp CPU, MLX, and trade-offs |
| [Install & run on RTX 1080](vi-install-and-run-rtx-1080.md) | Per-platform install, GPU verify, and model picks for 8 GB VRAM |

## Mental model

```text
Hugging Face repo  →  weights on disk  →  runtime (Ollama / llama.cpp / vLLM / …)  →  API or UI
```

| Step | You decide |
|------|------------|
| **Model** | Size, license, chat vs code, quantization (Q4, Q8, …) |
| **Runtime** | Ease of use vs throughput vs GPU requirement |
| **Hardware** | RAM for weights + KV cache; VRAM if using GPU |

## Study order

[Downloading from Hugging Face](ii-downloading-from-huggingface.md) → [Local run platforms](iii-local-run-platforms.md) → [Model RAM requirements](iv-model-ram-requirements.md) → [CPU & lightweight runners](v-cpu-and-lightweight-runners.md) → [Install & run on RTX 1080](vi-install-and-run-rtx-1080.md)

## When to run locally vs use an API

| Run locally | Use a hosted API |
|-------------|------------------|
| Data must stay on your machine | You want the newest frontier models |
| Predictable cost at high volume | No GPU/RAM to manage |
| Offline or air-gapped | You need minimal setup time |
| Fine-tuned or niche open weights | Compliance allows cloud inference |
