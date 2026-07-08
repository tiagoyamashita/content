---
label: "IV"
subtitle: "統合と実践"
group: "SRE"
order: 4
---
SRE ツール — Alertmanager: 統合と実践

Prometheus を Alertmanager に接続し、ページングを正常に保ちます。

## 1. Prometheus を Alertmanager にポイントします

で **`prometheus.yml`** (または演算子 **`Prometheus`** CR **`spec.alerting`**):

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093   # Service DNS in-cluster
```

Prometheus オペレータのセットアップは、多くの場合、クラスタに**事前に接続**されています**`Alertmanager`** サービス - オーバーライドを避ける **`alerting`** 偶然。

## 2. アラート ルールの例 (Prometheus)

ラベルは Alertmanager でルートします。 **`annotations`** Slack/メール テンプレートを入力します:

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

- デザイン **`severity`** したがって、ページングは​​ **ユーザーに影響を与える** または **SLO-burn** 条件の場合にのみ発生します。
- 置く **`runbook_url`** （または **`description`** with links) in **annotations** so notifications open context fast.
- テスト **`alertmanager.yml`** と **`amtool check-config`**; prod ルートの前に **ステージング** Slack/PagerDuty Webhook を実行します。
- 好む **`AlertmanagerConfig`** 共有クラスター上の名前空間ごとの RBAC により、巨大なグローバル ファイルを 1 つ持たずにチームがレシーバーを所有できるようになります。

## 4. ペアリング

**Prometheus** はルールを評価し、アラートの発生を転送します。 **Alertmanager** は、**重複排除、グループ化、ルーティング**、および Slack、PagerDuty などへの**配信**を所有しています。
