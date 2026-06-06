---
label: "III"
subtitle: "構成と受信機"
group: "SRE"
order: 3
---
SRE ツール — アラートマネージャー: 構成と受信者

**`alertmanager.yml`** は、ルート、レシーバー (Slack、PagerDuty、Webhook)、および禁止ルールを定義します。

## 1. 必需品

1 つのファイルでは、**ルート**、**レシーバー**、およびオプションの**`inhibit_rules`**を定義します。 Prometheus は、**ラベル** と **注釈** を使用してアラートを送信します。ルートは、これらのラベルで **`matchers`** (または従来の **`match:`**) を使用します。

## 2. 最小限のスケルトン

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

**マッチャー:** **`severity = critical`** スタイル (Alertmanager ≥ v0.22 **`routes[].matchers`**)。古い **`match:`** キー/値マップは、依然として多くの Helm チャートに表示されます。

## 3. 阻害

同じ論理インシデントに対して **`critical`** が発生しているときに **`warning`** をミュートします。

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

## 5. レシーバーの要約

|受信機のタイプ |一般的な使用法 |
|--------------|---------------|
| **`slack_configs`** |チーム チャネル、リッチ テキスト |
| **`pagerduty_configs`** |オンコール エスカレーション (**routing_key** / イベント API) |
| **`email_configs`** |低ノイズダイジェスト |
| **`webhook_configs`** |カスタムオートメーション、チケット発行 |

PagerDuty は Alertmanager の代替品ではありません。**`receivers`** 内に構成された **1 つの出力チャネル**です。
