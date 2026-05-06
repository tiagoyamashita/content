---
label: "II"
subtitle: "Prometheus"
group: "SRE"
order: 2
---
SRE tooling — Prometheus
Time-series metrics collection and querying.

## 1. Role

**Prometheus** scrapes HTTP **metrics endpoints** (typically **`/metrics`** in **Prometheus exposition format**), stores samples in its TSDB, and exposes **PromQL** for alerting and dashboards.

## 2. Core concepts

- **Target** — something scraped on an interval (PodMonitor / ServiceMonitor in Kubernetes, static configs, etc.).
- **Metric types** — counters, gauges, histograms, summaries; choose types that match SLIs (e.g. latency histogram for percentiles).
- **Recording & alerting rules** — pre-aggregate expensive queries; define **`ALERT`** rules evaluated periodically.
- **High availability** — federation, Thanos, Cortex / Mimir for long-term storage and global query.

## 3. SRE practices

- Instrument apps with **RED** (rate, errors, duration) or **USE** (utilization, saturation, errors) style metrics where appropriate.
- Align **`severity`** and **`team`** labels on alerts so routing stays predictable.
- Avoid high-cardinality labels (user IDs, raw URLs) that explode series count.

## 4. Pairing

**Grafana** charts PromQL results; **Alertmanager** handles notification routing for Prometheus firing alerts.
