---
label: "II"
subtitle: "CLI workflow"
group: "SRE"
order: 2
---
SRE tooling — Terraform: CLI workflow
Daily commands from **`init`** through **`apply`**, plus variables and refreshes.

## 1. Standard lifecycle

```text
terraform init          # providers + backends + modules
terraform validate      # config correctness (no API calls)
terraform fmt -recursive
terraform plan -out=plan.tfplan
terraform apply plan.tfplan
```

**`plan`** without **`apply`** is what gates merges—capture textual/HTML plans in CI artifacts.

## 2. Workspaces & environments

- **CLI workspaces** (`terraform workspace select prod`) split **state** namespaces inside one backend configuration—simple but easy to misuse; many teams prefer separate directories (`env/prod`) + distinct **`backend.key`** or entirely separate state buckets.
- Pass environment specifics via **`-var-file=prod.tfvars`** and CI secrets.

## 3. Variables & secrets

```hcl
variable "db_password" {
  type      = string
  sensitive = true
}
```

Avoid committing **`.tfvars`** with secrets—use env vars **`TF_VAR_db_password`**, Vault, or CI secret stores.

## 4. Imports & targeted ops

- **`terraform import aws_instance.app i-0abc123`** attaches existing infra—still requires matching resource blocks.
- **`-target`** for surgical fixes—escape hatch only; dependency skew risks hiding problems.

## 5. Refresh & drift

- Default plans refresh remote objects—detect manual console edits as drift.
- **`terraform refresh`** / deprecated standalone refresh semantics folded into plan—understand that ignoring drift breeds Terraform/state divergence.

## 6. Destroy & replaces

- **`terraform destroy`** removes managed objects—protect prod with approvals + scoped workspaces/modules.
- **`lifecycle { prevent_destroy = true }`** guards critical datasets—combine with backups anyway.

Next: **Modules / backends / state**, then **CI & practices**.
