---
label: "IV"
subtitle: "Integration & practices"
group: "SRE"
order: 4
---
SRE tooling — Alertmanager: Integration & practices
Wire Prometheus to Alertmanager and keep paging sane.

## 1. Point Prometheus at Alertmanager

In **`prometheus.yml`** (or Operator **`Prometheus`** CR **`spec.alerting`**):

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093   # Service DNS in-cluster
```

Prometheus Operator setups are often **pre-wired** to the cluster **`Alertmanager`** Service—avoid overriding **`alerting`** accidentally.

## 2. Example alert rule (Prometheus)

Labels route in Alertmanager; **`annotations`** populate Slack/email templates:

```yaml
groups:
  - name: example
    rules:
      - alert: HighErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Elevated 5xx rate"
          description: "Check dashboard X — runbook https://wiki/runbooks/high-5xx"
```

## 3. SRE practices

- Design **`severity`** so paging only happens for **user-impacting** or **SLO-burn** conditions.
- Put **`runbook_url`** (or **`description`** with links) in **annotations** so notifications open context fast.
- Test **`alertmanager.yml`** with **`amtool check-config`**; exercise **staging** Slack/PagerDuty webhooks before prod routes.
- Prefer **`AlertmanagerConfig`** per-namespace RBAC on shared clusters so teams own receivers without one giant global file.

## 4. Pairing

**Prometheus** evaluates rules and forwards firing alerts; **Alertmanager** owns **dedupe, grouping, routing**, and **delivery** to Slack, PagerDuty, etc.
