---
label: "I"
subtitle: "Grafana"
group: "SRE"
order: 1
---
SRE tooling — Grafana
Dashboards, alerting UI, and the glue layer for metrics, logs, and traces.

## 1. Role

**Grafana** connects to **datasources** (Prometheus, Loki, Tempo/Jaeger, cloud vendors), renders **dashboards** and **panels**, and can evaluate **alert rules** (UI-managed or provisioned as code) routed to **Alertmanager**, Slack, PagerDuty, etc.

## 2. Core concepts

- **Datasource** — configured endpoint + auth; use **organization** / **folder** boundaries for teams.
- **Dashboard JSON** — version in Git; avoid “click ops only” drift between environments.
- **Variables** — `$cluster`, `$namespace` templating keeps one dashboard reusable.
- **Unified alerting** — Grafana-managed rules vs Prometheus-native rules; pick one model per signal path to avoid duplicates.

## 3. SRE practices

- Build **golden signals** views (latency, traffic, errors, saturation) per critical service.
- Link dashboards from **runbooks** and from **Alertmanager** annotations for faster MTTR.
- Dashboard **performance**: selective queries, recording rules for heavy PromQL, sane refresh intervals.

## 4. Pairing

Typical stack: **Prometheus** → metrics datasource; **Loki** → logs; **Tempo** → traces—**Grafana** ties investigations together.
