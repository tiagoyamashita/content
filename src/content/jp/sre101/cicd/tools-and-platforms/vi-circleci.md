---
label: "VI"
subtitle: "サークルCI"
group: "CI/CD"
order: 6
---
サークルCI

強力な **キャッシュ**、**orbs** (再利用可能な構成パッケージ)、高速 Linux/Docker エグゼキューターを備えた SaaS CI。

## 1. 構成の基本

**`.circleci/config.yml`** — バージョン 2.1 を推奨:

```yaml
version: 2.1

orbs:
  node: circleci/node@6.1.0

jobs:
  test:
    docker:
      - image: cimg/node:22.0
    steps:
      - checkout
      - node/install-packages:
          pkg-manager: npm
      - run:
          name: Run tests
          command: npm test

workflows:
  ci:
    jobs:
      - test
```

## 2. Maven / Java オーブ

```yaml
version: 2.1

orbs:
  maven: circleci/maven@2.1.0

jobs:
  verify:
    executor:
      name: maven/default
      tag: "22.0"
    steps:
      - checkout
      - maven/verify

workflows:
  build:
    jobs:
      - verify
```

## 3. Docker のビルドとプッシュ

```yaml
jobs:
  build-image:
    docker:
      - image: cimg/base:stable
    steps:
      - checkout
      - setup_remote_docker:
          docker_layer_caching: true
      - run:
          name: Build and push
          command: |
            echo "$REGISTRY_PASS" | docker login $REGISTRY -u "$REGISTRY_USER" --password-stdin
            docker build -t $REGISTRY/myapp:${CIRCLE_SHA1} .
            docker push $REGISTRY/myapp:${CIRCLE_SHA1}

workflows:
  deploy:
    jobs:
      - build-image:
          context: registry-credentials
```

**コンテキスト** グループ シークレット (`registry-credentials`) がプロジェクト間で共有されます。

## 4. 承認ゲートを使用したワークフロー

```yaml
workflows:
  release:
    jobs:
      - test
      - hold:
          type: approval
          requires:
            - test
      - deploy:
          requires:
            - hold
```

## 5. キャッシング

CircleCI は、ロックファイルのチェックサムによってキー設定された **`~/.npm`**、**`~/.m2`**、**`~/.gradle`** をキャッシュします。

```yaml
- restore_cache:
    keys:
      - npm-deps-{{ checksum "package-lock.json" }}
- run: npm ci
- save_cache:
    key: npm-deps-{{ checksum "package-lock.json" }}
    paths:
      - ~/.npm
```

**Docker レイヤー キャッシュ** (`setup_remote_docker: docker_layer_caching: true`) により、イメージのビルドが高速化されます。

## 6. CircleCI を選択する場合

|長所 |短所 |
|------|------|
|優れたキャッシュ UX | GitHub/GitLab UI から分離 |
|オーブは定型文を削減します |高同時実行時の価格設定 |
|高速スタートアップ | GitLab オールインワンよりも組み込み機能が少ない |

|良いフィット感 |あまり理想的ではない |
|----------|-----------|
|共有 Orbs を使用した Polyrepo | GitHub アクションにすでに全力を尽くしています |
|セルフホストのない SaaS を望んでいるチーム Jenkins |厳密にオンプレミスのみ |

**関連:** [プラットフォームの選択](viii-choosing-a-platform.md)、[CI の Docker](v-docker-in-ci.md)。
