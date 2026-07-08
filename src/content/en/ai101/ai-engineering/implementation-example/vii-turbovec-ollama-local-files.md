---
label: "VII"
subtitle: "TurboVec + Ollama + local files"
group: "AI Applied"
order: 7
---
TurboVec + Ollama + local files

Build a **fully local RAG** stack: your files stay on disk, **Ollama** embeds and generates, **[TurboVec](https://github.com/RyanCodrai/turbovec)** stores compressed vectors on disk — no cloud APIs, no managed vector DB.

For when vector search fits vs MCP vs skills, see [Vector DB, skills & reference](../how-mcp-works/v-vector-db-skills-and-reference.md).

## 1. What TurboVec does

| Piece | Role |
|-------|------|
| **Your files** | Source of truth — `.md`, `.txt`, `.pdf` (after text extract), code, runbooks |
| **Ollama `nomic-embed-text`** | Turns each chunk into a 768-dim embedding vector |
| **TurboVec** | Compresses vectors (TurboQuant, 4-bit default) and runs fast similarity search |
| **Ollama LLM** (e.g. `qwen2.5-coder:7b`) | Reads retrieved chunks and answers |

```text
Local files  →  chunk  →  Ollama embed  →  TurboVec index (.tvim + .nodes.json)
                                                              ↓
User question  →  embed  →  top-k chunks  →  prompt  →  Ollama LLM  →  answer
```

TurboVec is **not** an MCP server by itself — it is the **retrieval engine** behind a Python/LlamaIndex app (or an MCP tool you write later that calls `search()`).

## 2. Prerequisites

```bash
# Ollama running
ollama serve   # or rely on systemd / app auto-start

# Embedding + chat models (768-dim embed matches TurboVec default path)
ollama pull nomic-embed-text
ollama pull qwen2.5-coder:7b    # coding; or qwen2.5:7b for general chat
```

| Model | Purpose | VRAM (approx) |
|-------|---------|---------------|
| `nomic-embed-text` | Embeddings | Small — loads on demand |
| `qwen2.5-coder:7b` | Answers / code | ~5 GB Q4 on GPU |

Verify Ollama:

```bash
curl http://localhost:11434/api/tags
```

## 3. Python environment

```bash
python3 -m venv ~/local-rag-venv
source ~/local-rag-venv/bin/activate
pip install -U pip
pip install "turbovec[llama-index]" llama-index llama-index-llms-ollama llama-index-embeddings-ollama
```

| Package | Role |
|---------|------|
| `turbovec[llama-index]` | `TurboQuantVectorStore` — drop-in for LlamaIndex simple store |
| `llama-index` | Chunking, indexing, query engine |
| `llama-index-llms-ollama` | Chat/completion via Ollama |
| `llama-index-embeddings-ollama` | Embeddings via Ollama |

## 4. Local file layout

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

Put **only** files you are allowed to index in `data/`. TurboVec persists chunk text in `store/*.nodes.json` — treat `store/` as sensitive.

## 5. Ingest local files and build the index

`ingest_and_ask.py`:

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

First run embeds every chunk through Ollama — slow on large corpora; later runs load from `store/`.

## 6. Ask questions (query engine)

Add to the same file or a separate `ask.py`:

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

Answers are grounded in chunks retrieved from **your** files — verify citations in the response text.

## 7. Re-index after file changes

| Change | Action |
|--------|--------|
| New or edited files | Re-run ingest (or write incremental `add()` for new docs only) |
| Start fresh | Delete `store/` and rebuild |
| Single doc removed | `vector_store.delete(ref_doc_id)` per [TurboVec LlamaIndex docs](https://github.com/RyanCodrai/turbovec/blob/main/docs/integrations/llama_index.md) |

TurboVec supports **online ingest** — no separate training phase; new vectors append to the index.

## 8. Minimal TurboVec without LlamaIndex

For scripts that already have embeddings as NumPy arrays:

```python
import numpy as np
from turbovec import TurboQuantIndex

index = TurboQuantIndex(dim=768, bit_width=4)
index.add(chunk_embeddings)  # shape (n, 768)

scores, indices = index.search(query_embedding, k=5)

index.write("my_index.tv")
loaded = TurboQuantIndex.load("my_index.tv")
```

Pair with your own chunker and `ollama embed` CLI or HTTP API for embeddings.

## 9. RTX 1080 notes

| Concern | Guidance |
|---------|----------|
| **VRAM** | Embed model is small; `qwen2.5-coder:7b` fits 8 GB — see [Install & run on RTX 1080](vi-install-and-run-rtx-1080.md) |
| **RAM** | TurboVec compresses vectors heavily — large doc sets stay smaller than raw float32 FAISS |
| **Speed** | Ingest is embed-bound (Ollama); search is fast on CPU thanks to SIMD kernels |
| **Coding docs** | `qwen2.5-coder:7b` + your repo markdown/code in `data/` |

Monitor during ingest:

```bash
watch -n1 nvidia-smi
ollama ps
```

## 10. Optional: expose as an MCP tool

Wrap search in a custom MCP server so Cursor can call `search_handbook(query)`:

```text
MCP tool handler  →  embed query (Ollama)  →  TurboVec search  →  return top chunks as text
```

See [How to create your custom MCP](../how-mcp-works/how-to-create-your-custom-mcp/i-overview.md).

## 11. Troubleshooting

| Problem | Fix |
|---------|-----|
| `connection refused` to Ollama | `ollama serve`; check `OLLAMA_BASE` |
| Wrong embedding dim | Use `nomic-embed-text` (768) or match `TurboQuantIndex(dim=…)` to your embed model |
| Empty answers | More chunks in `data/`; increase `similarity_top_k`; check file encoding |
| Slow ingest | Normal — embed every chunk once; persist and reuse `store/` |
| `persist` JSON error | Metadata on nodes must be JSON-serializable |

## Related

- [Downloading from Hugging Face](ii-downloading-from-huggingface.md) — if you switch from Ollama to HF embed models
- [Vector DB, skills & reference](../how-mcp-works/v-vector-db-skills-and-reference.md)
- [RAG for users](../custom-assistants-and-knowledge/iii-rag-and-knowledge-libraries.md)
