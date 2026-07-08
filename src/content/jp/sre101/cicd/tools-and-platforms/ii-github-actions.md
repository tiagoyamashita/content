---
label: "II"
subtitle: "GitHub アクション"
group: "CI/CD"
order: 2
---
GitHub アクション

**GitHub** リポジトリのネイティブ CI/CD。ワークフローは YAML として **`.github/workflows/`** に存在します。ジョブは **GitHub ホスト** または **自己ホスト** ランナーで実行されます。

## 1. 中心となる概念

|用語 |意味 |
|-----|----------|
| **ワークフロー** | YAML ファイル。イベントによって引き起こされる |
| **仕事** | 1 人のランナーで実行されます。他の仕事に依存できる |
| **ステップ** |シェル コマンドまたは **`uses:`** アクション |
| **アクション** |再利用可能なユニット (チェックアウト、セットアップノード、デプロイ) |
| **ランナー** |ジョブを実行している VM/コンテナ |

## 2. トリガー

```yaml
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 6 * * 1"   # weekly Monday 06:00 UTC
  workflow_dispatch:        # manual run button
```

## 3. 最小限の Node.js CI の例

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm

      - run: npm ci
      - run: npm test
      - run: npm run build
```

## 4. マトリックスの構築

OS / ランタイム バージョン間で同じジョブを実行します。

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        node: [20, 22]
        os: [ubuntu-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
      - run: npm ci && npm test
```

## 5. Java / Maven の例

```yaml
jobs:
  maven:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "22"
          cache: maven
      - run: mvn -B verify
```

## 6. Docker イメージをビルドしてプッシュする

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v6
        with:
          context: .
          push: ${{ github.ref == 'refs/heads/main' }}
          tags: ghcr.io/${{ github.repository }}:latest
```

## 7. 環境を使用してデプロイする

**必須レビュー担当者**によるゲート制作:

```yaml
jobs:
  deploy-prod:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://api.example.com
    steps:
      - run: ./scripts/deploy.sh
        env:
          DEPLOY_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

**[設定] → [環境] → [運用] → [必要なレビュー担当者]** を構成します。

## 8. 再利用可能なワークフロー

**`.github/workflows/reusable-test.yml`:**

```yaml
on:
  workflow_call:
    inputs:
      node-version:
        required: true
        type: string

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ inputs.node-version }}
      - run: npm ci && npm test
```

**発信者:**

```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "22"
```

## 9. シークレットと権限

|練習 |なぜ |
|----------|-----|
|トークンの場合は `secrets.*` |資格情報を決してコミットしないでください |
|最小特権 `permissions:` |デフォルトの GITHUB_TOKEN スコープ |
| OIDC からクラウドへ (`aws-actions/configure-aws-credentials`) |有効期間の長い AWS キーはありません |
|フォーク PR はシークレットを取得しません。セキュリティのデフォルト |

## 10. アクションを選択する場合

|長所 |短所 |
|------|------|
| GitHub のネイティブ | GitHub (またはミラー) に関連付けられています |
|巨大な **マーケットプレイス** |大規模な複雑な組織の請求 |
|パブリック リポジトリの無料分 |自己ホスト型ランナーには運用が必要 |

**関連:** [CI の Docker](v-docker-in-ci.md)、[秘密と OIDC](../security-and-best-practices/iii-secrets-and-oidc.md)。
