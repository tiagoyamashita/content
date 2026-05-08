---
label: "I"
subtitle: "Intro & architecture"
group: "SRE"
order: 1
---
SRE tooling — Kubernetes: Intro & architecture
Run containers at scale with a declarative API you automate against.

## 1. Role

**Kubernetes** schedules Pods onto Nodes, reconciles desired state (**Deployments**, **StatefulSets**, etc.), exposes stable networking (**Services**, **Ingress** / Gateway API), and layers ops primitives (**Resource quotas**, **NetworkPolicies**, **PodDisruptionBudgets**) teams rely on for safer upgrades.

## 2. Control plane vs workloads

| Piece | Responsibility |
|-------|----------------|
| **kube-apiserver** | Validates REST requests; single coordination façade for the cluster. |
| **etcd** | Stores desired cluster state (watch semantics drive controllers). |
| **kube-scheduler** | Assigns unscheduled Pods to suitable Nodes. |
| **kube-controller-manager** | ReplicaSets, Deployments, Jobs, endpoints… reconcile loops. |
| **cloud-controller-manager** | Bridges vendor LB/route integrations where enabled. |
| **kubelet** | Runs on each Node—starts Pods via container runtime, reports status. |

Worker Nodes execute Pods; the control plane failure modes tend to be **cluster-wide**—protect apiserver/etcd HA topologies accordingly.

## 3. Namespaces & isolation baseline

- **`namespaces`** segment RBAC, quotas, DNS zones (**`<svc>.<ns>.svc.cluster.local`**), and operator-managed stacks (**kube-system**, **`monitoring`**, etc.).
- Strong isolation usually adds **NetworkPolicy**, quota enforcement, and admission policy—not namespaces alone.

## 4. Declarative workflow

You mostly **`kubectl apply -f`** YAML (or Helm/Kustomize manifests). Controllers converge reality toward spec; drift can still happen via broken controllers or manual **`kubectl edit`**—**GitOps** (see **GitOps & operations**) adds audit trail + rollback semantics.

Continue with **Workloads & health**, **Networking & policy**, and **GitOps & operations** in this folder.
