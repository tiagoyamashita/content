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


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 148" role="img" aria-label="Prometheus evaluates alerting rules and sends firing alerts to Alertmanager; Alertmanager dedupes groups routes then notifies Slack PagerDuty email webhook">
  <defs>
    <marker id="am-flow-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0 0 L8 4 L0 8 Z" fill="#71717a"/>
    </marker>
  </defs>
  <!-- Prometheus -->
  <rect x="16" y="36" width="132" height="52" rx="6" fill="#27272a" stroke="#52525b" stroke-width="1"/>
  <text x="82" y="58" fill="#86efac" font-size="12" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Prometheus</text>
  <text x="82" y="74" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">evaluates alerting rules</text>
  <!-- Arrow 1 -->
  <line x1="148" y1="62" x2="198" y2="62" stroke="#71717a" stroke-width="2" marker-end="url(#am-flow-arr)"/>
  <text x="172" y="54" fill="#71717a" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">HTTP</text>
  <!-- Alertmanager -->
  <rect x="206" y="28" width="156" height="68" rx="6" fill="#27272a" stroke="#60a5fa" stroke-width="1"/>
  <text x="284" y="52" fill="#93c5fd" font-size="12" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Alertmanager</text>
  <text x="284" y="68" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">dedupe · group · route</text>
  <text x="284" y="84" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">inhibit · silence</text>
  <!-- Arrow 2 -->
  <line x1="362" y1="62" x2="408" y2="62" stroke="#71717a" stroke-width="2" marker-end="url(#am-flow-arr)"/>
  <!-- Receivers -->
  <rect x="416" y="36" width="132" height="52" rx="6" fill="#27272a" stroke="#52525b" stroke-width="1"/>
  <text x="482" y="56" fill="#fbbf24" font-size="12" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Receivers</text>
  <text x="482" y="74" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Slack · PagerDuty · …</text>
  <!-- Caption -->
  <text x="280" y="118" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Firing alerts are grouped then delivered — escalation apps live behind receivers.</text>
</svg></figure>

## 2. Core concepts

- **Route tree** — matchers decide which **receiver** (Slack, PagerDuty, email, webhook) gets which alerts.
- **Inhibit rules** — e.g. suppress warnings when the critical alert for the same cluster already fired.
- **Silences** — temporary mute during maintenance (with audit trail).
- **Grouping / repeat_interval** — batch noisy alerts; control how often reminders repeat.

## 3. Alertmanager vs PagerDuty (and similar)

**Alertmanager** is open-source **routing** software in the Prometheus ecosystem—it decides **how** alerts are grouped and **where** they are sent.

**PagerDuty**, Opsgenie, VictorOps, etc. are **destinations**: you configure them under **`receivers`** (e.g. **`pagerduty_configs`**). They handle **on-call schedules**, escalations, and mobile push—not the same thing as Alertmanager; they **consume** notifications **from** Alertmanager (or from other tools).

Continue with **Deployment**, **Configuration & receivers**, and **Integration & practices** in this folder.
