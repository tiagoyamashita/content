---
label: "II"
subtitle: "CLI ワークフロー"
group: "SRE"
order: 2
---
SRE ツール — Terraform: CLI ワークフロー

**`init`** から **`apply`** までの毎日のコマンドと変数およびリフレッシュ。

## 1. 標準的なライフサイクル

```text
terraform init          # providers + backends + modules
terraform validate      # config correctness (no API calls)
terraform fmt -recursive
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

**`apply`** のない **`plan`** は、ゲートがマージするものであり、CI アーティファクト内のテキスト/HTML プランをキャプチャします。

## 2. ワークスペースと環境

- **CLI ワークスペース** (`terraform workspace select prod`) は、1 つのバックエンド構成内で **state** 名前空間を分割します。シンプルですが、悪用されやすいです。多くのチームは、個別のディレクトリ (`env/prod`) + 個別の **`backend.key`**、または完全に個別の状態バケットを好みます。
- **`-var-file=prod.tfvars`** および CI シークレットを介して環境の詳細を渡します。

## 3. 変数と秘密

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

シークレットを使用した **`.tfvars`** のコミットは避けてください。環境変数 **`TF_VAR_db_password`**、Vault、または CI シークレット ストアを使用してください。

## 4. インポートとターゲットを絞った操作

- **`terraform import aws_instance.app i-0abc123`** は既存のインフラを接続します。依然として一致するリソース ブロックが必要です。
- **`-target`** 外科的修正の場合 - 避難ハッチのみ。依存関係の偏りは問題を隠す危険性があります。

## 5. リフレッシュ＆ドリフト

- デフォルト プランはリモート オブジェクトを更新します。手動によるコンソール編集をドリフトとして検出します。
- **`terraform refresh`** / 計画に組み込まれた非推奨のスタンドアロン更新セマンティクス - ドリフトを無視すると、Terraform/状態の相違が生じることを理解してください。

## 6. 破壊して置き換える

- **`terraform destroy`** は管理オブジェクトを削除します。承認とスコープ指定されたワークスペース/モジュールで本番環境を保護します。
- **`lifecycle { prevent_destroy = true }`** は重要なデータセットを保護します。とにかくバックアップと組み合わせます。

次: **モジュール / バックエンド / 状態**、次に **CI とプラクティス**。
