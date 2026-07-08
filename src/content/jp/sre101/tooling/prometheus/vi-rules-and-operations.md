---
label: "VI"
subtitle: "ルールと運営"
group: "SRE"
order: 6
---
SRE ツール — Prometheus: ルールと操作

記録ルール、警告ルール、HA ヒント、およびオペレーターの習慣。

## 1. ルールファイル

** から YAML ルール グループを参照`prometheus.yml`**:

```yaml
rule_files:
  - /etc/prometheus/rules/*.yml
```

## 2. 記録ルール

負荷の高いクエリを ** ごとに 1 回事前計算します`evaluation_interval`**:

```yaml
groups:
  - name: recording.rules
    interval: 30s
    rules:
      - record: job:http_requests:rate5m
        expr: sum(rate(http_requests_total[5m])) by (job)
```

ダッシュボードとアラートのリファレンス **`job:http_requests:rate5m`** 長く繰り返す代わりに **`rate`** 式。

## 3. アラートルール

Prometheus は ** を評価します`expr`**; ** が true の場合`for`** 継続時間、**Alertmanager** にアラートを起動します:

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

整列 **`severity`** **Alertmanager** ルート (`critical`対`warning`）。

## 4. 配線 Alertmanager

```yaml
alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
```

オペレーター管理の Prometheus は通常、これが事前構成された状態で出荷されます。Helm 値をカスタマイズした後に確認してください。

## 5. 高可用性と長期保管

- **HA スクレイピング**: 同一の構成で AZ ごとに Prometheus を複製します。クエリ レイヤーで重複を排除するか、アラート用の重複を受け入れます (Alertmanager 重複排除通知)。
- **フェデレーション**: 階層型 Prometheus プル **`/federate`** 上向きに凝集します。
- **Thanos / Mimir / Cortex**: 耐久性のあるストレージ + グローバル クエリ。リモート書き込みサイドカーはブロックをオフノードに出荷します。

## 6. 保持と容量

チューニング**`--storage.tsdb.retention.time`** とディスク;カーディナリティは生のスクレイピング レートよりも RAM/disk を支配します。インストルメンテーションおよび ** のラベルを保護します。`metric_relabel_configs`**。

## 7. __​​ IT0__ の実践

- クリティカル パス用のツール **RED** / **USE**。レイテンシのパーセンタイルのヒストグラム。
- 保つ **`team`**、**`severity`**、**`service`** ルーティングが予測可能なラベル。
- テストルール **`expr`** Grafana を使用して **探索**してから、人間にページングしてください。

**Grafana** は PromQL を視覚化します。 **Alertmanager** は通知ルーティングを所有します。Tooling の **Alertmanager** サブフォルダーを参照してください。
