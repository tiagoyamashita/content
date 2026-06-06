---
label: "V"
subtitle: "検索システム"
group: "システム設計"
order: 5
---
検索システム

**全文**検索と**セマンティック**検索には、行ごとのテーブル スキャンではなく、**用語**または**ベクトル**による検索用に最適化されたインデックスが必要です。

## 1. 転置インデックス

Maps each **token** → list of `(document_id, positions)`.

```text
"quick"  → [(doc1, [0]), (doc7, [3])]
"brown"  → [(doc1, [1]), (doc9, [0])]
```

| Relational DB | Search index |
|---------------|--------------|
| `WHERE body LIKE '%foo%'` | O(n) scan | Posting list lookup |
| Good for exact PK lookups | Good for relevance ranking |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Inverted index from documents to term postings">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Inverted index</text>
  <rect x="12" y="36" width="80" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="58" fill="#e4e4e7" font-size="9">doc1: quick brown</text>
  <path d="M92 54 H120" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="120" y="32" width="72" height="22" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="132" y="47" fill="#e4e4e7" font-size="8">quick→doc1</text>
  <rect x="120" y="58" width="72" height="22" rx="2" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="132" y="73" fill="#e4e4e7" font-size="8">brown→doc1</text>
  <text x="12" y="100" fill="#a1a1aa" font-size="9">Query "quick brown" → intersect posting lists → score (BM25)</text>
</svg></figure>

## 2. 書き込みパスと読み取りパス

**書き込みパス**

1. ドキュメントが到着します (JSON、行)。
2. **トークン化** — テキストを分割し、ストップワードを削除します (オプション)。
3. **正規化** — 小文字、語幹 (「running」→「run」)。
4. インデックスの **シャード** (Elasticsearch プライマリ シャード + レプリカ) を更新します。

**読み取りパス**

1. クエリを解析します (ブール値、フレーズ、ファジー)。
2. 学期ごとに投稿リストを取得します。
3. **スコア** — BM25 / TF-IDF (+ ブースト、フィルター)。
4. ランク付けされたヒット + ハイライトを返します。

## 3. DB とインデックスの同期を維持する

|戦略 |フロー |リスク |
|----------|------|------|
| **二重書き込み** |アプリは DB + ES を並行して書き込みます。部分故障→ドリフト |
| **CDC** | DB binlog → Kafka → インデクサー |最終的な遅れ。業界標準 |
| **バッチリビルド** |夜間の完全なインデックスの再作成 |ジョブが完了するまで古い |

**CDC スタック (共通):** Debezium は Postgres/MySQL WAL → Kafka トピック → Elasticsearch シンク コネクタを読み取ります。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 100" role="img" aria-label="CDC from database to search index">
  <rect x="12" y="40" width="64" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="60" fill="#e4e4e7" font-size="9">OLTP DB</text>
  <path d="M76 56 H120" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="120" y="40" width="64" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="132" y="60" fill="#e4e4e7" font-size="9">CDC</text>
  <path d="M184 56 H228" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="228" y="40" width="64" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="240" y="60" fill="#e4e4e7" font-size="9">Kafka</text>
  <path d="M292 56 H336" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="336" y="40" width="88" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="348" y="60" fill="#e4e4e7" font-size="9">Elasticsearch</text>
</svg></figure>

## 4. Elasticsearch の概念 (概要)

|コンセプト |役割 |
|-------|------|
| **インデックス** |論理名前空間 (DB など) |
| **シャード** |インデックスの水平パーティション |
| **レプリカ** |読み取りスケール + フェイルオーバー用のコピー |
| **ほぼリアルタイム** |検索が表示されるまでの更新間隔 (デフォルトは約 1 秒) |

## 5. ベクトル/セマンティック検索

|ステップ |アクション |
|------|----------|
|インデックス時間 |ドキュメントテキストを埋め込む → ベクター + メタデータを保存 |
|クエリ時間 |クエリを埋め込む → **ANN** 検索 (HNSW、IVF) |
|ハイブリッド | **BM25** キーワード + ベクトル スコア → **RRF** 融合 |

製品: pgvector、Pinecone、OpenSearch k-NN、Elasticsearchdensity_vector。

## 6. 面接チェックリスト

- Why inverted index beats `LIKE` at scale?
- Dual-write failure modes?
- How CDC handles deletes and updates?
- When hybrid search beats pure vector?

**Related:** [Message queues & async](iii-message-queues-and-async.md) (Kafka), Part I (SQL vs search store).
