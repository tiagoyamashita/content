---
label: "VI"
subtitle: "Observability, SLI & SLO"
group: "Cloud architecture"
order: 6
---
Observability, SLI & SLO
You cannot operate what you cannot see. **Observability** combines logs, metrics, and traces; **SLOs** turn measurements into actionable targets.

## 1. Three pillars

| Pillar | What | Tooling examples |
|--------|------|------------------|
| **Logs** | Discrete events with context | CloudWatch Logs, Datadog, ELK |
| **Metrics** | Numeric time series | Prometheus, CloudWatch Metrics |
| **Traces** | Request path across services | OpenTelemetry → Jaeger, Tempo, X-Ray |

```text
Request abc-123
  ├─ span: gateway (12 ms)
  ├─ span: auth-service (45 ms)     ← slowest
  ├─ span: orders-service (8 ms)
  └─ span: postgres (3 ms)
```

## 2. Structured logging

**JSON logs** — machine-parseable, filterable in log aggregators.

```json
{
  "timestamp": "2026-05-19T14:22:01.123Z",
  "level": "ERROR",
  "service": "orders-api",
  "traceId": "7f3a9c2e8b1d4f6a",
  "spanId": "a1b2c3d4",
  "message": "Payment declined",
  "orderId": "ord-9281",
  "userId": "usr-441",
  "durationMs": 842
}
```

| Bad | Good |
|-----|------|
| `ERROR payment failed for user` | JSON with `orderId`, `traceId`, `errorCode` |
| Log PII (full card number) | Mask or omit sensitive fields |

## 3. Correlation ID

Inject at **API Gateway**; propagate on every hop.

```http
GET /api/orders/9281 HTTP/1.1
X-Request-Id: 7f3a9c2e-8b1d-4f6a-9c2e-8b1d4f6a9c2e
traceparent: 00-7f3a9c2e8b1d4f6a-a1b2c3d4e5f60708-01
```

```java
// MDC for logging — Java 22
MDC.put("traceId", traceId);
try {
  log.info("Processing order {}", orderId);
} finally {
  MDC.clear();
}
```

Search logs by one ID → entire request story across services.

## 4. Metrics that matter (RED method)

For each service:

| Metric | Meaning |
|--------|---------|
| **Rate** | Requests per second |
| **Errors** | Failed requests / total |
| **Duration** | Latency (p50, p95, p99) |

**USE method** for infrastructure: **Utilization**, **Saturation**, **Errors** (CPU, disk queue depth).

## 5. SLI, SLO, SLA

| Term | Definition | Example |
|------|------------|---------|
| **SLI** | **Indicator** — what you measure | p99 latency = 120 ms |
| **SLO** | **Objective** — internal target | p99 latency < 200 ms over 30 days |
| **SLA** | **Agreement** — contractual | 99.9% uptime or credit |

```text
SLI (measure)  →  SLO (target)  →  SLA (contract with customer)
     │                │
     └── error budget: 100% - SLO = allowed bad minutes/month
```

**Error budget:** if SLO is 99.9%, you have ~43 min downtime/month. Budget exhausted → freeze features, focus on reliability.

## 6. Example SLO table

| Service | SLI | SLO (30-day) | Alert |
|---------|-----|--------------|-------|
| Public API | Availability | 99.95% | < 99.9% in 1h window |
| Public API | Latency p99 | < 300 ms | p99 > 500 ms for 5 min |
| Checkout | Success rate | 99.5% | Error rate > 1% |
| Batch jobs | Completion | 99% on time | DLQ depth > 100 |

## 7. Alerting principles

| Alert on | Don't alert on |
|----------|----------------|
| SLO burn rate | Every log ERROR line |
| Symptom (latency up) | Possible cause (CPU 80% alone) |
| User-visible impact | Dev environment noise |

```text
Page on-call:  SLO breach imminent (fast burn)
Ticket only:   Disk 70% — trend warning
```

## 8. OpenTelemetry flow

```text
App SDK → OTLP exporter → Collector → Backend (Tempo, Datadog)
                │
                └── same traceId in logs (log correlation)
```

One instrumentation standard for metrics, logs, traces.

## 9. Cloud-native services

| AWS | Azure | GCP |
|-----|-------|-----|
| CloudWatch + X-Ray | Monitor + App Insights | Cloud Monitoring + Trace |
| Managed Grafana | | |

Prefer **OpenTelemetry** for portable instrumentation across clouds.

## 10. Rehearsal answers

- **Three pillars** — logs, metrics, traces.
- **Correlation ID** — ties one user request across services.
- **SLI vs SLO** — measurement vs target; SLA adds contract/penalties.
- **Why structured JSON** — queryable fields, not regex on plain text.

**Related:** `v-api-gateway-and-service-mesh.md`, CI/CD `vi-pipeline-observability-and-dora.md`.
