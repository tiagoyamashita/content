---
label: "VI"
subtitle: "Setup & providers"
group: "API Gateway"
order: 6
---
API gateway — setup & providers
Concrete patterns for **AWS API Gateway**, **Kong**, and **NGINX** — plus how they pair with [CDN](../cdn/i-overview.md) origins.

## 1. AWS: CloudFront + API Gateway + Lambda

```text
CloudFront
  /assets/*  → S3
  /api/*     → API Gateway (HTTP API) → Lambda
```

HTTP API (v2) — lower latency/cost than REST API for Lambda proxy:

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

Use when services are long-lived containers, not Lambda.

## 3. Kong on Kubernetes

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

Kong **Admin API** manages routes; or **Ingress Controller** CRDs.

## 4. NGINX as reverse proxy / gateway

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

Add **lua** or **OpenResty** for JWT validation, or terminate auth at separate OIDC proxy (oauth2-proxy).

## 5. Managed API management

| Product | Best for |
|---------|----------|
| **Azure API Management** | Policies in XML, developer portal |
| **Google Apigee** | Enterprise API products |
| **AWS REST API** | API keys, usage plans, SDK generation |

Developer portal, monetization, and lifecycle — beyond simple routing.

## 6. Local development

| Approach | Notes |
|----------|-------|
| **Direct to service** | `localhost:8080` — skip gateway locally |
| **Docker Compose Kong** | Parity with prod routes |
| **Tilt / Skaffold** | K8s gateway in dev cluster |

Maintain **route config in git** — same repo as OpenAPI spec when possible.

## 7. Observability hooks

Enable at gateway:

- **Access logs** (path, status, latency, client IP)
- **Metrics** (4xx/5xx rate, p99 latency)
- **Trace propagation** — W3C `traceparent` header ([Observability at scale](../sysdesign/scalable-patterns/viii-observability-at-scale.md))

## Next

Continue with [Operations & troubleshooting](vii-operations-and-troubleshooting.md) for logs, 502 debug, and runbooks.
