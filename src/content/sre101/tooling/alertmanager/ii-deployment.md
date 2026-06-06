---
label: "II"
subtitle: "導入"
group: "SRE"
order: 2
---
SRE ツール — アラートマネージャー: 導入

Alertmanager をローカルまたは Kubernetes 上で実行します。

## 1. Docker (最も速いラボ)

```text
docker run -d --name alertmanager -p 9093:9093 \
  -v /absolute/path/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  prom/alertmanager \
  --config.file=/etc/alertmanager/alertmanager.yml \
  --web.external-url=http://localhost:9093
```

UI: **`http://localhost:9093`**。 **`/absolute/path`** をあなたのマシンに置き換えてください。

## 2. Kubernetes (kube-prometheus-stack / Prometheus Operator)

Helm は通常、オペレーターによって管理される **`Alertmanager`** CR (**`monitoring.coreos.com/v1`**) を出荷します。 **`alertmanager.config`** (または有効な場合は **`AlertmanagerConfig`** CRD) をカスタマイズすると、生成された **`Secret`** に値がマージされます。 **`Alertmanager`** CR で **`replicas`** を使用して HA をスケールします。

ラフヘルム **`values.yaml`** スケッチ:

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

**`api_url`** とトークンをシークレット (**ExternalSecrets**、**SealedSecrets**、または CSI) として扱います。実際の URL のコミットは避けてください。

## 3. バイナリ/VM

Prometheus プロジェクトからリリースをダウンロードします。 **`alertmanager.yml`**の地点**`--config.file`**。 root なしで **`Restart=always`** および **`User`** を使用して **systemd** の下で実行します。

次へ: **構成と受信機**、**`alertmanager.yml`** の詳細。
