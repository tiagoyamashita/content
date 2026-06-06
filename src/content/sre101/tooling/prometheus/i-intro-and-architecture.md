---
label: "I"
subtitle: "Intro & architecture"
group: "SRE"
order: 1
---
SRE tooling — Prometheus: Intro & architecture
How Prometheus fits into observability and how its pieces connect.

## 1. Role

**Prometheus** **scrapes** HTTP endpoints that expose **Prometheus text exposition format** (often **`/metrics`**), appends samples into a **local time-series database (TSDB)**, and answers queries with **PromQL**. It also evaluates **alerting rules** and forwards firing alerts to **Alertmanager**—it does **not** send Slack/PagerDuty itself.

## 2. Pull model

- Prometheus **calls your app** on an interval (**`scrape_interval`**). Your service **does not** push samples during normal operation (that avoids back-pressure coupling but requires scrape targets to be reachable).
- **Pushgateway** exists for **batch / short-lived jobs** (CI job finishes, pushes once). Do **not** use it as a generic metrics buffer for long-lived services—you lose instance semantics and complicate lifecycle.

## 3. Main moving parts

| Piece | Purpose |
|-------|---------|
| **Scrape discovery** | **`static_configs`**, Kubernetes SD, Consul, file SD, etc.—produce a list of targets. |
| **Relabeling** | **`relabel_configs`** / **`metric_relabel_configs`** rewrite labels before ingest or drop noisy series. |
| **Storage** | TSDB blocks on disk; compaction; configurable **retention** (`--storage.tsdb.retention.time`). |
| **PromQL** | Query language for Grafana dashboards and **`expr`** in rules. |
| **Rules** | **Recording** rules precompute heavy queries; **alerting** rules emit alerts to Alertmanager. |

## 4. What Prometheus is not

- **Not** a log store → pair with **Loki** or ELK.
- **Not** distributed tracing → pair with **Tempo** / Jaeger.
- **Not** the same binary as **Alertmanager**—operators deploy **both**, wired via Prometheus **`alerting.alertmanagers`**.

## 5. Pairing in the stack

- **Grafana** queries Prometheus with PromQL for dashboards.
- **Alertmanager** receives alerts from Prometheus and handles routing, silences, Slack/PagerDuty, etc.

Continue in this folder with **metrics & PromQL**, **instrumentation**, **scrape & discovery**, **Kubernetes**, and **rules / operations**.
