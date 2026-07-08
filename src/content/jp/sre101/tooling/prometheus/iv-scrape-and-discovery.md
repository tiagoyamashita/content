---
label: "IV"
subtitle: "スクレイピングと発見"
group: "SRE"
order: 4
---
SRE ツール — Prometheus: スクレイピングと検出

**何を**スクレイピングするか、**どのくらいの頻度で**、**ラベルをTSDBにマッピングする方法**を構成します。

## 1. 静的な目標 (非 Kubernetes)

最小限 **`prometheus.yml`** フラグメント:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: checkout-api
    metrics_path: /actuator/prometheus   # or /metrics
    static_configs:
      - targets:
          - checkout-api.internal:8080
        labels:
          env: prod
          region: us-east-1
```

**`job_name`** がデフォルトになります **`job`** 再ラベル付けしない限り、ラベルを付けます。

## 2. 一般的なクレープノブ

|フィールド |目的 |
|------|-----------|
| **`scrape_interval`** |ジョブごとにグローバルをオーバーライドします。 |
| **`metrics_path`** | **以外のパス`/metrics`**。 |
| **`scheme`** | **`https`** ポッド上で TLS が終了したとき。 |
| **`basic_auth`/`bearer_token`** |内部の擦り傷は稀です。ネットワークの信頼境界を優先します。 |
| **`honor_labels`** |ターゲットが提供したものを維持 **`job`**/`instance`—フットガンが簡単です。有効にする前に理解してください。 |

## 3. サービスディスカバリ（概要）

Prometheus は、**Kubernetes**、**Consul**、**EC2**、**DNS**、**ファイル** などからターゲットを検出できます。 **Kubernetes ポッド** の例 (生の Prometheus 構成 - Operator CRD ではありません):

```yaml
scrape_configs:
  - job_name: kubernetes-pods
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

オペレーター (**kube-prometheus-stack**) は通常、** からこれを生成します。`ServiceMonitor`** - Prometheus 構成を手動で保守する場合を除き、そのパスを優先します。

## 4. 考え方のラベルを付け直す

2つのフェーズ:

- **`relabel_configs`** — **ターゲット メタデータ** で実行されます (`__meta_*`) 削る前。セット**`__address__`**、**`__metrics_path__`**、ターゲットをドロップします (**`action: drop`**)、ラベルをシリーズにコピーします。
- **`metric_relabel_configs`** — 取り込む前に **スクレイピングされたサンプル** で実行されます。高価なメトリクスを削除し、ラベルを書き換えます。

例: ハイカーディナリティのメトリックを **保存前に削除**:

```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: noisy_http_path_bucket
    action: drop
```

使用 **`labeldrop`** / **`labelkeep`** 控えめに - 器具を固定することを好みます。

## 5. フェデレーションとスケーリングのスクレイピング (ヒント)

1 つの Prometheus がすべてをスクレイピングできない場合、**フェデレーション** は他の Prometheus サーバーから選択されたシリーズをプルします (**`/federated`**); **Thanos / Mimir / Cortex** は、長期ストレージとグローバル クエリを拡張します。**ルールと操作**を参照してください。
