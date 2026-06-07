---
label: "V"
subtitle: "Kubernetes"
group: "SRE"
order: 5
---
SRE ツール — Prometheus: Kubernetes






**Prometheus 演算子** ** を使用します`ServiceMonitor`** / **`PodMonitor`** 手作業で巨大なメンテナンスを行う代わりに **`scrape_configs`** 可能な場合。

## 1. 前提条件

ワークロードにより **`/actuator/prometheus`** または **`/metrics`** コンテナポート上 (例 **8080**)。 **`Prometheus`** CR は **選択してください** **`ServiceMonitor`** 経由の ** オブジェクト`serviceMonitorSelector`** / **`serviceMonitorNamespaceSelector`** (**kube-prometheus-stack** などの Helm チャートでは、** のようなラベルが必要になることがよくあります)`release: kube-prometheus-stack`** - クラスターと一致します)。

## 2. 名前付きポートを利用したサービス

**`ServiceMonitor`** 参考文献 **`port: http`** 名前** さん:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: checkout-api
  labels:
    app: checkout-api
spec:
  selector:
    app: checkout-api
  ports:
    - name: http
      port: 8080
      targetPort: 8080
```

## 3. サービスモニター

サービスによって選択されたすべてのポッドをスクレイピングします。

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: checkout-api
  labels:
    app: checkout-api
    release: kube-prometheus-stack   # must match Prometheus CR selector
spec:
  selector:
    matchLabels:
      app: checkout-api
  endpoints:
    - port: http
      interval: 30s
      path: /actuator/prometheus       # or /metrics
      scheme: http
```

## 4. ポッドモニター

Pod を直接スクレイピングする場合 (安定したサービスがない場合、または単一コンテナーに焦点を当てた場合) に使用します。

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PodMonitor
metadata:
  name: checkout-api
  labels:
    release: kube-prometheus-stack
spec:
  selector:
    matchLabels:
      app: checkout-api
  podMetricsEndpoints:
    - port: http
      interval: 30s
      path: /actuator/prometheus
```

Pod テンプレートは ** を宣言する必要があります`ports`** と **`name: http`** (または ** を揃える)`port`**あなたの名前に）。

## 5. ポッドのアノテーション (レガシー/インスターラー)

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/actuator/prometheus"
```

好む **`ServiceMonitor`** ローリング アップデートと安定した DNS 用。

## 6. マルチネームスペース

場所 **`ServiceMonitor`** アプリサービスの横、または ** を広げます`serviceMonitorNamespaceSelector`** の **`Prometheus`** CR なので、1 つの Prometheus が名前空間全体でモニターを検出します (RBAC を使用)。
