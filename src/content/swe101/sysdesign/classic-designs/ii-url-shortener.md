---
label: "II"
subtitle: "URL短縮ツール"
group: "システム設計"
order: 2
---
URL短縮ツール

**Bitly スタイル** サービス: 短いリンクを作成し、長い URL に **リダイレクト**し、オプションで **分析** します。

## 1. 要件

|機能性 |機能しない |
|-----------|----------------|
|長い URL から短い URL を作成 |低いリダイレクト遅延 (p99 < 50 ms) |
| Redirect short → long | Highly **read-heavy** |
| Optional expiry, custom alias | 99.9%+ availability |
| Click analytics (async OK) | Scale: see below |

**Scale (example):** 100 M URLs created/day; 10 B redirects/day → ~**115 K reads/s** average (peaks higher).

## 2. API sketch

| Method | Path | Purpose |
|--------|------|---------|
| POST | 0 | Create 1 → 2 |
| GET | 3 | **302/301** redirect to long URL |
| GET | 4 | Analytics (authenticated) |

## 3. Short key generation

| Approach | How | Pros | Cons |
|----------|-----|------|------|
| **Hash + truncate** | MD5/SHA of URL → base62 first 7 chars | Stateless | Collisions — must check DB |
| **Counter + base62** | Global counter → encode | No collision | Single counter hotspot |
| **KGS pool** | Key Generation Service pre-allocates batches | Fast insert, no collision at write | Extra service |

Base62 charset: 5 → 7 chars ≈ 62^7 ≈ 3.5 trillion keys.

## 4. Data model

| Column | Type | Notes |
|--------|------|-------|
| 6 | VARCHAR PK | 7–8 chars |
| 7 | TEXT | Target |
| 8 | BIGINT | Optional owner |
| 9 | TIMESTAMP | |
| 10 | TIMESTAMP | Nullable |

**Shard key:** hash(11) → N DB shards.

## 5. Redirect: 301 vs 302

| Code | Browser behavior | Analytics |
|------|------------------|-----------|
| **301** Permanent | May cache redirect — fewer origin hits | Under-counts clicks |
| **302** Temporary | Hits server every click | Accurate counts |

Product choice: **302** for analytics; **301** + async click log if load dominates.

<figure class="notes-diagram"><svg xmlns="14 viewBox="0 0 440 120" role="img" aria-label="URL shortener read path with cache">)
  <rect x="12" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">クライアント</text>
  <path d="M68 60 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="44" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="64" fill="#e4e4e7" font-size="9">レディス</text>
  <text x="108" y="88" fill="#86efac" font-size="8">キャッシュアサイド ヒット</text>
  <path d="M172 60 H212" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 3"/>
  <rect x="212" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="220" y="64" fill="#e4e4e7" font-size="9">DBシャード</text>
  <path d="M268 60 H308" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="308" y="44" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="316" y="64" fill="#e4e4e7" font-size="9">302リダイレクト</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">リダイレクトホットパス</text>
</svg></figure>

## 6. 読み取りのスケーリング

1. **Redis** キャッシュアサイド: `GET short:{code}` → 長い URL。 TTL + LRU エビクション。
2. 人気のあるリンクのエッジで **CDN** (分析が重要な場合は短い TTL)。
3. `short_code` ハッシュによる **DB シャーディング**。
4. **分析:** 非同期 — イベント → Kafka → Flink → ClickHouse をクリックします (リダイレクトをブロックしないでください)。

## 7. ボトルネック

|リスク |緩和 |
|------|-----------|
|ホットショートリンク | CDN + ローカル キャッシュ |
| KGSシングルポイント |パーティション化された範囲を持つ複数の KGS インスタンス |
|シャードの不均衡 |一貫したハッシュ。再シャード計画 |

**関連:** スケーラブル パターン [CDN およびエッジ キャッシュ](../scalable-patterns/vi-cdn-and-edge-caching.md)、パート I キャッシュ/シャーディング。
