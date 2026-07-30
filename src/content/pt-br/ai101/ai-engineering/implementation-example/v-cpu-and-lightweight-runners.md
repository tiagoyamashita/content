---
label: "V"
subtitle: "CPU e corredores leves"
group: "AI Applied"
order: 5
---
CPU e corredores leves

Nem toda máquina possui 24 GB GPU. Esses tempos de execução priorizam **baixa VRAM**, **CPU inferência** ou **descarregamento de camada** para que você ainda possa executar modelos abertos úteis em um laptop ou pequena instância de nuvem.

## 1. Comparação de corredores

| Corredor | Idéia | GPU necessário? | Melhor quando |
|--------|------|-------------|-----------|
| **[lhama.cpp](https://github.com/ggerganov/llama.cpp)** | Inferência GGUF otimizada; parcial`-ngl`descarregar | Opcional | Padrão para CPU + GGUF; enorme comunidade |
| **[Ollama](https://ollama.com)** | Envolve llama.cpp (e outros) com puxões fáceis | Opcional | Igual a llama.cpp, mas mais simples UX |
| **[arLLM](https://github.com/lyogavin/airllm)** | Transmita **uma camada por vez** por meio de GPU | Pequeno VRAM OK | Classe 70B em **4 GB** VRAM (lento) |
| **[MLX](https://github.com/ml-explore/mlx)** | Núcleos de Apple Metal | Silício da Apple | Melhor desempenho local em Macs M1/M2/M3 |
| **[GPT4Todos](https://gpt4all.io)** | Aplicativo de desktop + back-ends CPU | Opcional | Usuários não técnicos, bate-papo offline |
| **[KoboldCPP](https://github.com/LostRuins/koboldcpp)** | garfo lhama.cpp + UI | Opcional | Binário portátil único |
| **[arquivo de chamada](https://github.com/Mozilla-Ocho/llamafile)** | Modelo + tempo de execução em um arquivo | Opcional | Executável drop-in, sem instalação |
| **transformadores +`device_map="cpu"`** | PyTorch puro em CPU | Não | Apenas prototipagem – muito lenta em escala |

## 2. airLLM — modelos grandes, minúsculos VRAM

**airLLM** mantém pesos totais no **sistema RAM** e move **uma camada de transformador** para a memória GPU por passo de avanço.

```text
70B model in RAM  →  layer 0 to GPU → compute → layer 1 to GPU → … → logits
```

| Prós | Contras |
|------|------|
| Execute modelos muito maiores que VRAM | **Muito mais lento** que carga completa de GPU |
| Funciona com tensores de segurança Hugging Face | Configuração de Python + CUDA; menos polido que Ollama |
| Útil para trabalhos em lote ocasionais | Ruim para bate-papo de baixa latência |

Instalação típica:

```bash
pip install airllm
```

```python
from airllm import AutoModel

model = AutoModel.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
# inference API per project README — layer-wise GPU execution
```

Use quando você **deve** executar um modelo HF específico e só tem **4–8 GB VRAM**, não para assistentes de codificação interativos.

## 3. llama.cpp em CPU (sem GPU)

Baixe um **Q4_K_M** GGUF e execute:

```bash
./llama-cli -m ./models/model-Q4_K_M.gguf -p "Hello" -n 128 -ngl 0
```

| Bandeira | Significado |
|------|---------|
|`-ngl 0`| **Não** GPU camadas — CPU puro |
|`-ngl 35`| Descarregar 35 camadas para GPU (dependente do modelo) |
|`-c 4096`| Tamanho do contexto — menor se OOM |

**llama-server** expõe a mesma pilha em HTTP para aplicativos.

| Prós | Contras |
|------|------|
| Funciona em praticamente qualquer máquina x86/ARM | Tokens/seg baixos em CPU (1–20 típico) |
| Pegada quantizada de RAM | Prompts longos parecem lentos |
| Mesmas escalas binárias do Pi para a estação de trabalho | Sem formação — apenas inferência |

Emparelhe com [requisitos do modelo RAM](iv-model-ram-requirements.md) — **3B Q4** em **8 GB** RAM é realista; **7B** em **16 GB** é a zona de conforto para CPU.

## 4. Silício da Apple - MLX

No Mac, **MLX** geralmente supera caminhos CPU genéricos usando **memória unificada** com eficiência:

```bash
pip install mlx-lm
mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Hello"
```

| Prós | Contras |
|------|------|
| Forte desempenho por watt na série M- | Somente hardware macOS/Apple |
| Modelos MLX de 4 bits em HF | Catálogo menor que GGUF |
| Bom para desenvolvedores locais com Cursor | Não para implantação de servidor Linux |

## 5. Modo Ollama CPU

Se nenhum GPU for detectado, Ollama ainda será executado - apoiado pelos kernels llama.cpp CPU:

```bash
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

Prefira tags **menores** (`3b`,`1.5b`) apenas para CPU. Definir`OLLAMA_NUM_GPU=0`para forçar CPU em máquinas híbridas durante a depuração.

## 6. Quando usar qual

| Meta | Escolha |
|------|------|
| **codificação** local diária | Ollama + **`qwen2.5-coder:7b`** |
| Bate-papo local diário (geral) | Ollama +`qwen2.5:7b`ou`llama3.2:3b`|
| RAM mais rígido, controle total | lhama.cpp + Q4_K_M GGUF |
| Máquina de desenvolvimento MacBook | MLX ou Ollama |
| 70B no experimento 8 GB VRAM | arLLM |
| Bastão USB com entreferro | lhamafile ou KoboldCPP portátil |
| Produção API rendimento | **Não** estes — use vLLM em GPU ([nota de plataforma](iii-local-run-platforms.md)) |

## 7. Expectativas realistas (CPU)

| Modelo | Tokens brutos/s (laptop moderno CPU) |
|-------|--------------------------------------|
| codificador qwen2.5 1.5B Q4 | 20–45 |
| 1–3BQ4 | 15–40 |
| codificador qwen2.5 7B Q4 | 3–12 |
| 13BQ4 | 1–5 |

Os números variam muito de acordo com o suporte AVX, contagem de núcleos e limites de potência. Para assistência de codificação, **`qwen2.5-coder:7b`em GPU** ou um **IT2__** hospedado geralmente supera **7B em CPU**.

## Relacionado

- [Baixando do Hugging Face](ii-downloading-from-huggingface.md)
- [Plataformas de execução local](iii-local-run-platforms.md)
- [Requisitos do modelo RAM](iv-model-ram-requirements.md)
