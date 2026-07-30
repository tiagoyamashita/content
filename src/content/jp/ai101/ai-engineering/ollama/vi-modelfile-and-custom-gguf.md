---
label: "VI"
subtitle: "Modelfile & custom GGUF"
group: "Ollama"
order: 6
---
Modelfile & custom GGUF

When a model is **not** in the Ollama library — or you want a **custom system prompt and parameters** baked in — use a **Modelfile** and `ollama create`.

## 1. Modelfile basics

```dockerfile
FROM qwen2.5-coder:7b
SYSTEM You are a concise Python tutor. Show types and one test per answer.
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
```

```bash
ollama create python-tutor -f Modelfile
ollama run python-tutor
```

| Instruction | Purpose |
|-------------|---------|
| `FROM` | Base model tag **or** path to `.gguf` |
| `SYSTEM` | Default system prompt |
| `PARAMETER` | Default runtime params |
| `TEMPLATE` | Chat template (advanced — usually inherited from base) |
| `LICENSE` | License text metadata |

## 2. Import a local GGUF (from Hugging Face)

Download GGUF first — see [Downloading from Hugging Face](../implementation-example/ii-downloading-from-huggingface.md):

```bash
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

Modelfile:

```dockerfile
FROM ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf
PARAMETER temperature 0.7
```

```bash
ollama create qwen-coder-local -f Modelfile
ollama run qwen-coder-local
```

Use **absolute or repo-relative** paths to the `.gguf` file in `FROM`.

## 3. Derive from existing model

```bash
ollama show qwen2.5-coder:7b --modelfile > Modelfile
# edit SYSTEM / PARAMETER
ollama create my-qwen-dev -f Modelfile
```

## 4. List custom models

```bash
ollama list
```

Custom names appear alongside library pulls (`python-tutor`, `qwen-coder-local`, etc.).

## 5. Share with team

| Approach | Detail |
|----------|--------|
| **Commit Modelfile** | Team runs `ollama create` after pulling same GGUF |
| **Commit only Modelfile + HF instructions** | Modelfile points to `FROM qwen2.5-coder:7b` — everyone `ollama pull` |
| **Do not commit** multi-GB `.gguf` blobs | Use `hf download` or `ollama pull` in README |

Example repo snippet:

```text
models/
  Modelfile              ← committed
  README.md              ← "run hf download … then ollama create …"
  *.gguf                 ← gitignored
```

## 6. When not to use Modelfile

| Situation | Better path |
|-----------|-------------|
| Model already in library | `ollama pull` only |
| Need max inference control | llama.cpp directly — [Local run platforms](../implementation-example/iii-local-run-platforms.md) |
| Production multi-user serving | vLLM / TGI — not Ollama desktop |

## Next

[GPU & troubleshooting](vii-gpu-troubleshooting.md) — fix CPU-only, OOM, slow generation.
