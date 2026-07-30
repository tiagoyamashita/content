---
label: "VI"
subtitle: "Instale e execute em RTX 1080"
group: "AI Applied"
order: 6
---
Instale e execute em RTX 1080

Configuração passo a passo para cada tempo de execução local principal em uma **NVIDIA GeForce RTX 1080** (8 GB VRAM, Pascal/computação **6.1**). Assume **Linux** (Ubuntu, Debian, Kali, etc.); O Windows observa onde o fluxo difere.

Consulte [Requisitos do modelo RAM](iv-model-ram-requirements.md) para a teoria do dimensionamento. Em 8 GB VRAM, comece com modelos **3B–7B** em **Q4_K_M** ou o quanto padrão de Ollama.

## 0. RTX 1080 restrições

| Especificações | Implicação |
|------|-------------|
| **8 GB VRAM** | Confortável: **3B–7B** Q4 em GPU. **8B** Q4 se encaixa em um contexto modesto. **13B+** precisa de descarregamento de CPU ou arLLM |
| **Pascal (sm_61)** | Funciona com compilações CUDA de Ollama, llama.cpp, KoboldCPP. **vLLM / TGI / TensorRT-LLM** tem como alvo GPUs mais recentes – muitas vezes doloroso ou sem suporte |
| **Sistema RAM** | Apontar para **16 GB+** então CPU descarrega e OS não trocam |

### Pré-requisitos compartilhados (todos os caminhos GPU)

```bash
# 1. NVIDIA driver (reboot after install)
nvidia-smi
# Should show RTX 1080 and driver 535+ (550+ recommended)

# 2. Optional but useful: CUDA toolkit for building llama.cpp
# Ubuntu/Debian example — match your distro
sudo apt update
sudo apt install -y build-essential cmake git
```

Se`nvidia-smi`falhar, corrija o driver antes de qualquer tempo de execução abaixo.

### Modelos recomendados para 8 GB VRAM

| Modelo | Formato | Cabe totalmente em GPU? |
|-------|--------|-------------------|
| **`qwen2.5-coder:7b`** (Ollama) | Pacote Ollama | **Sim — melhor codificador aberto para 8 GB** |
|`qwen2.5-coder:3b`| Ollama / Q4 GGUF | Sim – mais rápido, mais leve |
|`llama3.2:3b`(Ollama) | Pacote Ollama | Sim — bate-papo geral, sem ajuste de código |
|`qwen2.5:7b`| Ollama / Q4 GGUF | Sim em Q4 — chat geral |
|`qwen2.5-coder:14b`| Q4 GGUF | Apertado - descarregamento parcial em 1080 |
|`qwen2.5-coder:32b`| Q4 GGUF | Não — precisa de 24 GB+ VRAM |

###

## 1. Ollama (mais fácil – comece aqui)

### Instalar

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Windows/macOS: baixe em [ollama.com/download](https://ollama.com/download).

### Verifique GPU

```bash
ollama run qwen2.5-coder:7b "Write hello world in Python."
# In another terminal while generating:
ollama ps
```

`ollama ps`deve mostrar **GPU** na coluna do processador. Se disser apenas CPU, verifique`nvidia-smi`e motorista.

### Puxar e executar modelos

```bash
# Best coding model for 8 GB VRAM (recommended)
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b

# Faster / lighter coding
ollama pull qwen2.5-coder:3b
ollama run qwen2.5-coder:3b

# General chat (not code-specialized)
ollama pull qwen2.5:7b
ollama run qwen2.5:7b

# Small general model
ollama pull llama3.2:3b
ollama run llama3.2:3b
```

### API compatível com OpenAI (Cursor, Continuar, etc.)

```bash
# Server starts automatically on first request; or:
ollama serve
```

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:7b",
    "messages": [{"role": "user", "content": "Write a bash script to list large files"}]
  }'
```

| Configuração Cursor / IDE | Valor |
|----------------------|-------|
| Base URL |`http://localhost:11434/v1`|
| Modelo | **`qwen2.5-coder:7b`** (codificação) ou`qwen2.5:7b`(bate-papo geral) |
| Chave API | qualquer espaço reservado (por exemplo`ollama`) |

### Execute um GGUF personalizado

