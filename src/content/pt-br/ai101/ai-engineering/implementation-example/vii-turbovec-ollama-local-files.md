---
label: "VII"
subtitle: "TurboVec + Ollama + arquivos locais"
group: "AI Applied"
order: 7
---
TurboVec + Ollama + arquivos locais

Crie uma pilha **RAG** totalmente local: seus arquivos permanecem no disco, **Ollama** incorpora e gera, **[TurboVec](https://github.com/RyanCodrai/turbovec)** armazena vetores compactados em disco — sem nuvem APIs, sem vetor gerenciado DB.

Para saber quando a pesquisa vetorial se ajusta vs MCP vs habilidades, consulte [Vetor DB, habilidades e referência](../how-mcp-works/v-vector-db-skills-and-reference.md).

## 1. O que o TurboVec faz

| Peça | Função |
|-------|------|
| **Seus arquivos** | Fonte da verdade -`.md`,`.txt`,`.pdf`(após extração de texto), código, runbooks |
| **Ollama`nomic-embed-text`** | Transforma cada pedaço em um vetor de incorporação de 768 dimensões |
| **TurboVec** | Compacta vetores (TurboQuant, padrão de 4 bits) e executa pesquisa rápida de similaridade |
| **Ollama LLM** (por ex.`qwen2.5-coder:7b`) | Lê pedaços recuperados e respostas |

```text
Local files  →  chunk  →  Ollama embed  →  TurboVec index (.tvim + .nodes.json)
                                                              ↓
User question  →  embed  →  top-k chunks  →  prompt  →  Ollama LLM  →  answer
```

TurboVec **não** é um servidor MCP por si só — é o **mecanismo de recuperação** por trás de um aplicativo Python/LlamaIndex (ou uma ferramenta MCP que você escreve mais tarde e que chama`search()`).

## 2. Pré-requisitos

```bash
# Ollama running
ollama serve   # or rely on systemd / app auto-start

# Embedding + chat models (768-dim embed matches TurboVec default path)
ollama pull nomic-embed-text
ollama pull qwen2.5-coder:7b    # coding; or qwen2.5:7b for general chat
```

| Modelo | Finalidade | VRAM (aprox.) |
|-------|------------|---------------|
|`nomic-embed-text`| Incorporações | Pequenas — cargas sob pedido |
|`qwen2.5-coder:7b`| Respostas/código | ~5 GB Q4 em GPU |

Verifique Ollama:

```bash
curl http://localhost:11434/api/tags
```

## 3. Ambiente Python

```bash
python3 -m venv ~/local-rag-venv
source ~/local-rag-venv/bin/activate
pip install -U pip
pip install "turbovec[llama-index]" llama-index llama-index-llms-ollama llama-index-embeddings-ollama
```

| Pacote | Função |
|--------|------|
|`turbovec[llama-index]`|`TurboQuantVectorStore`- visita à loja simples LlamaIndex |
|`llama-index`| Chunking, indexação, mecanismo de consulta |
|`llama-index-llms-ollama`| Bate-papo/conclusão via Ollama |
|`llama-index-embeddings-ollama`| Incorporações via Ollama |

## 4. Layout de arquivo local

```text
~/local-rag/
  data/                 # your documents (gitignore secrets)
    handbook.md
    runbooks/
      deploy.txt
    notes/
  store/                # persisted TurboVec index (created by script)
  ingest_and_ask.py
```

Coloque **somente** arquivos nos quais você tem permissão para indexar`data/`. TurboVec persiste em pedaços de texto`store/*.nodes.json`- tratar`store/`tão sensível.

## 5. Ingerir arquivos locais e construir o índice

`ingest_and_ask.py`TÉCNICO.:

```python
from pathlib import Path

from llama_index.core import Settings, SimpleDirectoryReader, StorageContext, VectorStoreIndex
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from turbovec.llama_index import TurboQuantVectorStore

DATA_DIR = Path("./data")
STORE_DIR = Path("./store")
OLLAMA_BASE = "http://localhost:11434"

# 1) Ollama models — all local
Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url=OLLAMA_BASE,
)
Settings.llm = Ollama(
    model="qwen2.5-coder:7b",
    base_url=OLLAMA_BASE,
    request_timeout=120.0,
)

# 2) Load files (recursive). Add readers for PDF/HTML if needed.
documents = SimpleDirectoryReader(
    input_dir=str(DATA_DIR),
    recursive=True,
).load_data()

# 3) TurboVec-backed vector store (4-bit compression; dim inferred on first add)
vector_store = TurboQuantVectorStore.from_params(bit_width=4)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# 4) Chunk → embed (Ollama) → compress → store in TurboVec
index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
)

# 5) Persist to disk — writes store/vectors.tvim + store/vectors.nodes.json
STORE_DIR.mkdir(parents=True, exist_ok=True)
storage_context.persist(persist_dir=str(STORE_DIR))

print(f"Indexed {len(documents)} document(s) into {STORE_DIR}")
```

```bash
cd ~/local-rag
python ingest_and_ask.py
```

A primeira execução incorpora cada pedaço através de Ollama – lento em corpora grandes; mais tarde executa o carregamento de`store/`.

## 6. Faça perguntas (mecanismo de consulta)

Adicione ao mesmo arquivo ou em um arquivo separado`ask.py`TÉCNICO.:

```python
from pathlib import Path

from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from turbovec.llama_index import TurboQuantVectorStore

STORE_DIR = Path("./store")
OLLAMA_BASE = "http://localhost:11434"

Settings.embed_model = OllamaEmbedding(
    model_name="nomic-embed-text",
    base_url=OLLAMA_BASE,
)
Settings.llm = Ollama(
    model="qwen2.5-coder:7b",
    base_url=OLLAMA_BASE,
    request_timeout=120.0,
)

vector_store = TurboQuantVectorStore.from_persist_dir(persist_dir=str(STORE_DIR))
storage_context = StorageContext.from_defaults(
    vector_store=vector_store,
    persist_dir=str(STORE_DIR),
)
index = load_index_from_storage(storage_context)

query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("How do we deploy to production?")
print(response)
```

```bash
python ask.py
```

As respostas são baseadas em partes recuperadas de **seus** arquivos — verifique as citações no texto da resposta.

## 7. Reindexar após alterações no arquivo

| Alterar | Ação |
|--------|--------|
| Arquivos novos ou editados | Execute novamente a ingestão (ou grave incremental`add()`somente para novos documentos) |
| Comece do zero | Excluir`store/`e reconstruir |
| Documento único removido |`vector_store.delete(ref_doc_id)`por [documentos do TurboVec LlamaIndex](https://github.com/RyanCodrai/turbovec/blob/main/docs/integrations/llama_index.md) |

TurboVec suporta **ingestão online** — sem fase de treinamento separada; novos vetores são anexados ao índice.

## 8. TurboVec mínimo sem LlamaIndex

Para scripts que já possuem embeddings como matrizes NumPy:

```python
import numpy as np
from turbovec import TurboQuantIndex

index = TurboQuantIndex(dim=768, bit_width=4)
index.add(chunk_embeddings)  # shape (n, 768)

scores, indices = index.search(query_embedding, k=5)

index.write("my_index.tv")
loaded = TurboQuantIndex.load("my_index.tv")
```

Combine com seu próprio chunker e`ollama embed`CLI ou HTTP API para incorporações.

## 9. RTX 1080 notas

| Preocupação | Orientação |
|--------|----------|
| **VRAM** | O modelo incorporado é pequeno;`qwen2.5-coder:7b`serve para 8 GB — consulte [Instalar e executar em RTX 1080](vi-install-and-run-rtx-1080.md) |
| **RAM** | O TurboVec compacta fortemente os vetores - grandes conjuntos de documentos permanecem menores que o float bruto32 FAISS |
| **Velocidade** | A ingestão é incorporada (Ollama); a pesquisa é rápida em CPU graças aos kernels SIMD |
| **Documentos de codificação** |`qwen2.5-coder:7b`+ sua marcação/código do repositório em`data/`|

Monitore durante a ingestão:

```bash
watch -n1 nvidia-smi
ollama ps
```

## 10. Opcional: expor como uma ferramenta MCP

Envolva a pesquisa em um servidor MCP personalizado para que Cursor possa chamar`search_handbook(query)`TÉCNICO.:

```text
MCP tool handler  →  embed query (Ollama)  →  TurboVec search  →  return top chunks as text
```

Consulte [Como criar seu MCP personalizado](../how-mcp-works/how-to-create-your-custom-mcp/i-overview.md).

## 11. Solução de problemas

| Problema | Correção |
|--------|-----|
|`connection refused`para Ollama |`ollama serve`; verificar`OLLAMA_BASE`|
| Incorporação errada dim | Usar`nomic-embed-text`(768) ou combinar`TurboQuantIndex(dim=…)`ao seu modelo incorporado |
| Respostas vazias | Mais pedaços em`data/`; aumentar`similarity_top_k`; verifique a codificação do arquivo |
| Ingestão lenta | Normal – incorpore cada pedaço uma vez; persistir e reutilizar`store/`|
|`persist`Erro JSON | Os metadados nos nós devem ser serializáveis ​​JSON |

## Relacionado

- [Baixando do Hugging Face](ii-downloading-from-huggingface.md) — se você mudar de modelos incorporados Ollama para HF
- [Vetor DB, habilidades e referência](../how-mcp-works/v-vector-db-skills-and-reference.md)
- [RAG para usuários](../custom-assistants-and-knowledge/iii-rag-and-knowledge-libraries.md)
