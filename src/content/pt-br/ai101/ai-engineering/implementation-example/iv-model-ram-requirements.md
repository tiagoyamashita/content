---
label: "IV"
subtitle: "Requisitos do modelo RAM"
group: "AI Applied"
order: 4
---
Requisitos do modelo RAM

A inferência local precisa de RAM (e VRAM em GPU) para **pesos** mais **KV cache** para a janela de contexto. O subdimensionamento causa OOM mortes, trocas ou recusa de carregamento.

## 1. Regras rápidas

| Componente | O que é | Dimensionamento aproximado |
|-----------|------------|-------------|
| **Pesos** | Parâmetros congelados no disco/na memória | Depende da contagem de parâmetros × bytes por peso |
| **KV cache** | Estado de atenção para prompt + geração | Cresce com **comprimento do contexto** e tamanho do lote |
| **Despesas gerais** | Tempo de execução, tokenizador, gráfico | Frequentemente **1–3 GB** extras em GPU; menos em CPU GGUF puro |

**Parâmetros → memória de peso (não quantizado):**

```text
GB ≈ (parameters in billions) × (bytes per parameter) × 1.07
```

| Precisão | Bytes/parâmetro | Modelo 7B | 13B | 70B |
|-----------|-------------|----------|-----|-----|
| FP16 | 2 | ~14 GB | ~26 GB | ~140 GB |
| INT8 | 1 | ~7 GB | ~13 GB | ~70 GB |
| INT4 | 0,5 | ~3,5 GB | ~6,5 GB | ~35 GB |

O fator **1,07** é responsável por pequenas despesas gerais; os quants reais GGUF variam de acordo com o esquema (Q4_K_M vs Q8_0).

## 2. GGUF folha de dicas quant (modelo de classe 7B)

**Apenas peso** RAM aproximado para um modelo ~7B:

| Quantidade | ~Peso RAM | Qualidade | Uso típico |
|-------|---------|---------|-------------|
| Q8_0 | ~7,5 GB | Perto de FP16 | 16 máquinas GB, sensíveis à qualidade |
| Q6_K | ~6 GB | Excelente | Ponto ideal em 16 GB |
| **Q4_K_M** | **~4,5 GB** | Bom padrão | **8–16 GB** notebooks |
| Q3_K_M | ~3,5 GB | Perda perceptível | Apertado apenas RAM |
| Q2_K | ~2,5 GB | Degradado | Apenas experimentação |

Dimensione linearmente por contagem de parâmetros: um **3B** Q4_K_M tem ~**2 GB** pesos; **13B** Q4_K_M é ~**8 GB**.

## 3. O comprimento do contexto adiciona RAM

O cache KV domina em contextos longos:

```text
KV cache grows with: layers × hidden_dim × context_tokens × 2 (K+V) × dtype
```

| Conclusão prática | Orientação |
|--------------------|----------|
| Contexto 4k padrão | Geralmente bem em cima da mesa de peso |
| Contexto 8k–32k | Adicione **2–8+ GB** dependendo do tamanho do modelo |
| Contexto de 128k | Freqüentemente precisa de **IT0__** dedicado ou descarregamento agressivo |

Se o aplicativo permitir que você defina **comprimento do contexto**, diminua-o ao pressionar OOM antes de reduzir o tamanho do modelo.

## 4. Tamanho do modelo → mínimo prático RAM

Assume **Q4_K_M**, **contexto 4k**, pequena sobrecarga. Adicione **4 GB** para OS + navegador se este for seu driver diário de laptop.

| Modelo (parâmetros) | Peso RAM (Q4_K_M) | **Sistema RAM mínimo** | Confortável |
|----------------|---------------------|-------------|------------|
| 1–3B | 1–2 GB | **8GB** | 16 GB |
| 7–8B | 4–5 GB | **8 GB** (apertado) | **16 GB** |
| 13–14B | 8–9 GB | **16 GB** | **32 GB** |
| 32B | ~18 GB | **32 GB** | **48–64 GB** |
| 70B | ~35 GB | **64 GB** + GPU ou descarga pesada | **96 GB+** |

**GPU VRAM:** pesos + KV geralmente devem caber no cartão para inferência GPU em velocidade total. Uma placa **12 GB** funciona **7B Q4** confortavelmente; **24 GB** lida com **13B Q4** ou **7B** em contexto longo.

## 5. Memória CPU vs GPU

| Modo | Comportamento |
|------|----------|
| **Completo GPU** | Pesos + KV em VRAM; mais rápido |
| **Descarregamento parcial** (llama.cpp`-ngl`) | Algumas camadas em GPU ficam em RAM - flexíveis, mas mais lentas |
| **CPU apenas** | Tudo no sistema RAM — funciona com GGUF; espere tokens baixos/s |
| **streaming de camada estilo airLLM** | Camadas puxadas para GPU em ondas — ajustam-se a modelos enormes em VRAM pequenos (consulte [CPU e corredores leves](v-cpu-and-lightweight-runners.md)) |

## 6. Exemplo de escolhas por máquina

| Seu hardware | Modelos iniciais razoáveis ​​|
|---------------|----------------------------|
| 8 GB RAM, não GPU | 1–3BQ4 (`qwen2.5-coder:1.5b`, Lhama 3.2 1B/3B) |
| 16 GB RAM, não GPU | 7B Q4_K_M (`qwen2.5-coder:7b`) |
| **8 GB VRAM (RTX 1080)** | **`qwen2.5-coder:7b`** — melhor codificador aberto para a camada |
| 16 GB RAM + 8 GB VRAM | 7B Q4/Q8 em GPU (`qwen2.5-coder:7b`); ou descarregamento parcial de 13B |
| 32 GB RAM + 24 GB VRAM |`qwen2.5-coder:32b`GPU completo; ou 13B Q4 com altura livre |
| 64 GB+ RAM | 32B–70B com mistura de descarregamento CPU/GPU |

### Família Qwen2.5-Coder (peso RAM em Q4_K_M)

| Modelo | ~Peso RAM | Min VRAM (4k ctx) | Notas |
|-------|------------|-------------------|-------|
| 0,5B / 1,5B | abaixo de 1 GB | 4GB | Brinquedo / preenchimento automático |
| 3B | ~2GB | 6 GB | Codificação rápida em GPUs antigos |
| **7B** | **~4,5 GB** | **8 GB** | **Local ideal para RTX 1080** |
| 14B | ~8,5 GB | 12 GB | Precisa de cartão 12 GB+ ou descarregamento |
| 32B | ~18 GB | 24 GB | Codificador aberto superior; corresponde à classe GPT-4o em muitos bancos de código |

## 7. Verifique antes de se comprometer

1. Observe **contagem de parâmetros** e **quant** na placa modelo HF ou Ollama.
2. Adicione a estimativa de peso das tabelas acima.
3. Adicione **2–4 GB** KV + sobrecarga para seu contexto de destino.
4. Deixe **20% de espaço** — OS e aplicativos de desktop também precisam de RAM.

## Próximo

[CPU e corredores leves](v-cpu-and-lightweight-runners.md) — quando você não consegue ajustar os pesos totalmente em GPU.
