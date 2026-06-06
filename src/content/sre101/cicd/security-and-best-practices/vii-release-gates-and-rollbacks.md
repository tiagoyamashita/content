---
label: "VII"
subtitle: "Release gates & rollbacks"
group: "CI/CD"
order: 7
---
Release gates & rollbacks
Shipping safely means **gating** who can deploy what, using **immutable artifacts**, and having a **tested rollback** before you need it.

## 1. Branch protection

| Rule | Purpose |
|------|---------|
| Require PR before merge | Review + CI on branch |
| Require status checks | Unit/integration must pass |
| Require signed commits | Verify author identity |
| Restrict who can push to `main` | No direct commits |

GitHub: **Settings → Branches → Branch protection rules**.

GitLab: **Protected branches** + **Merge request approvals** (e.g. 2 approvers for `main`).

## 2. Environment protection

```yaml
# GitHub — production gate
jobs:
  deploy-prod:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - run: ./deploy.sh ${{ github.sha }}
```

Configure **required reviewers** and **wait timer** in environment settings. Same pattern on GitLab `environment: production` with **protected environments**.

## 3. Immutable deploy artifacts

Deploy by **digest** or **semver tag** — never `latest` in prod.

| Bad | Good |
|-----|------|
| `myapp:latest` | `myapp:1.4.2` or `@sha256:abc...` |
| Rebuild on server | Pull pre-built image from CI |
| Floating branch deploy | Tag `v1.4.2` on commit SHA |

```yaml
- name: Deploy
  run: |
    kubectl set image deploy/api api=registry.example.com/myapp:${{ github.sha }}
    kubectl rollout status deploy/api --timeout=5m
```

CI built and scanned that exact image in an earlier stage [Docker in CI](../tools-and-platforms/v-docker-in-ci.md).

## 4. Progressive delivery

| Strategy | Behavior | Rollback |
|----------|----------|----------|
| **Rolling** | Replace pods in batches | `kubectl rollout undo` |
| **Blue/green** | Switch traffic to new stack | Switch back |
| **Canary** | 5% → 25% → 100% traffic | Route traffic to old version |

```yaml
# Flagger canary (Kubernetes)
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: api
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  progressDeadlineSeconds: 60
  service:
    port: 8080
  analysis:
    interval: 1m
    threshold: 5
    maxWeight: 50
    stepWeight: 10
    metrics:
      - name: request-success-rate
        threshold: 99
```

Automated promotion when metrics pass; automatic rollback when they fail.

## 5. Manual approval in CI

**GitHub Actions:**

```yaml
jobs:
  hold:
    runs-on: ubuntu-latest
    environment: production   # triggers approval
    steps:
      - run: echo "Approved for deploy"

  deploy:
    needs: hold
    runs-on: ubuntu-latest
    steps:
      - run: ./deploy-prod.sh
```

**GitLab:**

```yaml
deploy_prod:
  stage: deploy
  when: manual
  environment: production
  script: ./deploy.sh
```

**Jenkins** — `input` step:

```groovy
stage('Approve') {
  when { branch 'main' }
  steps {
    input message: 'Deploy to production?', ok: 'Deploy'
  }
}
```

## 6. Rollback playbook

| Step | Action |
|------|--------|
| 1 | Stop forward deploy / canary |
| 2 | Identify last known good **image tag** or **git SHA** |
| 3 | Redeploy previous version (`rollout undo` or redeploy job) |
| 4 | Verify health checks and key SLOs |
| 5 | Post-incident: fix forward, add test |

```bash
# Kubernetes — one command rollback
kubectl rollout undo deployment/api
kubectl rollout status deployment/api
```

Keep rollback **tested quarterly** — untested rollbacks fail under pressure.

## 7. Feature flags vs hot deploy

| Approach | Use when |
|----------|----------|
| **Feature flag** | Hide incomplete logic; toggle without redeploy |
| **Hotfix branch** | Critical bug; skip normal train |
| **Rollback** | Bad binary/config in prod |

Flags decouple **deploy** (safe, frequent) from **release** (business decision).

## 8. Deployment anti-patterns

| Anti-pattern | Risk |
|--------------|------|
| Deploy Friday 5pm | No one to rollback |
| No health check after deploy | Silent partial failure |
| Shared prod/staging credentials | Staging breach → prod |
| Database migration without backward compatibility | Rollback breaks schema |

**Expand-contract migrations:** add column → dual-write → backfill → remove old — allows rollback of app without breaking DB.

## 9. Checklist before first prod deploy

- [ ] Branch protection + required CI checks
- [ ] Production environment requires approval
- [ ] Deploy uses immutable tag/digest
- [ ] Health check / smoke test post-deploy
- [ ] Rollback command documented and rehearsed
- [ ] On-call notified on deploy failure

**Related:** [Testing strategy](v-testing-strategy.md), [Supply chain & SLSA](ii-supply-chain-and-slsa.md) (signed images), [Secrets & OIDC](iii-secrets-and-oidc.md).