```bash
# After hf download (see Hugging Face note)
cat > Modelfile <<'EOF'
FROM ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf
PARAMETER temperature 0.7
EOF
ollama create qwen-coder-local -f Modelfile
ollama run qwen-coder-local
```

###

## 2. llama.cpp (compilação CUDA - controle máximo)

### Instalar (construir com CUDA)

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j "$(nproc)"
```

Os binários chegam`build/bin/`- por ex.`llama-cli`,`llama-server`.

Se o CMake não conseguir encontrar CUDA, defina:

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### Baixe um GGUF

```bash
pip install -U "huggingface_hub[cli]"
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

### Execute interativamente

```bash
./build/bin/llama-cli \
  -m ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  -ngl 99 \
  -c 4096 \
  -p "You are an expert programmer." \
  --interactive
```

| Bandeira | RTX orientação 1080 |
|------|-------------------|
|`-ngl 99`| Descarregar **todas** camadas para GPU (use para 3B–7B Q4) |
|`-ngl 35`| Descarregamento parcial se 8B+ OOM — descanso em CPU |
|`-c 4096`| Tokens de contexto — caem para **2048** se OOM |
|`-ngl 0`| Forçar CPU (somente depuração) |

### HTTP servidor

```bash
./build/bin/llama-server \
  -m ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  -ngl 99 \
  -c 4096 \
  --host 127.0.0.1 \
  --port 8080
```

