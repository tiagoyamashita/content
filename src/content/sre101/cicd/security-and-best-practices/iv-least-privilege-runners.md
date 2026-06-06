---
label: "IV"
subtitle: "最も権限のないランナー"
group: "CI/CD"
order: 4
---
最も権限のないランナー

**ランナー**は、許可された資格情報とネットワーク アクセスを使用してパイプライン ステップを実行します。デフォルトは、組織全体の管理者トークンではなく、ジョブごとの **最小権限** です。

## 1. 原則

|リソース |最小特権とは |
|----------|--------------------------|
| **GitHub `GITHUB_TOKEN`** |ジョブがプッシュしない限り、`contents: read` |
| **クラウド IAM の役割** | S3 バケット プレフィックス、`s3:*` ではない |
| **K8s サービス アカウント** | 1 つの名前空間、1 つのデプロイ ロール |
| **ネットワーク** |ビルド ランナーが本番 DB に到達できません。

## 2. GitHub アクションの権限

**ワークフロー** または **ジョブ** レベルで設定します:

```yaml
# Default deny — add only what you need
permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write   # post PR comment with coverage
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  release:
    needs: test
    permissions:
      contents: write        # create GitHub Release
      id-token: write        # OIDC to cloud
    steps:
      - run: ./publish.sh
```

|許可 |一般的な使用法 |
|-----------|---------------|
| `contents: read` |チェックアウト、リポジトリの読み取り |
| `contents: write` |タグ付け、リリース、プッシュコミット |
| `id-token: write` | OIDC フェデレーション |
| `packages: write` | GitHub コンテナ レジストリへのプッシュ |
| `pull-requests: write` |コメントボット、レーベルPR |

## 3. GitLab ジョブ トークン

GitLab **CI_JOB_TOKEN** のスコープはプロジェクトに限定されており、構成するダウンストリーム プロジェクトが許可されます。

```yaml
# Limit who can trigger deploy
deploy:
  stage: deploy
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  environment:
    name: production
  script: ./deploy.sh
```

**保護されたブランチ** + **保護された変数**を使用して、メンテナのみが `main` にマージされるようにします。

## 4. 自己ホスト型ランナー

|リスク |緩和 |
|------|-----------|
|ジョブ間のワークスペース汚染 | **一時** ランナー (ジョブごとの新しい VM/コンテナー) |
|悪意のある PR コードがネットワーク上で実行される |シークレットを使用してセルフホストでフォーク PR を実行しないでください。
|ランナーの妥協 = 長期間のアクセス |トラストゾーンごとに個別のランナープール |
| Docker ソケット アクセス |ルートと同等 — DinD を分離 |

**GitHub** — ランナー グループとラベルを使用します。

```yaml
jobs:
  internal-test:
    runs-on: [self-hosted, linux, internal]   # no prod access

  prod-deploy:
    runs-on: [self-hosted, linux, deploy-pool]  # prod network only
    environment: production
```

**一時的なパターン:** GitHub Actions スケールセット、`docker+machine` を備えた GitLab Runner、またはジョブ後にポッドを削除する K8s executor。

## 5. フォークと信頼できないコード

```yaml
# Safe pattern — standard pull_request event
on:
  pull_request:   # runs in fork context without secrets

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm ci && npm test
```

ベース ブランチ シークレットが必要な場合を除き、**`pull_request_target`** は避けてください。また、信頼できないコードをレビューせずに PR ヘッドからチェックアウトしないでください。

## 6. Jenkins エージェントの分離

```groovy
pipeline {
  agent { label 'linux-build' }   // build pool — no prod creds

  stages {
    stage('Test') {
      steps { sh 'mvn verify' }
    }
    stage('Deploy') {
      agent { label 'deploy' }     // separate agent with deploy role
      when { branch 'main' }
      steps { sh './deploy.sh' }
    }
  }
}
```

本番認証情報は、グローバルではなく **フォルダー スコープ** 認証情報に保存します。

## 7. ネットワークのセグメンテーション図

<figure class="notes-diagram"><svg xmlns="18 viewBox="0 0 460 100" role="img" aria-label="Runner network zones">
  <rect x="12" y="32" width="100" height="48" rx="4" fill="rgba(59,130,246,0.1)" stroke="#60a5fa"/>
  <text x="24" y="52" fill="#e4e4e7" font-size="9">Public SaaS runners</text>
  <text x="24" y="66" fill="#71717a" font-size="8">PR tests only</text>
  <rect x="130" y="32" width="100" height="48" rx="4" fill="rgba(251,191,36,0.1)" stroke="#fbbf24"/>
  <text x="142" y="52" fill="#e4e4e7" font-size="9">Internal build pool</text>
  <text x="142" y="66" fill="#71717a" font-size="8">artifact registry</text>
  <rect x="248" y="32" width="100" height="48" rx="4" fill="rgba(248,113,113,0.1)" stroke="#f87171"/>
  <text x="260" y="52" fill="#e4e4e7" font-size="9">Deploy pool</text>
  <text x="260" y="66" fill="#71717a" font-size="8">prod API only</text>
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Separate runner pools by trust zone</text>
</svg></figure>

## 8. チェックリスト

- [ ] ワークフロー `permissions` が明示的に設定されています (デフォルトのすべて書き込みではありません)
- [ ] Prod ジョブは `environment` 保護を使用します
- [ ] 自己ホスト型ランナーが一時的であるか、ジョブ間でクリーンアップされる
- [ ] シークレットなしで孤立したランナーの PR をフォークします
- [ ] 導入エージェントは任意の PR コードをコンパイルできません

**関連:** [秘密と OIDC](iii-secrets-and-oidc.md)、[ジェンキンス](../tools-and-platforms/iv-jenkins.md)。
