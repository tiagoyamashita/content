---
label: "VIII"
subtitle: "Observability at scale"
group: "System design"
order: 8
---
Observability at scale
At high scale, one slow dependency **cascades**. **Metrics**, **logs**, and **traces** — plus **SLOs** and controlled **chaos** — keep failures visible and bounded.

## 1. Three pillars

| Pillar | Answers | Tools (examples) |
|--------|---------|------------------|
| **Metrics** | How much? How fast? Error rate? | Prometheus, Datadog, CloudWatch |
| **Logs** | What happened on this instance? | Loki, ELK, Cloud Logging |
| **Traces** | Which hop was slow in this request? | Jaeger, Tempo, Zipkin, X-Ray |

**Correlation:** same `trace_id` / `request_id` across all three.

## 2. Alerting — symptoms not causes

| Alert on (good) | Alert on (noisy) |
|-----------------|------------------|
| Error rate > 1% for 5 min | CPU > 80% |
| p99 latency > 500 ms | Single pod restart |
| SLO burn rate 14× budget | Disk 70% full |

**SLO example:** 99.9% availability = ~43 min downtime/month **error budget**. Page when **burn rate** consumes budget too fast.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Distributed trace waterfall across services">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Trace waterfall (one request)</text>
  <rect x="12" y="36" width="200" height="14" rx="2" fill="rgba(34,197,94,0.3)" stroke="#86efac"/>
  <text x="16" y="47" fill="#e4e4e7" font-size="8">api-gateway 120ms</text>
  <rect x="40" y="54" width="120" height="14" rx="2" fill="rgba(59,130,246,0.3)" stroke="#60a5fa"/>
  <text x="44" y="65" fill="#e4e4e7" font-size="8">orders 80ms</text>
  <rect x="60" y="72" width="280" height="14" rx="2" fill="rgba(248,113,113,0.35)" stroke="#f87171"/>
  <text x="64" y="83" fill="#e4e4e7" font-size="8">postgres query 240ms ← bottleneck</text>
</svg></figure>

## 3. Distributed tracing

1. **API gateway** creates or accepts trace id (**W3C Trace Context** headers).
2. Each service creates a **span** (name, start, duration, status).
3. Propagate headers on outbound HTTP/gRPC/message metadata.
4. Backend stores spans; UI shows **waterfall**.

| Header | Purpose |
|--------|---------|
| `traceparent` | Trace and span ids (W3C) |
| `tracestate` | Vendor-specific hints |
| `X-Request-Id` | Support correlation (not a full trace) |

## 4. Capacity planning

| Metric | Use |
|--------|-----|
| p50 / p95 / p99 latency | Tail latency drives UX |
| QPS / throughput | Scale triggers |
| Saturation (CPU, pool wait) | Headroom before failure |

**Model growth:** if DAU +20%/month, when does DB connection pool or shard limit break? **Load test** before launches (k6, Locust, Gatling).

## 5. Chaos engineering

Deliberately inject failure in **staging** (or controlled prod):

| Experiment | Validates |
|------------|-----------|
| Kill random pod | K8s restart + LB health |
| Add 500 ms latency to dependency | Timeouts + circuit breakers |
| Partition AZ | Failover + replica promotion |

Tools: Chaos Monkey, Litmus, AWS FIS. **Every alert** should link a **runbook**.

## 6. Runbook template

| Section | Content |
|---------|---------|
| Symptom | What users see |
| Dashboards | Links to graphs |
| Likely causes | Ordered checklist |
| Mitigation | Scale, rollback, feature flag |
| Escalation | Who to page next |

## 7. Rehearsal

- Define SLO for a hypothetical API (availability + latency).
- Draw trace propagation through 4 services.
- Why alert on error rate instead of CPU?

**Related:** SRE tooling notes (Prometheus, Alertmanager), **Bottleneck analysis** submenu (`bottleneck-analysis/`).
