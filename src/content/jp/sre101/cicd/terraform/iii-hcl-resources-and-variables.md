---
label: "III"
subtitle: "HCL、リソースと変数"
group: "CI/CD"
order: 3
---
HCL、リソースと変数







**HCL** (HashiCorp 構成言語) は人間が判読可能で、JSON 互換です。ほとんどの Terraform は、プロバイダー、リソース、変数、出力などの`.tf`ファイル内に存在します。

## 1. プロジェクトファイルのレイアウト

```text
infra/
  main.tf           # primary resources
  variables.tf      # input variables
  outputs.tf        # exported values
  providers.tf      # provider + terraform block
  terraform.tfvars  # variable values (often gitignored for secrets)
  versions.tf       # provider version constraints
```

## 2. terraform ブロックとブロックプロバイダー

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

| 問題 | 意味 |
|----------|----------|
|`~> 5.0`| 6.0 ではなく 5.x を許可する |
|`>= 1.6.0`| Terraform CLI の最小バージョン |

## 3. リソースブロック

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

** 参照構文:**`resource_type.logical_name.attribute`

-`aws_instance.web.id`— インスタンス ID
-`aws_subnet.public.id`— サブネット ID

## 4. 変数

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

値を与えます。

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

## 5.出力

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

出力を使用してモジュールを接続するか、値を Ansible/CI に渡します。

## 6. データソース — 管理せずに注意する

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

| |リソース |データソース |
|---|----------|---------------|
|ライフサイクルを管理する |はい |いいえ |
|作成/破壊できる |はい |いいえ |
|使用例 |新しいインフラ |既存の AMI、VPC、サブネットを検索します。

## 7. ローカルと式

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

文字列補間:`"${var.project}-web"`Terraform 0.12以降では、型が一致します`"${var.project}-web"`またはプレーン参照も許可されます。

## 8. count と for_each

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

参照:`aws_subnet.private[0].id`、`aws_instance.app["web-a"].id`。

## 9. ライフサイクルのメタ引数

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

**関連:** [AWS の例 — VPC と EC2](iv-aws-example-vpc-and-ec2.md)、[モジュールと環境](vi-modules-and-environments.md)。
