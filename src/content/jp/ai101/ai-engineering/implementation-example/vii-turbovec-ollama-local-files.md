---
label: "VII"
subtitle: "TurboVec + Ollama + ローカル ファイル"
group: "AI Applied"
order: 7
---
TurboVec + Ollama + ローカル ファイル

**完全にローカルな RAG** スタックを構築します。ファイルはディスク上に残り、**Ollama** が埋め込み、生成します。**[TurboVec](https://github.com/RyanCodrai/turbovec)** は圧縮ベクトルをディスクに保存します。クラウド API や管理ベクトル DB はありません。

ベクトル検索が MCP とスキルのどちらに適しているかについては、[Vector DB、スキルとリファレンス](../how-mcp-works/v-vector-db-skills-and-reference.md）。

## 1. TurboVec の機能

|ピース |役割 |
|------|------|
| **あなたのファイル** |真実の情報源 —`.md`、`.txt`、`.pdf`(テキスト抽出後)、コード、Runbook |
| **Ollama`nomic-embed-text`** |各チャンクを 768 次元の埋め込みベクトルに変換します。
| **ターボベック** |ベクトルを圧縮し (TurboQuant、デフォルトは 4 ビット)、高速な類似性検索を実行します。
| **Ollama LLM** (例:`qwen2.5-coder:7b`) |取得したチャンクと応答を読み取ります。

```text
Local files  →  chunk  →  Ollama embed  →  TurboVec index (.tvim + .nodes.json)
                                                              ↓
User question  →  embed  →  top-k chunks  →  prompt  →  Ollama LLM  →  answer
```

TurboVec は、それ自体は MCP サーバーではありません**。Python/LlamaIndex アプリ (または、後で作成する MCP ツールを呼び出す) の背後にある **検索エンジン**です。`search()`）。

## 2. 前提条件

```bash
# Ollama running
ollama serve   # or rely on systemd / app auto-start

# Embedding + chat models (768-dim embed matches TurboVec default path)
ollama pull nomic-embed-text
ollama pull qwen2.5-coder:7b    # coding; or qwen2.5:7b for general chat
```

|モデル |目的 | VRAM (おおよそ) |
|------|-------|------|
|`nomic-embed-text`|埋め込み |小規模 — オンデマンドでロード |
|`qwen2.5-coder:7b`|答え/コード | ~5 GB Q4 (GPU) |

Ollama を確認します:

```bash
curl http://localhost:11434/api/tags
```

## 3. Python 環境

```bash
python3 -m venv ~/local-rag-venv
source ~/local-rag-venv/bin/activate
pip install -U pip
pip install "turbovec[llama-index]" llama-index llama-index-llms-ollama llama-index-embeddings-ollama
```

|パッケージ |役割 |
|-------|------|
|`turbovec[llama-index]`|`TurboQuantVectorStore`— LlamaIndex シンプルストアのドロップイン |
|`llama-index`|チャンキング、インデックス作成、クエリ エンジン |
|`llama-index-llms-ollama`| Ollama 経由のチャット/完了 |
|`llama-index-embeddings-ollama`| Ollama による埋め込み |

## 4. ローカルファイルのレイアウト

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

インデックス付けが許可されている **のみ** ファイルを配置します`data/`。 TurboVec はチャンク テキストを永続化します`store/*.nodes.json`- 扱う`store/`敏感なほど。

## 5. ローカル ファイルを取り込み、インデックスを構築する

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

最初の実行では、Ollama を介してすべてのチャンクが埋め込まれます。大規模なコーパスでは時間がかかります。後でロードを実行します`store/`。

## 6. 質問する (クエリ エンジン)

同じファイルまたは別のファイルに追加`ask.py`:

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

回答は **あなたの** ファイルから取得されたチャンクに基づいています。回答テキスト内の引用を確認してください。

## 7. ファイル変更後のインデックスの再作成

|変更 |アクション |
|----------|----------|
|新しいファイルまたは編集されたファイル |インジェストを再実行する (または増分を書き込む)`add()`新しいドキュメントのみ) |
|新たに始める |消去`store/`そして再構築します |
|単一のドキュメントが削除されました |`vector_store.delete(ref_doc_id)`[TurboVec LlamaIndex ドキュメント](https://github.com/RyanCodrai/turbovec/blob/main/docs/integrations/llama_index.md) |

TurboVec は **オンライン インジェスト** をサポートしています。個別のトレーニング フェーズはありません。新しいベクトルがインデックスに追加されます。

## 8. LlamaIndex を使用しない最小限の TurboVec

すでに NumPy 配列として埋め込みがあるスクリプトの場合:

```python
import numpy as np
from turbovec import TurboQuantIndex

index = TurboQuantIndex(dim=768, bit_width=4)
index.add(chunk_embeddings)  # shape (n, 768)

scores, indices = index.search(query_embedding, k=5)

index.write("my_index.tv")
loaded = TurboQuantIndex.load("my_index.tv")
```

独自のチャンカーと組み合わせて、`ollama embed`埋め込みの場合は CLI または HTTP API。

## 9. RTX 1080 メモ

|懸念事項 |ガイダンス |
|----------|----------|
| **VRAM** |埋め込みモデルは小さいです。`qwen2.5-coder:7b`8 GB に適合 — [RTX 1080 でのインストールと実行](を参照)vi-install-and-run-rtx-1080.md) |
| **RAM** | TurboVec はベクトルを大幅に圧縮します。大きなドキュメント セットは生の float32 FAISS よりも小さいままです。
| **速度** |取り込みは埋め込みバインドされています (Ollama)。 SIMD カーネルのおかげで、CPU では検索が高速になります。
| **コーディングドキュメント** |`qwen2.5-coder:7b`+ リポジトリのマークダウン/コード`data/`|

取り込み中の監視:

```bash
watch -n1 nvidia-smi
ollama ps
```

## 10. オプション: MCP ツールとして公開します

Cursor が呼び出せるように、カスタム MCP サーバーで検索をラップします。`search_handbook(query)`:

```text
MCP tool handler  →  embed query (Ollama)  →  TurboVec search  →  return top chunks as text
```

[カスタム MCP の作成方法](../how-mcp-works/how-to-create-your-custom-mcp/i-overview.md）。

## 11. トラブルシューティング

|問題 |修正 |
|----------|-----|
|`connection refused`Ollama へ |`ollama serve`;チェック`OLLAMA_BASE`|
|間違った埋め込みディム |使用`nomic-embed-text`(768) または一致`TurboQuantIndex(dim=…)`埋め込みモデルへ |
|空の答え |より多くのチャンクが含まれる`data/`;増加`similarity_top_k`;ファイルのエンコーディングをチェックする |
|遅い取り込み |通常 — すべてのチャンクを 1 回埋め込みます。永続化と再利用`store/`|
|`persist`JSON エラー |ノード上のメタデータは JSON シリアル化可能である必要があります。

＃＃ 関連している

- [ハグフェイスからダウンロード](ii-downloading-from-huggingface.md) — Ollama から HF 埋め込みモデルに切り替える場合
- [Vector DB、スキルとリファレンス](../how-mcp-works/v-vector-db-skills-and-reference.md)
- [RAG ユーザー向け](../custom-assistants-and-knowledge/iii-rag-and-knowledge-libraries.md）
