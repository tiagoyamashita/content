---
label: "III"
subtitle: "Local run platforms"
group: "AI Applied"
order: 3
---
Local run platforms

After weights are on disk, a **runtime** loads them and exposes chat — CLI, desktop app, or HTTP API. Pick based on hardware, throughput, and how much setup you will tolerate.

## 1. Platform comparison

| Platform | Best for | GPU | CPU | API | Pros | Cons |
|----------|----------|-----|-----|-----|------|------|
| **[Ollama](https://ollama.com)** | Fast local start, dev machines | Yes (CUDA/Metal) | Yes (slow) | OpenAI-compatible `/v1` | One command `ollama pull`; cross-platform; simple UI | Fewer tuning knobs; model catalog curated |
| **[llama.cpp](https://github.com/ggerganov/llama.cpp)** (`llama-server`) | Maximum control, GGUF ecosystem | Yes | **Strong** | HTTP server built-in | Huge quant community; low RAM options; embeddable | CLI-first; you manage models/paths |
| **[LM Studio](https://lmstudio.ai)** | Desktop users, experimentation | Yes | Yes | Local server | GUI for search/download/chat; easy GPU offload slider | Desktop only; less suited to headless servers |
| **[vLLM](https://github.com/vllm-project/vllm)** | Production GPU serving, batching | **Required** (NVIDIA) | No | OpenAI-compatible | High throughput; PagedAttention; multi-GPU | Heavy setup; needs Linux + recent GPU |
| **[TGI](https://github.com/huggingface/text-generation-inference)** (HF) | HF-native GPU deploy | **Required** | No | REST / gRPC | Good HF integration; production features | Opinionated stack; GPU-focused |
| **[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)** | NVIDIA max perf | **Required** (NVIDIA) | No | Custom / Triton | Fastest on supported GPUs | Complex build; NVIDIA-only |
| **[MLX](https://github.com/ml-explore/mlx)** | Apple Silicon Macs | Metal | N/A (Apple GPU) | Python / local | Optimized for M-series; low friction on Mac | Apple hardware only |
| **[GPT4All](https://gpt4all.io)** | Offline desktop, low spec | Optional | **Yes** | Local API | Very approachable; bundles models | Smaller model selection; less hackable |
| **[KoboldCPP](https://github.com/LostRuins/koboldcpp)** | Creative writing, single binary | Yes | Yes | Web UI + API | Portable; story-mode features | Niche UI; smaller community than Ollama |

## 2. Decision shortcuts

```text
"I just want it running tonight"     → Ollama or LM Studio
"I have a MacBook"                   → Ollama, MLX, or LM Studio
"I have a Linux box + NVIDIA GPU"    → vLLM or TGI for APIs; Ollama for simplicity
"CPU only / 16 GB RAM"               → llama.cpp + small Q4 GGUF (see RAM note)
"Ship to production at scale"        → vLLM, TGI, or TensorRT-LLM — not desktop apps
```

## 3. Format compatibility

| Runtime | Typical weight format |
|---------|----------------------|
| Ollama | Ollama bundle (Modelfile) or import GGUF |
| llama.cpp / LM Studio / KoboldCPP | **GGUF** |
| vLLM / TGI / transformers | **safetensors**, AWQ, GPTQ, FP8 |
| MLX | MLX-converted weights (often linked from HF) |

Downloading the wrong format means convert or re-download — see [Downloading from Hugging Face](ii-downloading-from-huggingface.md).

## 4. API shape (integration)

Most local stacks expose an **OpenAI-compatible** HTTP API so existing clients work:

```bash
# Ollama example
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"llama3.2","messages":[{"role":"user","content":"Hello"}]}'
```

| Platform | Default base URL |
|----------|------------------|
| Ollama | `http://localhost:11434/v1` |
| llama-server | `http://localhost:8080` (configurable) |
| LM Studio | `http://localhost:1234/v1` |
| vLLM | `http://localhost:8000/v1` |

Point Cursor, Continue, or your app at that URL with a dummy API key if the server does not enforce auth.

## 5. Security on local servers

| Risk | Mitigation |
|------|------------|
| Open port on LAN | Bind to `127.0.0.1` only unless you intend remote access |
| No authentication | Do not expose `:11434` or `:8080` to the internet raw |
| Model license | Local run does not bypass HF or Meta license terms |

## Next

[Model RAM requirements](iv-model-ram-requirements.md) — size models to your machine before picking quant and context length.
