---
label: "V"
subtitle: "現実世界への展開"
group: "SRE"
order: 5
---
SRE ツール — Terraform: 実際の展開

チームが実際に出荷するパターン: **リモート状態**、**環境分割**、**VPC + Kubernetes**、**追加モジュール** - 明確にするためにトリミングされています。

## 1. シナリオ

**ステージング**と**本番**を 1 つの AWS アカウント (または別のアカウント - 同じレイアウト、異なる **) で実行します。`backend`** キー / **`providers`** エイリアス)。インフラには次のものが含まれます。

- 共有スタイル **VPC** (プライベート + パブリック サブネット、出力用 NAT)。
- **EKS** ワークロード用クラスター。
- Helm または GitOps を介したオプションの **アドオン** (Ingress コントローラー、メトリクス サーバー)。爆発範囲を制限するためにすべてが 1 つの Terraform ルートに含まれることは**ありません**。以下では、**ネットワーク + コントロール プレーン**に焦点を当てています。

## 2. リポジトリのレイアウト

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

それぞれ **`env/<name>`** は **独自の Terraform ルート** → 別個の **`terraform.tfstate`** （違う **`key`** S3)。

## 3. バックエンドとプロバイダー (`env/prod/backend.tf`)

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

## 4. VPC モジュール (`env/prod/main.tf`抜粋）

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

## 5. EKS モジュール (`env/prod/main.tf`抜粋）

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

ピン**`version`** すべてのモジュール。メジャー バージョンにアップグレードする前に、モジュール アップグレード ガイドをお読みください。

## 6. 変数のスケッチ (`env/prod/variables.tf`)

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

**`prod.tfvars`** には具体的な CIDR/AZ/クラスター名が含まれます。ここにはパスワードはありません。

## 7. __​​ IT0__で起こるか

1.**`terraform fmt -check`** / **`validate`** PR で。
2.**`terraform plan`** と **`AWS_ROLE_ARN`** OIDC 経由 (有効期間の長いキーはありません)。
3. 人間の承認 → **`terraform apply`** マージまたはプロモートされたワークフローについて。

ステージングスタックの重複 **`env/staging`** より小さいノード プールと **`single_nat_gateway = true`** コストを節約するため。

## 8. 2日目の分割 (現実世界での一般的な選択)

- **Terraform** は、**VPC**、**EKS**、**IAM**、**RDS** スケルトン、**Route53** ゾーンを所有しています。
- **Helm / Argo CD / Flux** は、毎日変更される **マイクロサービス** をデプロイします。アプリの調整に 40 分かかる Terraform 計画を回避できます。

GitOps または ** を参照する専用の Terraform スタックで可観測性 (**Prometheus Operator**、**Ingress**) を維持します。`cluster_endpoint`** 経由 **`remote_state`** または手動出力。

## 9. このレイアウトで抜け穴を回避できる

- 単一の巨人**`tfstate`** 200 個のアプリの場合 → ロックの痛み; **爆発半径** (ネットワーク、クラスター、アプリ) によって分割されます。
- **`apply`** ロックのないラップトップから → **常に**リモート バックエンドを使用します。
- リリース ノートを読まずに EKS をアップグレードする → ** をピン留めする`cluster_version`**、最初に **ステージング** でテストしてください。

プロバイダー/リージョンをクラウドに合わせて調整します。**形状** (環境ディレクトリ、リモート状態、VPC → クラスター → GitOps) は、異なるモジュールを使用して **GCP/GKE** および **Azure/AKS** に転送されます。
