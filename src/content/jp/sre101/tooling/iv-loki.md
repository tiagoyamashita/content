---
label: "IV"
subtitle: "ロキ"
group: "SRE"
order: 4
---
SRE ツール — ロキ

すべての全文インデックス作成ではなく、ラベルに合わせて調整されたログ集約。

## 1. 役割

**Grafana Loki** は、**ラベル** (クラスター、名前空間、ポッド、アプリ) で識別されるログ ストリームを取り込みます。ラベルのインデックスを大量に作成し、ログのチャンクを圧縮します。すべてのフィールドをインデックス付きの列として扱うよりもコストがかかりません。

## 2. 中心となる概念

- **Promtail / Fluent Bit / OpenTelemetry** — 一貫したラベルを付けてログを送信するエージェント。
- **LogQL** — ラベル セレクターとライン フィルターおよびログに対するメトリック クエリを組み合わせたクエリ言語。
- **保持とストレージ** — チャンクのオブジェクトストア バックエンド。テナントごとの保持ポリシー。

## 3. SRE の実践

- Standardize **label schema** across teams so investigations (`{namespace="payments"} |= "timeout"`) stay fast.
- Correlate with traces/metrics via shared **trace IDs** or **request IDs** in log lines.
- Avoid logging secrets; scrub at the agent where possible.

## 4. ペアリング

同じサービスと時間範囲の **Grafana** のログを Prometheus グラフと並べて調べます。
