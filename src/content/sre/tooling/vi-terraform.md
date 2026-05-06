---
label: "VI"
subtitle: "Terraform"
group: "SRE"
order: 6
---
SRE tooling — Terraform
Declarative infrastructure as code for clouds and SaaS APIs.

## 1. Role

**Terraform** maintains **state** mapping desired resources to real IDs, plans **diffs**, and applies changes via provider plugins (AWS, GCP, Azure, Kubernetes, Grafana, etc.).

## 2. Core concepts

- **Modules** — reusable packages (VPC, EKS cluster, observability stack); pin versions.
- **Workspaces / stacks** — isolate prod vs non-prod state; avoid manual console edits that drift state.
- **Plan in CI** — required reviews on **`terraform plan`** output before **`apply`** on protected branches.

## 3. SRE practices

- Encode **runbooks** next to modules when defaults encode operational assumptions (regions, capacity).
- Manage **observability resources** (datasources, folders, alert rules) as code alongside clusters.
- Backup or remote-lock **state**; treat state corruption as a severity-1 operational risk.

## 4. Pairing

Provision **Kubernetes**, load balancers, and managed Prometheus/Grafana where vendors expose Terraform providers—one pipeline from cluster to dashboards.
