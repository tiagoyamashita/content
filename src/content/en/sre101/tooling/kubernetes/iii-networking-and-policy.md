---
label: "III"
subtitle: "Networking & policy"
group: "SRE"
order: 3
---
SRE tooling — Kubernetes: Networking & policy
Clusters default **allow-all** Pod-to-Pod traffic until you tighten **NetworkPolicy**.

## 1. Services & DNS

- **ClusterIP** — virtual IP inside cluster; **`kube-proxy`** (iptables/IPVS) or eBPF datapaths route traffic to healthy endpoints (Pods passing readiness).
- **NodePort** — publishes port on every Node—handy for labs; prod usually fronts with LB/Ingress.
- **LoadBalancer** — cloud integration allocates external LB (implementation varies by provider).
- **Headless (`clusterIP: None`)** — DNS **`A`** records per Pod—common with StatefulSets.

Cluster DNS (**CoreDNS**) resolves **`my-svc.my-ns.svc.cluster.local`**.

## 2. Ingress vs Gateway API

- **Ingress** — HTTP routing via controller (nginx, contour, etc.); **`IngressClass`** selects implementation.
- **Gateway API** — richer routing/TLS models with **`Gateway`** / **`HTTPRoute`** CRDs—preferred greenfield when supported.

TLS termination may live at Ingress/LB or mesh—pick one story per environment.

## 3. NetworkPolicy

Without policies, any Pod can reach any Pod/CIDR allowed by CNI defaults. Example deny-by-default baseline (illustrative—adapt labels/CIDRs):

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

## 4. Multitenancy knobs

Combine **namespaces**, **ResourceQuota** / **LimitRange**, **RBAC**, **NetworkPolicy**, and optionally **PodSecurity** / admission (OPA/Kyverno) for safer shared clusters.

## 5. Pairing with observability

Service meshes / CNIs emit metrics—Prometheus targets often scrape **`kube-state-metrics`**, **cAdvisor/node-exporter**, and app **`ServiceMonitor`** objects (see **Prometheus → Kubernetes** in Tooling).
