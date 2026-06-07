---
label: "VI"
subtitle: "セットアップとプロバイダー"
group: "API Gateway"
order: 6
---
API ゲートウェイ — セットアップとプロバイダー


Concrete patterns for **AWS API Gateway**, **Kong**, and **NGINX** — plus how they pair with [CDN](../cdn/i-overview.md) origins.

## 1. AWS: CloudFront + API Gateway + Lambda

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

Custom domain: **ACM cert** + **`api.example.com`** → API Gateway stage → CloudFront origin for single-host SPA.

## 2. AWS: API Gateway + ALB + ECS/K8s

```text
API Gateway (VPC Link) → ALB → target group → pods
```

サービスが Lambda ではなく、存続期間の長いコンテナである場合に使用します。

## 3. Kubernetes のコング

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

Kong **管理者 API** がルートを管理します。または **Ingress コントローラー** CRD。

## 4. リバース プロキシ/ゲートウェイとしての NGINX

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

JWT 検証用に **lua** または **OpenResty** を追加するか、別の OIDC プロキシ (oauth2-proxy) で認証を終了します。

## 5. API 管理の管理

|製品 |こんな方に最適 |
|----------|----------|
| **Azure API 管理** | XML のポリシー、開発者ポータル |
| **Google Apigee** |エンタープライズ API 製品 |
| **AWS REST API** | API キー、使用計画、SDK 生成 |

単純なルーティングを超えた、開発者ポータル、収益化、ライフサイクル。

## 6. 地域開発

| Approach | Notes |
|----------|-------|
| **Direct to service** | `localhost:8080` — skip gateway locally |
| **Docker Compose Kong** | Parity with prod routes |
| **Tilt / Skaffold** | K8s gateway in dev cluster |

**ルート設定を git** で維持します。可能な場合は、OpenAPI 仕様と同じリポジトリを維持します。

## 7. 可観測性フック

ゲートウェイで有効にする:

- **Access logs** (path, status, latency, client IP)
- **Metrics** (4xx/5xx rate, p99 latency)
- **Trace propagation** — W3C `traceparent` header ([Observability at scale](../sysdesign/scalable-patterns/viii-observability-at-scale.md))

＃＃ 次

Continue with [Operations & troubleshooting](vii-operations-and-troubleshooting.md) for logs, 502 debug, and runbooks.
