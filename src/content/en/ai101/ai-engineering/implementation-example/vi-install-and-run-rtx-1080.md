---
label: "VI"
subtitle: "Install & run on RTX 1080"
group: "AI Applied"
order: 6
---
Install & run on RTX 1080

Step-by-step setup for each major local runtime on an **NVIDIA GeForce RTX 1080** (8 GB VRAM, Pascal / compute **6.1**). Assumes **Linux** (Ubuntu, Debian, Kali, etc.); Windows notes where the flow differs.

See [Model RAM requirements](iv-model-ram-requirements.md) for sizing theory. On 8 GB VRAM, start with **3B–7B** models at **Q4_K_M** or Ollama’s default quant.

## 0. RTX 1080 constraints

| Spec | Implication |
|------|-------------|
| **8 GB VRAM** | Comfortable: **3B–7B** Q4 on GPU. **8B** Q4 fits with modest context. **13B+** needs CPU offload or airLLM |
| **Pascal (sm_61)** | Works with CUDA builds of Ollama, llama.cpp, KoboldCPP. **vLLM / TGI / TensorRT-LLM** target newer GPUs — often painful or unsupported |
| **System RAM** | Aim for **16 GB+** so CPU offload and OS do not swap |

### Shared prerequisites (all GPU paths)

```bash
# 1. NVIDIA driver (reboot after install)
nvidia-smi
# Should show RTX 1080 and driver 535+ (550+ recommended)

# 2. Optional but useful: CUDA toolkit for building llama.cpp
# Ubuntu/Debian example — match your distro
sudo apt update
sudo apt install -y build-essential cmake git
```

If `nvidia-smi` fails, fix the driver before any runtime below.

### Recommended models for 8 GB VRAM

| Model | Format | Fits fully on GPU? |
|-------|--------|-------------------|
| `llama3.2:3b` (Ollama) | Ollama bundle | Yes — fastest start |
| `mistral:7b` / `llama3.1:8b` | Ollama / Q4 GGUF | Yes at Q4, 4k context |
| `qwen2.5:7b` | Ollama / Q4 GGUF | Yes at Q4 |
| `llama3.1:8b` + long context | Q4 GGUF | Tight — lower `-c` or offload layers |
| `codellama:7b` | Ollama | Yes — coding tasks |

---

## 1. Ollama (easiest — start here)

