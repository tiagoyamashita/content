---
label: "III"
subtitle: "Secrets & OIDC"
group: "CI/CD"
order: 3
---
Secrets & OIDC
**Secrets** in CI must never live in source control. **OIDC** (OpenID Connect) lets pipelines exchange a short-lived identity token for cloud credentials — no long-lived API keys.

## 1. Secret storage by platform

| Platform | Store | Scope |
|----------|-------|-------|
| GitHub Actions | Settings → Secrets | org / repo / environment |
| GitLab CI | Settings → CI/CD → Variables | project / group |
| Jenkins | Credentials plugin | global / folder / job |

Rules:

- **Mask** secrets in logs (platform default).
- **Narrow scope** — prod secrets only on `environment: production` jobs.
- **Rotate** on schedule and after any leak suspicion.
- **Never** echo secrets in `run:` scripts.

```yaml
# GitHub — reference secret
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

```yaml
# GitLab — masked variable
deploy:
  script: deploy.sh
  variables:
    DEPLOY_TOKEN: $DEPLOY_TOKEN   # set in UI, masked + protected
```

## 2. Fork PR safety

| Platform | Default for fork PRs |
|----------|----------------------|
| GitHub Actions | No access to repo secrets |
| GitLab | Protected variables hidden on MR from forks |

Malicious PRs can exfiltrate secrets if workflows run with elevated access. Use **`pull_request`** (not `pull_request_target`) for untrusted code unless you understand the risk.

## 3. OIDC — why it beats static keys

| Static AWS key | OIDC |
|----------------|------|
| Lives months/years | Minutes TTL |
| Stored as secret | No secret — trust relationship |
| Same key every run | Scoped per workflow/repo/branch |
| Hard to audit | Cloud audit log shows subject |

## 4. GitHub Actions → AWS

**AWS IAM** — trust GitHub OIDC provider; role with least privilege.

```yaml
permissions:
  id-token: write   # required for OIDC
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-deploy
          aws-region: us-east-1

      - run: aws ecs update-service --cluster prod --service api --force-new-deployment
```

IAM trust policy (simplified):

```json
{
  "Effect": "Allow",
  "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
  "Action": "sts:AssumeRoleWithWebIdentity",
  "Condition": {
    "StringEquals": {
      "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
    },
    "StringLike": {
      "token.actions.githubusercontent.com:sub": "repo:myorg/myapp:ref:refs/heads/main"
    }
  }
}
```

Restrict **`sub`** to specific repo and branch.

## 5. GitHub Actions → GCP / Azure

**GCP** — Workload Identity Federation:

```yaml
- uses: google-github-actions/auth@v2
  with:
    workload_identity_provider: projects/123/locations/global/workloadIdentityPools/pool/providers/github
    service_account: deploy@myproject.iam.gserviceaccount.com
```

**Azure** — federated credential on app registration:

```yaml
- uses: azure/login@v2
  with:
    client-id: ${{ secrets.AZURE_CLIENT_ID }}
    tenant-id: ${{ secrets.AZURE_TENANT_ID }}
    subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
```

Only the **client/tenant/subscription IDs** are stored — no client secret when using federation.

## 6. GitLab CI OIDC example

```yaml
deploy:
  id_tokens:
    AWS_TOKEN:
      aud: https://gitlab.com
  script:
    - >
      export $(printf "AWS_ACCESS_KEY_ID=%s AWS_SECRET_ACCESS_KEY=%s AWS_SESSION_TOKEN=%s"
      $(aws sts assume-role-with-web-identity
      --role-arn arn:aws:iam::123456789012:role/gitlab-deploy
      --role-session-name gitlab
      --web-identity-token $AWS_TOKEN
      --query 'Credentials.[AccessKeyId,SecretAccessKey,SessionToken]'
      --output text))
    - aws s3 sync ./dist s3://my-bucket/
```

## 7. Jenkins credentials

```groovy
pipeline {
  environment {
    DEPLOY_KEY = credentials('deploy-ssh-key')
  }
  stages {
    stage('Deploy') {
      steps {
        sh 'ansible-playbook deploy.yml'
      }
    }
  }
}
```

Prefer **HashiCorp Vault** or cloud OIDC plugins over long-lived Jenkins-stored keys for new setups.

## 8. Rotation checklist

| Step | Action |
|------|--------|
| 1 | Identify secret age and scope |
| 2 | Create new credential in cloud |
| 3 | Update CI secret / IAM role |
| 4 | Run smoke deploy |
| 5 | Revoke old credential |
| 6 | Document in runbook |

## 9. Anti-patterns

| Anti-pattern | Risk |
|--------------|------|
| `AWS_ACCESS_KEY_ID` in repo | Permanent blast radius |
| Same prod secret in dev CI | Lateral movement |
| Logging `env` in debug step | Secret in log archive |
| OIDC role trusts `*` repos | Any repo can assume |

**Related:** **Terraform** submenu → [Terraform in CI/CD](../terraform/vii-terraform-in-cicd.md) (OIDC in plan/apply), [Least-privilege runners](iv-least-privilege-runners.md).
