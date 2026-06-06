---
label: "III"
subtitle: "GitLab CI"
group: "CI/CD"
order: 3
---
GitLab CI/CD
Pipelines defined in **`.gitlab-ci.yml`** at the repo root. Runners execute jobs on **GitLab.com shared** runners or **self-hosted** agents.

## 1. Core concepts

| Term | Meaning |
|------|---------|
| **Pipeline** | Full run for a commit/tag |
| **Stage** | Ordered group (`build` → `test` → `deploy`) |
| **Job** | Script + image on a runner |
| **Runner** | Executes jobs (shell or Docker executor) |

## 2. Minimal pipeline

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

## 3. Spring Boot / Maven example

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

## 4. DRY with `extends` and `include`

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

**Root file:**

```yaml
include:
  - local: .gitlab/ci/test-template.yml

stages:
  - test
```

## 5. DAG with `needs:`

Skip strict stage ordering — start deploy docs as soon as lint passes:

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

## 6. Environments

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

**Auto-stop** environments after inactivity — useful for review apps.

## 7. Built-in registry

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

## 8. GitLab vs GitHub (quick)

| Feature | GitLab CI | GitHub Actions |
|---------|-----------|----------------|
| Config | Single `.gitlab-ci.yml` | Multiple workflow files |
| DAG | `needs:` | `needs:` on jobs |
| Registry | Built-in | GHCR separate setup |
| Self-host | Mature runner model | Self-hosted runners |

## 9. When to choose GitLab CI

| Pros | Cons |
|------|------|
| All-in-one DevOps platform | Heavier if you only need CI |
| Strong self-managed option | YAML can grow large |
| Review apps, security scanning built-in | |

**Related:** `v-docker-in-ci.md`, `../security-and-best-practices/i-overview.md`.
