---
label: "I"
subtitle: "概要"
group: "CI/CD"
order: 1
---
Terraform — 概要

**Terraform** (HashiCorp、IBM 2024) は **コードとしてのインフラストラクチャ (IaC)**: クラウド リソースを **HCL**、バージョンは Git で記述し、環境間で一貫して適用されます。これは **クラウドに依存しない** — AWS 製品ではありません (AWS ネイティブ IaC は **CloudFormation**)。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [Terraformとは](ii-what-is-terraform.md) | IaC が解決する問題、vs CloudFormation、ワークフロー |
| [HCL、リソースと変数](iii-hcl-resources-and-variables.md) | HCL 構文、変数、出力、データ ソース |
| [AWS の例 — VPC & EC2](iv-aws-example-vpc-and-ec2.md) | VPC、サブネット、EC2 — 完全な動作例 |
| [状態とリモート バックエンド](v-state-and-remote-backends.md) | tfstate、S3 バックエンド、ロック、状態 CLI |
| [モジュールと環境](vi-modules-and-environments.md) |モジュール、レジストリ、ワークスペース、環境分割 |
| [CI/CD の Terraform](vii-terraform-in-cicd.md) | PR で計画し、メイン、OIDC、Atlantis に適用 |

**関連:** パート I の基礎、**セキュリティとベスト プラクティス** → [秘密と OIDC](../security-and-best-practices/iii-secrets-and-oidc.md)、**ツールとプラットフォーム** → GitHub アクション。

##コアワークフロー

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" role="img" aria-label="Terraform init plan apply destroy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Plan before apply — always</text>
  <rect x="12" y="40" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="20" y="60" fill="#e4e4e7" font-size="8">init</text>
  <path d="M68 56 H88" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="88" y="40" width="56" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="96" y="60" fill="#e4e4e7" font-size="8">plan</text>
  <path d="M144 56 H164" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="164" y="40" width="56" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="172" y="60" fill="#e4e4e7" font-size="8">apply</text>
  <path d="M220 56 H240" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 2"/>
  <rect x="240" y="40" width="64" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="248" y="60" fill="#e4e4e7" font-size="8">destroy</text>
  <text x="320" y="56" fill="#71717a" font-size="9">teardown only</text>
</svg></figure>

## 主要なプロパティ

|プロパティ |意味 |
|----------|----------|
| **宣言的** |希望する状態を指定します。 Terraform は diff | を計算します。
| **冪等** |同じ設定を再適用 → 追加の変更は不要 |
| **計画第一** |プレビューは APIs に触れる前に作成/更新/削除を行います。
| **プロバイダーベース** | AWS、Azure、GCP、K8s、GitHub、Datadog — 3000 以上のプロバイダー |

## Terraform を使用する場合

|良いフィット感 |代替案を検討する |
|----------|--------------------------|
|マルチクラウドまたはマルチサービスインフラ | AWS-限定ショップ → CloudFormation/CDK |
|チームには状態の共有とレビューが必要 |小規模な個人プロジェクト → クリック操作 OK |
| GitOps スタイルのインフラ変更 | VM 上のアプリ構成 → Ansible (`ansible-and-jenkins/`) |

## リハーサル

- Terraform 対 CloudFormation — それぞれをロックインするのは誰ですか?
- なぜ決してコミットしないのか`terraform.tfstate`?
- 何をするのですか`terraform plan`見せる？
