---
label: "I"
subtitle: "Intro & architecture"
group: "SRE"
order: 1
---
SRE tooling — Terraform: Intro & architecture
Describe infrastructure declaratively; Terraform computes dependency graphs and reconciles cloud APIs via providers.

## 1. Role

**Terraform** (HashiCorp; ecosystem peers include **OpenTofu**) keeps **state** that maps logical addresses (`aws_instance.app`) to real IDs (`i-0abc…`). **`terraform plan`** diffs desired configuration vs state + remote APIs; **`apply`** executes creates/updates/deletes through **providers**.

## 2. How a run works (mental model)

1. Parse `.tf` → build DAG of resources + data sources.
2. Refresh **state** / provider reads unless constrained (**`-refresh=false`**).
3. Diff desired vs actual → execution plan.
4. Mutate APIs in dependency-safe order; update **state**.

Providers encapsulate vendor quirks—AWS/GCP/Azure/**Kubernetes**/Datadog/Grafana/etc.—via plugins pinned by **`required_providers`** blocks.

## 3. Core vocabulary

| Idea | Meaning |
|------|---------|
| **Resource** | Creates/manages something (`resource "aws_s3_bucket" "logs"`). |
| **Data source** | Read-only lookup (`data.aws_vpc.default`). |
| **Provider** | Plugin configuring endpoints/credentials (`provider "aws" {}`). |
| **Module** | Callable package of resources (`module "vpc" { … }`). |
| **State** | Bindings + outputs persisted locally or remotely—must stay consistent. |

## 4. Configuration snippets (`providers`)

Pin Terraform & providers:

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "aws" {
  region = var.region
}
```

Continue with **CLI workflow**, **Modules / backends / state**, then **CI & practices**.
