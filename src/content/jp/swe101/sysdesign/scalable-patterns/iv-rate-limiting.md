---
label: "IV"
subtitle: "レート制限"
group: "システム設計"
order: 4
---
レート制限

**レート制限** は、クライアント (ユーザー、IP、API キー) がウィンドウ内で実行できるリクエストの数を制限し、コスト、公平性、安定性を保護します。

## 1. なぜ制限するのか

|目標 |例 |
|-----|----------|
| **虐待防止** |スクレイピング、クレデンシャルスタッフィング |
| **公平性** |無料枠 100 リクエスト/分と有料枠 10,000 |
| **コスト管理** |高価な LLM または GPU エンドポイント |
| **安定性** | 1 つのテナントによる共有 DB の飽和を防ぐ |

## 2. アルゴリズム

### トークンバケット

- バケットには最大で **B** トークンが保持されます。 **R** トークン/秒で補充されます。
- 各リクエストには **1** トークンがかかります。空のバケツ→拒否。

|パラム |効果 |
|------|----------|
|大 **B** | B まで **バースト** が可能 |
|高 **R** |持続的なスループットの上限 |

### 漏れのあるバケツ

- リクエストは**キュー**に入ります。 **固定レート**で処理されます。
- キューがいっぱい→ドロップ。 **スムーズ** バースト (大きなスパイクはありません)。

### 固定ウィンドウカウンター

- 暦分ごとのリクエストの数。境界でリセットします。
- **欠陥:** ウィンドウの端で 2 回のバースト (隣接する 2 分間で 599 + 599)。

### スライディング ウィンドウ ログ

- リクエストごとにタイムスタンプを保存します。最後の **T** 秒間のカウント。
- **正確な**; QPS が高いとメモリが重くなります。

### 引き違い窓カウンター

- 以前のウィンドウ数と現在のウィンドウ数をブレンドします — 精度とメモリの適切なバランス (Redis 実装で一般的)。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Token bucket allows burst then steady rate">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Token bucket (B=5, R=1/s)</text>
  <rect x="12" y="32" width="120" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="24" y="48" fill="#e4e4e7" font-size="9">●●●●● tokens</text>
  <text x="140" y="48" fill="#a1a1aa" font-size="9">5 rapid requests OK</text>
  <rect x="12" y="64" width="120" height="24" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="80" fill="#e4e4e7" font-size="9">○ empty</text>
  <text x="140" y="80" fill="#f87171" font-size="9">6th rejected until refill</text>
</svg></figure>

## 3. 比較表

|アルゴリズム |バーストフレンドリー |メモリ |エッジケース |
|----------|-----|----------|----------|
|トークンバケット |はい (制限あり) |低い |チューンB vs R |
|漏れやすいバケツ |いいえ |キューのサイズ |定常出力のみ |
|固定ウィンドウ |境界ではい |低い |エッジでのダブルバースト |
|スライディングウィンドウログ |制御された |高 |リクエストごとのタイムスタンプ |
|引き違い窓カウンター |制御された |中 |本番環境で人気 |

## 4. どこで強制するか

|レイヤー |長所 |短所 |
|------|------|------|
| **API Gateway** |中央ポリシー、WAF 統合 |単一構成の爆発半径 |
| **サービス メッシュ** |ルートごとの制限 |運用の複雑さ |
| **アプリ + Redis** |きめ細かいビジネス ルール |すべてのサービスは | を実装する必要があります。
| **CDN / エッジ** |発信元の前に悪用をブロック |限定されたロジック |

**Key dimensions:** `user_id`, `api_key`, `IP`, `tenant_id`, route (`POST /v1/generate`).

## 5. クライアントの応答

```http
HTTP/1.1 429 Too Many Requests
Retry-After: 42
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716120060
```

API ドキュメントのドキュメント制限。クライアントはジッタを急激に**後退**する必要があります。

## 6. 分散レート制限

Multiple API instances need a **shared counter** — typically **Redis** (`INCR` + `EXPIRE`, or sliding window Lua script). Clock skew matters for window boundaries; prefer monotonic TTL keys.

**Related:** [API design](ii-api-design.md) (429 status), Part I caching (Redis).
