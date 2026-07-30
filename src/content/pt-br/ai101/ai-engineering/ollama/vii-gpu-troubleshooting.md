---
label: "VII"
subtitle: "GPU e solução de problemas"
group: "Ollama"
order: 7
---
GPU e solução de problemas

## 1. Confirme que GPU é usado

```bash
ollama run qwen2.5-coder:7b "hi"
# second terminal:
ollama ps
watch -n1 nvidia-smi
```

|`ollama ps`shows | Significado |
|-------------------|---------|
| **100% GPU** | Bom — modelo no cartão |
| **100% CPU** | GPU não usado — veja as correções abaixo |
| **% misto** | Descarregamento parcial — normal para VRAM apertado |

## 2. CPU - somente quando GPU é esperado

| Verifique | Correção |
|-------|-----|
|`nvidia-smi`falha | Instalar/corrigir o driver NVIDIA; reiniciar |
| Modelo muito grande | Etiqueta menor (`3b`não`32b`) |
| Motorista muito velho | Atualizar para 535+/550+ |
| Compilação Ollama errada | Reinstale em [ollama.com](https://ollama.com/download) |
| Forçar teste CPU |`OLLAMA_NUM_GPU=0`— remover para uso normal |

Linux: garanta que o usuário possa acessar GPU (`nvidia-smi`como mesmo usuário executando Ollama).

## 3. Sem memória (OOM)

| Sintoma | Correção |
|--------|-----|
| CUDA OOM / falha na carga | Modelo menor;`qwen2.5-coder:3b`|
| OOM durante um longo bate-papo | Mais baixo`num_ctx`(`/set num_ctx 2048`) |
| Vários modelos carregados |`ollama ps`— aguarde o descarregamento ocioso ou reinicie o serviço |
| Disco cheio ao puxar |`ollama rm`modelos antigos;`df -h ~/.ollama`|

Guia VRAM: [Requisitos do modelo RAM](../implementation-example/iv-model-ram-requirements.md). Especificações de RTX 1080: [Instalar e executar em RTX 1080](../implementation-example/vi-install-and-run-rtx-1080.md).

## 4. Geração lenta

| Causa | Orientação |
|-------|----------|
| **7B em GPU** mais antigo | ~20–35 tok/s é normal para RTX 1080 |
| **CPU inferência** | Muito mais lento — corrija GPU primeiro |
| **Início a frio** | O primeiro token após o carregamento ocioso é mais lento |
| **Contexto muito longo** | Custo de cache KV – encurtar`num_ctx`|

## 5. Erros de conexão (API / Cursor)

| Erro | Correção |
|-------|-----|
|`connection refused`|`ollama serve`ou`systemctl start ollama`|
| Nome de modelo errado |`ollama list`— use tag exata |
| Cursor não pode acessar API | A base URL deve ser`http://localhost:11434/v1`|
| Máquina remota | SSH túnel ou conjunto`OLLAMA_HOST`(somente rede confiável) |

## 6. Falhas de pull/download

| Problema | Correção |
|--------|-----|
| Download interrompido | Executar novamente`ollama pull`— currículos |
| Sem espaço em disco | Remover modelos com`ollama rm`|
| Proxy/firewall | Configurar proxy do sistema; verificar inspeção corporativa SSL |

## 7. Redefinir

```bash
sudo systemctl stop ollama
# optional: backup then clear models
# rm -rf ~/.ollama/models/*
sudo systemctl start ollama
ollama pull qwen2.5-coder:7b
```

Use a redefinição somente quando o cache estiver corrompido – baixa novamente todos os modelos.

## Relacionado

- [Instalar e configurar](ii-install-and-setup.md)
- [integração API e IDE](v-api-and-ide-integration.md)
- [Exemplos de implementação](../implementation-example/i-overview.md)
