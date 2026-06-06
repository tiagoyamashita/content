---
label: "III"
subtitle: "Gitラボ CI"
group: "CI/CD"
order: 3
---
Gitラボ CI/CD

リポジトリ ルートの **`.gitlab-ci.yml`** で定義されたパイプライン。ランナーは、**GitLab.com 共有** ランナーまたは **自己ホスト型** エージェントでジョブを実行します。

## 1. 中心となる概念

|用語 |意味 |
|-----|----------|
| **パイプライン** |コミット/タグの完全な実行 |
| **ステージ** |順序付けされたグループ (`build` → `test` → `deploy`) |
| **仕事** |ランナー上のスクリプト + 画像 |
| **ランナー** |ジョブを実行します (シェルまたは Docker エグゼキューター) |

## 2. 最小限のパイプライン

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test

variables:
  NODE_VERSION: "22"

build:
  stage: build
  image: node:22-bookworm
  script:
    - npm ci
    - npm run build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

test:
  stage: test
  image: node:22-bookworm
  script:
    - npm ci
    - npm test
```

## 3. Spring Boot / Maven の例

```yaml
stages:
  - test
  - package

test:
  stage: test
  image: eclipse-temurin:22-jdk
  script:
    - ./mvnw -B test
  cache:
    key: maven-$CI_COMMIT_REF_SLUG
    paths:
      - .m2/repository

package:
  stage: package
  image: docker:27
  services:
    - docker:27-dind
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  only:
    - main
```

## 4. `extends` および `include` を使用した DRY

**`.gitlab/ci/test-template.yml`:**

```yaml
.test_template:
  image: node:22-bookworm
  before_script:
    - npm ci
  cache:
    key: npm-$CI_COMMIT_REF_SLUG
    paths:
      - node_modules/

unit-test:
  extends: .test_template
  stage: test
  script:
    - npm run test:unit
```

**ルートファイル:**

```yaml
include:
  - local: .gitlab/ci/test-template.yml

stages:
  - test
```

## 5. `needs:` を使用した DAG

ステージの厳密な順序付けをスキップします。lint が通過したらすぐにドキュメントのデプロイを開始します。

```yaml
stages:
  - lint
  - test
  - deploy

lint:
  stage: lint
  script: npm run lint

test:
  stage: test
  needs: [lint]
  script: npm test

pages:
  stage: deploy
  needs: [lint]    # does not wait for test
  script:
    - npm run build:docs
  artifacts:
    paths:
      - public
  only:
    - main
```

## 6. 環境

```yaml
deploy_staging:
  stage: deploy
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl apply -f k8s/staging/
  only:
    - main

deploy_production:
  stage: deploy
  environment:
    name: production
    url: https://example.com
  script:
    - kubectl apply -f k8s/prod/
  when: manual
  only:
    - main
```

非アクティブ状態になった後の **自動停止** 環境 - アプリのレビューに役立ちます。

## 7. 組み込みレジストリ

```yaml
variables:
  DOCKER_TLS_CERTDIR: "/certs"

publish:
  image: docker:27
  services:
    - docker:27-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_TAG
  rules:
    - if: $CI_COMMIT_TAG
```

## 8. GitLab と GitHub (簡単)

|特集 | GitLab CI | GitHub アクション |
|----------|----------|-----|
|構成 |シングル `.gitlab-ci.yml` |複数のワークフロー ファイル |
| DAG | `needs:` |求人に関する`needs:` |
|レジストリ |内蔵 | GHCR 別セットアップ |
|セルフホスト |成熟したランナーモデル |自己ホストランナー |

## 9. GitLab CI を選択する場合

|長所 |短所 |
|------|------|
|オールインワンの DevOps プラットフォーム | CI だけが必要な場合はさらに重い |
|強力な自己管理オプション | YAML は大きくなる可能性があります |
|レビューアプリ、セキュリティスキャン内蔵 | |

**関連:** [CI の Docker](v-docker-in-ci.md)、[概要](../security-and-best-practices/i-overview.md)。
