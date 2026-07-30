---
label: "II"
subtitle: "Baixando do Hugging Face"
group: "AI Applied"
order: 2
---
Baixando do Hugging Face

[Abraçando o rosto](https://huggingface.co) hospeda o modelo **pesos**, **tokenizers** e **configs**. Uma página de repositório (por exemplo`meta-llama/Llama-3.2-3B-Instruct`) é uma pasta com versão – não um único instalador.

## 1. O que você está baixando

| Artefato | Finalidade |
|----------|---------|
|`config.json`| Arquitetura, tamanho oculto, contagem de camadas |
|`tokenizer.json`-&#09;o`tokenizer.model`| Texto → tokens |
|`*.safetensors`ou`*.bin`| Pesos do modelo (grandes) |
|`generation_config.json`| Configurações de decodificação padrão |
|`README.md`| Licença, formato de prompt, notas de avaliação |

**GGUF** repositórios (para importações llama.cpp / Ollama) enviam um ou mais`.gguf`arquivos com quantização já incorporada. **Os repositórios originais** enviam tensores de segurança de precisão total ou HF-quantizados para tempos de execução Python.

## 2. Pré-requisitos

```bash
# Hugging Face CLI — installs the `hf` command (current)
pip install -U "huggingface_hub[cli]"

# Optional: Git LFS for clone-based workflows
git lfs install
```

Faça login se o modelo for **bloqueado** (é necessária a aceitação da licença):

```bash
hf auth login
```

`huggingface-cli`está **obsoleto** - use`hf`para todas as tarefas CLI (`hf download`,`hf auth login`,`hf --help`).

Crie um token em [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) com acesso de **leitura**.

### Modelos fechados (Meta Llama, etc.) — necessários antes do download

`meta-llama/Llama-3.2-3B-Instruct`é **fechado**. Downloads não autenticados falham com:

```text
Error: Access denied. This repository requires approval.
Warning: You are sending unauthenticated requests to the HF Hub.
```

**Corrigir – execute todas as três etapas em ordem:**

| Etapa | Ação |
|------|--------|
| **1. Aprovação Web** | Abra [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) enquanto estiver logado → **Concordar e acessar o repositório** (formulário de meta licença). A aprovação geralmente é instantânea. |
| **2. CLI login** |`hf auth login`→ cole um token de **leitura** de [settings/tokens](https://huggingface.co/settings/tokens) |
| **3. Tente novamente** | Mesmo`hf download`comando |

Verifique a autenticação antes de baixar:

```bash
hf auth whoami
# Should print your HF username — confirms login only, NOT gated-repo access
```

(R)`hf auth whoami`ter sucesso não significa que você pode baixar o Llama.** Para repositórios fechados, você também deve concluir a **etapa 1 (aprovação da web)** na página do modelo enquanto estiver conectado como o **mesmo usuário HF** do CLI. Se o download ainda disser`requires approval`, abra o repositório URL em um navegador e procure **Concordar e acessar o repositório** — até que esse botão desapareça e você veja a guia Arquivos, os downloads de CLI falharão.

**Token alternativo env var** (scripts, CI ou se o cache de login falhar):

```bash
export HF_TOKEN="hf_xxxxxxxx"   # your read token — never commit this
hf download meta-llama/Llama-3.2-3B-Instruct --local-dir ./models/llama-3.2-3b
```

**Skip gate para GGUF** local — os repositórios quantitativos da comunidade geralmente estão abertos; bom para Ollama / llama.cpp:

```bash
hf download bartowski/Llama-3.2-3B-Instruct-GGUF \
  Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

Ou use **Ollama** (sem conta HF para o catálogo padrão):`ollama pull llama3.2:3b`.

### Modelos abertos recomendados (2025–2026)

| Caso de uso | Modelo | Fechado? | Ollama | Abraçando o rosto |
|----------|-------|--------|--------|-------------|
| **Codificação local (padrão)** | **Instrução Qwen2.5-Coder 7B** | Não |`qwen2.5-coder:7b`| [Qwen/Qwen2.5-Coder-7B-Instrução](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) |
| Bate-papo geral 7B | Qwen2.5 7B Instruir | Não |`qwen2.5:7b`|`Qwen/Qwen2.5-7B-Instruct`|
| Rápido/pequeno GPU | Qwen2.5-Codificador 3B | Não |`qwen2.5-coder:3b`|`Qwen/Qwen2.5-Coder-3B-Instruct`|
| Melhor codificador aberto (24 GB+ VRAM) | Instrução Qwen2.5-Coder 32B | Não |`qwen2.5-coder:32b`|`Qwen/Qwen2.5-Coder-32B-Instruct`|
| Chat geral (fechado) | Lhama 3.2 3B Instruir | **Sim** (Meta) |`llama3.2:3b`|`meta-llama/Llama-3.2-3B-Instruct`|

**Qwen2.5-Coder** é a escolha usual para **geração de código, correções e assistentes IDE** — Apache 2.0, sem etapa de aprovação HF, benchmarks fortes em comparação com outros codificadores abertos. Use o **`-Instruct`** variante para chat/codificação; os pesos básicos são apenas para ajuste fino.

**Baixe o Qwen2.5-Coder (sem bloqueio):**

```bash
# Full safetensors (transformers / vLLM)
hf download Qwen/Qwen2.5-Coder-7B-Instruct --local-dir ./models/qwen2.5-coder-7b

# Single GGUF file (llama.cpp / Ollama import)
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

Ou pule HF:`ollama pull qwen2.5-coder:7b`.

## 3. Método A -`hf download`(preferido)

Baixe um repositório inteiro ou arquivos específicos em uma pasta local:

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

| Bandeira | Usar |
|------|-----|
|`--local-dir`| Layout de repositório de espelho no disco |
|`--local-dir-use-symlinks False`| Arquivos reais, não links simbólicos (cópias portáteis) |
|`--revision`| Fixe um branch, tag ou commit |

A retomada é automática – os downloads interrompidos continuam de onde pararam.

## 4. Método B — clone Git + LFS

```bash
git clone https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
cd Llama-3.2-3B-Instruct
git lfs pull
```

| Prós | Contras |
|------|------|
| Fluxo de trabalho Git familiar | Mais lento para grandes repositórios; Cota LFS em HF |
| Confirmações fáceis de fixar | Extrai todo o repositório, a menos que o sparse-checkout esteja configurado |

Para modelos fechados, use HTTPS com um token ou chave SSH vinculada à sua conta HF.

## 5. Método C — Python`snapshot_download`

Útil dentro de scripts ou notebooks:

```python
from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    local_dir="./models/qwen2.5-coder-7b",
    local_dir_use_symlinks=False,
)
```

`transformers`também pode buscar no primeiro uso:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
```

Os pesos vão para o cache HF (`~/.cache/huggingface/hub`) a menos que você passe`cache_dir`ou`local_dir`.

## 6. Escolhendo a variante de repositório certa

| Você quer | Procure |
|----------|----------|
| **Assistente de codificação / IDE** | **Qwen2.5-Codificador**`*-Instruct`ou`qwen2.5-coder:7b`em Ollama |
| **llama.cpp / KoboldCPP** |`*-GGUF`repositórios ou`.gguf`na guia Arquivos |
| **Ollama** | Muitas vezes`ollama pull <name>`— Ollama downloads para você; ou importe um GGUF |
| **vLLM / TGI / transformadores** | Repositório de tensores de segurança originais ou AWQ/GPTQ quant |
| **Pequeno espaço em disco** | Q4_K_M, Q5_K_M GGUF ou AWQ 4 bits |

Leia sempre a **licença** no cartão do modelo. Muitos pesos proíbem o uso comercial ou exigem registro.

## 7. Verifique o download

```bash
# Check total size vs repo "Files and versions" tab
du -sh ./models/qwen2.5-coder-7b

# List safetensors shards
ls -lh ./models/qwen2.5-coder-7b/*.safetensors
```

Se um fragmento for pequeno (poucos KB), Git LFS pode não ter sido extraído – execute`git lfs pull`ou reexecutar`hf download`.

## 8. Problemas comuns

| Problema | Correção |
|--------|-----|
| **Acesso negado/requer aprovação** | Repo fechado – concluir [aprovação da web](#gated-models-meta-llama-etc--required-before-download), então`hf auth login`; confirme com`hf auth whoami`|
| **Aviso de solicitações não autenticadas** | Mesmo – você não está logado; definir`HF_TOKEN`ou correr`hf auth login`|
| **403 / repositório fechado** | Aceite a licença no site HF **primeiro** (logado) e depois`hf auth login`|
| **Sem disco** | Baixe um GGUF quant em vez de tensores de segurança completos |
| **Primeira puxada lenta** | Usar`hf download`com conexão com fio; fixar um quanto |
| **Formato incorreto para tempo de execução** | GGUF → lhama.cpp/Ollama; tensores de segurança → transformadores/vLLM |

## Próximo

[Plataformas de execução local](iii-local-run-platforms.md) — onde carregar esses arquivos e servir inferência.
