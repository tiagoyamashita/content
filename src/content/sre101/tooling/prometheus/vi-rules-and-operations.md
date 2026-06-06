---
label: "VI"
subtitle: "Rules & operations"
group: "SRE"
order: 6
---
SRE tooling — Prometheus: Rules & operations
Recording rules, alerting rules, HA hints, and operator habits.

## 1. Rule files

Reference YAML rule groups from **`prometheus.yml`**:

```yaml
rule_files:
  - /etc/prometheus/rules/*.yml
```

## 2. Recording rules

Precompute expensive queries once per **`evaluation_interval`**:

```yaml
groups:
  - name: recording.rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

Dashboards and alerts reference **`job:http_requests:rate5m`** instead of repeating long **`rate`** expressions.

## 3. Alerting rules

Prometheus evaluates **`expr`**; when true for **`for`** duration, it fires an alert to **Alertmanager**:

```yaml
groups:
  - name: alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Elevated 5xx fraction"
          description: "See runbook https://wiki/runbooks/high-5xx"
```

Align **`severity`** with **Alertmanager** routes (`critical` vs `warning`).

## 4. Wiring Alertmanager

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
```

Operator-managed Prometheus usually ships this preconfigured—verify after customizing Helm values.

## 5. High availability & long-term storage

- **HA scrape**: duplicate Prometheus per AZ with identical config—dedupe in query layer or accept overlap for alerting (Alertmanager dedupes notifications).
- **Federation**: hierarchical Prometheus pulls **`/federate`** aggregates upward.
- **Thanos / Mimir / Cortex**: durable storage + global query; remote-write sidecars ship blocks off-node.

## 6. Retention & capacity

Tune **`--storage.tsdb.retention.time`** and disk; cardinality dominates RAM/disk more than raw scrape rate—guard labels in instrumentation and **`metric_relabel_configs`**.

## 7. SRE practices

- Instrument **RED** / **USE** for critical paths; histograms for latency percentiles.
- Keep **`team`**, **`severity`**, **`service`** labels predictable for routing.
- Test rule **`expr`** with Grafana **Explore** before paging humans.

**Grafana** visualizes PromQL; **Alertmanager** owns notification routing—see the **Alertmanager** subfolder in Tooling.
