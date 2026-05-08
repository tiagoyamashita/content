---
label: "I"
subtitle: "Intro"
group: "SRE"
order: 1
---
SRE tooling — Alertmanager: Intro
Dedupe, group, and route Prometheus alerts to humans and systems.

## 1. Role

**Alertmanager** receives alerts from **Prometheus** (or compatible sources), **suppresses** duplicates, **groups** related fires into single notifications, and **routes** them by labels (team, severity, region).

## 2. Core concepts

- **Route tree** — matchers decide which **receiver** (Slack, PagerDuty, email, webhook) gets which alerts.
- **Inhibit rules** — e.g. suppress warnings when the critical alert for the same cluster already fired.
- **Silences** — temporary mute during maintenance (with audit trail).
- **Grouping / repeat_interval** — batch noisy alerts; control how often reminders repeat.

## 3. Alertmanager vs PagerDuty (and similar)

**Alertmanager** is open-source **routing** software in the Prometheus ecosystem—it decides **how** alerts are grouped and **where** they are sent.

**PagerDuty**, Opsgenie, VictorOps, etc. are **destinations**: you configure them under **`receivers`** (e.g. **`pagerduty_configs`**). They handle **on-call schedules**, escalations, and mobile push—not the same thing as Alertmanager; they **consume** notifications **from** Alertmanager (or from other tools).

Continue with **Deployment**, **Configuration & receivers**, and **Integration & practices** in this folder.
