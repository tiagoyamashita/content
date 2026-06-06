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

- レジストリ モジュールまたは Git 参照用のピン **`version`** (`?ref=v1.2.3`)。
- semver タグを使用して **Git/Terraform レジストリ** 経由で内部モジュールを公開します (ドキュメントの入力/出力 (`README`、テスト))。

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

**Terraform Cloud / Enterprise** は、RBAC、投機的プラン、ポリシー セットを追加します (**Sentinel** / **OPA** 統合はさまざまです)。多くの場合、オーダーメイドの S3+Dynamo セットアップが置き換えられます。

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

- 破損/競合を **重大度-1** として扱い、**バージョン管理されたバックアップ**を維持します (S3 バージョン管理、Terraform Cloud 状態履歴)。
- **`terraform state`** 操作 (`mv`、`rm`) を実行できる IAM を制限します。
- 災害復旧ランブックで要求されない限り、**`terraform.tfstate`** を手動で編集しないでください。

## 5. コードとしての可観測性リソース

ベンダー プロバイダー (**Grafana**、**Datadog**) を **`kubernetes_manifest`** / **Helm** リソースとともに使用して、ダッシュボード/アラートがクラスター リビジョンに合わせて移動できるようにします。Git の **Prometheus**/**Alertmanager** フォルダーと組み合わせてください。
