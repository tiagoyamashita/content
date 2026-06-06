---
label: "II"
subtitle: "URL 短縮ツール"
group: "システム設計"
order: 2
---
URL 短縮ツール

**Bitly スタイル** サービス: 短いリンクを作成し、長い URL への **リダイレクト**、オプションの **分析**。

## 1. 要件

|機能性 |機能しない |
|-----------|----------------|
|長い URL から短い URL を作成する |低いリダイレクト遅延 (p99 < 50 ミリ秒) |
|短い→長いへリダイレクト |非常に **読み取り負荷が高い** |
|オプションの有効期限、カスタムエイリアス | 99.9% 以上の可用性 |
|クリック分析 (非同期 OK) |スケール: 以下を参照 |

**規模 (例):** 1 日あたり 1 億の URL が作成されます。 1 日あたり 10 億のリダイレクト → 平均 ~**115,000 読み取り/秒** (ピークはさらに高くなります)。

## 2. API スケッチ

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/v1/urls` | Create `{ long_url, custom_alias?, ttl? }` → `{ short_url }` |
| GET | `/{short_code}` | **302/301** redirect to long URL |
| GET | `/v1/urls/{code}/stats` | Analytics (authenticated) |

## 3. 短い鍵の生成

|アプローチ |どのように |長所 |短所 |
|----------|-----|------|------|
| **ハッシュ + トランケート** | URL の MD5/SHA → Base62 の最初の 7 文字 |無国籍 |衝突 — DB を確認する必要があります |
| **カウンター + Base62** |グローバルカウンター → エンコード |衝突なし |シングルカウンターホットスポット |
| **KGS プール** |キー生成サービスはバッチを事前に割り当てます。高速挿入、書き込み時の衝突なし |追加サービス |

Base62 charset: `[a-zA-Z0-9]` → 7 chars ≈ 62^7 ≈ 3.5 trillion keys.

## 4. データモデル

| Column | Type | Notes |
|--------|------|-------|
| `short_code` | VARCHAR PK | 7–8 chars |
| `long_url` | TEXT | Target |
| `user_id` | BIGINT | Optional owner |
| `created_at` | TIMESTAMP | |
| `expires_at` | TIMESTAMP | Nullable |

**Shard key:** hash(`short_code`) → N DB shards.

## 5. リダイレクト: 301 対 302

|コード |ブラウザの動作 |分析 |
|------|-------|-----------|
| **301** 常設 |リダイレクトをキャッシュする可能性があります - オリジン ヒットが少なくなります |クリック数を過少カウント |
| **302** 一時的 |クリックするたびにサーバーにアクセスします |正確なカウント |

製品の選択: **302** 分析用。 **301** + 負荷が優勢な場合の非同期クリック ログ。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="URL shortener read path with cache">
  <rect x="12" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">Client</text>
  <path d="M68 60 H108" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="108" y="44" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="64" fill="#e4e4e7" font-size="9">Redis</text>
  <text x="108" y="88" fill="#86efac" font-size="8">cache-aside hit</text>
  <path d="M172 60 H212" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 3"/>
  <rect x="212" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="220" y="64" fill="#e4e4e7" font-size="9">DB shard</text>
  <path d="M268 60 H308" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="308" y="44" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="316" y="64" fill="#e4e4e7" font-size="9">302 redirect</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Redirect hot path</text>
</svg></figure>

## 6. 読み取りのスケーリング

1. **Redis** cache-aside: `GET short:{code}` → long URL; TTL + LRU eviction.
2. **CDN** at edge for popular links (short TTL if analytics matter).
3. **DB sharding** by `short_code` hash.
4. **Analytics:** async — click event → Kafka → Flink → ClickHouse (don’t block redirect).

## 7. ボトルネック

|リスク |緩和 |
|------|-----------|
|ホットショートリンク | CDN + ローカル キャッシュ |
| KGS シングルポイント |パーティション化された範囲を持つ複数の KGS インスタンス |
|シャードの不均衡 |一貫したハッシュ。再シャード計画 |

**Related:** Scalable patterns [CDN & edge caching](../scalable-patterns/vi-cdn-and-edge-caching.md), Part I caching/sharding.