API:`http://localhost:8080`- Endpoints estilo OpenAI por [documentos do servidor llama.cpp](https://github.com/ggerganov/llama.cpp/blob/master/tools/server/README.md).

###

## 3. LM Estúdio (GUI — Linux ou Windows)

### Instalar

1. Baixe em [lmstudio.ai](https://lmstudio.ai) (`.AppImage`no Linux, instalador no Windows).
2. Execute o aplicativo; abra **Descobrir** → pesquisar **`Qwen2.5-Coder-7B`** → escolha **Q4** quant.
3. **Meus modelos** → carregar modelo → **GPU** descarregar o controle deslizante para **max** (todas as camadas).

### Correr

- Guia **Bate-papo** para uso interativo.
- **Desenvolvedor** → **Servidor Local** → iniciar servidor em`http://localhost:1234/v1`.

| RTX dica 1080 | Ação |
|--------------|--------|
| OOM em carga | Modelo menor ou contexto inferior nas configurações do modelo |
| Primeiro token lento | Normal em 1080 para 7B — espere ~15–40 tok/s para 7B Q4 |

Nenhum fluxo de trabalho de servidor Linux headless - use Ollama ou llama-server para caixas SSH.

###

## 4. KoboldCPP (binário portátil + web UI)

### Instalar

```bash
# CUDA-enabled release from GitHub (pick latest cu12.x asset for Linux)
wget https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp-linux-x64-cuda12
chmod +x koboldcpp-linux-x64-cuda12
mv koboldcpp-linux-x64-cuda12 koboldcpp
```

Janelas: agarrar`koboldcpp.exe`CUDA compilado a partir da mesma página de lançamentos.

### Correr

```bash
./koboldcpp --model ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --gpulayers 99 \
  --contextsize 4096 \
  --port 5001
```

Abrir`http://localhost:5001`em um navegador. Mais baixo`--gpulayers`se você clicar em OOM nos modelos 8B.

###

## 5. GPT4All (desktop, opcional CUDA)

### Instalar

Baixe em [gpt4all.io](https://gpt4all.io) -Linux`.deb`/AppImage ou instalador do Windows.

### Correr

1. **Adicionar modelo** → escolha um modelo de chat **3B–7B** (evite 13B+ em 1080).
2. Configurações → ativar a aceleração **GPU** (Vulkan/CUDA dependendo da compilação).
3. **Local API** nas configurações se você precisar de HTTP.

Melhor para bate-papo offline casual; os desenvolvedores geralmente preferem Ollama à ergonomia de API.

###

## 6. airLLM (modelos grandes HF em 8 GB VRAM)

Streaming de camada - ajusta **13B+** lentamente quando a carga completa de GPU não cabe.

### Instalar

```bash
python3 -m venv ~/airllm-venv
source ~/airllm-venv/bin/activate
pip install -U pip airllm torch --index-url https://download.pytorch.org/whl/cu121
hf auth login
```

### Executar (Python)

```python
from airllm import AutoModel

model = AutoModel.from_pretrained(
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    compression="4bit",
)
input_tokens = model.tokenizer(
    ["def fib(n):"],
    return_tensors="pt",
    return_attention_mask=False,
)
generation = model.generate(input_tokens["input_ids"].cuda(), max_new_tokens=50)
print(model.tokenizer.decode(generation[0]))
```

Use para **experimentos**, não para bate-papos de baixa latência. A primeira execução baixa os pesos do Hugging Face.

###

## 7. vLLM — não recomendado em RTX 1080

[vLLM](https://github.com/vllm-project/vllm) tem como alvo **datacenter GPUs** (Ampere **sm_80+**). Pascal **sm_61** muitas vezes **não é suportado** ou requer compilação a partir do código-fonte com recursos reduzidos – ROI ruim em um 1080.

Se você ainda quiser tentar (somente Linux):

```bash
python3 -m venv ~/vllm-venv
source ~/vllm-venv/bin/activate
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-Coder-7B-Instruct \
  --dtype half \
  --max-model-len 2048
```

Espere falhas de compilação ou erros de tempo de execução no Pascal. **Use Ollama ou llama.cpp** neste cartão.

###

## 8. TGI & TensorRT-LLM – pule em 1080

| Plataforma | RTX 1080 veredicto |
|----------|------------------|
| **[TGI](https://github.com/huggingface/text-generation-inference)** | Pilha Docker + NVIDIA; as imagens oficiais assumem GPUs mais recentes. Possível com imagens CUDA antigas, mas sem suporte para uso diário |
| **[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)** | Otimizado para **Tensor Core** GPUs (Turing+). Pascal não possui Tensor Cores – não vale a pena instalar |

Para APIs de produção em hardware moderno, revisite-os em um **RTX 3060 12GB+** ou nuvem GPU.

###

## 9. MLX — não aplicável

[MLX](https://github.com/ml-explore/mlx) é **Apenas Apple Silicon**. Pule em um RTX 1080 PC.

###

## 10. Escolha rápida para RTX 1080

| Meta | Instalar | Executar |
|------|---------|-----|
| **Codificação local (recomendado)** | Ollama |`ollama pull qwen2.5-coder:7b && ollama run qwen2.5-coder:7b`|
| **IDE API para código** | Ollama |`http://localhost:11434/v1`+`qwen2.5-coder:7b`|
| **Bate-papo geral mais rápido** | Ollama |`ollama pull llama3.2:3b && ollama run llama3.2:3b`|
| **GPU/controle refinado** | lhama.cpp CUDA construir |`llama-server -ngl 99 -m …Qwen2.5-Coder…Q4_K_M.gguf`|
| **Web UI, sem terminal** | LM Studio ou KoboldCPP | Pesquisar Qwen2.5-Coder-7B em GUI |
| **Experiência 13B+** | arLLM |`Qwen/Qwen2.5-Coder-14B-Instruct`+ streaming de camada |

## 11. Solução de problemas

| Sintoma | Correção |
|--------|-----|
| **CUDA OOM** | Modelo menor (3B), Q4 quant, inferior`-c`/ contexto, reduzir`--gpulayers`|
| **Funciona apenas em CPU** |`nvidia-smi`; reinstalar o driver; reconstruir llama.cpp com`-DGGML_CUDA=ON`|
| **Geração lenta** | Normal para 7B em 1080 (~20–35 tok/s Q4); use 3B para velocidade |
| **Modelo não encontrado** |`ollama pull <name>`ou verifique o caminho GGUF |
| **Modelo fechado HF** |`hf auth login`+ aceitar licença |

Monitore VRAM durante uma execução:

```bash
watch -n1 nvidia-smi
```

## Relacionado

- [Baixando do Hugging Face](ii-downloading-from-huggingface.md)
- [Plataformas de execução local](iii-local-run-platforms.md)
- [Requisitos do modelo RAM](iv-model-ram-requirements.md)
- [CPU e corredores leves](v-cpu-and-lightweight-runners.md)
