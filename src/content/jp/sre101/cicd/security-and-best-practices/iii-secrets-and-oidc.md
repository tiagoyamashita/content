---
label: "III"
subtitle: "秘密と OIDC"
group: "CI/CD"
order: 3
---
秘密と OIDC

CI の **シークレット** はソース管理内に存在してはなりません。 **OIDC** (OpenID Connect) を使用すると、パイプラインでクラウド資格情報の有効期間の短い ID トークンを交換できます。有効期間の長い API キーは必要ありません。

## 1. プラットフォーム別の秘密ストレージ

|プラットフォーム |ストア |範囲 |
|----------|----------|----------|
| GitHub アクション |設定 → 秘密 |組織/リポジトリ/環境 |
| Gitラボ CI |設定 → CI/CD → 変数 |プロジェクト / グループ |
| Jenkins |認証情報プラグイン |グローバル / フォルダー / ジョブ |

ルール:

- ログ内のシークレットを **マスク**します (プラットフォームのデフォルト)。
- **範囲が狭い** — `environment: production` ジョブのみの prod シークレット。
- **漏れの疑いがある場合は、予定通りに**ローテーション**します。
- **決して** `run:` スクリプトでシークレットをエコーし​​ないでください。

```yaml
# GitHub — reference secret
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

```yaml
# GitLab — masked variable
deploy:
  script: deploy.sh
  variables:
    DEPLOY_TOKEN: $DEPLOY_TOKEN   # set in UI, masked + protected
```

## 2. フォーク PR の安全性

|プラットフォーム |フォーク PR のデフォルト |
|----------|----------------------|
| GitHub アクション |リポジトリのシークレットにアクセスできません |
| Gitラボ |フォークから MR に隠された保護された変数 |

ワークフローが昇格されたアクセスで実行されている場合、悪意のある PR によってシークレットが漏洩される可能性があります。リスクを理解していない限り、信頼できないコードには **`pull_request`** (`pull_request_target` ではない) を使用してください。

## 3. OIDC — 静的キーに勝る理由

|静的 AWS キー | OIDC |
|--|------|
|数か月/数年生きます |議事録 TTL |
|シークレットとして保存 |秘密はありません - 信頼関係 |
|実行ごとに同じキー |ワークフロー/リポジトリ/ブランチごとのスコープ |
|監査が難しい |クラウド監査ログには件名 | が示されています

## 4. GitHub アクション → AWS

**AWS IAM** — GitHub OIDC プロバイダーを信頼します。最小限の権限を持つ役割。

```yaml
permissions:
  id-token: write   # required for OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-deploy
          aws-region: us-east-1

      - run: aws ecs update-service --cluster prod --service api --force-new-deployment
```

IAM 信頼ポリシー (簡略化):

```json
{
  "Effect": "Allow",
  "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
    },
    "StringLike": {
      "token.actions.githubusercontent.com:sub": "repo:myorg/myapp:ref:refs/heads/main"
    }
  }
}
```

**`sub`** を特定のリポジトリとブランチに制限します。

## 5. GitHub アクション → GCP / Azure

**GCP** — Workload Identity Federation:

```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/123/locations/global/workloadIdentityPools/pool/providers/github
    service_account: deploy@myproject.iam.gserviceaccount.com
```

**Azure** — アプリ登録時のフェデレーション資格情報:

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

**クライアント/テナント/サブスクリプション ID** のみが保存されます。フェデレーションを使用する場合、クライアント シークレットは保存されません。

## 6. GitLab CI OIDC の例

```yaml
deploy:
  id_tokens:
    AWS_TOKEN:
      aud: https://gitlab.com
  script:
    - >
      export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s"
      $(aws sts assume-role-with-web-identity
      --role-arn arn:aws:iam::123456789012:role/gitlab-deploy
      --role-session-name gitlab
      --web-identity-token $AWS_TOKEN
      --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]'
      --output text))
    - aws s3 sync ./dist s3://my-bucket/
```

## 7. __​​IT0__ 認証情報

```groovy
pipeline {
  environment {
    DEPLOY_KEY = credentials('deploy-ssh-key')
  }
  stages {
    stage('Deploy') {
      steps {
        sh 'ansible-playbook deploy.yml'
      }
    }
  }
}
```

新しいセットアップでは、長期間有効な Jenkins に保存されたキーよりも **HashiCorp Vault** またはクラウド OIDC プラグインを優先します。

## 8. ローテーションチェックリスト

|ステップ |アクション |
|------|----------|
| 1 |秘密の年齢と範囲を特定する |
| 2 |クラウドで新しい認証情報を作成する |
| 3 | CI シークレット / IAM ロールを更新 |
| 4 |スモークデプロイを実行する |
| 5 |古い資格情報を取り消す |
| 6 |ランブック内の文書 |

## 9. アンチパターン

|アンチパターン |リスク |
|--------------|------|
|リポジトリ内の `AWS_ACCESS_KEY_ID` |永続的な爆発範囲 |
|開発 CI の同じ prod シークレット |横方向の動き |
|デバッグ ステップで `env` をログに記録する |ログアーカイブの秘密 |
| OIDC ロールは `*` リポジトリを信頼します。どのリポジトリでも | を想定できます。

**関連:** **Terraform** サブメニュー → [CI/CD の Terraform](../terraform/vii-terraform-in-cicd.md) (計画/適用の OIDC)、[最小特権ランナー](iv-least-privilege-runners.md)。
