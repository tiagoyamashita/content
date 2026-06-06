---
label: "VI"
subtitle: "モジュールと環境"
group: "CI/CD"
order: 6
---
モジュールと環境

**モジュール** は、再利用可能なインフラストラクチャをパッケージ化します。 **ワークスペース** または **ディレクトリごとの環境** パターンは、コピーアンドペーストすることなく開発、ステージング、本番環境を分離します。

## 1. モジュールの基本

|用語 |意味 |
|-----|----------|
| **ルートモジュール** | `terraform`を実行するディレクトリ |
| **子モジュール** | `module "name" { ... }`経由で電話をかけました |

ローカルモジュール:

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

## 2. パブリックレジストリモジュール

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

参照: [registry.terraform.io](21)。

|ソースタイプ |例 |
|-----------|-----------|
|レジストリ | `terraform-aws-modules/vpc/aws` |
|ギット | `git::https://github.com/org/module.git?ref=v1.2.0` |
|ローカル | `./modules/vpc` |

ピン **`version`** または **`ref`** — フローティング タグにより再現性が損なわれます。

## 3. モジュールの作成

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

モジュールは **入力** (変数) と **出力** を公開し、内部リソース名を非表示にします。

## 4. 環境戦略

### A. 環境ごとのディレクトリ (推奨)

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

明確な分離。さまざまなバックエンド、変数、承認パス。

### B. Terraform ワークスペース

```bash
terraform workspace new staging
terraform workspace select prod
terraform workspace list
```

コードは同じですが、状態の名前空間は異なります。小規模なチームに適しています。大規模になると混乱する可能性があります。

### C. 単一ルート + `-var-file`

```bash
terraform apply -var-file=environments/prod.tfvars
```

ワークスペースまたは個別のバックエンド キーと組み合わせない限り、1 つの状態。

## 5. 環境ごとの tfvars

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

Git の tfvars にはシークレットを決して置かないでください。env vars、Vault、または CI シークレットを使用してください。

```bash
export TF_VAR_db_password="$(vault read -field=password secret/db)"
```

## 6. モジュール構成例

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

1 つのモジュールからの出力が別のモジュールに入力をフィードします。つまり、Terraform がグラフを構築します。

## 7. アンチパターン

|アンチパターン |修正 |
|--------------|-----|
|環境ごとに `.tf` をコピーして貼り付け |モジュール + tfvars |
|固定されていないモジュールのバージョン |ピン `version` / git `ref` |
|モノリシック 2000 行ルート |ドメインごとにモジュールを分割 (ネットワーク、コンピューティング、データ) |
|本番環境と開発環境が 1 つの状態にある |個別のバックエンド キー |

**関連:** [AWS の例 — VPC および EC2](iv-aws-example-vpc-and-ec2.md)、[CI/CD での Terraform](vii-terraform-in-cicd.md)。
