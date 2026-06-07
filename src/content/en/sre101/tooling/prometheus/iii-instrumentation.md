---
label: "III"
subtitle: "Instrumentation"
group: "SRE"
order: 3
---
SRE tooling — Prometheus: Instrumentation
Expose **`/metrics`** (or framework equivalent) from your application process.

## 1. Principles

Prometheus **pulls** from your process—you expose an HTTP handler returning **text exposition format**. Long-lived services should **not** push through **Pushgateway** except unusual batch patterns.

## 2. Spring Boot (Micrometer)

Add Actuator + the Prometheus registry so **`/actuator/prometheus`** exposes JVM and HTTP metrics automatically:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,prometheus
```

Register **business** signals via **`MeterRegistry`** (`Counter`, `Timer`, **`DistributionSummary`**). **`Timer`** maps well to **histograms** for latency SLIs. Defaults already cover JVM and MVC/WebFlux HTTP metrics when starters match your stack.

## 3. Other runtimes (patterns)

- **Go** — **`prometheus/client_golang`**: register collectors, **`promhttp.Handler()`** on **`/metrics`**.
- **Python** — **`prometheus_client`**: **`Counter`**, **`Histogram`**, expose via **`start_http_server`** or **`generate_latest()`** in Flask/FastAPI/Starlette.
- **Node.js** — **`prom-client`**: **`collectDefaultMetrics()`** plus app counters; expose **`register.metrics()`** on HTTP.

## 4. Security & topology

- Bind scrape endpoints **inside** the cluster/VPC (NetworkPolicy, security groups)—metrics often leak deployment topology.
- Prefer **one scrape port per process**; sidecar exporters for third-party apps that cannot embed a client.

## 5. Instrumentation checklist

1. **RED** per critical handler/service: **rate**, **errors**, **duration** (histogram).
2. Bounded label dimensions (**`method`**, **`status`**, **`tenant_tier`**)—never raw user IDs.
3. Name metrics **`_<unit>_total`** / **`_seconds`** / **`_bytes`** consistently (`*_bucket`, `*_sum`, `*_count` for histograms).

Next: **Scrape & discovery** for Prometheus-side config, or **Kubernetes** if you deploy on k8s only.
