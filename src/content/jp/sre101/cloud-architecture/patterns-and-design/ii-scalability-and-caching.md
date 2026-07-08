---
label: "II"
subtitle: "スケーラビリティとキャッシュ"
group: "クラウドアーキテクチャ"
order: 2
---
スケーラビリティとキャッシュ

コンピューティングの**スケーリング**と繰り返しの読み取りの**オフロード**により、増大に対処します。クラウドの自動スケーリングは、**ステートレス** アプリケーション層を前提としています。

## 1. 垂直スケーリングと水平スケーリング

| | Vertical (scale up) | Horizontal (scale out) |
|---|---------------------|------------------------|
| Action | Bigger VM (more CPU/RAM) | More instances behind LB |
| Pros | Simple, no code change | High ceiling, fault tolerant |
| Cons | Hard ceiling, SPOF | App must be stateless or shared state |
| Cloud example | `t3.micro` → `t3.xlarge` | ASG 2 → 20 EC2 instances |

```text
Vertical:  [====      ]  →  [============]
Horizontal: [==] [==]     →  [==] [==] [==] [==] [==]
            load balancer distributes requests
```

## 2. ステートレス サービス

各リクエストには、**任意**のインスタンスが処理できる十分なコンテキストが含まれている必要があります。

|ステートフル (スケールアウトには悪い) |無国籍 (良い) |
|----------------------------|---------------|
| JVM メモリ内のセッション | JWT または Redis のセッション |
|ローカル ファイル アップロード キャッシュ | S3 署名済みアップロード |
|インメモリショッピングカート | DB/Redis のカート |

```http
GET /api/orders HTTP/1.1
Authorization: Bearer eyJhbG...
X-Request-Id: 7f3a9c2e-...
```

ロード バランサーの背後にある任意のポッドがリクエストを処理できます。

## 3. オートスケーリング

**AWS Auto Scaling グループ** (類似: Azure VMSS、GKE HPA):

|ポリシーの種類 |行動 |
|---------------|----------|
| **ターゲット追跡** |指標を目標値に維持する (例: CPU 60%) — 最も単純 |
| **ステップスケーリング** | CPU > 80% の場合、N 個のインスタンスを追加します。
| **予定** |既知のピークの前にスケールアップ (ブラック フライデー) |

```yaml
# Conceptual ASG target tracking
TargetValue: 60.0
PredefinedMetricType: ASGAverageCPUUtilization
ScaleOutCooldown: 300   # seconds — prevent thrashing
ScaleInCooldown: 300
```

|設定 |なぜ |
|----------|-----|
| **クールダウン** |ノイズの多いメトリクスでの追加/削除ループを回避する |
| **最小/最大/希望** | HA の下限、コストの上限 |
| **健康診断** | LB は、スケールインの前に異常なインスタンスの登録を解除します。

## 4. レイヤーのキャッシュ

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" role="img" aria-label="Cache tiers CDN Redis read replica">
  <rect x="12" y="36" width="72" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="56" fill="#e4e4e7" font-size="9">CDN edge</text>
  <path d="M84 52 H104" stroke="#a1a1aa"/>
  <rect x="104" y="36" width="72" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="116" y="56" fill="#e4e4e7" font-size="9">Redis</text>
  <path d="M176 52 H196" stroke="#a1a1aa"/>
  <rect x="196" y="36" width="88" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="208" y="56" fill="#e4e4e7" font-size="9">Read replica</text>
  <path d="M284 52 H304" stroke="#a1a1aa"/>
  <rect x="304" y="36" width="72" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="316" y="56" fill="#e4e4e7" font-size="9">Primary DB</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Closer to user = lower latency</text>
</svg></figure>

|レイヤー |店舗 | TTL / 無効化 |
|------|--------|--------|
| **CDN** (CloudFront、Cloudflare) |静的アセット、キャッシュ可能な GET APIs |キャッシュ制御ヘッダー |
| **インメモリ** (Redis、Memcached) |ホット行、セッション、レート制限 |キー TTL、パブリッシュ/サブスクライブの無効化 |
| **リードレプリカ** | DB の完全なコピー |非同期レプリケーションの遅延 |
| **アプリケーション** |計算された集計 |ローカルカフェイン — 古くなったものに注意 |

## 5. キャッシュアサイドパターン

```text
1. GET key from Redis
2. Miss → read DB → SET Redis → return
3. Write → update DB → DELETE Redis key (or update)
```

|落とし穴 |緩和 |
|-----------|-----------|
| **キャッシュスタンピード** |シングルフライト ロック、合体要求 |
| **古い記事** |短い TTL + 書き込み時の無効化 |
| **ホットキー** |シャード キー、ローカル L1 キャッシュ |

## 6. 読み取りと書き込みのスケーリング

|ボトルネック |パターン |
|-----------|-----------|
|読み取りが多い |レプリカ + Redis + CDN |
|書き込みが多い |シャーディング、キューバック書き込み、パーティションキー |
|混合 | CQRS — 個別の読み取りモデルと書き込みモデル |

## 7. 例: 電子商取引の商品ページ

```text
User → CloudFront (product image, static JS)
     → ALB → API pods (stateless, HPA on CPU)
     → Redis (product catalog cache, 5 min TTL)
     → RDS primary (orders) + read replica (browse catalog)
```

要求レートに応じて API ポッドをスケールします。デプロイ時に Redis をウォームします。転送されたバイトの 90% が CDN です。

## 8. アンチパターン

|アンチパターン |修正 |
|--------------|-----|
| LB のスティッキー セッション |セッションを外部化 |
| DB を垂直方向に永遠に拡大縮小する |リードレプリカ、キャッシュ、シャード |
| TTL を使用せずにすべてをキャッシュする |鮮度要件を定義する |
|根本原因のないインシデント中のスケールアウト |まずリーク/OOM を修正してください |

**Related:** [Microservices vs monolith](iii-microservices-vs-monolith.md), system design scalable-patterns CDN note.
