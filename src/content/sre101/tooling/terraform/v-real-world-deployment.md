---
label: "V"
subtitle: "Real world deployment"
group: "SRE"
order: 5
---
SRE tooling — Terraform: Real world deployment
A pattern teams actually ship: **remote state**, **environment splits**, **VPC + Kubernetes**, and **additive modules**—trimmed for clarity.

## 1. Scenario

You run **staging** and **prod** in one AWS account (or separate accounts—same layout, different **`backend`** keys / **`providers`** aliases). Infra includes:

- Shared-style **VPC** (private + public subnets, NAT for egress).
- **EKS** cluster for workloads.
- Optional **addons** (Ingress controller, metrics-server) via Helm or GitOps—often **not** all in one Terraform root to limit blast radius; below focuses on **network + control plane**.

## 2. Repository layout

```text
terraform/
  modules/
    labels/           # standard tags (env, owner, cost_center)
  env/
    staging/
      backend.tf
      providers.tf
      main.tf
      variables.tf
      outputs.tf
      staging.tfvars
    prod/
      backend.tf
      providers.tf
      main.tf
      variables.tf
      outputs.tf
      prod.tfvars       # never commit secrets — inject via CI
```

Each **`env/<name>`** is its **own Terraform root** → separate **`terraform.tfstate`** (different **`key`** in S3).

## 3. Backend & providers (`env/prod/backend.tf`)

```hcl
terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    bucket         = "tf-state-myorg"
    key            = "prod/eks-base/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.region

  default_tags {
    tags = {
      Environment = "prod"
      ManagedBy   = "terraform"
      Repository  = "platform/eks-base"
    }
  }
}
```

## 4. VPC module (`env/prod/main.tf` excerpt)

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = var.azs
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs

  enable_nat_gateway   = true
  single_nat_gateway   = false      # prod: one NAT per AZ for HA
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb"           = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "owned"
  }
}
```

## 5. EKS module (`env/prod/main.tf` excerpt)

```hcl
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    general = {
      instance_types = ["m6i.large"]
      min_size       = 3
      max_size       = 12
      desired_size   = 3
    }
  }

  enable_irsa = true

  tags = {
    Environment = "prod"
  }
}

output "cluster_endpoint" {
  value     = module.eks.cluster_endpoint
  sensitive = true
}

output "configure_kubectl" {
  value = "aws eks update-kubeconfig --region ${var.region} --name ${var.cluster_name}"
}
```

Pin **`version`** on every module; read module upgrade guides before bumping major versions.

## 6. Variables sketch (`env/prod/variables.tf`)

```hcl
variable "region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type = string
}

variable "vpc_cidr" {
  type = string
}

variable "azs" {
  type = list(string)
}

variable "private_subnet_cidrs" {
  type = list(string)
}

variable "public_subnet_cidrs" {
  type = list(string)
}

variable "kubernetes_version" {
  type = string
}
```

**`prod.tfvars`** holds concrete CIDRs/AZs/cluster name—no passwords here.

## 7. What happens in CI

1. **`terraform fmt -check`** / **`validate`** on PR.
2. **`terraform plan`** with **`AWS_ROLE_ARN`** via OIDC (no long-lived keys).
3. Human approval → **`terraform apply`** on merge or promoted workflow.

Staging stack duplicates **`env/staging`** with smaller node pools and **`single_nat_gateway = true`** to save cost.

## 8. Day-two split (common real-world choice)

- **Terraform** owns **VPC**, **EKS**, **IAM**, **RDS** skeletons, **Route53** zones.
- **Helm / Argo CD / Flux** deploy **microservices** that change daily—avoids 40-minute Terraform plans for app tweaks.

Keep observability (**Prometheus Operator**, **Ingress**) in GitOps or a dedicated Terraform stack that references **`cluster_endpoint`** via **`remote_state`** or manual outputs.

## 9. Pitfalls this layout avoids

- Single giant **`tfstate`** for 200 apps → locking pain; split by **blast radius** (network vs cluster vs apps).
- **`apply`** from laptops without locks → use remote backend **always**.
- Upgrading EKS without reading release notes → pin **`cluster_version`**, test in **staging** first.

Adjust providers/regions to your cloud—the **shape** (env dirs, remote state, VPC → cluster → GitOps) transfers to **GCP/GKE** and **Azure/AKS** with different modules.
