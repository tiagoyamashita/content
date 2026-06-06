---
label: "IV"
subtitle: "CI & practices"
group: "SRE"
order: 4
---
SRE tooling — Terraform: CI & practices
Automate **`plan`** review, reduce drift, and document operational assumptions baked into modules.

## 1. CI gates

Typical pipeline stages:

1. **`terraform fmt -check`** — blocks noisy diffs.
2. **`terraform validate`** — catches syntax/provider misconfig early.
3. **`terraform plan`** — upload textual plan to PR; require reviewer acknowledgement before **`apply`** on protected branches.
4. Optional **`tfsec` / `checkov` / `tflint`** — policy-as-code for insecure defaults.

For GitOps-heavy flows (**Atlantis**, Terraform Cloud run tasks), map approvals to team RBAC.

## 2. Apply discipline

- **`apply`** from CI with OIDC/IAM roles—not long-lived static keys on laptops where avoidable.
- Separate workspaces/backends per environment—never **`apply`** prod stacks accidentally using staging vars.

## 3. Runbooks & modules

When defaults encode capacity assumptions (**instance sizes**, **regions**, **retention**), mirror operational context:

- Module **`README`** — SLIs touched by defaults (e.g. NAT concurrency).
- Linked wiki/runbook URLs inside observability resources provisioned alongside infra.

## 4. Drift & imports

- Schedule **`terraform plan`** against prod weekly—even without merges—to detect manual console edits early.
- **`import`** discovered orphans deliberately instead of letting unmanaged infra linger.

## 5. Pairing with Kubernetes & observability

Provision **EKS/GKE/AKS**, node pools, IAM roles (**IRSA** / workload identity), load balancers, DNS—then layer Helm/`kubernetes_manifest` resources or GitOps controllers.

Managed Prometheus/Grafana stacks often expose Terraform providers—keep **cluster**, **network**, **dashboards**, and **Alertmanager** routes evolving together in one reviewed pipeline when feasible.

## 6. Where Terraform stops

Day-two workload rollout semantics remain Kubernetes controllers—Terraform provisions clusters/add-ons; **kubectl/Helm/GitOps** handle frequent microservice churn unless you intentionally unify via **`kubernetes_*`** resources (trade-offs on blast radius & plan runtime).

See **Real world deployment** for a concrete repo layout and VPC + EKS module sketch.
