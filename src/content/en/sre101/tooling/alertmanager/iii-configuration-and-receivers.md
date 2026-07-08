---
label: "III"
subtitle: "Configuration & receivers"
group: "SRE"
order: 3
---
SRE tooling — Alertmanager: Configuration & receivers
**`alertmanager.yml`** defines routes, receivers (Slack, PagerDuty, webhooks), and inhibit rules.

## 1. Essentials

One file defines **routes**, **receivers**, and optional **`inhibit_rules`**. Prometheus sends alerts with **labels** and **annotations**—routes use **`matchers`** (or legacy **`match:`**) on those labels.

## 2. Minimal skeleton

```yaml
global:
  resolve_timeout: 5m

route:
  receiver: default
  group_by: [alertname, cluster]
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - matchers:
        - severity = critical
      receiver: pager
      continue: false
    - matchers:
        - severity = warning
      receiver: slack_warnings

receivers:
  - name: default
    webhook_configs:
      - url: http://example.invalid/no-op

  - name: slack_warnings
    slack_configs:
      - api_url: https://hooks.slack.com/services/REPLACE_ME
        channel: "#warnings"
        send_resolved: true
        title: "{{ .Status | toUpper }} {{ .CommonLabels.alertname }}"
        text: "{{ range .Alerts }}{{ .Annotations.description }}\n{{ end }}"

  - name: pager
    pagerduty_configs:
      - routing_key: <SERVICE_ROUTING_KEY>
```

**Matchers:** **`severity = critical`** style (Alertmanager ≥ v0.22 **`routes[].matchers`**); older **`match:`** key/value maps still appear in many Helm charts.

## 3. Inhibition

Mute **`warning`** when **`critical`** is firing for the same logical incident:

```yaml
inhibit_rules:
  - source_matchers:
      - severity = critical
    target_matchers:
      - severity = warning
    equal: [alertname, namespace]
```

## 4. Validate

```text
amtool check-config alertmanager.yml
```

## 5. Receivers recap

| Receiver type | Typical use |
|---------------|-------------|
| **`slack_configs`** | Team channels, rich text |
| **`pagerduty_configs`** | On-call escalation (**routing_key** / Events API) |
| **`email_configs`** | Low-noise digests |
| **`webhook_configs`** | Custom automation, ticketing |

PagerDuty is **not** a substitute for Alertmanager—it is **one output channel** configured inside **`receivers`**.
