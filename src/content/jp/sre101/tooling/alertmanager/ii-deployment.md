---
label: "II"
subtitle: "導入"
group: "SRE"
order: 2
---
SRE ツール — Alertmanager: 導入

Alertmanager をローカルまたは Kubernetes 上で実行します。

## 1. Docker (最も早いラボ)

```text
docker run -d --name alertmanager -p 9093:9093 \
  -v /absolute/path/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --web.external-url=http://localhost:9093
```

UI: **`http://localhost:9093`**。スワップ**`/absolute/path`** お使いのマシンの場合。

## 2. Kubernetes (kube-prometheus-stack / Prometheus オペレーター)

Helm は通常 ** を出荷します`Alertmanager`** CR (**`monitoring.coreos.com/v1`**) オペレーターによって管理されます。 **をカスタマイズします`alertmanager.config`** （または **`AlertmanagerConfig`** CRD が有効な場合) - 生成された ** に値がマージされます。`Secret`**。 ** を使用して HA をスケールします`replicas`** の **`Alertmanager`** CR。

ラフヘルム**`values.yaml`** スケッチ:

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

扱う **`api_url`** およびシークレットとしてのトークン (**ExternalSecrets**、**SealedSecrets**、または CSI) - 実際の URL のコミットを避けます。

## 3. バイナリ / VM

Prometheus プロジェクトからリリースをダウンロードします。ポイント **`--config.file`** で **`alertmanager.yml`**; **systemd** で ** を使用して実行します`Restart=always`** そして **`User`** ルートなし。

次へ: ** の **構成と受信機**`alertmanager.yml`** 詳細。
