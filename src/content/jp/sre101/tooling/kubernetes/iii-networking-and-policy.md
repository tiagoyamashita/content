---
label: "III"
subtitle: "ネットワーキングとポリシー"
group: "SRE"
order: 3
---
SRE ツール — Kubernetes: ネットワーキングとポリシー

**NetworkPolicy** を強化するまで、クラスターはデフォルトで **allow-all** ポッド間のトラフィックを許可します。

## 1. サービスと DNS

- **ClusterIP** — virtual IP inside cluster; **`kube-proxy`** (iptables/IPVS) or eBPF datapaths route traffic to healthy endpoints (Pods passing readiness).
- **NodePort** — publishes port on every Node—handy for labs; prod usually fronts with LB/Ingress.
- **LoadBalancer** — cloud integration allocates external LB (implementation varies by provider).
- **Headless (`clusterIP: None`)** — DNS **`A`** records per Pod—common with StatefulSets.

Cluster DNS (**CoreDNS**) resolves **`my-svc.my-ns.svc.cluster.local`**.

## 2. Ingress とゲートウェイ API

- **Ingress** — HTTP routing via controller (nginx, contour, etc.); **`IngressClass`** selects implementation.
- **Gateway API** — richer routing/TLS models with **`Gateway`** / **`HTTPRoute`** CRDs—preferred greenfield when supported.

TLS 終端は Ingress/LB またはメッシュに存在する可能性があります。環境ごとに 1 つのストーリーを選択してください。

## 3. ネットワークポリシー

ポリシーがなければ、どの Pod も CNI デフォルトで許可されている任意の Pod/CIDR に到達できます。デフォルト拒否ベースラインの例 (例示 - ラベル/CIDR の適応):

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: payments
spec:
  podSelector: {}
  policyTypes:
    - Ingress
    - Egress
```

Then add **allow** policies per app (`podSelector` + `namespaceSelector` + **`ports`**). Verify with **`kubectl exec`** + **`nc`** / **`curl`** from representative Pods.

## 4. マルチテナンシーノブ

**名前空間**、**ResourceQuota** / **LimitRange**、**RBAC**、**NetworkPolicy**、およびオプションで **PodSecurity** / アドミッション (OPA/Kyverno) を組み合わせて、より安全な共有クラスターを実現します。

## 5. 可観測性とのペアリング

Service meshes / CNIs emit metrics—Prometheus targets often scrape **`kube-state-metrics`**, **cAdvisor/node-exporter**, and app **`ServiceMonitor`** objects (see **Prometheus → Kubernetes** in Tooling).
