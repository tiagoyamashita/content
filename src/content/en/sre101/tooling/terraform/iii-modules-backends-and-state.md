---
label: "III"
subtitle: "Modules backends & state"
group: "SRE"
order: 3
---
SRE tooling — Terraform: Modules, backends & state
Modules reuse patterns; remote **state** needs locking and backup discipline.

## 1. Modules

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.5"

  name = "prod-vpc"
  cidr = "10.0.0.0/16"

  azs             = var.azs
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
}
```

- Pin **`version`** for registry modules or Git refs (`?ref=v1.2.3`).
- Publish internal modules via **Git/Terraform Registry** with semver tags—document inputs/outputs (`README`, tests).

## 2. Remote backends & locking

Example **AWS S3 + DynamoDB locking**:

```hcl
terraform {
  backend "s3" {
    bucket         = "tf-state-myorg"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Terraform Cloud / Enterprise** adds RBAC, speculative plans, policy sets (**Sentinel** / **OPA** integration varies)—often replaces bespoke S3+Dynamo setups.

## 3. Remote state consumers

```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "tf-state-myorg"
    key    = "prod/network/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_db_subnet_group" "app" {
  subnet_ids = data.terraform_remote_state.network.outputs.private_subnets
}
```

Explicit contracts (**outputs**) beat implicit coupling across stacks.

## 4. State hygiene

- Treat corruption / contention as **severity-1**—maintain **versioned backups** (S3 versioning, Terraform Cloud state history).
- Restrict IAM who may **`terraform state`** operations (`mv`, `rm`).
- Never edit **`terraform.tfstate`** manually unless disaster recovery runbooks demand it.

## 5. Observability resources as code

Use vendor providers (**Grafana**, **Datadog**) alongside **`kubernetes_manifest`** / **Helm** resources so dashboards/alerts travel with cluster revisions—pair with **Prometheus**/**Alertmanager** folders in Git.
