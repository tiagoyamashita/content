---
label: "III"
subtitle: "計装"
group: "SRE"
order: 3
---
SRE ツール — Prometheus: 計測器


Expose **`/metrics`** (or framework equivalent) from your application process.

## 1. 原則

Prometheus **プロセスから**プルします。**テキスト表示形式**を返す HTTP ハンドラーを公開します。存続期間の長いサービスは、異常なバッチ パターンを除き、**プッシュゲートウェイ**を介してプッシュすべきではありません**。

## 2. Spring Boot (マイクロメーター)

Add Actuator + the Prometheus registry so **`/actuator/prometheus`** exposes JVM and HTTP metrics automatically:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
  <groupId>io.micrometer</groupId>
  <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
```

```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,prometheus
```

Register **business** signals via **`MeterRegistry`** (`Counter`, `Timer`, **`DistributionSummary`**). **`Timer`** maps well to **histograms** for latency SLIs. Defaults already cover JVM and MVC/WebFlux HTTP metrics when starters match your stack.

## 3. その他のランタイム (パターン)

- **Go** — **`prometheus/client_golang`**: register collectors, **`promhttp.Handler()`** on **`/metrics`**.
- **Python** — **`prometheus_client`**: **`Counter`**, **`Histogram`**, expose via **`start_http_server`** or **`generate_latest()`** in Flask/FastAPI/Starlette.
- **Node.js** — **`prom-client`**: **`collectDefaultMetrics()`** plus app counters; expose **`register.metrics()`** on HTTP.

## 4. セキュリティとトポロジ

- クラスター/VPC (ネットワーク ポリシー、セキュリティ グループ) の**内部** にスクレイピング エンドポイントをバインドします。メトリクスにより展開トポロジが漏洩することがよくあります。
- **プロセスごとに 1 つのスクレープ ポート** を推奨します。クライアントを埋め込むことができないサードパーティ アプリ用のサイドカー エクスポーター。

## 5. 計測器のチェックリスト

1. **RED** per critical handler/service: **rate**, **errors**, **duration** (histogram).
2. Bounded label dimensions (**`method`**, **`status`**, **`tenant_tier`**)—never raw user IDs.
3. Name metrics **`_<unit>_total`** / **`_seconds`** / **`_bytes`** consistently (`*_bucket`, `*_sum`, `*_count` for histograms).

次: **スクレイピングと検出** (Prometheus 側構成の場合)、または k8s のみにデプロイする場合は **Kubernetes**。
