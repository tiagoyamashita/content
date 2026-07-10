---
label: "I"
subtitle: "Overview"
group: "Ollama"
order: 1
---
Ollama — overview

**[Ollama](https://ollama.com)** runs open LLMs locally — one install, `ollama pull`, chat in the terminal or via an OpenAI-compatible API. Best first choice for **local coding with Cursor**, **offline chat**, and **quick experiments** without Hugging Face gating or manual GGUF paths.

For comparing Ollama vs llama.cpp / vLLM, see [Local run platforms](../implementation-example/iii-local-run-platforms.md). For RAM/VRAM sizing, see [Model RAM requirements](../implementation-example/iv-model-ram-requirements.md).

## Map of this submenu

| Note | Focus |
|------|--------|
| [Install & setup](ii-install-and-setup.md) | Linux, macOS, Windows; verify install |
| [Models — pull & manage](iii-models-pull-and-manage.md) | `pull`, `list`, `rm`, tags, embeddings |
| [Run, chat & parameters](iv-run-chat-and-parameters.md) | `ollama run`, `/set`, context, system prompt |
| [API & IDE integration](v-api-and-ide-integration.md) | `/v1` API, Cursor, Continue, env vars |
| [Modelfile & custom GGUF](vi-modelfile-and-custom-gguf.md) | Import HF weights, `ollama create` |
| [GPU & troubleshooting](vii-gpu-troubleshooting.md) | `ollama ps`, CPU-only fixes, OOM |

## Mental model

```text
ollama pull <model>   →  weights cached on disk (~/.ollama)
ollama run <model>    →  load into RAM/VRAM → chat (CLI)
ollama serve          →  HTTP API on :11434 (OpenAI-compatible /v1)
```

| Piece | You control | Ollama handles |
|-------|-------------|----------------|
| **Which model** | `ollama pull qwen2.5-coder:7b` | Download, default quant |
| **GPU vs CPU** | Model size; env vars | llama.cpp backend, offload |
| **IDE access** | Point Cursor at `localhost:11434/v1` | Serves chat completions |
| **Custom model** | `Modelfile` + `ollama create` | Bundles GGUF + params |

## Recommended models (2025–2026)

| Use case | Model tag | VRAM (approx) |
|----------|-----------|---------------|
| **Local coding** | `qwen2.5-coder:7b` | ~5 GB |
| General chat 7B | `qwen2.5:7b` | ~5 GB |
| Fast / small GPU | `qwen2.5-coder:3b`, `llama3.2:3b` | ~2–3 GB |
| Embeddings (RAG) | `nomic-embed-text` | Small |
| Best open coder (24 GB+) | `qwen2.5-coder:32b` | ~20 GB |

8 GB GPU (e.g. RTX 1080): start with **`qwen2.5-coder:7b`**. Details: [Install & run on RTX 1080](../implementation-example/vi-install-and-run-rtx-1080.md).

## Study order

[Install & setup](ii-install-and-setup.md) → [Models — pull & manage](iii-models-pull-and-manage.md) → [Run, chat & parameters](iv-run-chat-and-parameters.md) → [API & IDE integration](v-api-and-ide-integration.md) → [Modelfile & custom GGUF](vi-modelfile-and-custom-gguf.md) → [GPU & troubleshooting](vii-gpu-troubleshooting.md)

## Start here (5 minutes)

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

Type a message; `/bye` to exit. Next: wire into Cursor — [API & IDE integration](v-api-and-ide-integration.md).

## Related

- [TurboVec + Ollama + local files](../implementation-example/vii-turbovec-ollama-local-files.md) — RAG over your documents
- [Downloading from Hugging Face](../implementation-example/ii-downloading-from-huggingface.md) — when you need weights Ollama does not catalog
