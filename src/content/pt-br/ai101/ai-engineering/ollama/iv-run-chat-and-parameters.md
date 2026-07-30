---
label: "IV"
subtitle: "Executar, conversar e parâmetros"
group: "Ollama"
order: 4
---
Executar, conversar e parâmetros

## 1. Bate-papo interativo

```bash
ollama run qwen2.5-coder:7b
```

| Comando (no chat) | Ação |
|-------------------|--------|
|`/bye`,`/exit`| Sair da sessão |
|`/clear`| Contexto claro |
|`/set parameter value`| Alterar parâmetro de tempo de execução (veja abaixo) |
|`/?`| Ajuda |

One-shot sem modo interativo:

```bash
ollama run qwen2.5-coder:7b "Write a Python function to merge two dicts"
```

## 2. Parâmetros comuns

Definido durante o bate-papo com`/set`ou em um **Modelfile** (persistente):

| Parâmetro | Típico | Efeito |
|-----------|---------|--------|
|`temperature`|`0.7`| Aleatoriedade (menor = mais determinística) |
|`num_ctx`|`4096`| Tokens de janela de contexto — aumente se você tiver VRAM |
|`top_p`|`0.9`| Amostragem de núcleo |
|`repeat_penalty`|`1.1`| Reduzir a repetição |

Exemplo em sessão:

```text
/set temperature 0.2
/set num_ctx 8192
```

Tarefas de codificação: experimente **`temperature 0.1–0.3`**.

## 3. Prompt do sistema

No bate-papo interativo, prompt do sistema multilinha:

```bash
ollama run qwen2.5-coder:7b
>>> /set system You are a senior Python engineer. Prefer stdlib. Always show types.
```

Para prompts permanentes do sistema, use um **Modelfile** — [Modelfile & custom GGUF](vi-modelfile-and-custom-gguf.md).

## 4. O que está carregado agora

```bash
ollama ps
```

| Coluna | Significado |
|--------|---------|
| **MODEL** | Marca de corrida |
| **PROCESSOR** |`100% GPU`,`100% CPU`ou misto |
| **UNTIL** | Temporizador de descarga ocioso |

Se **PROCESSOR** mostrar CPU apenas em uma máquina GPU, consulte [GPU e solução de problemas](vii-gpu-troubleshooting.md).

## 5. Mantenha o modelo na memória

Padrão: Ollama descarrega modelos ociosos após alguns minutos.

```bash
# Keep loaded 30 minutes after last request (example)
OLLAMA_KEEP_ALIVE=30m ollama serve
```

Ou por solicitação via API`keep_alive`campo — [integração API e IDE](v-api-and-ide-integration.md).

## 6. Entrada multilinha

Cole blocos de código diretamente em`ollama run`. Termine com uma linha em branco ou use o modo one-shot com heredoc:

```bash
ollama run qwen2.5-coder:7b <<'EOF'
Review this function for bugs:

def divide(a, b):
    return a / b
EOF
```

## Próximo

[Integração API e IDE](v-api-and-ide-integration.md) — Cursor, Continuar, enrolar.
