---
label: "I"
subtitle: "概要"
group: "API Gateway"
order: 1
---
API ゲートウェイ — 概要

**API ゲートウェイ** は、バックエンドへのクライアント トラフィックの **単一のパブリック エントリ**です。リクエストをサービスに**ルーティング**し、TLS、認証、レート制限、リクエスト変換、可観測性フックなどの**横断的なポリシー**を適用します。

**CDN** caches static and some GET responses at the edge; **gateway** handles **dynamic API** traffic. Most SaaS stacks use both — see [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md).

For architecture patterns (north-south vs service mesh), see [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md).

## このトラックの地図

|パート |フォーカス |
|------|----------|
| **I — 概要** |役割、ロード バランサー、CDN |
| **II — ゲートウェイの仕組み** |リクエスト フロー、南北トラフィック |
| **III — ルーティングとバージョン** |パス、ホスト ルール、カナリア、リライト |
| **IV — 認証** | JWT、API キー、エッジの OAuth |
| **V — レート制限と復元力** |スロットリング、タイムアウト、サーキット ブレーカー |
| **VI — セットアップとプロバイダー** | AWS、Kong、NGINX、クラウド管理 |
| **VII — 操作とトラブルシューティング** |ログ、デバッグ、一般的なエラー |

## ゲートウェイと他のエッジ部分

| Component | Primary question |
|-----------|------------------|
| **CDN** | “Can I serve a cached copy?” ([CDN track](../cdn/i-overview.md)) |
| **API gateway** | “Who is allowed, and where does this request go?” |
| **Load balancer (ALB/NLB)** | “Which healthy instance gets this TCP/HTTP connection?” |
| **Reverse proxy (NGINX)** | Often **is** the gateway, or sits behind it |
| **WAF** | “Is this request malicious?” — often bundled with CDN/gateway |

```text
Client → CDN (optional) → API Gateway → Load balancer → Service pods
```

## ゲートウェイが通常行うこと

| Capability | Example |
|------------|---------|
| **Routing** | `GET /api/v1/orders` → orders-service |
| **TLS termination** | HTTPS for `api.example.com` |
| **Authentication** | Validate JWT, API key, mTLS |
| **Rate limiting** | 1000 req/min per API key |
| **Request/response transform** | Strip path prefix, add headers |
| **Observability** | Access logs, metrics, trace ID injection |

ゲートウェイを**薄く**保つ — ビジネス ルールはサービス内に残ります。

## 一般的な製品

|製品 |メモ |
|----------|----------|
| **AWS API Gateway** | REST API、HTTP API、Lambda/HTTP の統合 |
| **コング / コング ゲートウェイ** |オープンソース、プラグイン、K8s フレンドリー |
| **NGINX / NGINX プラス** |リバース プロキシ + ゲートウェイ パターン |
| **Azure API 管理** |完全な API ライフサイクル |
| **Google API Gateway / Apigee** | GCP およびエンタープライズ API 管理 |
| **特使 + グルー / アンバサダー** | Kubernetes ネイティブ |
| **Cloudflare API シールド** |エッジ + スキーマ検証 |

## ゲートウェイが必要な場合

|ゲートウェイが必要 |今はスキップしてください |
|--------------|--------------|
| 1 つの API ホストの背後にある複数のバックエンド サービス |単一モノリス、1 ポート |
|パートナー/パブリック API とキーとクォータ |内部専用 VPC 呼び出し |
|中央認証とレート制限 |クライアントが少ない、アプリ OK に制限がある |
| API エッジでのバージョン管理 |アプリルート内のみのバージョン |

＃＃ 次

Continue with [How gateways work](ii-how-api-gateways-work.md) for request flow and north-south traffic.
