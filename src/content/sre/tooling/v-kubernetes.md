---
label: "V"
subtitle: "Kubernetes"
group: "SRE"
order: 5
---
SRE tooling — Kubernetes
Orchestration platform most SRE tooling targets first.

## 1. Role

**Kubernetes** schedules workloads, exposes declarative APIs (**Deployments**, **StatefulSets**, **Services**, **Ingress**), and provides primitives (**HPAs**, **pdb**, **NetworkPolicies**) operations teams rely on.

## 2. Core concepts for SRE

- **Control plane** — API server, etcd, scheduler, controllers; failures here are cluster-wide.
- **Workload health** — readiness vs liveness probes; restart policies; surge vs unavailable during rollouts.
- **Observability hooks** — **PodMonitor** / **ServiceMonitor** (Prometheus Operator), **DaemonSets** for agents, **Admission webhooks** for policy.
- **Resource limits** — CPU/memory requests and limits prevent noisy neighbors and drive scheduling.

## 3. SRE practices

- Treat cluster config (**GitOps**) as code; peer-review manifest changes.
- Define **SLOs** at the service edge (Ingress/gateway) and inside the mesh or stack as needed.
- Practice **failure drills** (node drain, AZ loss simulation) where blast radius is understood.

## 4. Pairing

Prometheus scrapes pod endpoints; Grafana dashboards often pivot on **`namespace`**, **`deployment`**, **`pod`** labels.
