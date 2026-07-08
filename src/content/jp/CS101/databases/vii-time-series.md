---
label: "VII"
subtitle: "時系列"
group: "データベース"
order: 7
---
時系列データベース

**時系列** データベースは、**(タイムスタンプ、測定値)** データの **追加の多い** ストリームを最適化します: サーバー メトリクス、センサー読み取り値、株価ティック、アプリケーション トレース。クエリでは、「主キーによる行 8812 のフェッチ」だけではなく、**時間範囲で何が起こったか**、**レート**、**バケットによる集計**が尋ねられます。

## 1. データモデル

典型的な **回線プロトコル** の形状 (InfluxDB / Prometheus の概念):

```text
measurement,tag1=v1,tag2=v2 field1=1.2,field2=42i 1716120000000000000
└─ name ─┘ └── labels (indexed) ──┘ └── values ──┘ └──── timestamp ────┘
```

例 - CPU メトリクス:

```text
cpu,host=web-01,region=us-east usage=0.73,idle=0.27 1716120000
```

|パート |役割 |
|------|------|
| **測定** |メトリック名 (`cpu`、`http_requests`) |
| **タグ/ラベル** |フィルター/グループの低カーディナリティ ディメンション (`host`、`region`) |
| **フィールド** |実際の数値 (使用量、バイト数、カウント) |
| **タイムスタンプ** |サンプルが採取されたとき (多くの場合、ナノ秒の精度) |

**タグ**にはインデックスが付けられます。 **カーディナリティの高いタグ** (すべてのリクエストのユーザー ID) はストレージを爆発させ、クエリを遅くします。慎重に設計してください。

## 2. アクセスパターン

|クエリの種類 |例 |
|-----------|-----------|
| **範囲スキャン** |過去 24 時間の `host=web-01` の CPU |
| **ダウンサンプル** | 5 分間のバケットごとの平均 |
| **レート/デリバティブ** |カウンタからの 1 秒あたりのリクエスト |
| **警告** | `avg(cpu) > 0.9` 5 分間 |

```text
Writes:  ──► append only (mostly immutable past)
Reads:   ──► recent window hot; old data cold or aggregated
```

## 3. 保持と圧縮

TSDB は古いデータを自動的に**ドロップまたはロールアップ**します。

```text
Raw 10s resolution  → keep 7 days
5m averages         → keep 90 days
1h averages         → keep 2 years
```

**圧縮** は、小さなファイルを大きなブロックにマージします。 **WAL** は取り込み時の耐久性を保証します。

## 4. Prometheus スタイルの例

メトリックの説明 (テキスト形式):

```text
http_requests_total{method="GET", status="200"} 1027
http_requests_total{method="POST", status="500"} 3
```

**PromQL** クエリ:

```promql
rate(http_requests_total{status="500"}[5m])
sum by (method) (rate(http_requests_total[1h]))
```

Prometheus はローカル **TSDB** を備えた **プルベース** (ターゲットをスクレイピング) であり、Kubernetes 監視では一般的です。

## 5. SQL 時系列拡張

**TimescaleDB** (PostgreSQL 拡張機能) と **InfluxDB 3** は、SQL との境界線を曖昧にしています。

```sql
SELECT time_bucket('5 minutes', ts) AS bucket,
       avg(cpu_usage)
FROM metrics
WHERE host = 'web-01'
  AND ts > NOW() - INTERVAL '24 hours'
GROUP BY bucket
ORDER BY bucket;
```

チームがすでに PostgreSQL を実行していて、**ハイブリッド** リレーショナル + メトリクスが必要な場合に使用します。

## 6. 強みと限界

**強み**

- **最適化された取り込み** — 毎秒数百万ポイント
- **組み込みのダウンサンプリング** および保持ポリシー
- **効率的な圧縮** (同様のタイムスタンプ、デルタ エンコーディング)
- **アラート** 統合 (Prometheus Alertmanager、流入タスク)

**制限**

- **一般的な OLTP** には悪い - ユーザー プロファイルをここに保存しないでください
- **カーディナリティ爆弾** — 無制限のタグ値は、TSDB ごとに害を及ぼします
- 過去の単一ポイントの **更新/削除** は厄介です (不変ログの考え方)
- ビジネス エンティティ全体にわたる **長距離アドホック JOIN** — **ウェアハウス** / SQL を使用します

## 7. 時系列とワイド列

どちらも大量の書き込みを処理します。 **TSDB** は **時間セマンティクス** (保持、ロールアップ、レート関数) を追加します。 **Cassandra** は時間順の行を保存できますが、ロールアップ ジョブは自分で作成します。監視が製品の場合は **TSDB** を選択します。 **ワイド列** イベントが多くの属性を持つ汎用行である場合 [ワイド列](v-wide-column.md)。

## 8. 時系列を選択する場合

- **可観測性** — メトリクス、ログ由来のカウンター、SLO ダッシュボード
- **IoT** — センサー ストリーム
- **財務** — ティック (多くの場合、分析用に特化したシステム + TSDB)
- **エネルギー / 産業** — SCADA の歴史

## 9. 例

|製品 |メモ |
|----------|----------|
| **Prometheus** |クラウドネイティブのメトリクス、PromQL |
| **InfluxDB** |ラインプロトコル、Flux / SQL |
| **タイムスケールDB** | PostgreSQL 拡張子 |
| **OpenTelemetry → バックエンド** | TSDB または SaaS へのベンダー中立の取り込み |

## 10. カーディナリティの経験則

```text
Good tags:   host, service, region, status_class  (bounded sets)
Risky tags:  user_id, request_id, url_path        (millions of values)
```

**クライアントでの集計** または **サンプリング** の高カーディナリティ ディメンションを優先します。

## 11. 関連

- **概要** — [データベースの概要](i-overview.md)
- **ワイドカラム** — TS 固有のロールアップを使用しない大規模なイベント ログ [ワイドカラム](v-wide-column.md)
- **Key-value** — エクスポート前の短期間のカウンター [Key-value](iii-key-value.md)
