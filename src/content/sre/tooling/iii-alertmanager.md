---
label: "III"
subtitle: "Alertmanager"
group: "SRE"
order: 3
---
SRE tooling — Alertmanager
Dedupe, group, and route Prometheus alerts to humans and systems.

## 1. Role

**Alertmanager** receives alerts from **Prometheus** (or compatible sources), **suppresses** duplicates, **groups** related fires into single notifications, and **routes** them by labels (team, severity, region).

## 2. Core concepts

- **Route tree** — matchers decide which receiver (Slack, PagerDuty, email, webhook) gets which alerts.
- **Inhibit rules** — e.g. suppress warnings when the critical alert for the same cluster already fired.
- **Silences** — temporary mute during maintenance (with audit trail).
- **Grouping / repeat_interval** — batch noisy alerts; control how often reminders repeat.

## 3. SRE practices

- Design **`severity`** so paging only happens for **user-impacting** or **SLO-burn** conditions.
- Document **runbooks** linked from annotations (`runbook_url`) in alert definitions.
- Test routes with **amtool** or synthetic alerts before incident Friday night.

## 4. Pairing

Prometheus evaluates rules; Alertmanager owns **who gets paged** and **when**.
