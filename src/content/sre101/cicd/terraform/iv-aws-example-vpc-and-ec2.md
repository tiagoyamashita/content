---
label: "IV"
subtitle: "AWS の例 — VPC と EC2"
group: "CI/CD"
order: 4
---
AWS の例 — VPC と EC2

最小限だが現実的なスタック: **VPC**、**パブリック サブネット**、**セキュリティ グループ**、データ ソースからの AMI を備えた **EC2**。

## 1. 変数.tf

```hcl
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "environment" {
  type    = string
  default = "dev"
}

variable "vpc_cidr" {
  type    = string
  default = "10.0.0.0/16"
}
```

## 2.main.tf

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
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = { Name = "${var.environment}-igw" }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = cidrsubnet(var.vpc_cidr, 8, 1)
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = { Name = "${var.environment}-public-a" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
}

resource "aws_route_table_association" "public" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}

resource "aws_security_group" "web" {
  name        = "${var.environment}-web-sg"
  description = "HTTP and SSH"
  vpc_id      = aws_vpc.main.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "aws_instance" "app" {
  ami                    = data.aws_ami.amazon_linux.id
  instance_type          = "t3.micro"
  subnet_id              = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.web.id]

  tags = {
    Name        = "${var.environment}-app"
    Environment = var.environment
  }
}
```

## 3.出力.tf

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "app_public_ip" {
  value = aws_instance.app.public_ip
}

output "app_instance_id" {
  value = aws_instance.app.id
}
```

## 4. ローカルで実行する

```bash
cd infra
terraform init
terraform plan
terraform apply   # type yes
terraform output app_public_ip
```

計画行の例:

```text
Plan: 8 to add, 0 to change, 0 to destroy.
  + aws_vpc.main
  + aws_internet_gateway.main
  + aws_subnet.public
  ...
```

## 5. 依存関係グラフ (簡略化)

<figure class="notes-diagram"><svg xmlns="8 viewBox="0 0 360 120" role="img" aria-label="Terraform AWS dependency graph">
  <text x="12" y="18" fill="#d4d4d8" font-size="11" font-weight="600">Resources apply in dependency order</text>
  <rect x="140" y="28" width="80" height="24" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="168" y="44" fill="#e4e4e7" font-size="8">aws_vpc</text>
  <rect x="60" y="68" width="80" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="78" y="84" fill="#e4e4e7" font-size="8">subnet</text>
  <rect x="220" y="68" width="80" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="232" y="84" fill="#e4e4e7" font-size="8">igw / sg</text>
  <rect x="140" y="92" width="80" height="24" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="158" y="108" fill="#e4e4e7" font-size="8">aws_instance</text>
  <path d="M180 52 V68 M100 68 H180 M260 68 H180 M180 68 V92" stroke="#71717a" stroke-width="1"/>
</svg></figure>

## 6. セキュリティに関する注意事項

|トピック |推薦 |
|------|----------------|
| SSH `0.0.0.0/0` |本番環境の要塞または VPN CIDR に制限する |
| IMDSv2 | EC2 に `metadata_options { http_tokens = "required" }` を設定する |
|国家機密 |リモートバックエンド。決してコミットしない状態 |
| IAM |最小権限を持つ CI ロール — 管理者ではない |

## 7. 解体する

```bash
terraform destroy
```

このルート モジュールの状態にあるすべてのリソースを破棄します。環境ごとに個別の状態を使用して、dev を破棄しても prod [状態とリモート バックエンド](v-state-and-remote-backends.md) に影響を与えないようにします。

**関連:** [HCL、リソースと変数](iii-hcl-resources-and-variables.md)、[モジュールと環境](vi-modules-and-environments.md)。
