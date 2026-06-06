---
label: "VII"
subtitle: "CI/CD での Terraform"
group: "CI/CD"
order: 7
---
CI/CD での Terraform

標準パターン: **PR → 計画 (レビュー) → マージ → 適用**。信頼できない PR ブランチでは **`apply`** しないでください。クラウド認証情報には **OIDC** を使用します。

## 1. パイプラインの流れ

<figure class="notes-diagram"><svg xmlns="19 viewBox="0 0 460 100" role="img" aria-label="Terraform PR plan merge apply">
  <rect x="12" y="40" width="64" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="60" fill="#e4e4e7" font-size="8">PR opened</text>
  <path d="M76 56 H96" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="96" y="40" width="64" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="108" y="60" fill="#e4e4e7" font-size="8">plan</text>
  <path d="M160 56 H180" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="180" y="40" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="192" y="60" fill="#e4e4e7" font-size="8">review</text>
  <path d="M244 56 H264" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="264" y="40" width="64" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="276" y="60" fill="#e4e4e7" font-size="8">apply</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Apply only on main after merge</text>
  <text x="12" y="88" fill="#71717a" font-size="9">Post plan output as PR comment for human review</text>
</svg></figure>

## 2. GitHub アクション — 完全なワークフロー

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infra/**']
  pull_request:
    paths: ['infra/**']

permissions:
  contents: read
  pull-requests: write
  id-token: write

env:
  TF_WORKING_DIR: infra/environments/staging
  AWS_REGION: us-east-1

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ env.TF_WORKING_DIR }}

    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-terraform
          aws-region: ${{ env.AWS_REGION }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.5

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init -input=false

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        id: plan
        run: terraform plan -input=false -no-color -out=tfplan
        continue-on-error: true

      - name: Comment plan on PR
        uses: actions/github-script@v7
        if: github.event_name == 'pull_request'
        env:
          PLAN: ${{ steps.plan.outputs.stdout }}
        with:
          script: |
            const output = `#### Terraform Plan 📖
            \`\`\`
            ${process.env.PLAN || 'Plan failed — see logs'}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

      - name: Terraform Plan Status
        if: steps.plan.outcome == 'failure'
        run: exit 1

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -input=false -auto-approve tfplan
```

|ルール |なぜ |
|------|-----|
| PR について `plan` |インフラ diff のようなコードを確認する |
| `apply`は`main`のみ |不正な PR をクラウドに適用しない |
| `-out=tfplan` |計画された変更を正確に適用する |
| OIDC の役割 |静的 AWS キーはありません [シークレットと OIDC](../security-and-best-practices/iii-secrets-and-oidc.md) |

## 3. GitLab CI の例

```yaml
stages: [validate, plan, apply]

variables:
  TF_ROOT: infra/environments/staging

.terraform:
  image:
    name: hashicorp/terraform:1.7
    entrypoint: [""]
  before_script:
    - cd $TF_ROOT
    - terraform init -input=false

fmt:
  extends: .terraform
  stage: validate
  script:
    - terraform fmt -check -recursive

plan:
  extends: .terraform
  stage: plan
  script:
    - terraform plan -input=false -out=tfplan
  artifacts:
    paths:
      - $TF_ROOT/tfplan
    expire_in: 1 week

apply:
  extends: .terraform
  stage: apply
  script:
    - terraform apply -input=false tfplan
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
  environment:
    name: staging
```

## 4. アトランティス

**Atlantis** — 自己ホスト型ボット。 PRトリガープラン/応募に関するコメント:

```text
# PR comment
atlantis plan

# After review
atlantis apply
```

`atlantis.yaml`:

```yaml
version: 3
projects:
  - name: staging
    dir: infra/environments/staging
    workflow: default
    autoplan:
      when_modified: ["**/*.tf", "**/*.tfvars"]
```

| | GitHub アクション |アトランティス |
|---|----------------|----------|
|ホスティング | GitHub ランナー |あなたのサーバー |
| UX |ワークフロー YAML | PRコメント |
|マルチプロジェクト |マトリックスの仕事 |組み込みプロジェクト ディレクトリ |

## 5. ポリシーとセキュリティのスキャン

```yaml
- name: tfsec
  uses: aquasecurity/tfsec-action@v1.0.0
  with:
    working_directory: infra/

- name: Checkov
  run: checkov -d infra/ --framework terraform
```

**HIGH** のゲート PR の設定ミス (オープン SG、暗号化されていない S3)。 [サプライチェーンとSLSA](../security-and-best-practices/ii-supply-chain-and-slsa.md)を補完します。

## 6. 自動化のための終了コードを計画する

```bash
terraform plan -detailed-exitcode -out=tfplan
# 0 = no changes
# 1 = error
# 2 = changes pending
```

終了コード 2 を使用して、必要な場合にのみ適用ジョブをトリガーします。

## 7. 本番環境の安全対策

|コントロール |実装 |
|----------|----------------|
|手動承認 | GitHub 環境、GitLab `when: manual` |
|個別の IAM ロール | `github-terraform-prod` ステージングよりも厳格 |
|個別の状態キー | `myapp/prod/terraform.tfstate` |
|ドリフト検出 |予定 `terraform plan` + アラート |

## 8. アンチパターン

|アンチパターン |リスク |
|--------------|------|
|すべての PR で `apply` |攻撃者の PR がインフラを破壊 |
| CI のローカル状態 |ランの間にロスト |
| CI ロールの管理者 IAM |爆発範囲 |
| PRに計画はない |マージ時の驚き |

## 9. リハーサルの答え

- **`terraform plan`** — 作成/更新/削除と状態のプレビュー。
- **リモート バックエンド** — チームの共有状態 + ロック。
- **`module` ソース** — レジストリ URL、git URL、またはローカル パス。
- **Terraform と CloudFormation** — HashiCorp マルチクラウドと AWS ネイティブ。

**関連:** [状態とリモート バックエンド](v-state-and-remote-backends.md)、[GitHub アクション](../tools-and-platforms/ii-github-actions.md)。
