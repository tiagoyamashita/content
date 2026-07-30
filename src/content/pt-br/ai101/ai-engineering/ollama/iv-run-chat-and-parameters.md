---
label: "IV"
subtitle: "Run, chat & parameters"
group: "Ollama"
order: 4
---
Run, chat & parameters

## 1. Interactive chat

```bash
ollama run qwen2.5-coder:7b
```

| Command (in chat) | Action |
|-------------------|--------|
| `/bye`, `/exit` | Quit session |
| `/clear` | Clear context |
| `/set parameter value` | Change runtime param (see below) |
| `/?` | Help |

One-shot without interactive mode:

```bash
ollama run qwen2.5-coder:7b "Write a Python function to merge two dicts"
```

## 2. Common parameters

Set during chat with `/set` or in a **Modelfile** (persistent):

| Parameter | Typical | Effect |
|-----------|---------|--------|
| `temperature` | `0.7` | Randomness (lower = more deterministic) |
| `num_ctx` | `4096` | Context window tokens — raise if you have VRAM |
| `top_p` | `0.9` | Nucleus sampling |
| `repeat_penalty` | `1.1` | Reduce repetition |

Example in session:

```text
/set temperature 0.2
/set num_ctx 8192
```

Coding tasks: try **`temperature 0.1–0.3`**.

## 3. System prompt

In interactive chat, multiline system prompt:

```bash
ollama run qwen2.5-coder:7b
>>> /set system You are a senior Python engineer. Prefer stdlib. Always show types.
```

For permanent system prompts, use a **Modelfile** — [Modelfile & custom GGUF](vi-modelfile-and-custom-gguf.md).

## 4. What is loaded right now

```bash
ollama ps
```

| Column | Meaning |
|--------|---------|
| **MODEL** | Running tag |
| **PROCESSOR** | `100% GPU`, `100% CPU`, or mixed |
| **UNTIL** | Idle unload timer |

If **PROCESSOR** shows CPU only on a GPU machine, see [GPU & troubleshooting](vii-gpu-troubleshooting.md).

## 5. Keep model in memory

Default: Ollama unloads idle models after a few minutes.

```bash
# Keep loaded 30 minutes after last request (example)
OLLAMA_KEEP_ALIVE=30m ollama serve
```

Or per-request via API `keep_alive` field — [API & IDE integration](v-api-and-ide-integration.md).

## 6. Multi-line input

Paste code blocks directly in `ollama run`. End with a blank line or use one-shot mode with heredoc:

```bash
ollama run qwen2.5-coder:7b <<'EOF'
Review this function for bugs:

def divide(a, b):
    return a / b
EOF
```

## Next

[API & IDE integration](v-api-and-ide-integration.md) — Cursor, Continue, curl.
