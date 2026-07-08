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
# Hugging Face CLI — installs the `hf` command (current)
pip install -U "huggingface_hub[cli]"

# Optional: Git LFS for clone-based workflows
git lfs install
```

Log in if the model is **gated** (license acceptance required):

```bash
hf auth login
```

`huggingface-cli` is **deprecated** — use `hf` for all CLI tasks (`hf download`, `hf auth login`, `hf --help`).

Create a token at [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) with **read** access.

### Gated models (Meta Llama, etc.) — required before download

`meta-llama/Llama-3.2-3B-Instruct` is **gated**. Unauthenticated downloads fail with:

```text
Error: Access denied. This repository requires approval.
Warning: You are sending unauthenticated requests to the HF Hub.
```

**Fix — do all three steps in order:**

| Step | Action |
|------|--------|
| **1. Web approval** | Open [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) while logged in → **Agree and access repository** (Meta license form). Approval is usually instant. |
| **2. CLI login** | `hf auth login` → paste a **read** token from [settings/tokens](https://huggingface.co/settings/tokens) |
| **3. Retry** | Same `hf download` command |

Verify auth before downloading:

```bash
hf auth whoami
# Should print your HF username — confirms login only, NOT gated-repo access
```

**`hf auth whoami` succeeding does not mean you can download Llama.** For gated repos you must also complete **step 1 (web approval)** on the model page while logged in as the **same HF user** as the CLI. If download still says `requires approval`, open the repo URL in a browser and look for **Agree and access repository** — until that button is gone and you see the Files tab, CLI downloads will fail.

**Alternative token env var** (scripts, CI, or if login cache fails):

```bash
export HF_TOKEN="hf_xxxxxxxx"   # your read token — never commit this
hf download meta-llama/Llama-3.2-3B-Instruct --local-dir ./models/llama-3.2-3b
```

**Skip gating for local GGUF** — community quant repos are usually open; fine for Ollama / llama.cpp:

```bash
hf download bartowski/Llama-3.2-3B-Instruct-GGUF \
  Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

Or use **Ollama** (no HF account for the default catalog): `ollama pull llama3.2:3b`.

### Recommended open models (2025–2026)

| Use case | Model | Gated? | Ollama | Hugging Face |
|----------|-------|--------|--------|--------------|
| **Local coding (default)** | **Qwen2.5-Coder 7B Instruct** | No | `qwen2.5-coder:7b` | [Qwen/Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) |
| General chat 7B | Qwen2.5 7B Instruct | No | `qwen2.5:7b` | `Qwen/Qwen2.5-7B-Instruct` |
| Fast / small GPU | Qwen2.5-Coder 3B | No | `qwen2.5-coder:3b` | `Qwen/Qwen2.5-Coder-3B-Instruct` |
| Best open coder (24 GB+ VRAM) | Qwen2.5-Coder 32B Instruct | No | `qwen2.5-coder:32b` | `Qwen/Qwen2.5-Coder-32B-Instruct` |
| General chat (gated) | Llama 3.2 3B Instruct | **Yes** (Meta) | `llama3.2:3b` | `meta-llama/Llama-3.2-3B-Instruct` |

**Qwen2.5-Coder** is the usual pick for **code generation, fixes, and IDE assistants** — Apache 2.0, no HF approval step, strong benchmarks vs other open coders. Use the **`-Instruct`** variant for chat/coding; base weights are for fine-tuning only.

**Download Qwen2.5-Coder (no gating):**

```bash
# Full safetensors (transformers / vLLM)
hf download Qwen/Qwen2.5-Coder-7B-Instruct --local-dir ./models/qwen2.5-coder-7b

# Single GGUF file (llama.cpp / Ollama import)
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

Or skip HF: `ollama pull qwen2.5-coder:7b`.

## 3. Method A — `hf download` (preferred)

Download an entire repo or specific files into a local folder:

```bash
# Qwen2.5-Coder — open, best default for coding (7B fits 8 GB GPU)
hf download Qwen/Qwen2.5-Coder-7B-Instruct --local-dir ./models/qwen2.5-coder-7b

# Single GGUF file (saves bandwidth)
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models

# Gated example — Meta Llama (requires web approval first)
hf download meta-llama/Llama-3.2-3B-Instruct --local-dir ./models/llama-3.2-3b
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
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    local_dir="./models/qwen2.5-coder-7b",
    local_dir_use_symlinks=False,
)
```

`transformers` can also fetch on first use:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
```

Weights land in the HF cache (`~/.cache/huggingface/hub`) unless you pass `cache_dir` or `local_dir`.

## 6. Picking the right repo variant

| You want | Look for |
|----------|----------|
| **Coding / IDE assistant** | **Qwen2.5-Coder** `*-Instruct` or `qwen2.5-coder:7b` on Ollama |
| **llama.cpp / KoboldCPP** | `*-GGUF` repos or `.gguf` in Files tab |
| **Ollama** | Often `ollama pull <name>` — Ollama downloads for you; or import a GGUF |
| **vLLM / TGI / transformers** | Original safetensors repo or AWQ/GPTQ quant |
| **Smaller disk footprint** | Q4_K_M, Q5_K_M GGUF or AWQ 4-bit |

Always read the **license** on the model card. Many weights forbid commercial use or require registration.

## 7. Verify the download

```bash
# Check total size vs repo "Files and versions" tab
du -sh ./models/qwen2.5-coder-7b

# List safetensors shards
ls -lh ./models/qwen2.5-coder-7b/*.safetensors
```

If a shard is tiny (few KB), Git LFS may not have pulled — run `git lfs pull` or re-run `hf download`.

## 8. Common issues

| Problem | Fix |
|---------|-----|
| **Access denied / requires approval** | Gated repo — complete [web approval](#gated-models-meta-llama-etc--required-before-download), then `hf auth login`; confirm with `hf auth whoami` |
| **Unauthenticated requests warning** | Same — you are not logged in; set `HF_TOKEN` or run `hf auth login` |
| **403 / gated repo** | Accept license on HF website **first** (logged in), then `hf auth login` |
| **Out of disk** | Download one GGUF quant instead of full safetensors |
| **Slow first pull** | Use `hf download` with a wired connection; pin one quant |
| **Wrong format for runtime** | GGUF → llama.cpp/Ollama; safetensors → transformers/vLLM |

## Next

[Local run platforms](iii-local-run-platforms.md) — where to load these files and serve inference.
