---
label: "V"
subtitle: "Kubernetes"
group: "SRE"
order: 5
---
SRE ツール — Prometheus: Kubernetes

可能であれば、巨大な **`scrape_configs`** を手作業で管理する代わりに、**Prometheus Operator** **`ServiceMonitor`** / **`PodMonitor`** を使用してください。

## 1. 前提条件

ワークロードはコンテナ ポート (例: **8080**) で **`/actuator/prometheus`** または **`/metrics`** を公開しています。 **`Prometheus`** CR は、**`serviceMonitorSelector`** / **`serviceMonitorNamespaceSelector`** を介して **`ServiceMonitor`** オブジェクトを**選択**する必要があります (**kube-prometheus-stack** などの Helm チャートでは、クラスターに一致する **`release: kube-prometheus-stack`** のようなラベルが必要になることがよくあります)。

## 2. 名前付きポートを使用したサービス

**`ServiceMonitor`** は **名前** によって **`port: http`** を参照しています:

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

Pod テンプレートでは、**`ports`** を **`name: http`** とともに宣言する必要があります (または **`port`** を名前に合わせて配置します)。

## 5. ポッドのアノテーション (レガシー/インストーラー)

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/actuator/prometheus"
```

ローリング アップデートと安定した DNS には **`ServiceMonitor`** を優先します。

## 6. マルチネームスペース

**`ServiceMonitor`** をアプリ サービスの横に配置するか、**`Prometheus`** CR の **`serviceMonitorNamespaceSelector`** を広げて、1 つの Prometheus が名前空間全体でモニターを検出できるようにします (RBAC を使用)。
