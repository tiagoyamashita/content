---
label: "III"
subtitle: "HCL, resources & variables"
group: "CI/CD"
order: 3
---
HCL, resources & variables
**HCL** (HashiCorp Configuration Language) is human-readable and JSON-compatible. Most Terraform lives in `.tf` files: providers, resources, variables, outputs.

## 1. Project file layout

```text
infra/
  main.tf           # primary resources
  variables.tf      # input variables
  outputs.tf        # exported values
  providers.tf      # provider + terraform block
  terraform.tfvars  # variable values (often gitignored for secrets)
  versions.tf       # provider version constraints
```

## 2. terraform and provider blocks

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "myapp"
      ManagedBy   = "terraform"
      Environment = var.environment
    }
  }
}
```

| Constraint | Meaning |
|------------|---------|
| `~> 5.0` | Allow 5.x, not 6.0 |
| `>= 1.6.0` | Minimum Terraform CLI version |

## 3. Resource block

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id

  tags = {
    Name        = "${var.project}-web"
    Environment = var.environment
  }
}
```

**Reference syntax:** `resource_type.logical_name.attribute`

- `aws_instance.web.id` — instance ID
- `aws_subnet.public.id` — subnet ID

## 4. Variables

```hcl
# variables.tf
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "environment must be dev, staging, or prod."
  }
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}

variable "allowed_cidrs" {
  type    = list(string)
  default = ["10.0.0.0/8"]
}
```

Assign values:

```hcl
# terraform.tfvars
environment   = "staging"
instance_type = "t3.small"
aws_region    = "us-east-1"
```

```bash
terraform plan -var="environment=prod"
terraform plan -var-file="prod.tfvars"
```

## 5. Outputs

```hcl
output "web_public_ip" {
  description = "Public IP of web server"
  value       = aws_instance.web.public_ip
}

output "web_instance_id" {
  value = aws_instance.web.id
}
```

```bash
terraform output web_public_ip
terraform output -json
```

Use outputs to wire modules together or pass values to Ansible/CI.

## 6. Data sources — read without managing

```hcl
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "web" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
}
```

| | Resource | Data source |
|---|----------|-------------|
| Manages lifecycle | Yes | No |
| Can create/destroy | Yes | No |
| Use case | New infra | Look up existing AMI, VPC, subnet |

## 7. Locals and expressions

```hcl
locals {
  name_prefix = "${var.project}-${var.environment}"
  common_tags = {
    Project     = var.project
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "${local.name_prefix}-logs"
  tags   = local.common_tags
}
```

String interpolation: `"${var.project}-web"`. Terraform 0.12+ also allows `"${var.project}-web"` or plain references where types match.

## 8. count and for_each

```hcl
# count — index-based
resource "aws_subnet" "private" {
  count             = length(var.availability_zones)
  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = var.availability_zones[count.index]
}

# for_each — map/set-based (preferred for named instances)
resource "aws_instance" "app" {
  for_each      = var.app_instances
  ami           = var.ami_id
  instance_type = each.value.instance_type
  subnet_id     = each.value.subnet_id
  tags = { Name = each.key }
}
```

Reference: `aws_subnet.private[0].id`, `aws_instance.app["web-a"].id`.

## 9. lifecycle meta-argument

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = "t3.micro"

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [tags["LastModified"]]
  }
}
```

**Related:** `iv-aws-example-vpc-and-ec2.md`, `vi-modules-and-environments.md`.
