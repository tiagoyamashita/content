---
label: "IV"
subtitle: "最も権限のないランナー"
group: "CI/CD"
order: 4
---
最も権限のないランナー

**ランナー**は、許可された資格情報とネットワーク アクセスを使用してパイプライン ステップを実行します。デフォルトは、組織全体の管理者トークンではなく、ジョブごとの **最小権限** です。

## 1. 原則

| Resource | Least privilege means |
|----------|------------------------|
| **GitHub `GITHUB_TOKEN`** | `contents: read` unless job pushes |
| **Cloud IAM role** | S3 bucket prefix, not `s3:*` |
| **K8s service account** | One namespace, one deploy role |
| **Network** | Build runners cannot reach prod DB |

## 2. GitHub アクション権限

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

| Permission | Typical use |
|------------|-------------|
| `contents: read` | Checkout, read repo |
| `contents: write` | Tag, release, push commit |
| `id-token: write` | OIDC federation |
| `packages: write` | Push to GitHub Container Registry |
| `pull-requests: write` | Comment bot, label PR |

## 3. GitLab ジョブ トークン

GitLab **CI_JOB_TOKEN** の範囲はプロジェクトに限定され、構成したダウンストリーム プロジェクトが許可されます。

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

Use **protected branches** + **protected variables** so only maintainers merge to `main`.

## 4. 自己ホスト型ランナー

|リスク |緩和 |
|------|-----------|
|ジョブ間のワークスペース汚染 | **一時** ランナー (ジョブごとに新しい VM/ コンテナー) |
|悪意のある PR コードがネットワーク上で実行されます。シークレットを使用してセルフホストでフォーク PR を実行しないでください。
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

**Ephemeral pattern:** GitHub Actions scale-set, GitLab Runner with `docker+machine`, or K8s executor that deletes pod after job.

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

Avoid **`pull_request_target`** unless you need base-branch secrets and never checkout untrusted code from the PR head without review.

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

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 100" role="img" aria-label="Runner network zones">
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

- [ ] Workflow `permissions` explicitly set (not default write-all)
- [ ] Prod jobs use `environment` protection
- [ ] Self-hosted runners ephemeral or cleaned between jobs
- [ ] Fork PRs on isolated runners without secrets
- [ ] Deploy agents cannot compile arbitrary PR code

**Related:** [Secrets & OIDC](iii-secrets-and-oidc.md), [Jenkins](../tools-and-platforms/iv-jenkins.md).
