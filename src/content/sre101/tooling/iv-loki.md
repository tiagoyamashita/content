---
label: "IV"
subtitle: "ロキ"
group: "SRE"
order: 4
---
SRE ツール — Loki

すべての全文インデックス作成ではなく、ラベルに合わせて調整されたログ集約。

## 1. 役割

**Grafana Loki** は、**ラベル** (クラスター、名前空間、ポッド、アプリ) で識別されるログ ストリームを取り込みます。ラベルのインデックスを大量に作成し、ログのチャンクを圧縮します。すべてのフィールドをインデックス付きの列として扱うよりもコストがかかりません。

## 2. 中心となる概念

- **Promtail / Fluent Bit / OpenTelemetry** — agents that ship logs with consistent labels.
- **LogQL** — query language combining label selectors with line filters and metric queries over logs.
- **Retention & storage** — object-store backends for chunks;テナントごとの保持ポリシー。

## 3. SRE の実践

- チーム全体で **ラベル スキーマ**を標準化することで、調査 (`{namespace="payments"} |= "timeout"`) を迅速に行うことができます。
- ログ行の共有 **トレース ID** または **リクエスト ID** を介してトレース/メトリクスと関連付けます。
- 秘密の記録を避ける。可能な場合はエージェントに問い合わせてください。

## 4. ペアリング

**Grafana** のログを、同じサービスと時間範囲の Prometheus グラフと並べて調査します。
