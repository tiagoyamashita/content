---
label: "V"
subtitle: "CPU & lightweight runners"
group: "AI Applied"
order: 5
---
CPU & lightweight runners

Not every machine has a 24 GB GPU. These runtimes prioritize **low VRAM**, **CPU inference**, or **layer offloading** so you can still run useful open models on a laptop or small cloud instance.

## 1. Runner comparison

| Runner | Idea | GPU needed? | Best when |
|--------|------|-------------|-----------|
| **[llama.cpp](https://github.com/ggerganov/llama.cpp)** | Optimized GGUF inference; partial `-ngl` offload | Optional | Default for CPU + GGUF; huge community |
| **[Ollama](https://ollama.com)** | Wraps llama.cpp (and others) with easy pulls | Optional | Same as llama.cpp but simpler UX |
| **[airLLM](https://github.com/lyogavin/airllm)** | Stream **one layer at a time** through GPU | Small VRAM OK | 70B-class on **4 GB** VRAM (slow) |
| **[MLX](https://github.com/ml-explore/mlx)** | Apple Metal kernels | Apple Silicon | Best local perf on M1/M2/M3 Macs |
| **[GPT4All](https://gpt4all.io)** | Desktop app + CPU backends | Optional | Non-technical users, offline chat |
| **[KoboldCPP](https://github.com/LostRuins/koboldcpp)** | llama.cpp fork + UI | Optional | Single portable binary |
| **[llamafile](https://github.com/Mozilla-Ocho/llamafile)** | Model + runtime in one file | Optional | Drop-in executable, no install |
| **transformers + `device_map="cpu"`** | Pure PyTorch on CPU | No | Prototyping only — very slow at scale |

## 2. airLLM — big models, tiny VRAM

**airLLM** keeps full weights in **system RAM** and moves **one transformer layer** into GPU memory per forward step.

```text
70B model in RAM  →  layer 0 to GPU → compute → layer 1 to GPU → … → logits
```

| Pros | Cons |
|------|------|
| Run models far larger than VRAM | **Much slower** than full GPU load |
| Works with Hugging Face safetensors | Python + CUDA setup; less polished than Ollama |
| Useful for occasional batch jobs | Poor for low-latency chat |

Typical install:

```bash
pip install airllm
```

```python
from airllm import AutoModel

model = AutoModel.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
# inference API per project README — layer-wise GPU execution
```

Use when you **must** run a specific HF model and only have **4–8 GB VRAM**, not for interactive coding assistants.

## 3. llama.cpp on CPU (no GPU)

Download a **Q4_K_M** GGUF and run:

```bash
./llama-cli -m ./models/model-Q4_K_M.gguf -p "Hello" -n 128 -ngl 0
```

| Flag | Meaning |
|------|---------|
| `-ngl 0` | **No** GPU layers — pure CPU |
| `-ngl 35` | Offload 35 layers to GPU (model-dependent) |
| `-c 4096` | Context size — lower if OOM |

**llama-server** exposes the same stack over HTTP for apps.

| Pros | Cons |
|------|------|
| Runs on almost any x86/ARM machine | Tokens/sec low on CPU (1–20 typical) |
| Quantized RAM footprint | Long prompts feel sluggish |
| Same binary scales from Pi to workstation | No training — inference only |

Pair with [Model RAM requirements](iv-model-ram-requirements.md) — **3B Q4** on **8 GB** RAM is realistic; **7B** on **16 GB** is the comfort zone for CPU.

## 4. Apple Silicon — MLX

On Mac, **MLX** often beats generic CPU paths by using **unified memory** efficiently:

```bash
pip install mlx-lm
mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Hello"
```

| Pros | Cons |
|------|------|
| Strong perf per watt on M-series | macOS / Apple hardware only |
| 4-bit MLX models on HF | Smaller catalog than GGUF |
| Good for local dev with Cursor | Not for Linux server deploy |

## 5. Ollama CPU mode

If no GPU is detected, Ollama still runs — backed by llama.cpp CPU kernels:

```bash
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

Prefer **smaller** tags (`3b`, `1.5b`) for CPU-only. Set `OLLAMA_NUM_GPU=0` to force CPU on hybrid machines when debugging.

## 6. When to use which

| Goal | Pick |
|------|------|
| Daily local **coding** | Ollama + **`qwen2.5-coder:7b`** |
| Daily local chat (general) | Ollama + `qwen2.5:7b` or `llama3.2:3b` |
| Tightest RAM, full control | llama.cpp + Q4_K_M GGUF |
| MacBook dev machine | MLX or Ollama |
| 70B on 8 GB VRAM experiment | airLLM |
| Air-gapped USB stick | llamafile or portable KoboldCPP |
| Production API throughput | **Not** these — use vLLM on GPU ([platforms note](iii-local-run-platforms.md)) |

## 7. Realistic expectations (CPU)

| Model | Rough tokens/sec (modern laptop CPU) |
|-------|--------------------------------------|
| qwen2.5-coder 1.5B Q4 | 20–45 |
| 1–3B Q4 | 15–40 |
| qwen2.5-coder 7B Q4 | 3–12 |
| 13B Q4 | 1–5 |

Numbers vary wildly by AVX support, core count, and power limits. For coding assistance, **`qwen2.5-coder:7b` on GPU** or a **hosted API** usually beats **7B on CPU**.

## Related

- [Downloading from Hugging Face](ii-downloading-from-huggingface.md)
- [Local run platforms](iii-local-run-platforms.md)
- [Model RAM requirements](iv-model-ram-requirements.md)
