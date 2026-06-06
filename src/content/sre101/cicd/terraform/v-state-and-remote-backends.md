---
label: "V"
subtitle: "状態およびリモートのバックエンド"
group: "CI/CD"
order: 5
---
状態およびリモートのバックエンド

**Terraform 状態** (`terraform.tfstate`) は、HCL を実際のクラウド リソース ID にマップします。チームは**ロック**を備えた**リモート バックエンド**を使用する必要があります**。状態を Git にコミットしないでください。

## 1. 状態に含まれるもの

```json
{
  "version": 4,
  "resources": [
    {
      "type": "aws_instance",
      "name": "app",
      "instances": [{
        "attributes": {
          "id": "i-0abc123def456",
          "public_ip": "54.123.45.67"
        }
      }]
    }
  ]
}
```

|状態が存在する理由 |詳細 |
|-------|------|
|マップ名 → ID | `aws_instance.app` → `i-0abc123` |
|パフォーマンス |各プランのすべてのリソースを再クエリすることを回避します。
|メタデータ |依存関係、シリアル、系統 |

状態には **機密値** (パスワード、キー) が含まれる場合があります。秘密として扱います。

## 2. 状態を Git にコミットしないでください。

|リスク |結果 |
|------|---------------|
| JSON の秘密 |リポジトリ履歴によるリーク |
|多様な地方州 | 2 人のエンジニアが矛盾する変更を適用します。
|ロックなし |破損したリソースを同時に適用します。

`.gitignore` に追加:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
.terraform.lock.hcl   # commit lock file — pins provider checksums
```

**コミット** `.terraform.lock.hcl` を実行して、再現可能なプロバイダーのバージョンを取得します。

## 3. S3 リモート バックエンド (AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "myapp/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

|コンポーネント |役割 |
|-----------|------|
| **S3 バケット** |状態ファイルを保存します |
| **DynamoDB テーブル** | ID をロック — 一度に 1 つずつ適用 |
| **暗号化** | SSE 休息中 |

バックエンド リソースを一度作成し (ブートストラップ スタックまたは別の管理プロセス)、すべての環境設定から参照します。

## 4. その他のバックエンド

|バックエンド | | に共通
|-----------|-----------|
| **Terraform クラウド / HCP** | HashiCorp がホストする状態 + 実行 |
| **アズールム** | Azure BLOB + リース |
| **gcs** | Google クラウド ストレージ |
| **ローカル** |ソロ開発者のみ |

## 5. 状態のロック

```text
Engineer A: terraform apply  → acquires lock
Engineer B: terraform apply  → Error: lock already held
Engineer A: apply completes  → releases lock
Engineer B: retry            → succeeds
```

ロックを使用しない場合、2 つの適用により API 呼び出しがインターリーブされ、インフラストラクチャの不整合が生じる可能性があります。

## 6. CLI コマンドをステートする

```bash
terraform state list
terraform state show aws_instance.app
terraform state mv aws_instance.old aws_instance.new
terraform state rm aws_instance.orphan   # remove from state, not cloud
terraform import aws_instance.app i-0abc123
```

|コマンド |使用 |
|----------|-----|
| **インポート** |既存のクラウド リソースを Terraform の下に置く |
| **MV** |破棄/作成を行わずに構成内のリソースの名前を変更します。
| **rm** |リソースの管理を停止する (手動クリーンアップ) |

## 7. 環境ごとの状態

```text
S3 key paths:
  myapp/dev/terraform.tfstate
  myapp/staging/terraform.tfstate
  myapp/prod/terraform.tfstate
```

個別のキー (または個別のバケット) は爆発範囲を分離します。 **決して**、開発環境と製品環境で 1 つの状態ファイルを共有しないでください。

## 8. ドリフト検出

**ドリフト** — 誰かが Terraform の外でクラウド コンソールを変更しました。

```bash
terraform plan   # shows ~ update or unexpected -/+ replace
```

CI: `terraform plan` をスケジュールどおりに実行します。プランが空でない場合はアラートを発します。オプション: **terraform plan -detailed-exitcode` — 変更が保留中の場合は 2 を終了します。

## 9. 敏感な出力

```hcl
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

状態のまま保存されます。リモート バックエンド暗号化とバケット上の IAM が必要です。

**関連:** [CI/CD の Terraform](vii-terraform-in-cicd.md)、[秘密と OIDC](../security-and-best-practices/iii-secrets-and-oidc.md)。
