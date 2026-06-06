---
label: "III"
subtitle: "構成と受信機"
group: "SRE"
order: 3
---
SRE ツール — Alertmanager: 構成と受信機






**`alertmanager.yml`** ルート、レシーバー (Slack、PagerDuty、Webhook)、および禁止ルールを定義します。

## 1. 必需品

1 つのファイルで **ルート**、**レシーバー**、およびオプションの ** を定義します`inhibit_rules`**。 Prometheus は **ラベル** と **注釈 ** を含むアラートを送信します。ルートは ** を使用します`matchers`** (または従来の **`match:`**) ラベルに記載されています。

## 2. かなりのスケルトン

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

**マッチャー:** **`severity = critical`** スタイル (Alertmanager ≥ v0.22 **`routes[].matchers`**);古い**`match:`** キー/値マップは依然として多くの Helm チャートに表示されます。

## 3. 阻害

ミュート **`warning`** いつ **`critical`** は同じ論理インシデントに対して起動しています:

```yaml
inhibit_rules:
  - source_matchers:
      - severity = critical
    target_matchers:
      - severity = warning
    equal: [alertname, namespace]
```

## 4. 検証する

```text
amtool check-config alertmanager.yml
```

## 5. レシーバーのまとめ

|受信機のタイプ |一般的な使用法 |
|--------------|---------------|
| **`slack_configs`** |チーム チャネル、リッチ テキスト |
| **`pagerduty_configs`** |オンコール エスカレーション (**routing_key** / イベント API) |
| **`email_configs`** |低ノイズダイジェスト |
| **`webhook_configs`** |カスタムオートメーション、チケット発行 |

PagerDuty は Alertmanager の代替品ではありません**。** 内部に構成された **1 つの出力チャネル**です`receivers`**。
