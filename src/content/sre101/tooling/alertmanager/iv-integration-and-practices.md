---
label: "IV"
subtitle: "統合と実践"
group: "SRE"
order: 4
---
SRE ツール — Alertmanager: 統合と実践

Prometheus を Alertmanager に接続し、ページングを正常に保ちます。

## 1. プロメテウスをアラートマネージャーに指示する

**`prometheus.yml`** (またはオペレータ **`Prometheus`** CR **`spec.alerting`**):

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093   # Service DNS in-cluster
```

Prometheus Operator のセットアップは、多くの場合、クラスター **`Alertmanager`** サービスに **事前に接続**されており、誤って **`alerting`** をオーバーライドすることを避けてください。

## 2. アラート ルールの例 (Prometheus)

Alertmanager でのラベルのルート。 **`annotations`** Slack/メール テンプレートを入力します:

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

## 3. SRE の実践

- ページングが **ユーザーに影響する** または **SLO 書き込み** の場合にのみ発生するように **`severity`** を設計します。
- **注釈**に **`runbook_url`** (またはリンクを含む **`description`**) を入力すると、通知でコンテキストがすぐに開きます。
- **`alertmanager.yml`** を **`amtool check-config`** でテストします。 prod ルートの前に **ステージング** Slack/PagerDuty Webhook を実行します。
- 共有クラスターでは **`AlertmanagerConfig`** 名前空間ごとの RBAC を優先するため、チームは 1 つの巨大なグローバル ファイルを使用せずにレシーバーを所有できます。

## 4. ペアリング

**Prometheus** はルールを評価し、アラートの発生を転送します。 **Alertmanager** は、**重複排除、グループ化、ルーティング**、および Slack、PagerDuty などへの**配信**を所有しています。
