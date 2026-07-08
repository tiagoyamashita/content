---
label: "II"
subtitle: "Metrics types & PromQL"
group: "SRE"
order: 2
---
SRE tooling — Prometheus: Metrics types & PromQL
Instrument with the right **metric type**, keep **labels** under control, and read graphs with **PromQL**.

## 1. Metric types (client ↔ exposition)

| Type | Meaning | Typical use |
|------|---------|----------------|
| **Counter** | Only increases (reset on process restart). | Requests served, errors total, bytes sent. |
| **Gauge** | Up or down. | Queue depth, memory in use, temperature. |
| **Histogram** | Observations in **buckets** + `_sum` + `_count`. | Latency, payload sizes—percentiles via **`histogram_quantile`**. |
| **Summary** | Precomputed quantiles at scrape time (client-side). | Prefer **histograms** when you want aggregation across pods in PromQL. |

Exposition looks like:

```text
http_requests_total{method="GET",status="200"} 14217
http_request_duration_seconds_bucket{le="0.1"} 900
http_request_duration_seconds_bucket{le="+Inf"} 950
http_request_duration_seconds_sum 84.2
http_request_duration_seconds_count 950
```

## 2. Labels & cardinality

- Every unique **label set** is a **new time series**. **`user_id="12345"`** per request → explosion → OOM and slow queries.
- Prefer **`route="/api/orders"`** (bounded set) over raw **`path`** with unbounded URLs.
- Use **`external_labels`** on Prometheus for **`cluster`**, **`env`**—consistent in federation / remote write.

## 3. Instant vs range vectors

- **`metric`** — instant vector “now” at evaluation step.
- **`metric[5m]`** — range vector (window of raw points); **illegal alone**—must wrap in a function like **`rate`**.

## 4. PromQL patterns

**Request rate** (per-second average over 5m):

```promql
sum(rate(http_requests_total[5m])) by (job)
```

**Error ratio** (adjust metric names to your app):

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

**95th percentile latency** from a **histogram** named **`http_request_duration_seconds`**:

```promql
histogram_quantile(
  0.95,
  sum by (le, job) (
    rate(http_request_duration_seconds_bucket[5m])
  )
)
```

Aggregate **`histogram_buckets`** **before** **`histogram_quantile`** when multiple replicas export the same **`le`** buckets.

**Saturation-ish signal** (example — tune to your exporter):

```promql
avg_over_time(process_cpu_seconds_total[5m])
```

## 5. `rate` vs `irate`

- **`rate(...[5m])`** — stable per-second average over window; **preferred** for alerting and dashboards.
- **`irate`** — reacts to last two points; spiky; rarely what you want for SLO burn unless you know why.

## 6. Recording rules (preview)

Heavy PromQL in many dashboards belongs in **recording rules** (see **Rules & operations** in this folder)—materialize **`job:request_latency:p95`** once per evaluation instead of recomputing ad hoc.
