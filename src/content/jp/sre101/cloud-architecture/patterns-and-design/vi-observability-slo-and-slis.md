---
label: "VI"
subtitle: "観察可能性、SLI & SLO"
group: "クラウドアーキテクチャ"
order: 6
---
可観測性、SLI および SLO

見えないものを操作することはできません。 **可観測性** は、ログ、メトリック、トレースを組み合わせます。 **SLO** は、測定値を実行可能な目標に変えます。

＃＃１．３つの柱

|柱 |何を |ツーリングの例 |
|------|------|------|
| **ログ** |コンテキスト付きの離散イベント | CloudWatch ログ、Datadog、ELK |
| **メトリクス** |数値時系列 | Prometheus、CloudWatch メトリクス |
| **痕跡** |サービス間のリクエスト パス | OpenTelemetry → イェーガー、テンポ、X-Ray |

```text
Request abc-123
  ├─ span: gateway (12 ms)
  ├─ span: auth-service (45 ms)     ← slowest
  ├─ span: orders-service (8 ms)
  └─ span: postgres (3 ms)
```

## 2. 構造化されたロギング

**JSON ログ** — マシン解析可能、ログ アグリゲーターでフィルタリング可能。

```json
{
  "timestamp": "2026-05-19T14:22:01.123Z",
  "level": "ERROR",
  "service": "orders-api",
  "traceId": "7f3a9c2e8b1d4f6a",
  "spanId": "a1b2c3d4",
  "message": "Payment declined",
  "orderId": "ord-9281",
  "userId": "usr-441",
  "durationMs": 842
}
```

|悪い |良い |
|-----|------|
|`ERROR payment failed for user`| JSON と`orderId`、`traceId`、`errorCode`|
|ログ PII (完全なカード番号) |機密フィールドをマスクまたは省略する |

## 3. 相関関係 ID

**API Gateway** に注入します。すべてのホップで伝播します。

```http
GET /api/orders/9281 HTTP/1.1
X-Request-Id: 7f3a9c2e-8b1d-4f6a-9c2e-8b1d4f6a9c2e
traceparent: 00-7f3a9c2e8b1d4f6a-a1b2c3d4e5f60708-01
```

```java
// MDC for logging — Java 22
MDC.put("traceId", traceId);
try {
  log.info("Processing order {}", orderId);
} finally {
  MDC.clear();
}
```

1 つの ID ごとにログを検索 → サービス全体のリクエスト ストーリー全体。

## 4. 重要なメトリクス (RED メソッド)

各サービスについて:

|メトリック |意味 |
|--------|--------|
| **料金** | 1 秒あたりのリクエスト |
| **エラー** |失敗したリクエスト / 合計 |
| **期間** |レイテンシー (p50、p95、p99) |

インフラストラクチャの **USE メソッド**: **使用率**、**飽和度**、**エラー** (CPU、ディスク キューの深さ)。

## 5. SLI、SLO、SLA

|用語 |定義 |例 |
|------|-----------|----------|
| **SLI** | **指標** — 測定するもの | p99 レイテンシ = 120 ミリ秒 |
| **SLO** | **目的** — 内部目標 | p99 レイテンシー< 200 ms over 30 days |
| **SLA** | **Agreement** — contractual | 99.9% uptime or credit |

```text
SLI (measure)  →  SLO (target)  →  SLA (contract with customer)
     │                │
     └── error budget: 100% - SLO = allowed bad minutes/month
```

**Error budget:** if SLO is 99.9%, you have ~43 min downtime/month. Budget exhausted → freeze features, focus on reliability.

## 6. Example SLO table

| Service | SLI | SLO (30-day) | Alert |
|---------|-----|--------------|-------|
| Public API | Availability | 99.95% | < 99.9% in 1h window |
| Public API | Latency p99 | < 300 ms | p99 >5分間500ミリ秒 |
|チェックアウト |成功率 | 99.5% |エラー率 > 1% |
|バッチジョブ |完成 | 99% 予定どおり | DLQ 深さ > 100 |

## 7. 警告の原則

| | に関するアラート| ではアラートを発しない
|----------|----------------|
| SLO 燃焼率 |すべてのログ ERROR 行 |
|症状（レイテンシーアップ） |考えられる原因 (CPU 80% のみ) |
|ユーザーに見える影響 |開発環境のノイズ |

```text
Page on-call:  SLO breach imminent (fast burn)
Ticket only:   Disk 70% — trend warning
```

## 8. OpenTelemetry フロー

```text
App SDK → OTLP exporter → Collector → Backend (Tempo, Datadog)
                │
                └── same traceId in logs (log correlation)
```

メトリクス、ログ、トレースのための 1 つのインストルメンテーション標準。

## 9. クラウドネイティブ サービス

| AWS |アズール | GCP |
|-----|----------|-----|
| CloudWatch + X-Ray |モニター + アプリのインサイト |クラウドモニタリング + トレース |
| Grafana を管理 | | |

クラウド間でのポータブル計測には **OpenTelemetry** を推奨します。

## 10. リハーサルの答え

- **3 つの柱** — ログ、メトリクス、トレース。
- **相関 ID** — 1 つのユーザー リクエストを複数のサービスに結び付けます。
- **SLI vs SLO** — 測定とターゲット。 SLA は契約/罰則を追加します。
- **構造化 JSON** を使用する理由 — プレーン テキストの正規表現ではなく、クエリ可能なフィールド。

**関連:** [API Gateway とサービス メッシュ](v-api-gateway-and-service-mesh.md)、CI/CD [パイプラインの可観測性と DORA](../../cicd/security-and-best-practices/vi-pipeline-observability-and-dora.md）。
