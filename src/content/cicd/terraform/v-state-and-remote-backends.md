---
label: "V"
subtitle: "State & remote backends"
group: "CI/CD"
order: 5
---
State & remote backends
**Terraform state** (`terraform.tfstate`) maps your HCL to real cloud resource IDs. Teams **must** use a **remote backend** with **locking** — never commit state to Git.

## 1. What state contains

```json
{
  "version": 4,
  "resources": [
    {
      "type": "aws_instance",
      "name": "app",
      "instances": [{
        "attributes": {
          "id": "i-0abc123def456",
          "public_ip": "54.123.45.67"
        }
      }]
    }
  ]
}
```

| Why state exists | Detail |
|------------------|--------|
| Map names → IDs | `aws_instance.app` → `i-0abc123` |
| Performance | Avoid re-querying every resource on each plan |
| Metadata | Dependencies, serial, lineage |

State may contain **sensitive values** (passwords, keys) — treat as secret.

## 2. Never commit state to Git

| Risk | Consequence |
|------|-------------|
| Secrets in JSON | Leak via repo history |
| Divergent local states | Two engineers apply conflicting changes |
| No locking | Concurrent applies corrupt resources |

Add to `.gitignore`:

```gitignore
.terraform/
*.tfstate
*.tfstate.*
.terraform.lock.hcl   # commit lock file — pins provider checksums
```

**Do commit** `.terraform.lock.hcl` for reproducible provider versions.

## 3. S3 remote backend (AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "myapp/prod/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}
```

| Component | Role |
|-----------|------|
| **S3 bucket** | Stores state file |
| **DynamoDB table** | Lock ID — one apply at a time |
| **encrypt** | SSE at rest |

Create backend resources once (bootstrap stack or separate admin process), then reference from all env configs.

## 4. Other backends

| Backend | Common for |
|---------|------------|
| **Terraform Cloud / HCP** | HashiCorp-hosted state + runs |
| **azurerm** | Azure Blob + lease |
| **gcs** | Google Cloud Storage |
| **local** | Solo dev only |

## 5. State locking

```text
Engineer A: terraform apply  → acquires lock
Engineer B: terraform apply  → Error: lock already held
Engineer A: apply completes  → releases lock
Engineer B: retry            → succeeds
```

Without locking, two applies can interleave API calls and leave infra inconsistent.

## 6. State CLI commands

```bash
terraform state list
terraform state show aws_instance.app
terraform state mv aws_instance.old aws_instance.new
terraform state rm aws_instance.orphan   # remove from state, not cloud
terraform import aws_instance.app i-0abc123
```

| Command | Use |
|---------|-----|
| **import** | Bring existing cloud resource under Terraform |
| **mv** | Rename resource in config without destroy/create |
| **rm** | Stop managing resource (manual cleanup) |

## 7. State per environment

```text
S3 key paths:
  myapp/dev/terraform.tfstate
  myapp/staging/terraform.tfstate
  myapp/prod/terraform.tfstate
```

Separate keys (or separate buckets) isolate blast radius. **Never** share one state file across dev and prod.

## 8. Drift detection

**Drift** — someone changed cloud console outside Terraform.

```bash
terraform plan   # shows ~ update or unexpected -/+ replace
```

CI: run `terraform plan` on schedule; alert if non-empty plan. Optional: **terraform plan -detailed-exitcode` — exit 2 if changes pending.

## 9. Sensitive outputs

```hcl
output "db_password" {
  value     = aws_db_instance.main.password
  sensitive = true
}
```

Still stored in state — remote backend encryption and IAM on bucket are required.

**Related:** `vii-terraform-in-cicd.md`, `../security-and-best-practices/iii-secrets-and-oidc.md`.
