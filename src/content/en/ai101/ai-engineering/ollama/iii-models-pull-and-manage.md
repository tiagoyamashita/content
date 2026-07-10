---
label: "III"
subtitle: "Models — pull & manage"
group: "Ollama"
order: 3
---
Models — pull & manage

Models are referenced by **tags** (`model:variant`). Ollama downloads weights on first `pull` and caches them locally.

## 1. Pull models

```bash
# Coding (recommended default)
ollama pull qwen2.5-coder:7b

# General chat
ollama pull qwen2.5:7b
ollama pull llama3.2:3b

# Embeddings (for RAG with Ollama)
ollama pull nomic-embed-text
```

Progress shows download size. Resume is automatic if interrupted.

## 2. List and inspect

```bash
ollama list
ollama show qwen2.5-coder:7b
ollama show qwen2.5-coder:7b --modelfile
```

`show` prints parameters, template, and license snippet.

## 3. Remove models (free disk)

```bash
ollama rm qwen2.5:7b
ollama rm model-name:tag
```

List first — blobs are not removed until no model references them.

## 4. Tag naming

| Pattern | Meaning |
|---------|---------|
| `llama3.2` | Default variant for that family |
| `llama3.2:3b` | Specific size |
| `qwen2.5-coder:7b` | Family + size |
| `@sha256:…` | Pin exact blob (advanced) |

Browse catalog: [ollama.com/library](https://ollama.com/library)

## 5. Model picks by hardware

| VRAM | Suggested tags |
|------|----------------|
| **8 GB** | `qwen2.5-coder:7b`, `llama3.2:3b`, `qwen2.5:7b` |
| **16 GB** | above + `qwen2.5-coder:14b` (may be tight) |
| **24 GB+** | `qwen2.5-coder:32b`, `llama3.1:70b` (quantized) |
| **CPU only** | `llama3.2:1b`, `qwen2.5-coder:3b` |

See [Model RAM requirements](../implementation-example/iv-model-ram-requirements.md) for theory.

## 6. Embedding models

For local RAG (with LlamaIndex, etc.):

```bash
ollama pull nomic-embed-text
ollama pull mxbai-embed-large
```

Use the **same** Ollama base URL for embed and chat in your app. Walkthrough: [TurboVec + Ollama + local files](../implementation-example/vii-turbovec-ollama-local-files.md).

## 7. Hugging Face vs Ollama library

| Source | When |
|--------|------|
| **`ollama pull`** | Model is in Ollama library — fastest |
| **Modelfile + GGUF** | You downloaded a `.gguf` from HF — see [Modelfile & custom GGUF](vi-modelfile-and-custom-gguf.md) |
| **Full HF safetensors** | Use transformers/vLLM, or convert to GGUF first |

Meta Llama gated repos need HF approval; many **Qwen** and **Mistral** models pull from Ollama without HF steps.

## Next

[Run, chat & parameters](iv-run-chat-and-parameters.md) — use models interactively.
