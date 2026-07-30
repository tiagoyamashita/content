---
label: "V"
subtitle: "Kubernetes"
group: "SRE"
order: 5
---
SRE tooling — Prometheus: Kubernetes
Use **Prometheus Operator** **`ServiceMonitor`** / **`PodMonitor`** instead of hand-maintaining huge **`scrape_configs`** when possible.

## 1. Prerequisites

Your workload exposes **`/actuator/prometheus`** or **`/metrics`** on a container port (example **8080**). The **`Prometheus`** CR must **select** **`ServiceMonitor`** objects via **`serviceMonitorSelector`** / **`serviceMonitorNamespaceSelector`** (Helm charts such as **kube-prometheus-stack** often require labels like **`release: kube-prometheus-stack`**—match your cluster).

## 2. Service with a named port

**`ServiceMonitor`** references **`port: http`** by **name**:

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

## 3. ServiceMonitor

Scrape all Pods selected by the Service:

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

## 4. PodMonitor

Use when you scrape Pods directly (no stable Service, or single-container focus):

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

The Pod template must declare **`ports`** with **`name: http`** (or align **`port`** to your name).

## 5. Pod annotations (legacy / installers)

```yaml
metadata:
  annotations:
    prometheus.io/scrape: "true"
    prometheus.io/port: "8080"
    prometheus.io/path: "/actuator/prometheus"
```

Prefer **`ServiceMonitor`** for rolling updates and stable DNS.

## 6. Multi-namespace

Place **`ServiceMonitor`** beside the app Service, or widen **`serviceMonitorNamespaceSelector`** on the **`Prometheus`** CR so one Prometheus discovers monitors across namespaces (with RBAC).
