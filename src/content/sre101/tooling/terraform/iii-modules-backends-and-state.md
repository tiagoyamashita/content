---
label: "III"
subtitle: "モジュールのバックエンドと状態"
group: "SRE"
order: 3
---
SRE ツール — Terraform: モジュール、バックエンド、状態

モジュールはパターンを再利用します。リモート **状態** にはロックとバックアップの規律が必要です。

## 1. モジュール

```hcl
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.5"

  name = "prod-vpc"
  cidr = "10.0.0.0/16"

  azs             = var.azs
  private_subnets = var.private_subnets
  public_subnets  = var.public_subnets
}
```

- Pin **`version`** for registry modules or Git refs (`?ref=v1.2.3`).
- Publish internal modules via **Git/Terraform Registry** with semver tags—document inputs/outputs (`README`, tests).

## 2. リモート バックエンドとロック

例 **AWS S3 + DynamoDB ロック**:

```hcl
terraform {
  backend "s3" {
    bucket         = "tf-state-myorg"
    key            = "prod/network/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
```

**Terraform クラウド / エンタープライズ** は、RBAC、投機的プラン、ポリシー セットを追加します (**Sentinel** / **OPA** 統合はさまざまです)。多くの場合、特注の S3+Dynamo セットアップが置き換えられます。

## 3. リモート状態のコンシューマ

```hcl
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "tf-state-myorg"
    key    = "prod/network/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_db_subnet_group" "app" {
  subnet_ids = data.terraform_remote_state.network.outputs.private_subnets
}
```

明示的なコントラクト (**出力**) は、スタック間の暗黙的な結合に勝ります。

## 4. 州の衛生状態

- Treat corruption / contention as **severity-1**—maintain **versioned backups** (S3 versioning, Terraform Cloud state history).
- Restrict IAM who may **`terraform state`** operations (`mv`, `rm`).
- Never edit **`terraform.tfstate`** manually unless disaster recovery runbooks demand it.

## 5. コードとしての可観測性リソース

Use vendor providers (**Grafana**, **Datadog**) alongside **`kubernetes_manifest`** / **Helm** resources so dashboards/alerts travel with cluster revisions—pair with **Prometheus**/**Alertmanager** folders in Git.
