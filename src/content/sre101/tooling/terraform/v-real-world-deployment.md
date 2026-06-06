---
label: "V"
subtitle: "現実世界への展開"
group: "SRE"
order: 5
---
SRE ツール — Terraform: 現実世界への展開

チームが実際に出荷するパターン: **リモート状態**、**環境分割**、**VPC + Kubernetes**、**追加モジュール** - 明確にするためにトリミングされています。

## 1. シナリオ

**staging** と **prod** を 1 つの AWS アカウント (または別のアカウント - 同じレイアウト、異なる **`backend`** キー / **`providers`** エイリアス) で実行します。インフラには次のものが含まれます。

- 共有スタイル **VPC** (プライベート + パブリック サブネット、下り用 NAT)。
- ワークロード用の **EKS** クラスター。
- Helm または GitOps を介したオプションの **アドオン** (Ingress コントローラー、メトリクス サーバー)。多くの場合、爆発範囲を制限するためにすべてが 1 つの Terraform ルートに含まれるわけではありません。以下では、**ネットワーク + コントロール プレーン**に焦点を当てています。

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

各 **`env/<name>`** は、**独自の Terraform ルート** → 個別の **`terraform.tfstate`** (S3 では異なる **`key`**) です。

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

## 4. VPC モジュール (`env/prod/main.tf` 抜粋)

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

## 5. EKS モジュール (`env/prod/main.tf` 抜粋)

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

すべてのモジュールに **`version`** をピン付けします。メジャー バージョンにアップグレードする前に、モジュール アップグレード ガイドをお読みください。

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

## 7. CI で何が起こるか

1. PR: **`terraform fmt -check`** / **`validate`**
2. OIDC 経由の **`terraform plan`** と **`AWS_ROLE_ARN`** (有効期間の長いキーなし)。
3. 人間による承認 → マージまたはプロモートされたワークフローに関する **`terraform apply`**。

スタックの重複 **`env/staging`** をより小さいノード プールと **`single_nat_gateway = true`** でステージングし、コストを節約します。

## 8. 2 日目の分割 (現実世界での一般的な選択)

- **Terraform** は、**VPC**、**EKS**、**IAM**、**RDS** スケルトン、**Route53** ゾーンを所有しています。
- **Helm / Argo CD / Flux** は、毎日変更される **マイクロサービス** をデプロイします。アプリの調整に 40 分間かかる Terraform 計画を回避できます。

GitOps または **`remote_state`** または手動出力を介して **`cluster_endpoint`** を参照する専用の Terraform スタックで可観測性 (**Prometheus Operator**、**Ingress**) を維持します。

## 9. このレイアウトで回避できる落とし穴

- 200 個のアプリの場合、単一の巨大な **`tfstate`** → ロックの痛み。 **爆発半径** (ネットワーク、クラスター、アプリ) によって分割されます。
- ロックのないラップトップから **`apply`** → リモート バックエンドを **常に**使用します。
- リリース ノートを読まずに EKS をアップグレードする → **`cluster_version`** をピン留めし、最初に **ステージング** でテストします。

プロバイダー/リージョンをクラウドに合わせて調整します。**形状** (環境ディレクトリ、リモート状態、VPC → クラスター → GitOps) は、異なるモジュールを使用して **GCP/GKE** および **Azure/AKS** に転送されます。
