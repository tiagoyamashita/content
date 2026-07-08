---
label: "II"
subtitle: "Workloads & health"
group: "SRE"
order: 2
---
SRE tooling — Kubernetes: Workloads & health
Pods, controllers, probes, capacity, and disruption budgets.

## 1. Pod & controller patterns

| Kind | When |
|------|------|
| **Deployment** | Stateless HTTP workers—ReplicaSet underneath manages rollouts. |
| **StatefulSet** | Stable identity + ordered rollout (databases you operate in-cluster). |
| **DaemonSet** | One Pod per Node—agents, log forwarders, node exporters. |
| **Job / CronJob** | Batch / scheduled tasks with retry semantics. |

## 2. Probes

- **livenessProbe** — kubelet restarts container if unhealthy (avoid expensive checks that flap).
- **readinessProbe** — removes Pod from **Service** endpoints until ready (traffic shaping during startup).
- **startupProbe** — protects slow-start apps so liveness does not kill them prematurely.

Probe **`failureThreshold`** × **`periodSeconds`** drives blast radius—tune with observed startup curves.

## 3. Resources & scheduling

- **`requests`** influence scheduling (kube-scheduler fits Pods onto Nodes with allocatable capacity).
- **`limits`** cap burst usage (CPU throttling vs hard memory **OOMKill** behavior differs—memory limits are not “soft”).
- **QoS classes** (`Guaranteed`, `Burstable`, `BestEffort`) affect eviction ordering under pressure—document assumptions for stateful tiers.

## 4. Horizontal scaling & PDB

- **HorizontalPodAutoscaler** scales Replica counts off metrics (often Prometheus Adapter `custom.metrics.k8s.io`).
- **PodDisruptionBudget** caps simultaneous voluntary disruptions (`maxUnavailable` / `minAvailable`) during node drains or deployments—pair PDBs with sensible **`Deployment.strategy`** (`RollingUpdate` **`maxSurge`/`maxUnavailable`**).

## 5. Quick kubectl cues

```text
kubectl rollout status deployment/checkout-api -n prod
kubectl rollout restart deployment/checkout-api -n prod
kubectl describe pod -n prod <pod-name>
kubectl logs -n prod deploy/checkout-api --tail=200 -f
```

Next: **Networking & policy**, then **GitOps & operations**. For **Dockerfiles**, images, and signals before you tune probes, see **Dockerizing apps**.
