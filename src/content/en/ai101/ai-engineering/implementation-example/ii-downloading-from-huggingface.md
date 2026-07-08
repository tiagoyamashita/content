---
label: "II"
subtitle: "Downloading from Hugging Face"
group: "AI Applied"
order: 2
---
Downloading from Hugging Face

[Hugging Face](https://huggingface.co) hosts model **weights**, **tokenizers**, and **configs**. A repo page (e.g. `meta-llama/Llama-3.2-3B-Instruct`) is a versioned folder — not a single installer.

## 1. What you are downloading

| Artifact | Purpose |
|----------|---------|
| `config.json` | Architecture, hidden size, layer count |
| `tokenizer.json` / `tokenizer.model` | Text → tokens |
| `*.safetensors` or `*.bin` | Model weights (large) |
| `generation_config.json` | Default decode settings |
| `README.md` | License, prompt format, eval notes |

**GGUF** repos (for llama.cpp / Ollama imports) ship one or more `.gguf` files with quantization already baked in. **Original** repos ship full-precision or HF-quantized safetensors for Python runtimes.

## 2. Prerequisites

```bash
# Hugging Face CLI (recommended)
pip install -U "huggingface_hub[cli]"

# Optional: Git LFS for clone-based workflows
git lfs install
```

Log in if the model is **gated** (license acceptance required):

```bash
huggingface-cli login
# or: hf auth login
```

Create a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) with **read** access. Accept the model license on its repo page before downloading.

## 3. Method A — `hf download` (preferred)

Download an entire repo or specific files into a local folder:

```bash
# Full repo
hf download meta-llama/Llama-3.2-3B-Instruct --local-dir ./models/llama-3.2-3b

# Single GGUF file (saves bandwidth)
hf download bartowski/Llama-3.2-3B-Instruct-GGUF \
  Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

| Flag | Use |
|------|-----|
| `--local-dir` | Mirror repo layout on disk |
| `--local-dir-use-symlinks False` | Real files, not symlinks (portable copies) |
| `--revision` | Pin a branch, tag, or commit |

Resume is automatic — interrupted downloads continue where they left off.

## 4. Method B — Git clone + LFS

```bash
git clone https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
cd Llama-3.2-3B-Instruct
git lfs pull
```

| Pros | Cons |
|------|------|
| Familiar Git workflow | Slower for huge repos; LFS quota on HF |
| Easy to pin commits | Pulls whole repo unless sparse-checkout configured |

For gated models, use HTTPS with a token or SSH key linked to your HF account.

## 5. Method C — Python `snapshot_download`

Useful inside scripts or notebooks:

```python
from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="meta-llama/Llama-3.2-3B-Instruct",
    local_dir="./models/llama-3.2-3b",
    local_dir_use_symlinks=False,
)
```

`transformers` can also fetch on first use:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
```

Weights land in the HF cache (`~/.cache/huggingface/hub`) unless you pass `cache_dir` or `local_dir`.

## 6. Picking the right repo variant

| You want | Look for |
|----------|----------|
| **llama.cpp / KoboldCPP** | `*-GGUF` repos or `.gguf` in Files tab |
| **Ollama** | Often `ollama pull <name>` — Ollama downloads for you; or import a GGUF |
| **vLLM / TGI / transformers** | Original safetensors repo or AWQ/GPTQ quant |
| **Smaller disk footprint** | Q4_K_M, Q5_K_M GGUF or AWQ 4-bit |

Always read the **license** on the model card. Many weights forbid commercial use or require registration.

## 7. Verify the download

```bash
# Check total size vs repo "Files and versions" tab
du -sh ./models/llama-3.2-3b

# List safetensors shards
ls -lh ./models/llama-3.2-3b/*.safetensors
```

If a shard is tiny (few KB), Git LFS may not have pulled — run `git lfs pull` or re-run `hf download`.

## 8. Common issues

| Problem | Fix |
|---------|-----|
| **403 / gated repo** | Accept license on HF; `huggingface-cli login` |
| **Out of disk** | Download one GGUF quant instead of full safetensors |
| **Slow first pull** | Use `hf download` with a wired connection; pin one quant |
| **Wrong format for runtime** | GGUF → llama.cpp/Ollama; safetensors → transformers/vLLM |

## Next

[Local run platforms](iii-local-run-platforms.md) — where to load these files and serve inference.
