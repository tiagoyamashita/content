---
label: "V"
subtitle: "Search systems"
group: "System design"
order: 5
---
Search systems
**Full-text** and **semantic** search need indexes optimized for lookup by **term** or **vector**, not row-by-row table scans.

## 1. Inverted index

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

## 2. Write and read paths

**Write path**

1. Document arrives (JSON, row).
2. **Tokenise** — split text, remove stop words (optional).
3. **Normalise** — lowercase, stem (“running” → “run”).
4. Update **shards** of the index (Elasticsearch primary shard + replicas).

**Read path**

1. Parse query (boolean, phrase, fuzzy).
2. Fetch posting lists per term.
3. **Score** — BM25 / TF-IDF (+ boosts, filters).
4. Return ranked hits + highlights.

## 3. Keeping DB and index in sync

| Strategy | Flow | Risk |
|----------|------|------|
| **Dual-write** | App writes DB + ES in parallel | Partial failure → drift |
| **CDC** | DB binlog → Kafka → indexer | Eventual lag; industry standard |
| **Batch rebuild** | Nightly full reindex | Stale until job completes |

**CDC stack (common):** Debezium reads Postgres/MySQL WAL → Kafka topic → Elasticsearch sink connector.

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

## 4. Elasticsearch concepts (brief)

| Concept | Role |
|---------|------|
| **Index** | Logical namespace (like a DB) |
| **Shard** | Horizontal partition of index |
| **Replica** | Copy for read scale + failover |
| **Near-real-time** | Refresh interval (~1s default) before search visible |

## 5. Vector / semantic search

| Step | Action |
|------|--------|
| Index time | Embed document text → store vector + metadata |
| Query time | Embed query → **ANN** search (HNSW, IVF) |
| Hybrid | **BM25** keyword + vector score → **RRF** fusion |

Products: pgvector, Pinecone, OpenSearch k-NN, Elasticsearch dense_vector.

## 6. Interview checklist

- Why inverted index beats `LIKE` at scale?
- Dual-write failure modes?
- How CDC handles deletes and updates?
- When hybrid search beats pure vector?

**Related:** [Message queues & async](iii-message-queues-and-async.md) (Kafka), Part I (SQL vs search store).
