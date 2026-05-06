---
label: "V"
subtitle: "Terraform"
group: "CI/CD"
order: 5
---
CI/CD — Part V: Terraform
Infrastructure as Code by HashiCorp — cloud-agnostic.

## 1. What is Terraform
Terraform: open-source IaC tool created by HashiCorp (acquired by IBM 2024).
- NOT an AWS product — it is cloud-agnostic.
- Works with AWS, Azure, GCP, Kubernetes, GitHub, Datadog, and 3000+ providers.
- AWS's own native IaC tool is CloudFormation (JSON/YAML, AWS-only).

What problem does it solve?
- Clicking through cloud consoles is slow, error-prone, and not reproducible.
- Terraform lets you describe infrastructure in code, version it in Git,
and apply it consistently across environments.

Key properties:
- Declarative — describe desired state; Terraform figures out the steps.
- Idempotent — applying the same config twice makes no extra changes.
- Plan before apply — shows a diff of what will change before touching anything.

## 2. Core concepts
- Provider: plugin that talks to a cloud API (aws, azurerm, google, …).
- Resource: a single infrastructure object (EC2 instance, S3 bucket, …).
- Data source: read existing infrastructure without managing it.
- Variable: parameterise configurations (like function arguments).
- Output: expose values after apply (IP addresses, ARNs, …).
- State: Terraform's record of what it has created (terraform.tfstate).
- Module: reusable package of Terraform resources.

Workflow:

```
terraform init     # download providers & modules
terraform plan     # preview changes (dry run)
terraform apply    # create / update resources
terraform destroy  # tear everything down
```


## 3. HCL basics
HCL (HashiCorp Configuration Language) — human-friendly, JSON-compatible.

Resource block:

```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name        = "web-server"
    Environment = var.environment
  }
}
```


Variable declaration:

```hcl
variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}
```


Output:

```hcl
output "instance_ip" {
  value = aws_instance.web.public_ip
}
```


## 4. AWS example — VPC + EC2
main.tf:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
  tags = { Name = "main-vpc" }
}

resource "aws_subnet" "public" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"
}

resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}
```

Reference syntax: resource_type.resource_name.attribute
- aws_vpc.main.id — the VPC ID output by the aws_vpc resource.

## 5. State & backends
terraform.tfstate: JSON file mapping config → real cloud resource IDs.
- NEVER commit this file to Git — it contains secrets and resource IDs.
- In a team, everyone must share the same state → use a remote backend.

S3 remote backend (common for AWS teams):

```hcl
terraform {
  backend "s3" {
    bucket         = "my-tf-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tf-state-lock"  # prevents concurrent applies
  }
}
```

Other backends: Terraform Cloud, Azure Blob, GCS.
- State locking prevents two engineers applying at the same time.
- terraform state list / show / rm — inspect and surgically modify state.

## 6. Modules
Module: a directory of .tf files consumed as a unit.
- Root module: the working directory you run terraform from.
- Child module: called with a module block.

Calling a module:

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.0"

  name = "my-vpc"
  cidr = "10.0.0.0/16"
  azs  = ["us-east-1a", "us-east-1b"]
}
```

- Public registry: registry.terraform.io — thousands of community modules.
- Private modules: Git URLs, local paths, or Terraform Cloud private registry.
- Modules promote DRY — define once, reuse across dev/staging/prod.

## 7. Terraform in CI/CD
Pattern: PR → plan → review → merge → apply.

GitHub Actions example:

```yaml
name: Terraform
on:
  push:
    branches: [main]
  pull_request:

jobs:
  terraform:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write   # OIDC for AWS
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3

      - name: Terraform Init
        run: terraform init

      - name: Terraform Plan
        run: terraform plan -out=tfplan

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply tfplan
```

- Use OIDC instead of long-lived AWS access keys (see Part III).
- Post the plan output as a PR comment so reviewers can see the diff.
- Never run apply on PRs — only on merge to main.
- Atlantis: dedicated bot that runs plan/apply triggered by PR comments.

## 8. Remember & rehearse
- Who makes Terraform? Is it AWS-specific?
- What is the difference between Terraform and CloudFormation?
- What does terraform plan do and why is it important?
- Why should terraform.tfstate never be committed to Git?
- What is a remote backend and why does a team need one?
- Explain the module block — what does source point to?
