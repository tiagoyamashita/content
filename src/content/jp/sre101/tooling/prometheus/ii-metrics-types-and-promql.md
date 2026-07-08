---
label: "II"
subtitle: "メトリクスのタイプとPromQL"
group: "SRE"
order: 2
---
SRE ツール — Prometheus: メトリクス タイプと PromQL

適切な **メトリクス タイプ**で計測し、**ラベル**を管理下に保ち、**PromQL** でグラフを読み取ります。

## 1. メトリクスの種類 (クライアント ↔ エクスポジション)

|タイプ |意味 |一般的な使用法 |
|-----|----------|----------------|
| **カウンター** |増加するだけです (プロセスの再起動時にリセットされます)。 |処理されたリクエスト、エラーの合計、送信されたバイト数。 |
| **ゲージ** |上か下か。 |キューの深さ、使用中のメモリ、温度。 |
| **ヒストグラム** | **バケツ**内の観察 +`_sum`+`_count`。 |レイテンシー、ペイロード サイズ - ** によるパーセンタイル`histogram_quantile`**。 |
| **概要** |スクレイピング時に事前に計算された分位数 (クライアント側)。 | PromQL でポッド全体の集計が必要な場合は、**ヒストグラム** を推奨します。 |

説明は次のようになります。

```text
http_requests_total{method="GET",status="200"} 14217
http_request_duration_seconds_bucket{le="0.1"} 900
http_request_duration_seconds_bucket{le="+Inf"} 950
http_request_duration_seconds_sum 84.2
http_request_duration_seconds_count 950
```

## 2. ラベルとカーディナリティ

- すべての一意の **ラベル セット**は **新しい時系列**です。 **`user_id="12345"`** リクエストごと → 爆発 → OOM と遅いクエリ。
- 好む **`route="/api/orders"`** (有界セット) を生の **`path`** 制限のない URL を使用します。
- 使用 **`external_labels`** Prometheus の **`cluster`**、**`env`** - フェデレーション/リモート書き込みで一貫性があります。

## 3.インスタントとレンジの連続

- **`metric`** — 評価ステップの「現在」のインスタント ベクトル。
- **`metric[5m]`** — 範囲ベクトル (生の点のウィンドウ)。 **単独では不正です** - ** のような関数でラップする必要があります`rate`**。

## 4. PromQL パターン

**リクエストレート** (5メートル以上1秒あたりの平均):

```promql
sum(rate(http_requests_total[5m])) by (job)
```

**エラー率** (アプリに合わせてメトリクス名を調整します):

```promql
sum(rate(http_requests_total{status=~"5.."}[5m]))
/
sum(rate(http_requests_total[5m]))
```

** という名前の **ヒストグラム** からの **95 パーセンタイル レイテンシー**`http_request_duration_seconds`**:

```promql
histogram_quantile(
  0.95,
  sum by (le, job) (
    rate(http_request_duration_seconds_bucket[5m])
  )
)
```

集計 **`histogram_buckets`** **前に** **`histogram_quantile`** 複数のレプリカが同じものをエクスポートする場合 **`le`** バケツ。

**満足っぽい信号** (例 — エクスポーターに合わせて調整します):

```promql
avg_over_time(process_cpu_seconds_total[5m])
```

＃＃５。`rate`対`irate`

- **`rate(...[5m])`** — ウィンドウ全体にわたる安定した 1 秒あたりの平均。 **アラートとダッシュボードに推奨**。
- **`irate`** — 最後の 2 つのポイントに反応します。とがった;理由がわからない限り、SLO に必要なものが燃えることはめったにありません。

## 6. 記録ルール (プレビュー)

多くのダッシュボードの重い PromQL は **記録ルール** に属します (このフォルダーの **ルールと操作**を参照してください) - マテリアライズ **`job:request_latency:p95`** アドホックに再計算するのではなく、評価ごとに 1 回。
