---
label: "III"
subtitle: "Tips and tricks"
group: "SRE"
order: 3
---
SRE tooling — Grafana: Tips and tricks
Operator-focused habits that keep dashboards and alerts usable.

## 1. Golden signals

Per critical user-facing service, aim for panels covering **latency**, **traffic**, **errors**, and **saturation** (or your agreed RED/USE slice)—same layout across services speeds on-call muscle memory.

## 2. Runbooks and drill-ins

- Put **`runbook_url`** (or dashboard links) in alert annotations so fires open context in one click.
- Use **dashboard links** and consistent **tags** (`team-payments`, `slo-checkout`) for discovery.

## 3. Performance

- Prefer **recording rules** in Prometheus for heavy PromQL used on every refresh.
- Raise dashboard **refresh interval** during steady state; avoid 5s everywhere.
- Limit **high-cardinality** template variables that explode query fan-out.

## 4. Alerting hygiene

- Avoid duplicating the same condition in **Prometheus** and **Grafana** unified alerting unless intentionally layered.
- Route noisy exploratory charts out of **production home** dashboards; keep exec summaries sparse.

## 5. Access and drift

- Restrict **Editor** vs **Viewer** roles; use **Git-synced** provisioning for dashboards and datasources where compliance matters.
- Periodically diff exported JSON against Git to catch silent UI edits.
