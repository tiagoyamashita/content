---
label: "I"
subtitle: "イントロとアーキテクチャ"
group: "SRE"
order: 1
---
SRE ツール — Prometheus: 概要とアーキテクチャ

Prometheus が可観測性にどのように適合し、その部分がどのように接続されるか。

## 1. 役割

**Prometheus** **scrapes** HTTP endpoints that expose **Prometheus text exposition format** (often **`/metrics`**), appends samples into a **local time-series database (TSDB)**, and answers queries with **PromQL**. It also evaluates **alerting rules** and forwards firing alerts to **Alertmanager**—it does **not** send Slack/PagerDuty itself.

## 2. プルモデル

- Prometheus **calls your app** on an interval (**`scrape_interval`**). Your service **does not** push samples during normal operation (that avoids back-pressure coupling but requires scrape targets to be reachable).
- **Pushgateway** exists for **batch / short-lived jobs** (CI job finishes, pushes once). Do **not** use it as a generic metrics buffer for long-lived services—you lose instance semantics and complicate lifecycle.

## 3. 主な可動部品

| Piece | Purpose |
|-------|---------|
| **Scrape discovery** | **`static_configs`**, Kubernetes SD, Consul, file SD, etc.—produce a list of targets. |
| **Relabeling** | **`relabel_configs`** / **`metric_relabel_configs`** rewrite labels before ingest or drop noisy series. |
| **Storage** | TSDB blocks on disk; compaction; configurable **retention** (`--storage.tsdb.retention.time`). |
| **PromQL** | Query language for Grafana dashboards and **`expr`** in rules. |
| **Rules** | **Recording** rules precompute heavy queries; **alerting** rules emit alerts to Alertmanager. |

## 4. Prometheus ではないもの

- **Not** a log store → pair with **Loki** or ELK.
- **Not** distributed tracing → pair with **Tempo** / Jaeger.
- **Not** the same binary as **Alertmanager**—operators deploy **both**, wired via Prometheus **`alerting.alertmanagers`**.

## 5. スタック内でのペアリング

- **Grafana** は、ダッシュボードに対して PromQL を使用して Prometheus をクエリします。
- **Alertmanager** は Prometheus からアラートを受信し、ルーティング、沈黙、Slack/PagerDuty などを処理します。

このフォルダーで **メトリクスと PromQL**、**インストルメンテーション**、**スクレイピングとディスカバリー**、**Kubernetes**、**ルール / オペレーション**を続けます。
