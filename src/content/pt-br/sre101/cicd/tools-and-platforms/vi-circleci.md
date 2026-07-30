---
label: "VI"
subtitle: "CircleCI"
group: "CI/CD"
order: 6
---
CircleCI
SaaS CI with strong **caching**, **orbs** (reusable config packages), and fast Linux/Docker executors.

## 1. Config basics

**`.circleci/config.yml`** — version 2.1 recommended:

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

## 2. Maven / Java orb

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

## 3. Docker build and push

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

**Contexts** group secrets (`registry-credentials`) shared across projects.

## 4. Workflow with approval gate

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

## 5. Caching

CircleCI caches **`~/.npm`**, **`~/.m2`**, **`~/.gradle`** keyed by checksum of lockfiles:

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

**Docker layer caching** (`setup_remote_docker: docker_layer_caching: true`) speeds image builds.

## 6. When to choose CircleCI

| Pros | Cons |
|------|------|
| Excellent cache UX | Separate from GitHub/GitLab UI |
| Orbs reduce boilerplate | Pricing at high concurrency |
| Fast startup | Less built-in than GitLab all-in-one |

| Good fit | Less ideal |
|----------|------------|
| Polyrepo with shared orbs | Already all-in on GitHub Actions |
| Teams wanting SaaS without self-host Jenkins | Strict on-prem only |

**Related:** [Choosing a platform](viii-choosing-a-platform.md), [Docker in CI](v-docker-in-ci.md).
