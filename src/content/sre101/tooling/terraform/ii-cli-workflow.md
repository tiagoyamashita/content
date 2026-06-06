---
label: "II"
subtitle: "CLI ワークフロー"
group: "SRE"
order: 2
---
SRE ツール — Terraform: CLI ワークフロー






**からの毎日のコマンド`init`** を通して **`apply`**、さらに変数とリフレッシュ。

## 1.標準的なライフサイクル

```text
terraform init          # providers + backends + modules
terraform validate      # config correctness (no API calls)
terraform fmt -recursive
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

**`plan`** それなし **`apply`** はゲートがマージするものです。テキスト/HTML プランを CI アーティファクトにキャプチャします。

## 2. ワークスペースと環境

- **CLI ワークスペース** (`terraform workspace select prod`) 1 つのバックエンド構成内で **state** 名前空間を分割します。単純ですが、悪用されやすいです。多くのチームは別のディレクトリを好みます (`env/prod`) + 個別の **`backend.key`** または完全に別個の状態バケット。
- ** 経由で環境の詳細を渡します`-var-file=prod.tfvars`** および CI シークレット。

## 3. 変数と秘密

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

コミットを避ける **`.tfvars`** シークレットを使用 - 環境変数を使用 **`TF_VAR_db_password`**、Vault、または CI シークレット ストア。

## 4. インポートとターゲットを絞った操作

- **`terraform import aws_instance.app i-0abc123`** 既存のインフラを接続します。依然として一致するリソース ブロックが必要です。
- **`-target`** 外科的修正の場合 - 避難ハッチのみ。依存関係の偏りは問題を隠す危険性があります。

## 5. リフレッシュ＆ドリフト

- デフォルト プランはリモート オブジェクトを更新します。手動によるコンソール編集をドリフトとして検出します。
- **`terraform refresh`** / 計画に組み込まれた非推奨のスタンドアロン リフレッシュ セマンティクス。ドリフトを無視すると Terraform/状態の相違が生じることを理解してください。

## 6.破壊して置き換える

- **`terraform destroy`** 管理対象オブジェクトを削除します。承認とスコープ指定されたワークスペース/モジュールで製品を保護します。
- **`lifecycle { prevent_destroy = true }`** 重要なデータセットを保護します。とにかくバックアップと組み合わせます。

次: **モジュール / バックエンド / 状態**、次に **CI とプラクティス**。
