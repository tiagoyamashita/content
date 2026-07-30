---
label: "VII"
subtitle: "GPU & troubleshooting"
group: "Ollama"
order: 7
---
GPU & troubleshooting

## 1. Confirm GPU is used

```bash
ollama run qwen2.5-coder:7b "hi"
# second terminal:
ollama ps
watch -n1 nvidia-smi
```

| `ollama ps` shows | Meaning |
|-------------------|---------|
| **100% GPU** | Good — model on card |
| **100% CPU** | GPU not used — see fixes below |
| **Mixed %** | Partial offload — normal for tight VRAM |

## 2. CPU-only when GPU expected

| Check | Fix |
|-------|-----|
| `nvidia-smi` fails | Install/fix NVIDIA driver; reboot |
| Model too large | Smaller tag (`3b` not `32b`) |
| Driver too old | Update to 535+ / 550+ |
| Wrong Ollama build | Reinstall from [ollama.com](https://ollama.com/download) |
| Force CPU test | `OLLAMA_NUM_GPU=0` — remove for normal use |

Linux: ensure user can access GPU (`nvidia-smi` as same user running Ollama).

## 3. Out of memory (OOM)

| Symptom | Fix |
|---------|-----|
| CUDA OOM / crash on load | Smaller model; `qwen2.5-coder:3b` |
| OOM during long chat | Lower `num_ctx` (`/set num_ctx 2048`) |
| Multiple models loaded | `ollama ps` — wait for idle unload or restart service |
| Disk full on pull | `ollama rm` old models; `df -h ~/.ollama` |

VRAM guide: [Model RAM requirements](../implementation-example/iv-model-ram-requirements.md). RTX 1080 specifics: [Install & run on RTX 1080](../implementation-example/vi-install-and-run-rtx-1080.md).

## 4. Slow generation

| Cause | Guidance |
|-------|----------|
| **7B on older GPU** | ~20–35 tok/s is normal for RTX 1080 |
| **CPU inference** | Much slower — fix GPU first |
| **Cold start** | First token after idle load is slower |
| **Context too long** | KV cache cost — shorten `num_ctx` |

## 5. Connection errors (API / Cursor)

| Error | Fix |
|-------|-----|
| `connection refused` | `ollama serve` or `systemctl start ollama` |
| Wrong model name | `ollama list` — use exact tag |
| Cursor cannot reach API | Base URL must be `http://localhost:11434/v1` |
| Remote machine | SSH tunnel or set `OLLAMA_HOST` (trusted network only) |

## 6. Pull / download failures

| Problem | Fix |
|---------|-----|
| Interrupted download | Re-run `ollama pull` — resumes |
| No disk space | Remove models with `ollama rm` |
| Proxy / firewall | Configure system proxy; check corporate SSL inspection |

## 7. Reset

```bash
sudo systemctl stop ollama
# optional: backup then clear models
# rm -rf ~/.ollama/models/*
sudo systemctl start ollama
ollama pull qwen2.5-coder:7b
```

Use reset only when cache is corrupted — re-downloads all models.

## Related

- [Install & setup](ii-install-and-setup.md)
- [API & IDE integration](v-api-and-ide-integration.md)
- [Implementation examples](../implementation-example/i-overview.md)
