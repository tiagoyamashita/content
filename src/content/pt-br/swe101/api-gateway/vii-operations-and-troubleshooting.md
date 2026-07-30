---
label: "VII"
subtitle: "Operations & troubleshooting"
group: "API Gateway"
order: 7
---
API gateway — operations & troubleshooting
Operate gateways with **access logs**, **upstream health**, and clear **timeout** alignment across CDN, gateway, and services.

## 1. Metrics to watch

| Metric | Signal |
|--------|--------|
| **4xx rate** | Auth misconfig, bad clients |
| **5xx rate** | Upstream or gateway overload |
| **Latency p50/p99** | Gateway overhead vs service slowness |
| **429 rate** | Rate limits working — tune thresholds |
| **Integration errors** | Lambda/ALB unreachable |

Split dashboards by **route** and **API version**.

## 2. Debug a failed request

```text
1. Reproduce with curl -v (include Authorization if needed)
2. Check gateway access log — was upstream called?
3. If 401/403 → auth plugin / JWT claims
4. If 429 → rate limit key / Redis counter
5. If 502/504 → upstream health, timeout, security group
6. Compare direct-to-upstream (VPN) vs via gateway
```

```bash
curl -v https://api.example.com/api/v1/health \
  -H "Authorization: Bearer $TOKEN"
```

## 3. Common failures

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| **502 Bad Gateway** | Upstream down, wrong port, VPC link broken | Health check target group |
| **504 Gateway Timeout** | Service slow; gateway timeout too low | Increase timeout or fix service |
| **401 on valid user** | Wrong JWKS, clock skew, `aud` mismatch | Sync NTP; fix issuer config |
| **CORS error in browser** | Gateway missing `Access-Control-*` | Add CORS plugin at gateway |
| **Double slash / 404** | `strip_path` mismatch | Align gateway rewrite with service mount |
| **Works in Postman, fails in prod** | Different host, missing WAF rule | Compare headers and path |

## 4. CDN + gateway incidents

| Symptom | Check |
|---------|-------|
| API cached for wrong user | CDN cache on `/api/*` — bypass or `no-store` |
| Intermittent 504 | CDN timeout &lt; gateway &lt; service — align |
| SSL errors | Cert on CDN vs gateway hostname mismatch |

Full topology: [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md).

## 5. Deployment and rollback

- **Blue/green upstream** — switch gateway target weights
- **Route config in CI** — lint OpenAPI, dry-run apply
- **Feature flags** in services — gateway routes stable; canary via weights

Keep **backward-compatible** `/api/v1` during `/api/v2` rollout.

## 6. Security operations

- Rotate API keys on schedule; audit unused consumers
- Review WAF blocks — false positives vs real attacks
- Pen-test public gateway surface — not just app server

## 7. Checklist

- [ ] Routes match OpenAPI / contract tests
- [ ] Auth enforced on all non-public paths
- [ ] Rate limits per tier documented
- [ ] Timeouts aligned CDN → gateway → service
- [ ] Access logs shipped to SIEM or log aggregator
- [ ] Trace ID from gateway through services
- [ ] `/health` and `/ready` excluded from heavy plugins
- [ ] CDN bypass or `no-store` on authenticated API

## Related notes

- [CDN & API gateway together](../cdn/viii-cdn-and-api-gateway-together.md) — combined edge architecture
- [CDN operations](../cdn/vii-operations-and-troubleshooting.md) — cache-side debug
- [Rate limiting](../sysdesign/scalable-patterns/iv-rate-limiting.md) — algorithms
- [API Gateway & service mesh](../../sre101/cloud-architecture/patterns-and-design/v-api-gateway-and-service-mesh.md) — mesh vs gateway
