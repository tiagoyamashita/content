---
label: "IV"
subtitle: "Least-privilege runners"
group: "CI/CD"
order: 4
---
Least-privilege runners
**Runners** execute pipeline steps with whatever credentials and network access you grant. Default to **minimum permissions** per job — not org-wide admin tokens.

## 1. Principle

| Resource | Least privilege means |
|----------|------------------------|
| **GitHub `GITHUB_TOKEN`** | `contents: read` unless job pushes |
| **Cloud IAM role** | S3 bucket prefix, not `s3:*` |
| **K8s service account** | One namespace, one deploy role |
| **Network** | Build runners cannot reach prod DB |

## 2. GitHub Actions permissions

Set at **workflow** or **job** level:

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

## 3. GitLab job tokens

GitLab **CI_JOB_TOKEN** is scoped to the project and allowed downstream projects you configure.

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

## 4. Self-hosted runners

| Risk | Mitigation |
|------|------------|
| Workspace pollution between jobs | **Ephemeral** runner (new VM/container per job) |
| Malicious PR code runs on your network | Do **not** run fork PRs on self-hosted with secrets |
| Runner compromise = long-lived access | Separate runner pools per trust zone |
| Docker socket access | Equivalent to root — isolate DinD |

**GitHub** — use runner groups and labels:

```yaml
jobs:
  internal-test:
    runs-on: [self-hosted, linux, internal]   # no prod access

  prod-deploy:
    runs-on: [self-hosted, linux, deploy-pool]  # prod network only
    environment: production
```

**Ephemeral pattern:** GitHub Actions scale-set, GitLab Runner with `docker+machine`, or K8s executor that deletes pod after job.

## 5. Fork and untrusted code

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

## 6. Jenkins agent isolation

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

Store production credentials in **folder-scoped** credentials, not global.

## 7. Network segmentation diagram

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

## 8. Checklist

- [ ] Workflow `permissions` explicitly set (not default write-all)
- [ ] Prod jobs use `environment` protection
- [ ] Self-hosted runners ephemeral or cleaned between jobs
- [ ] Fork PRs on isolated runners without secrets
- [ ] Deploy agents cannot compile arbitrary PR code

**Related:** [Secrets & OIDC](iii-secrets-and-oidc.md), [Jenkins](../tools-and-platforms/iv-jenkins.md).
