---
label: "II"
subtitle: "Instalar e configurar"
group: "Ollama"
order: 2
---
Instalar e configurar

## 1. Instalar

### Linux (script – recomendado)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Instala o`ollama`binário e um serviço **systemd** (inicia na inicialização na maioria das distros).

###macOS

Baixe em [ollama.com/download](https://ollama.com/download) ou:

```bash
brew install ollama
```

Usa **Metal** no Apple Silicon automaticamente.

###Janelas

Instalador de [ollama.com/download](https://ollama.com/download). Usa **CUDA** quando um NVIDIA GPU e um driver estão presentes.

## 2. Verifique

```bash
ollama --version
ollama list          # empty until first pull
```

Inicie o servidor (geralmente iniciado automaticamente após a instalação):

```bash
ollama serve         # foreground — optional if service already running
```

Verifique o API:

```bash
curl http://localhost:11434/api/tags
```

## 3. Pré-requisitos GPU (NVIDIA Linux)

```bash
nvidia-smi
```

| Verifique | Esperado |
|-------|----------|
| Motorista | 535+ (550+ recomendado) |
| GPU listado | Seu cartão (por exemplo, RTX 1080) |
| Sem erros | Corrija o driver antes de culpar Ollama |

Ollama agrupa seu próprio tempo de execução CUDA — você **não** precisa de uma instalação separada do kit de ferramentas CUDA para uso básico.

## 4. Onde os arquivos ficam

| Caminho | Conteúdo |
|------|----------|
|`~/.ollama/models/`| Blobs de modelo baixados (grandes) |
|`~/.ollama/`| Configuração e estado |
| **Serviço** |`systemctl status ollama`(Linux) |

Disco livre antes de grandes extrações - um modelo 7B tem aproximadamente **4–8 GB** no disco, dependendo do quant.

## 5. Gerenciamento de serviços (Linux)

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

Registros:

```bash
journalctl -u ollama -f
```

## Próximo

[Modelos – puxar e gerenciar](iii-models-pull-and-manage.md) — baixe seus primeiros modelos.
