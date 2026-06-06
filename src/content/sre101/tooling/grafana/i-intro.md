---
label: "I"
subtitle: "Intro"
group: "SRE"
order: 1
---
SRE tooling — Grafana: Intro
What Grafana is for in an observability stack.

## 1. Role

**Grafana** connects to **datasources** (Prometheus, Loki, Tempo/Jaeger, cloud vendors), renders **dashboards** and **panels**, and can evaluate **alert rules** (UI-managed or provisioned as code) routed to **Alertmanager**, Slack, PagerDuty, webhooks, etc.

## 2. Core concepts

- **Datasource** — configured endpoint plus credentials; use **organizations** and **folders** so teams do not overwrite each other.
- **Dashboard JSON** — treat dashboards as code: export or provision from Git instead of only clicking in prod.
- **Variables** — `$cluster`, `$namespace`, `$job` templating keeps one dashboard reusable across environments.
- **Unified alerting** — Grafana-managed rules vs Prometheus-native rules; pick **one** primary model per signal path so you do not double-notify.

## 3. Typical stack

**Prometheus** → metrics; **Loki** → logs; **Tempo** (or Jaeger) → traces—**Grafana** is usually where engineers pivot during incidents.

Continue with **Installation** and **Tips and tricks** in this folder.
