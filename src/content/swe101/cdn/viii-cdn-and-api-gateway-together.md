---
label: "VIII"
subtitle: "CDN と API ゲートウェイの併用"
group: "CDN"
order: 8
---
CDN と API ゲートウェイ — それらがどのように連携するか

**CDN** と **API ゲートウェイ** はシステムの **エッジ** に位置しますが、さまざまな問題を解決します。運用スタックでは、キャッシュ可能なバイトには CDN、**動的 API トラフィック**にはゲートウェイの**両方**を使用することがよくあります。ゲートウェイの完全な詳細は、[API ゲートウェイ](../api-gateway/i-overview.md) トラックに記載されています。

クラウド アーキテクチャのフレーム構成 (ノース-サウス vs メッシュ) については、[API ゲートウェイとサービス メッシュ](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md) を参照してください。

## 1. 2 つのレイヤー、1 つのクライアント リクエスト

```text
Browser / mobile app
        │
        ▼
   ┌─────────┐
   │   CDN   │  Static: /assets/*, some GET /public/*
   └────┬────┘
        │ cache MISS or non-cacheable path
        ▼
   ┌─────────────┐
   │ API Gateway │  /api/* — auth, rate limit, route
   └──────┬──────┘
          ▼
   ALB / K8s Ingress / Lambda / microservices
```

|コンポーネント |主な仕事 |典型的なパス |
|----------|---------------|----------|
| **CDN** | **応答をユーザーの近くにキャッシュします | `*.js`、`*.css`、画像、キャッシュ可能な GET |
| **API ゲートウェイ** |動的リクエストの **ルート + ポリシー** | `/api/v1/*`、パートナー Webhook |
| **オリジン / サービス** |ビジネスロジック、データベース |ゲートウェイの背後のみ |

CDN は次のように答えます。「**保存されたコピー** を提供できますか?」  
ゲートウェイは、「**このクライアントは誰**ですか、**許可されています**、**どのサービス**がそれを処理しますか?」と答えます。

## 2. 一般的な組み合わせトポロジー

### Web アプリ + REST API (AWS スタイル)

```text
CloudFront (CDN)
  ├── /assets/*     → S3 origin (long TTL)
  ├── /index.html   → S3 (short TTL)
  └── /api/*        → API Gateway → Lambda or ALB → services
```

1 つのホスト名 (`app.example.com`) または分割 (`cdn.` 対 `api.`)。

### SPA + 別個の API ドメイン

```text
cdn.example.com   → CDN → S3 (static only)
api.example.com   → API Gateway → services (no CDN cache on authenticated routes)
```

明確な分離 — プライベート JSON でのキャッシュミスが減少します。

### Cloudflare はすべてをプロキシします

```text
Orange-cloud DNS → CDN/WAF edge
  ├── Cache static by path rule
  └── /api/* → bypass cache → origin or Workers → upstream
```

ゲートウェイ機能は、**Cloudflare API シールド**、**Workers**、またはオリジン **Kong/NGINX** です。

## 3. 各層が行うべきこと

|懸念事項 | CDN | APIゲートウェイ |
|----------|-----|---------------|
| **TLS** |はい — 公開証明書 |多くの場合、はい (または CDN が最初に終了します)。
| **キャッシュGET** |はい — ヘッダーで許可されている場合 |認証された API をほとんどキャッシュしない |
| **JWT / API キーの検証** |回避 — ゲートウェイを使用 |はい |
| **レート制限** |基本 (プロバイダー WAF) |プライマリ — キー/ユーザーごと ([レート制限](../sysdesign/scalable-patterns/iv-rate-limiting.md)) |
| **パスルーティング** |パスによる原点選択 |サービスルーティング`/orders`→orders-svc |
| **WAF / DDoS** | CDNエッジ |ゲートウェイ + CDN の組み合わせ |
| **リクエスト ID / トレース** |エッジではオプション | `X-Request-Id` を挿入、コンテキストをトレース |

**シン ゲートウェイ:** 検証、ルーティング、制限 — ゲートウェイ構成のビジネス ルールではありません。

## 4. リクエストのウォークスルー

**静的アセット (キャッシュ ヒット):**

```text
GET /assets/main.a1b2.js
  → CDN edge HIT → 200 (origin never touched)
```

**ログイン API (CDN キャッシュなし):**

```text
POST /api/v1/auth/login
  → CDN BYPASS (POST never cached)
  → API Gateway: rate limit, optional WAF
  → auth-service → 200 + Set-Cookie
  → Cache-Control: no-store on response
```

**パブリック構成 GET (オプションの CDN キャッシュ):**

```text
GET /api/v1/public/config
  → CDN MISS → Gateway → config-service
  → Cache-Control: public, max-age=120
  → CDN stores; next user in region HIT
```

`/api/me` がキャッシュしないように CDN **動作**を構成します。[API と動的コンテンツ](vi-apis-and-dynamic-content.md) を参照してください。

## 5. TLS とホスト名のフロー

```text
Client ──HTTPS──► CDN (cert: app.example.com)
                      ├── static → S3
                      └── /api → HTTPS → API Gateway (custom origin)
                                      └── HTTPS → internal ALB
```

**CDN** および **ゲートウェイ** の証明書は、クライアントが使用するホスト名と一致する必要があります。 Origin は VPC 内のプライベート CA を使用できます。

## 6. 1 つだけ必要な場合

|セットアップ | | いつでも十分です。
|------|-----------|
| **CDN のみ** |静的サイト、パブリック API なし |
| **ゲートウェイのみ** |内部 API、グローバル静的アセットなし |
| **両方** |典型的な SaaS — SPA + 認証済み API + グローバル ユーザー |

## 7. 組み合わせる際の落とし穴

|落とし穴 |修正 |
|----------|-----|
| CDN キャッシュ `/api/user` |バイパスまたは `no-store`;別の `api.` ホスト |
|ゲートウェイのタイムアウト < CDN タイムアウト |タイムアウトを調整します。 CDN が待機し、クライアントがハングします。
| CORS はゲートウェイのみ | CDN は `Origin` を転送する必要があります。どちらも一貫して CORS ヘッダーを発行します。
|アプリ内のみのレート制限 |最初にゲートウェイで強制します — アプリは最後の行です |
|ダブルgzip | 1 つのレイヤーのみで圧縮 |

## 8. 次にどこへ行くか

|トピック |注 |
|------|------|
| **API ゲートウェイ トラック** | [概要](../api-gateway/i-overview.md) — ルーティング、認証、プロバイダー |
| **CDN オペレーション** | [操作とトラブルシューティング](vii-operations-and-troubleshooting.md) |
| **レート制限** | [レート制限](../sysdesign/scalable-patterns/iv-rate-limiting.md) |
| **Redis リミッター** | [Redis パターン](../redis/iv-patterns-and-use-cases.md) — アプリ層の補完 |
