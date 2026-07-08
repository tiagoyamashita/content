---
label: "II"
subtitle: "What is Terraform"
group: "CI/CD"
order: 2
---
What is Terraform
Console clicking is slow, error-prone, and not reproducible. **Terraform** lets you describe infrastructure in code, review in PRs, and apply the same config to dev, staging, and prod.

## 1. Who makes it

| Tool | Vendor | Scope |
|------|--------|-------|
| **Terraform** | HashiCorp (IBM) | Multi-cloud, 3000+ providers |
| **CloudFormation** | AWS | AWS only (JSON/YAML) |
| **ARM / Bicep** | Microsoft | Azure |
| **Deployment Manager** | Google | GCP |
| **Pulumi / CDK** | Various | General-purpose languages |

Terraform is **not** an AWS product. Teams on AWS-only stacks sometimes still choose Terraform for modules, community, or multi-account patterns.

## 2. Core concepts

| Term | Definition |
|------|------------|
| **Provider** | Plugin that talks to an API (`aws`, `azurerm`, `google`) |
| **Resource** | Managed object (`aws_instance`, `azurerm_resource_group`) |
| **Data source** | Read existing infra without managing it |
| **Variable** | Input parameter |
| **Output** | Value exported after apply (IP, ARN) |
| **State** | Map of config → real resource IDs (`terraform.tfstate`) |
| **Module** | Reusable bundle of `.tf` files |

## 3. CLI workflow

```bash
terraform init      # Download providers & modules; configure backend
terraform validate  # Syntax check
terraform fmt       # Format HCL
terraform plan      # Preview diff (dry run)
terraform apply     # Create / update / delete to match config
terraform destroy   # Tear down all managed resources
```

```text
┌─────────┐    ┌─────────┐    ┌─────────┐
│  init   │ →  │  plan   │ →  │  apply  │
└─────────┘    └─────────┘    └─────────┘
     │              │               │
     ▼              ▼               ▼
 providers      diff vs        cloud API
 & backend       state          calls
```

## 4. How Terraform applies changes

1. Read current **state** (local or remote).
2. Refresh — query cloud for actual resource attributes.
3. Compare desired config (`.tf` files) vs state.
4. Build **execution plan**: `+` create, `~` update, `-` destroy.
5. On `apply`, call provider APIs in dependency order.

**Dependency graph** — Terraform knows `aws_subnet` depends on `aws_vpc` via `vpc_id = aws_vpc.main.id`.

## 5. Declarative vs imperative

```hcl
# Declarative — desired count
resource "aws_instance" "web" {
  count         = 3
  instance_type = "t3.micro"
  ami           = var.ami_id
}
```

You do not script "create instance 1, then 2". You declare **3 instances**; Terraform reconciles.

## 6. Terraform vs Ansible

| | Terraform | Ansible |
|---|-----------|---------|
| Primary use | **Provision** infra (VPC, DB, K8s cluster) | **Configure** servers (packages, files, services) |
| Model | Declarative state | Declarative tasks |
| Agent | None (API calls) | SSH to hosts |

Common pattern: Terraform creates EC2 + security groups; Ansible installs app on those hosts (`ansible-and-jenkins/`).

## 7. OpenTofu fork

After HashiCorp's license change (BSL), **OpenTofu** is a community fork under MPL 2.0. CLI and HCL are largely compatible — check org policy for which binary CI uses.

**Related:** [HCL, resources & variables](iii-hcl-resources-and-variables.md), [State & remote backends](v-state-and-remote-backends.md).