### Install

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Windows/macOS: download from [ollama.com/download](https://ollama.com/download).

### Verify GPU

```bash
ollama run llama3.2:3b "Say hello in one sentence."
# In another terminal while generating:
ollama ps
```

`ollama ps` should show **GPU** in the processor column. If it says CPU only, check `nvidia-smi` and driver.

### Pull and run models

```bash
# Small + fast on 1080
ollama pull llama3.2:3b
ollama run llama3.2:3b

# General chat / code (7–8B — good default on 8 GB)
ollama pull qwen2.5:7b
ollama run qwen2.5:7b

# Alternative 7B
ollama pull mistral:7b
ollama run mistral:7b
```

### OpenAI-compatible API (Cursor, Continue, etc.)

```bash
# Server starts automatically on first request; or:
ollama serve
```

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:7b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

| Cursor / IDE setting | Value |
|----------------------|-------|
| Base URL | `http://localhost:11434/v1` |
| Model | `qwen2.5:7b` (or whatever you pulled) |
| API key | any placeholder (e.g. `ollama`) |

### Run a custom GGUF

```bash
# After hf download (see Hugging Face note)
cat > Modelfile <<'EOF'
FROM ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf
PARAMETER temperature 0.7
EOF
ollama create my-local -f Modelfile
ollama run my-local
```

---

## 2. llama.cpp (CUDA build — max control)

### Install (build with CUDA)

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j "$(nproc)"
```

Binaries land in `build/bin/` — e.g. `llama-cli`, `llama-server`.

If CMake cannot find CUDA, set:

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### Download a GGUF

```bash
pip install -U "huggingface_hub[cli]"
hf download bartowski/Llama-3.2-3B-Instruct-GGUF \
  Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

### Run interactively

```bash
./build/bin/llama-cli \
  -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  -ngl 99 \
  -c 4096 \
  -p "You are a helpful assistant." \
  --interactive
```

| Flag | RTX 1080 guidance |
|------|-------------------|
| `-ngl 99` | Offload **all** layers to GPU (use for 3B–7B Q4) |
| `-ngl 35` | Partial offload if 8B+ OOM — rest on CPU |
| `-c 4096` | Context tokens — drop to **2048** if OOM |
| `-ngl 0` | Force CPU (debug only) |

### HTTP server

```bash
./build/bin/llama-server \
  -m ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  -ngl 99 \
  -c 4096 \
  --host 127.0.0.1 \
  --port 8080
```

API: `http://localhost:8080` — OpenAI-style endpoints per [llama.cpp server docs](https://github.com/ggerganov/llama.cpp/blob/master/tools/server/README.md).

---

## 3. LM Studio (GUI — Linux or Windows)

### Install

1. Download from [lmstudio.ai](https://lmstudio.ai) (`.AppImage` on Linux, installer on Windows).
2. Run the app; open **Discover** → search model → pick a **4-bit / Q4** **3B–7B** variant.
3. **My Models** → load model → **GPU** offload slider to **max** (all layers).

### Run

- **Chat** tab for interactive use.
- **Developer** → **Local Server** → start server on `http://localhost:1234/v1`.

| RTX 1080 tip | Action |
|--------------|--------|
| OOM on load | Smaller model or lower context in model settings |
| Slow first token | Normal on 1080 for 7B — expect ~15–40 tok/s for 7B Q4 |

No headless Linux server workflow — use Ollama or llama-server for SSH boxes.

---

## 4. KoboldCPP (portable binary + web UI)

### Install

```bash
# CUDA-enabled release from GitHub (pick latest cu12.x asset for Linux)
wget https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp-linux-x64-cuda12
chmod +x koboldcpp-linux-x64-cuda12
mv koboldcpp-linux-x64-cuda12 koboldcpp
```

Windows: grab `koboldcpp.exe` CUDA build from the same releases page.

### Run

```bash
./koboldcpp --model ./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --gpulayers 99 \
  --contextsize 4096 \
  --port 5001
```

Open `http://localhost:5001` in a browser. Lower `--gpulayers` if you hit OOM on 8B models.

---

## 5. GPT4All (desktop, optional CUDA)

### Install

Download from [gpt4all.io](https://gpt4all.io) — Linux `.deb` / AppImage or Windows installer.

### Run

1. **Add Model** → choose a **3B–7B** chat model (avoid 13B+ on 1080).
2. Settings → enable **GPU acceleration** (Vulkan/CUDA depending on build).
3. **Local API** in settings if you need HTTP.

Best for casual offline chat; developers usually prefer Ollama for API ergonomics.

---

## 6. airLLM (large HF models on 8 GB VRAM)

Layer-streaming — fits **13B+** slowly when full GPU load does not fit.

### Install

```bash
python3 -m venv ~/airllm-venv
source ~/airllm-venv/bin/activate
pip install -U pip airllm torch --index-url https://download.pytorch.org/whl/cu121
huggingface-cli login
```

### Run (Python)

```python
from airllm import AutoModel

model = AutoModel.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct",
    compression="4bit",  # or None if RAM allows
)
input_tokens = model.tokenizer(
    ["What is the capital of France?"],
    return_tensors="pt",
    return_attention_mask=False,
)
generation = model.generate(input_tokens["input_ids"].cuda(), max_new_tokens=50)
print(model.tokenizer.decode(generation[0]))
```

Use for **experiments**, not low-latency chat. First run downloads weights from Hugging Face.

---

## 7. vLLM — not recommended on RTX 1080

[vLLM](https://github.com/vllm-project/vllm) targets **datacenter GPUs** (Ampere **sm_80+**). Pascal **sm_61** is often **unsupported** or requires building from source with reduced features — poor ROI on a 1080.

If you still want to try (Linux only):

```bash
python3 -m venv ~/vllm-venv
source ~/vllm-venv/bin/activate
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.2-3B-Instruct \
  --dtype half \
  --max-model-len 2048
```

Expect build failures or runtime errors on Pascal. **Use Ollama or llama.cpp instead** on this card.

---

## 8. TGI & TensorRT-LLM — skip on 1080

| Platform | RTX 1080 verdict |
|----------|------------------|
| **[TGI](https://github.com/huggingface/text-generation-inference)** | Docker + NVIDIA stack; official images assume newer GPUs. Possible with old CUDA images but unsupported for daily use |
| **[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)** | Optimized for **Tensor Core** GPUs (Turing+). Pascal lacks Tensor Cores — not worth installing |

For production APIs on modern hardware, revisit these on a **RTX 3060 12GB+** or cloud GPU.

---

## 9. MLX — not applicable

[MLX](https://github.com/ml-explore/mlx) is **Apple Silicon only**. Skip on an RTX 1080 PC.

---

## 10. Quick pick for RTX 1080

| Goal | Install | Run |
|------|---------|-----|
| **Fastest path** | Ollama one-liner | `ollama pull llama3.2:3b && ollama run llama3.2:3b` |
| **Best 7B daily driver** | Ollama | `ollama pull qwen2.5:7b && ollama run qwen2.5:7b` |
| **IDE API** | Ollama | `http://localhost:11434/v1` + model name |
| **Fine-grained GPU/control** | llama.cpp CUDA build | `llama-server -ngl 99 -m …Q4_K_M.gguf` |
| **Web UI, no terminal** | LM Studio or KoboldCPP | GUI or `http://localhost:5001` |
| **13B+ experiment** | airLLM | Python layer streaming |

## 11. Troubleshooting

| Symptom | Fix |
|---------|-----|
| **CUDA OOM** | Smaller model (3B), Q4 quant, lower `-c` / context, reduce `--gpulayers` |
| **Runs on CPU only** | `nvidia-smi`; reinstall driver; rebuild llama.cpp with `-DGGML_CUDA=ON` |
| **Slow generation** | Normal for 7B on 1080 (~20–35 tok/s Q4); use 3B for speed |
| **Model not found** | `ollama pull <name>` or verify GGUF path |
| **Gated HF model** | `huggingface-cli login` + accept license |

Monitor VRAM during a run:

```bash
watch -n1 nvidia-smi
```

## Related

- [Downloading from Hugging Face](ii-downloading-from-huggingface.md)
- [Local run platforms](iii-local-run-platforms.md)
- [Model RAM requirements](iv-model-ram-requirements.md)
- [CPU & lightweight runners](v-cpu-and-lightweight-runners.md)
