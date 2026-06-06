---
label: "II"
subtitle: "GitHub Actions"
group: "CI/CD"
order: 2
---
GitHub Actions
Native CI/CD for **GitHub** repos. Workflows live in **`.github/workflows/`** as YAML; jobs run on **GitHub-hosted** or **self-hosted** runners.

## 1. Core concepts

| Term | Meaning |
|------|---------|
| **Workflow** | YAML file; triggered by events |
| **Job** | Runs on one runner; can depend on other jobs |
| **Step** | Shell command or **`uses:`** action |
| **Action** | Reusable unit (checkout, setup-node, deploy) |
| **Runner** | VM/container executing the job |

## 2. Triggers

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

## 3. Minimal Node.js CI example

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

## 4. Matrix builds

Run the same job across OS / runtime versions:

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

## 5. Java / Maven example

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

## 6. Build and push Docker image

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

## 7. Deploy with environments

Gate production with **required reviewers**:

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

Configure **Settings → Environments → production → Required reviewers**.

## 8. Reusable workflows

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

**Caller:**

```yaml
jobs:
  call-test:
    uses: ./.github/workflows/reusable-test.yml
    with:
      node-version: "22"
```

## 9. Secrets and permissions

| Practice | Why |
|----------|-----|
| `secrets.*` for tokens | Never commit credentials |
| Least-privilege `permissions:` | Default GITHUB_TOKEN scope |
| OIDC to cloud (`aws-actions/configure-aws-credentials`) | No long-lived AWS keys |
| Fork PRs don't get secrets | Security default |

## 10. When to choose Actions

| Pros | Cons |
|------|------|
| Native on GitHub | Tied to GitHub (or mirror) |
| Huge **Marketplace** | Complex org billing at scale |
| Free minutes for public repos | Self-hosted runners need ops |

**Related:** [Docker in CI](v-docker-in-ci.md), [Secrets & OIDC](../security-and-best-practices/iii-secrets-and-oidc.md).
