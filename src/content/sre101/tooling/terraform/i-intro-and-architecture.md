---
label: "I"
subtitle: "イントロとアーキテクチャ"
group: "SRE"
order: 1
---
SRE ツール — Terraform: 概要とアーキテクチャ

インフラストラクチャを宣言的に記述します。 Terraform は依存関係グラフを計算し、プロバイダーを介してクラウド API を調整します。

## 1. 役割

**Terraform** (HashiCorp、エコシステム ピアには **OpenTofu** が含まれます) は、論理アドレス (`aws_instance.app`) を実際の ID (`i-0abc…`) にマップする **状態** を保持します。 **`terraform plan`** は、必要な構成と状態 + リモート API の違いを示します。 **`apply`** は **プロバイダ** を通じて作成/更新/削除を実行します。

## 2. ランニングの仕組み (メンタルモデル)

1. `.tf` を解析 → リソース + データ ソースの DAG を構築します。
2. 制約されない限り (**`-refresh=false`**)、**状態** / プロバイダーの読み取りを更新します。
3. 希望と実際の差 → 実行計画。
4. 依存関係が安全な順序で API を変更します。 **状態**を更新します。

プロバイダーは、**`required_providers`** ブロックで固定されたプラグインを介して、ベンダーの癖 (AWS/GCP/Azure/**Kubernetes**/Datadog/Grafana など) をカプセル化します。

## 3. 基本的な語彙

|アイデア |意味 |
|-----|----------|
| **リソース** |何かを作成/管理します (`resource "aws_s3_bucket" "logs"`)。 |
| **データソース** |読み取り専用の検索 (`data.aws_vpc.default`)。 |
| **プロバイダー** |エンドポイント/資格情報を構成するプラグイン (`provider "aws" {}`)。 |
| **モジュール** |リソースの呼び出し可能なパッケージ (`module "vpc" { … }`)。 |
| **州** |バインディングと出力はローカルまたはリモートで保持され、一貫性を保つ必要があります。 |

## 4. 構成スニペット (`providers`)

Terraform とプロバイダーを固定する:

```hcl
terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.30"
    }
  }
}

provider "aws" {
  region = var.region
}
```

**CLI ワークフロー**、**モジュール/バックエンド/状態**、**CI とプラクティス**に進みます。
