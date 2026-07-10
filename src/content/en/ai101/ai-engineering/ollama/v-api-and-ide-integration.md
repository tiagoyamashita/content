---
label: "V"
subtitle: "API & IDE integration"
group: "Ollama"
order: 5
---
API & IDE integration

Ollama exposes an **OpenAI-compatible** HTTP API so IDEs and tools work with a local model instead of a cloud API.

## 1. Base URL and auth

| Setting | Value |
|---------|-------|
| **Base URL** | `http://localhost:11434/v1` |
| **API key** | Any placeholder (e.g. `ollama`) — not enforced locally |
| **Model name** | Exact tag: `qwen2.5-coder:7b` |

Server starts on first request, or run explicitly:

```bash
ollama serve
```

## 2. Test with curl

**Chat completions:**

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:7b",
    "messages": [
      {"role": "user", "content": "Hello"}
    ]
  }'
```

**Streaming:**

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:7b",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
```

**Embeddings:**

```bash
curl http://localhost:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": "Hello world"
  }'
```

## 3. Cursor

1. Pull model: `ollama pull qwen2.5-coder:7b`
2. Cursor Settings → **Models** → add **OpenAI-compatible** provider (wording varies by version):
   - Base URL: `http://localhost:11434/v1`
   - API key: `ollama`
   - Model: `qwen2.5-coder:7b`
3. Select that model in chat or agent mode.

Ollama must be running on the **same machine** as Cursor (or use SSH tunnel for remote).

## 4. Continue (VS Code / JetBrains)

In `config.json`:

```json
{
  "models": [
    {
      "title": "Qwen Coder 7B",
      "provider": "ollama",
      "model": "qwen2.5-coder:7b"
    }
  ]
}
```

Continue detects local Ollama when the extension is installed and `ollama` is on PATH.

## 5. Environment variables

| Variable | Effect |
|----------|--------|
| `OLLAMA_HOST` | Bind address (default `127.0.0.1:11434`) |
| `OLLAMA_KEEP_ALIVE` | How long models stay loaded (e.g. `30m`, `0` = unload immediately) |
| `OLLAMA_NUM_GPU` | Force GPU layer count; `0` = CPU only |
| `OLLAMA_MODELS` | Custom models directory |

Example — listen on LAN (use only on trusted networks):

```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

## 6. Security

| Risk | Mitigation |
|------|------------|
| Open port on LAN/internet | Keep `127.0.0.1` unless you intend remote access |
| No API auth | Do not expose `:11434` to the public internet |
| Sensitive prompts | Local only — data stays on machine; still log-aware |

## Next

[Modelfile & custom GGUF](vi-modelfile-and-custom-gguf.md) — import models not in the library.
