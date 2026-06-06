---
label: "IV"
subtitle: "スクレイピングと発見"
group: "SRE"
order: 4
---
SRE ツール — Prometheus: スクレイピングと発見

**何を**スクレイピングするか、**どのくらいの頻度で**、**ラベルをTSDBにマッピングする方法**を構成します。

## 1. 静的ターゲット (Kubernetes 以外)

最小 **`prometheus.yml`** フラグメント:

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

**`job_name`** は、ラベルを変更しない限り、デフォルトの **`job`** ラベルになります。

## 2. 一般的なスクレープノブ

|フィールド |目的 |
|------|-----------|
| **`scrape_interval`** |ジョブごとにグローバルをオーバーライドします。 |
| **`metrics_path`** | **`/metrics`** 以外のパス。 |
| **`scheme`** | **`https`** ポッド上で TLS が終了するとき。 |
| **`basic_auth` / `bearer_token`** |内部の擦り傷は稀です。ネットワークの信頼境界を優先します。 |
| **`honor_labels`** |ターゲットが供給された状態を維持 **`job`**/`instance`—フットガンが簡単。有効にする前に理解してください。 |

## 3. サービスディスカバリ（概要）

Prometheus は、**Kubernetes**、**Consul**、**EC2**、**DNS**、**files** などからターゲットを検出できます。 **Kubernetes ポッド** の例 (Operator CRD ではなく、生の Prometheus 構成):

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

通常、オペレーター (**kube-prometheus-stack**) は **`ServiceMonitor`** からこれを生成します。Prometheus 構成を手動で保守しない限り、そのパスを優先します。

## 4. 考え方のラベルを付け直す

2 つのフェーズ:

- **`relabel_configs`** — スクレイピングの前に **ターゲット メタデータ** (`__meta_*`) に対して実行されます。 **`__address__`**、**`__metrics_path__`** を設定し、ターゲット (**`action: drop`**) を削除し、ラベルをシリーズにコピーします。
- **`metric_relabel_configs`** — 取り込み前に**スクレイピングされたサンプル**に対して実行されます。高価なメトリクスを削除し、ラベルを書き換えます。

例: 高カーディナリティのメトリックを **保存前に削除**:

```yaml
metric_relabel_configs:
  - source_labels: [__name__]
    regex: noisy_http_path_bucket
    action: drop
```

**`labeldrop`** / **`labelkeep`** は慎重に使用してください。器具の固定を優先します。

## 5. フェデレーションとスケーリングのスクレイピング (ヒント)

1 つの Prometheus がすべてをスクレイピングできない場合、**フェデレーション** は他の Prometheus サーバー (**`/federated`**) から選択されたシリーズをプルします。 **Thanos / Mimir / Cortex** は、長期ストレージとグローバル クエリを拡張します。**ルールと操作**を参照してください。
