---
label: "VII"
subtitle: "Terraform in CI/CD"
group: "CI/CD"
order: 7
---
Terraform in CI/CD
Standard pattern: **PR → plan (review) → merge → apply**. Never **`apply`** on untrusted PR branches; use **OIDC** for cloud credentials.

## 1. Pipeline flow

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 100" role="img" aria-label="Terraform PR plan merge apply">
  <rect x="12" y="40" width="64" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="24" y="60" fill="#e4e4e7" font-size="8">PR opened</text>
  <path d="M76 56 H96" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="96" y="40" width="64" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="108" y="60" fill="#e4e4e7" font-size="8">plan</text>
  <path d="M160 56 H180" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="180" y="40" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="192" y="60" fill="#e4e4e7" font-size="8">review</text>
  <path d="M244 56 H264" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="264" y="40" width="64" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="276" y="60" fill="#e4e4e7" font-size="8">apply</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Apply only on main after merge</text>
  <text x="12" y="88" fill="#71717a" font-size="9">Post plan output as PR comment for human review</text>
</svg></figure>

## 2. GitHub Actions — full workflow

```yaml
name: Terraform

on:
  push:
    branches: [main]
    paths: ['infra/**']
  pull_request:
    paths: ['infra/**']

permissions:
  contents: read
  pull-requests: write
  id-token: write

env:
  TF_WORKING_DIR: infra/environments/staging
  AWS_REGION: us-east-1

jobs:
  terraform:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: ${{ env.TF_WORKING_DIR }}

    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-terraform
          aws-region: ${{ env.AWS_REGION }}

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: 1.7.5

      - name: Terraform Format
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init -input=false

      - name: Terraform Validate
        run: terraform validate

      - name: Terraform Plan
        id: plan
        run: terraform plan -input=false -no-color -out=tfplan
        continue-on-error: true

      - name: Comment plan on PR
        uses: actions/github-script@v7
        if: github.event_name == 'pull_request'
        env:
          PLAN: ${{ steps.plan.outputs.stdout }}
        with:
          script: |
            const output = `#### Terraform Plan 📖
            \`\`\`
            ${process.env.PLAN || 'Plan failed — see logs'}
            \`\`\``;
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: output
            });

      - name: Terraform Plan Status
        if: steps.plan.outcome == 'failure'
        run: exit 1

      - name: Terraform Apply
        if: github.ref == 'refs/heads/main' && github.event_name == 'push'
        run: terraform apply -input=false -auto-approve tfplan
```

| Rule | Why |
|------|-----|
| `plan` on PR | Review infra diff like code |
| `apply` only on `main` | No rogue PR applying to cloud |
| `-out=tfplan` | Apply exact planned changes |
| OIDC role | No static AWS keys (`../security-and-best-practices/iii-secrets-and-oidc.md`) |

## 3. GitLab CI example

```yaml
stages: [validate, plan, apply]

variables:
  TF_ROOT: infra/environments/staging

.terraform:
  image:
    name: hashicorp/terraform:1.7
    entrypoint: [""]
  before_script:
    - cd $TF_ROOT
    - terraform init -input=false

fmt:
  extends: .terraform
  stage: validate
  script:
    - terraform fmt -check -recursive

plan:
  extends: .terraform
  stage: plan
  script:
    - terraform plan -input=false -out=tfplan
  artifacts:
    paths:
      - $TF_ROOT/tfplan
    expire_in: 1 week

apply:
  extends: .terraform
  stage: apply
  script:
    - terraform apply -input=false tfplan
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
  when: manual
  environment:
    name: staging
```

## 4. Atlantis

**Atlantis** — self-hosted bot; comments on PR trigger plan/apply:

```text
# PR comment
atlantis plan

# After review
atlantis apply
```

`atlantis.yaml`:

```yaml
version: 3
projects:
  - name: staging
    dir: infra/environments/staging
    workflow: default
    autoplan:
      when_modified: ["**/*.tf", "**/*.tfvars"]
```

| | GitHub Actions | Atlantis |
|---|----------------|----------|
| Hosting | GitHub runners | Your server |
| UX | Workflow YAML | PR comments |
| Multi-project | Matrix jobs | Built-in project dirs |

## 5. Policy and security scanning

```yaml
- name: tfsec
  uses: aquasecurity/tfsec-action@v1.0.0
  with:
    working_directory: infra/

- name: Checkov
  run: checkov -d infra/ --framework terraform
```

Gate PR on **HIGH** misconfigs (open SG, unencrypted S3). Complements `../security-and-best-practices/ii-supply-chain-and-slsa.md`.

## 6. Plan exit codes for automation

```bash
terraform plan -detailed-exitcode -out=tfplan
# 0 = no changes
# 1 = error
# 2 = changes pending
```

Use exit code 2 to trigger apply job only when needed.

## 7. Production safeguards

| Control | Implementation |
|---------|----------------|
| Manual approval | GitHub Environment, GitLab `when: manual` |
| Separate IAM role | `github-terraform-prod` stricter than staging |
| Separate state key | `myapp/prod/terraform.tfstate` |
| Drift detection | Scheduled `terraform plan` + alert |

## 8. Anti-patterns

| Anti-pattern | Risk |
|--------------|------|
| `apply` on every PR | Attacker PR destroys infra |
| Local state in CI | Lost between runs |
| Admin IAM for CI role | Blast radius |
| No plan in PR | Surprises at merge |

## 9. Rehearsal answers

- **`terraform plan`** — preview create/update/delete vs state.
- **Remote backend** — shared state + locking for teams.
- **`module` source** — registry URL, git URL, or local path.
- **Terraform vs CloudFormation** — HashiCorp multi-cloud vs AWS-native.

**Related:** `v-state-and-remote-backends.md`, `../tools-and-platforms/ii-github-actions.md`.
