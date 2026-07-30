---
label: "II"
subtitle: "Install & setup"
group: "Ollama"
order: 2
---
Install & setup

## 1. Install

### Linux (script — recommended)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Installs the `ollama` binary and a **systemd** service (starts on boot on most distros).

### macOS

Download from [ollama.com/download](https://ollama.com/download) or:

```bash
brew install ollama
```

Uses **Metal** on Apple Silicon automatically.

### Windows

Installer from [ollama.com/download](https://ollama.com/download). Uses **CUDA** when an NVIDIA GPU and driver are present.

## 2. Verify

```bash
ollama --version
ollama list          # empty until first pull
```

Start the server (often auto-started after install):

```bash
ollama serve         # foreground — optional if service already running
```

Check the API:

```bash
curl http://localhost:11434/api/tags
```

## 3. GPU prerequisites (NVIDIA Linux)

```bash
nvidia-smi
```

| Check | Expected |
|-------|----------|
| Driver | 535+ (550+ recommended) |
| GPU listed | Your card (e.g. RTX 1080) |
| No errors | Fix driver before blaming Ollama |

Ollama bundles its own CUDA runtime — you do **not** need a separate CUDA toolkit install for basic use.

## 4. Where files live

| Path | Contents |
|------|----------|
| `~/.ollama/models/` | Downloaded model blobs (large) |
| `~/.ollama/` | Config and state |
| **Service** | `systemctl status ollama` (Linux) |

Free disk before large pulls — a 7B model is roughly **4–8 GB** on disk depending on quant.

## 5. Service management (Linux)

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

Logs:

```bash
journalctl -u ollama -f
```

## Next

[Models — pull & manage](iii-models-pull-and-manage.md) — download your first models.
