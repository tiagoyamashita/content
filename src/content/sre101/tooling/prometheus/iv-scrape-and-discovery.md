---
label: "IV"
subtitle: "Scrape & discovery"
group: "SRE"
order: 4
---
SRE tooling — Prometheus: Scrape & discovery
Configure **what** to scrape, **how often**, and **how labels map** into the TSDB.

## 1. Static targets (non-Kubernetes)

Minimal **`prometheus.yml`** fragment:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: checkout-api
    metrics_path: /actuator/prometheus   # or /metrics
    static_configs:
      - targets:
          - checkout-api.internal:8080
        labels:
          env: prod
          region: us-east-1
```

**`job_name`** becomes the default **`job`** label unless relabeled.

## 2. Common scrape knobs

| Field | Purpose |
|-------|---------|
| **`scrape_interval`** | Overrides global per job. |
| **`metrics_path`** | Path other than **`/metrics`**. |
| **`scheme`** | **`https`** when TLS terminates on the pod. |
| **`basic_auth` / `bearer_token`** | Rare for internal scrape; prefer network trust boundaries. |
| **`honor_labels`** | Keep target-supplied **`job`**/`instance`—easy to footgun; understand before enabling. |

## 3. Service discovery (overview)

Prometheus can discover targets from **Kubernetes**, **Consul**, **EC2**, **DNS**, **files**, etc. Example **Kubernetes pods** (raw Prometheus config—not Operator CRDs):

```yaml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

Operators (**kube-prometheus-stack**) usually generate this for you from **`ServiceMonitor`**—prefer that path unless you maintain Prometheus config by hand.

## 4. Relabeling mindset

Two phases:

- **`relabel_configs`** — runs on **target metadata** (`__meta_*`) before scrape; sets **`__address__`**, **`__metrics_path__`**, drops targets (**`action: drop`**), copies labels onto the series.
- **`metric_relabel_configs`** — runs on **scraped samples** before ingest—drop expensive metrics, rewrite labels.

Example: drop high-cardinality metric **before storage**:

```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: noisy_http_path_bucket
    action: drop
```

Use **`labeldrop`** / **`labelkeep`** sparingly—prefer fixing instrumentation.

## 5. Federation & scaling scrape (hint)

When one Prometheus cannot scrape everything, **federation** pulls selected series from other Prometheus servers (**`/federated`**); **Thanos / Mimir / Cortex** extend long-term storage and global query—see **Rules & operations**.
