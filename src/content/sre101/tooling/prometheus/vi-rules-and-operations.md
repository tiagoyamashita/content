---
label: "VI"
subtitle: "ルールと運営"
group: "SRE"
order: 6
---
SRE ツール — Prometheus: ルールと操作

記録ルール、警告ルール、HA ヒント、オペレーターの習慣。

## 1. ルールファイル

**`prometheus.yml`** の YAML ルール グループを参照します。

```yaml
rule_files:
  - /etc/prometheus/rules/*.yml
```

## 2. 記録ルール

負荷の高いクエリを **`evaluation_interval`** ごとに 1 回事前計算します。

```yaml
groups:
  - name: recording.rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

ダッシュボードとアラートは、長い **`rate`** 式を繰り返すのではなく、**`job:http_requests:rate5m`** を参照します。

## 3. アラートルール

プロメテウスは **`expr`** を評価します。 **`for`** 期間にわたって true の場合、**Alertmanager** にアラートが発行されます。

```yaml
groups:
  - name: alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Elevated 5xx fraction"
          description: "See runbook https://wiki/runbooks/high-5xx"
```

**`severity`** を **Alertmanager** ルートに合わせます (`critical` 対 `warning`)。

## 4. 配線アラートマネージャー

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
```

オペレーター管理の Prometheus は通常、これが事前構成された状態で出荷されます。Helm 値をカスタマイズした後に確認してください。

## 5. 高可用性と長期保管

- **HA スクレイピング**: 同一の構成で AZ ごとに Prometheus を複製します。クエリ レイヤーで重複排除するか、アラート用の重複を受け入れます (Alertmanager 重複排除通知)。
- **フェデレーション**: 階層型 Prometheus は **`/federate`** アグリゲートを上方にプルします。
- **Thanos / Mimir / Cortex**: 耐久性のあるストレージ + グローバル クエリ。リモート書き込みサイドカーはブロックをオフノードに出荷します。

## 6. 保持と容量

**`--storage.tsdb.retention.time`** とディスクを調整します。カーディナリティは、生のスクレイピング レートよりも RAM/ディスクを支配します。インストルメンテーションおよび **`metric_relabel_configs`** のラベルを保護します。

## 7. SRE の実践

- クリティカル パスには **RED** / **USE** を設定します。レイテンシのパーセンタイルのヒストグラム。
- **`team`**、**`severity`**、**`service`** ラベルをルーティング用に予測可能な状態に保ちます。
- 人間にページングする前に、Grafana **Explore** を使用してルール **`expr`** をテストします。

**Grafana** は PromQL を視覚化します。 **Alertmanager** は通知ルーティングを所有します。Tooling の **Alertmanager** サブフォルダーを参照してください。
