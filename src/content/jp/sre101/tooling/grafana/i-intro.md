---
label: "I"
subtitle: "イントロ"
group: "SRE"
order: 1
---
SRE ツール — Grafana: はじめに

可観測性スタックにおける Grafana の目的。

## 1. 役割

**Grafana** は **データソース** (Prometheus、Loki、Tempo/Jaeger、クラウド ベンダー) に接続し、**ダッシュボード** と **パネル**をレンダリングし、**Alertmanager**、Slack、PagerDuty、Webhook などにルーティングされた **アラート ルール** (UI- 管理またはコードとしてプロビジョニング) を評価できます。

## 2. 中心となる概念

- **Datasource** — configured endpoint plus credentials; use **organizations** and **folders** so teams do not overwrite each other.
- **Dashboard JSON** — treat dashboards as code: export or provision from Git instead of only clicking in prod.
- **Variables** — `$cluster`, `$namespace`, `$job` templating keeps one dashboard reusable across environments.
- **Unified alerting** — Grafana-managed rules vs Prometheus-native rules; pick **one** primary model per signal path so you do not double-notify.

## 3. 一般的なスタック

**Prometheus** → メトリクス; **ロキ** → 丸太; **テンポ** (またはイェーガー) → トレース—**Grafana** は通常、インシデント中にエンジニアが中心となる場所です。

このフォルダー内の **インストール** と **ヒントとテクニック** に進みます。
