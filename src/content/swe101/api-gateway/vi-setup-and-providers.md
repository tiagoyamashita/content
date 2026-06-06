---
label: "VI"
subtitle: "セットアップとプロバイダー"
group: "APIゲートウェイ"
order: 6
---
API ゲートウェイ — セットアップとプロバイダー

**AWS API Gateway**、**Kong**、**NGINX** の具体的なパターン、および [CDN](../cdn/i-overview.md) オリジンとのペアリング方法。

## 1. AWS: CloudFront + API ゲートウェイ + Lambda

```text
CloudFront
  /assets/*  → S3
  /api/*     → API Gateway (HTTP API) → Lambda
```

HTTP API (v2) — Lambda プロキシの REST API よりもレイテンシー/コストが低い:

```yaml
# Conceptual SAM / CloudFormation idea
Resources:
  HttpApi:
    Type: AWS::ApiGatewayV2::Api
    Properties:
      ProtocolType: HTTP
  Integration:
    Type: AWS::ApiGatewayV2::Integration
    Properties:
      IntegrationType: AWS_PROXY
      PayloadFormatVersion: "2.0"
```

カスタム ドメイン: **ACM cert** + **`api.example.com`** → API Gateway ステージ → 単一ホスト SPA の CloudFront オリジン。

## 2. AWS: API ゲートウェイ + ALB + ECS/K8s

```text
API Gateway (VPC Link) → ALB → target group → pods
```

サービスが Lambda ではなく、存続期間の長いコンテナである場合に使用します。

## 3. Kubernetes 上の Kong

```text
Internet → LoadBalancer → Kong → Ingress → services
```

```yaml
# Conceptual Ingress + Kong plugin
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api
  annotations:
    konghq.com/plugins: rate-limiting, jwt
spec:
  rules:
    - host: api.example.com
      http:
        paths:
          - path: /api/v1/orders
            pathType: Prefix
            backend:
              service:
                name: orders-svc
                port:
                  number: 80
```

Kong **Admin API** はルートを管理します。または **Ingress コントローラー** CRD。

## 4. リバースプロキシ/ゲートウェイとしてのNGINX

```nginx
upstream orders {
  server orders-svc:8080;
}

server {
  listen 443 ssl;
  server_name api.example.com;

  location /api/v1/orders/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://orders;
    proxy_set_header X-Request-Id $request_id;
    proxy_connect_timeout 5s;
    proxy_read_timeout 30s;
  }
}
```

JWT 検証のために **lua** または **OpenResty** を追加するか、別の OIDC プロキシ (oauth2-proxy) で認証を終了します。

## 5. マネージド API 管理

|製品 |こんな方に最適 |
|----------|----------|
| **Azure API 管理** | XML のポリシー、開発者ポータル |
| **Google Apigee** |エンタープライズ API 製品 |
| **AWS REST API** | API キー、使用プラン、SDK の生成 |

単純なルーティングを超えた、開発者ポータル、収益化、ライフサイクル。

## 6. 地域開発

|アプローチ |メモ |
|----------|----------|
| **サービスへ直接** | `localhost:8080` — ゲートウェイをローカルでスキップする |
| **Docker Compose Kong** | prod ルートとのパリティ |
| **傾斜/足場** |開発クラスタの K8s ゲートウェイ |

**ルート設定を git** で維持します。可能な場合は、OpenAPI 仕様と同じリポジトリを維持します。

## 7. 可観測性フック

ゲートウェイで有効にする:

- **アクセス ログ** (パス、ステータス、遅延、クライアント IP)
- **メトリクス** (4xx/5xx レート、p99 レイテンシー)
- **トレース伝播** — W3C `traceparent` ヘッダー ([大規模な可観測性](../sysdesign/scalable-patterns/viii-observability-at-scale.md))

＃＃ 次

ログ、502 デバッグ、および Runbook については、[操作とトラブルシューティング](vii-operations-and-troubleshooting.md) に進みます。
