---
label: "II"
subtitle: "テラフォームとは"
group: "CI/CD"
order: 2
---
テラフォームとは

コンソールのクリックは遅く、エラーが発生しやすく、再現性がありません。 **Terraform** を使用すると、コードでインフラストラクチャを記述し、PR でレビューし、同じ構成を開発、ステージング、本番環境に適用できます。

## 1. 誰が作るのか

|ツール |ベンダー |範囲 |
|------|--------|------|
| **テラフォーム** |ハシコープ (IBM) |マルチクラウド、3000 以上のプロバイダー |
| **クラウドフォーメーション** | AWS | AWS のみ (JSON/YAML) |
| **腕 / 上腕二頭筋** |マイクロソフト |アズール |
| **展開マネージャー** |グーグル | GCP |
| **プルミ / CDK** |いろいろ |汎用言語 |

Terraform は AWS 製品ではありません**。 AWS のみのスタックを使用するチームは、モジュール、コミュニティ、またはマルチアカウント パターンに Terraform を選択する場合があります。

## 2. 中心となる概念

|用語 |定義 |
|------|-----------|
| **プロバイダー** | API と通信するプラグイン (`aws`、`azurerm`、`google`) |
| **リソース** |管理対象オブジェクト (`aws_instance`、`azurerm_resource_group`) |
| **データソース** |既存のインフラを管理せずに読み取る |
| **変数** |入力パラメータ |
| **出力** |適用後にエクスポートされる値 (IP、ARN) |
| **州** |構成 → 実リソース ID のマップ (`terraform.tfstate`) |
| **モジュール** |再利用可能な `.tf` ファイルのバンドル |

## 3. CLI ワークフロー

```bash
terraform init      # Download providers & modules; configure backend
terraform validate  # Syntax check
terraform fmt       # Format HCL
terraform plan      # Preview diff (dry run)
terraform apply     # Create / update / delete to match config
terraform destroy   # Tear down all managed resources
```

```text
┌─────────┐    ┌─────────┐    ┌─────────┐
│  init   │ →  │  plan   │ →  │  apply  │
└─────────┘    └─────────┘    └─────────┘
     │              │               │
     ▼              ▼               ▼
 providers      diff vs        cloud API
 & backend       state          calls
```

## 4. Terraform が変更を適用する方法

1. 現在の **状態** (ローカルまたはリモート) を読み取ります。
2. 更新 — 実際のリソース属性についてクラウドをクエリします。
3. 目的の構成 (`.tf` ファイル) と状態を比較します。
4. **実行計画**を構築します: `+` 作成、`~` 更新、`-` 破棄。
5. `apply` で、依存関係の順序でプロバイダ API を呼び出します。

**依存関係グラフ** — Terraform は、`aws_subnet` が `vpc_id = aws_vpc.main.id` を介して `aws_vpc` に依存していることを認識します。

## 5. 宣言型と命令型

```hcl
# Declarative — desired count
resource "aws_instance" "web" {
  count         = 3
  instance_type = "t3.micro"
  ami           = var.ami_id
}
```

「インスタンス 1 を作成してから 2 を作成する」というスクリプトは作成しません。 **3 つのインスタンス**を宣言します。 Terraform は調和します。

## 6. Terraform と Ansible

| |テラフォーム |アンシブル |
|---|----------|----------|
|主な用途 | **プロビジョニング** インフラ (VPC、DB、K8s クラスター) | **構成** サーバー (パッケージ、ファイル、サービス) |
|モデル |宣言状態 |宣言的タスク |
|エージェント |なし (API 呼び出し) |ホストへの SSH |

一般的なパターン: Terraform は EC2 + セキュリティ グループを作成します。 Ansible はそれらのホストにアプリをインストールします (`ansible-and-jenkins/`)。

## 7. OpenTofu フォーク

HashiCorp のライセンス変更 (BSL) の後、**OpenTofu** は MPL 2.0 のコミュニティ フォークになりました。 CLI と HCL はほぼ互換性があります。バイナリ CI が使用する組織ポリシーを確認してください。

**関連:** [HCL、リソースと変数](iii-hcl-resources-and-variables.md)、[状態とリモート バックエンド](v-state-and-remote-backends.md)。
