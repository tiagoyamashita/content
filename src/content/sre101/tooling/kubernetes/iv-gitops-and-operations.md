---
label: "IV"
subtitle: "GitOps & operations"
group: "SRE"
order: 4
---
SRE tooling — Kubernetes: GitOps & operations
Day-two habits: safe rollouts, drills, and pipelines that treat manifests like production code.

## 1. GitOps mindset

- Manifests live in Git (**Flux**, **Argo CD**, **Terraform Kubernetes provider**, etc.)—peer review + CI validation precedes cluster reconcile.
- Avoid silent **`kubectl apply`** hotfixes without backporting YAML—drift becomes undebuggable during incidents.

## 2. Safe rollouts & escalations

```text
kubectl apply -k overlays/prod
kubectl rollout undo deployment/checkout-api -n prod        # rollback RS
kubectl cordon node/ip-10-0-3-42                             # stop new placements
kubectl drain node/ip-10-0-3-42 --ignore-daemonsets --delete-emptydir-data
```

Coordinate drains with **PodDisruptionBudgets** and cloud maintenance windows.

## 3. RBAC hygiene

- Separate **`cluster-admin`** break-glass from everyday **`Role`**/`RoleBinding` scoped to namespaces.
- Prefer **OIDC** integration over long-lived static **`kubeconfig`** tokens where possible.

## 4. Failure drills

Run controlled exercises when blast radius is understood:

- Node cordon/drain + workload reschedule.
- kube-apiserver/etcd follower loss (with infra team).
- AZ/network partition simulations for regional clusters.

Document findings in runbooks—tie alerts/SLO burn dashboards from **Prometheus/Grafana**.

## 5. Observability hooks

- **DaemonSets** ship node-level metrics/logs (Promtail/Fluent Bit, node-exporter).
- **Admission webhooks** enforce labels, resource defaults, image signatures—surface webhook latency via metrics.

## 6. Pairing

Prometheus scrapes Pod endpoints; Grafana dashboards pivot on **`namespace`**, **`deployment`**, **`pod`**, **`node`** labels—align label conventions across metrics and Kubernetes labels (`prometheus.io/*` annotations vs **`ServiceMonitor`**).
