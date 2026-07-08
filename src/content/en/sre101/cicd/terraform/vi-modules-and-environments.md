---
label: "VI"
subtitle: "Modules & environments"
group: "CI/CD"
order: 6
---
Modules & environments
**Modules** package reusable infrastructure. **Workspaces** or **directory-per-env** patterns separate dev, staging, and prod without copy-paste.

## 1. Module basics

| Term | Meaning |
|------|---------|
| **Root module** | Directory where you run `terraform` |
| **Child module** | Called via `module "name" { ... }` |

Local module:

```text
modules/
  vpc/
    main.tf
    variables.tf
    outputs.tf
env/
  staging/
    main.tf      # calls modules/vpc
  production/
    main.tf
```

```hcl
# env/staging/main.tf
module "vpc" {
  source = "../../modules/vpc"

  name       = "myapp-staging"
  cidr_block = "10.1.0.0/16"
  azs        = ["us-east-1a", "us-east-1b"]
}

output "vpc_id" {
  value = module.vpc.vpc_id
}
```

## 2. Public registry module

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.13.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["us-east-1a", "us-east-1b"]

  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = var.environment != "prod"
}
```

Browse: [registry.terraform.io](https://registry.terraform.io).

| Source type | Example |
|-------------|---------|
| Registry | `terraform-aws-modules/vpc/aws` |
| Git | `git::https://github.com/org/module.git?ref=v1.2.0` |
| Local | `./modules/vpc` |

Pin **`version`** or **`ref`** — floating tags break reproducibility.

## 3. Writing a module

```hcl
# modules/vpc/variables.tf
variable "name" { type = string }
variable "cidr_block" { type = string }

# modules/vpc/main.tf
resource "aws_vpc" "this" {
  cidr_block = var.cidr_block
  tags       = { Name = var.name }
}

# modules/vpc/outputs.tf
output "vpc_id" {
  value = aws_vpc.this.id
}
```

Modules expose **inputs** (variables) and **outputs** — hide internal resource names.

## 4. Environment strategies

### A. Directory per environment (recommended)

```text
infra/
  modules/
  environments/
    dev/
      main.tf
      backend.tf      # key = myapp/dev/...
      terraform.tfvars
    prod/
      main.tf
      backend.tf
      terraform.tfvars
```

Clear separation; different backends, vars, and approval paths.

### B. Terraform workspaces

```bash
terraform workspace new staging
terraform workspace select prod
terraform workspace list
```

Same code, different state namespaces. Works for small teams; can get confusing at scale.

### C. Single root + `-var-file`

```bash
terraform apply -var-file=environments/prod.tfvars
```

One state unless combined with workspace or separate backend keys.

## 5. tfvars per environment

```hcl
# environments/prod.tfvars
environment   = "prod"
instance_type = "t3.medium"
vpc_cidr      = "10.0.0.0/16"

# environments/dev.tfvars
environment   = "dev"
instance_type = "t3.micro"
vpc_cidr      = "10.10.0.0/16"
```

Never put secrets in tfvars in Git — use env vars, Vault, or CI secrets:

```bash
export TF_VAR_db_password="$(vault read -field=password secret/db)"
```

## 6. Module composition example

```hcl
module "vpc" {
  source = "./modules/vpc"
  # ...
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 20.0"

  cluster_name    = "${var.environment}-cluster"
  vpc_id          = module.vpc.vpc_id
  subnet_ids      = module.vpc.private_subnets
  cluster_version = "1.29"
}
```

Outputs from one module feed inputs to another — Terraform builds the graph.

## 7. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| Copy-paste `.tf` per env | Module + tfvars |
| Unpinned module version | Pin `version` / git `ref` |
| Monolithic 2000-line root | Split modules by domain (network, compute, data) |
| Prod and dev in one state | Separate backend keys |

**Related:** [AWS example — VPC & EC2](iv-aws-example-vpc-and-ec2.md), [Terraform in CI/CD](vii-terraform-in-cicd.md).
