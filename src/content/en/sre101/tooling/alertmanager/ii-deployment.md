---
label: "II"
subtitle: "Deployment"
group: "SRE"
order: 2
---
SRE tooling — Alertmanager: Deployment
Run Alertmanager locally or on Kubernetes.

## 1. Docker (quickest lab)

```text
docker run -d --name alertmanager -p 9093:9093 \
  -v /absolute/path/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --web.external-url=http://localhost:9093
```

UI: **`http://localhost:9093`**. Swap **`/absolute/path`** for your machine.

## 2. Kubernetes (kube-prometheus-stack / Prometheus Operator)

Helm usually ships an **`Alertmanager`** CR (**`monitoring.coreos.com/v1`**) managed by the Operator. You customize **`alertmanager.config`** (or **`AlertmanagerConfig`** CRDs if enabled)—values merge into the generated **`Secret`**. Scale HA with **`replicas`** on the **`Alertmanager`** CR.

Rough Helm **`values.yaml`** sketch:

```yaml
alertmanager:
  enabled: true
  alertmanagerSpec:
    replicas: 2
  config:
    global:
      resolve_timeout: 5m
    route:
      receiver: default
      group_by: ["alertname", "namespace"]
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 12h
    receivers:
      - name: default
        slack_configs:
          - api_url: https://hooks.slack.com/services/XXX/YYY/ZZZ
            channel: "#alerts"
```

Treat **`api_url`** and tokens as secrets (**ExternalSecrets**, **SealedSecrets**, or CSI)—avoid committing real URLs.

## 3. Binary / VM

Download release from Prometheus projects; point **`--config.file`** at **`alertmanager.yml`**; run under **systemd** with **`Restart=always`** and **`User`** without root.

Next: **Configuration & receivers** for **`alertmanager.yml`** details.
