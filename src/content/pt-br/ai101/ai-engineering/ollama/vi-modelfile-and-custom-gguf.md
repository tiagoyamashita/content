---
label: "VI"
subtitle: "Arquivo de modelo e GGUF personalizado"
group: "Ollama"
order: 6
---
Arquivo de modelo e GGUF personalizado

Quando um modelo **não** está na biblioteca Ollama — ou você deseja um **prompt e parâmetros personalizados do sistema** incorporados — use um **Modelfile** e`ollama create`.

## 1. Noções básicas do arquivo de modelo

```dockerfile
FROM qwen2.5-coder:7b
SYSTEM You are a concise Python tutor. Show types and one test per answer.
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
```

```bash
ollama create python-tutor -f Modelfile
ollama run python-tutor
```

| Instrução | Finalidade |
|------------|---------|
|`FROM`| Tag do modelo base **ou** caminho para`.gguf`|
|`SYSTEM`| Prompt de sistema padrão |
|`PARAMETER`| Parâmetros de tempo de execução padrão |
|`TEMPLATE`| Modelo de bate-papo (avançado — geralmente herdado da base) |
|`LICENSE`| Metadados de texto de licença |

## 2. Importe um GGUF local (do Hugging Face)

Baixe GGUF primeiro - veja [Baixando do Hugging Face](../implementation-example/ii-downloading-from-huggingface.md):

```bash
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

Arquivo de modelo:

```dockerfile
FROM ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf
PARAMETER temperature 0.7
```

```bash
ollama create qwen-coder-local -f Modelfile
ollama run qwen-coder-local
```

Use caminhos **absolutos ou relativos ao repositório** para o`.gguf`arquivo em`FROM`.

## 3. Derive do modelo existente

```bash
ollama show qwen2.5-coder:7b --modelfile > Modelfile
# edit SYSTEM / PARAMETER
ollama create my-qwen-dev -f Modelfile
```

## 4. Listar modelos personalizados

```bash
ollama list
```

Os nomes personalizados aparecem ao lado dos pulls da biblioteca (`python-tutor`,`qwen-coder-local`, etc.).

## 5. Compartilhe com a equipe

| Abordagem | Detalhe |
|----------|--------|
| **Commit arquivo de modelo** | Corridas em equipe`ollama create`depois de puxar o mesmo GGUF |
| **Commit apenas Modelfile + instruções HF** | Arquivo de modelo aponta para`FROM qwen2.5-coder:7b`- todos`ollama pull`|
| **Não confirme** multi-GB`.gguf`bolhas | Usar`hf download`ou`ollama pull`em README |

Exemplo de snippet de repositório:

```text
models/
  Modelfile              ← committed
  README.md              ← "run hf download … then ollama create …"
  *.gguf                 ← gitignored
```

## 6. Quando não usar Modelfile

| Situação | Melhor caminho |
|-----------|------------|
| Modelo já na biblioteca |`ollama pull`apenas |
| Precisa de controle máximo de inferência | llama.cpp diretamente — [Plataformas de execução local](../implementation-example/iii-local-run-platforms.md) |
| Serviço multiusuário de produção | vLLM / TGI — não Ollama desktop |

## Próximo

[GPU e solução de problemas](vii-gpu-troubleshooting.md) - corrige apenas CPU, OOM, geração lenta.
