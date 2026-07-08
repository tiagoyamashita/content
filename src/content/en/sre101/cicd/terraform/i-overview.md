---
label: "I"
subtitle: "Overview"
group: "CI/CD"
order: 1
---
Terraform — overview
**Terraform** (HashiCorp, IBM 2024) is **Infrastructure as Code (IaC)**: describe cloud resources in **HCL**, version in Git, apply consistently across environments. It is **cloud-agnostic** — not an AWS product (AWS native IaC is **CloudFormation**).

## Map of this submenu

| Note | Focus |
|------|--------|
| [What is Terraform](ii-what-is-terraform.md) | Problem IaC solves, vs CloudFormation, workflow |
| [HCL, resources & variables](iii-hcl-resources-and-variables.md) | HCL syntax, variables, outputs, data sources |
| [AWS example — VPC & EC2](iv-aws-example-vpc-and-ec2.md) | VPC, subnet, EC2 — full working example |
| [State & remote backends](v-state-and-remote-backends.md) | tfstate, S3 backend, locking, state CLI |
| [Modules & environments](vi-modules-and-environments.md) | Modules, registry, workspaces, env split |
| [Terraform in CI/CD](vii-terraform-in-cicd.md) | Plan on PR, apply on main, OIDC, Atlantis |

**Related:** Part I fundamentals, **Security & best practices** → [Secrets & OIDC](../security-and-best-practices/iii-secrets-and-oidc.md), **Tools & platforms** → GitHub Actions.

## Core workflow

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" role="img" aria-label="Terraform init plan apply destroy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Plan before apply — always</text>
  <rect x="12" y="40" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="20" y="60" fill="#e4e4e7" font-size="8">init</text>
  <path d="M68 56 H88" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="88" y="40" width="56" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="96" y="60" fill="#e4e4e7" font-size="8">plan</text>
  <path d="M144 56 H164" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="164" y="40" width="56" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="172" y="60" fill="#e4e4e7" font-size="8">apply</text>
  <path d="M220 56 H240" stroke="#a1a1aa" stroke-width="1.5" stroke-dasharray="4 2"/>
  <rect x="240" y="40" width="64" height="32" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="248" y="60" fill="#e4e4e7" font-size="8">destroy</text>
  <text x="320" y="56" fill="#71717a" font-size="9">teardown only</text>
</svg></figure>

## Key properties

| Property | Meaning |
|----------|---------|
| **Declarative** | You specify desired state; Terraform computes diff |
| **Idempotent** | Re-apply same config → no extra changes |
| **Plan-first** | Preview creates/updates/deletes before touching APIs |
| **Provider-based** | AWS, Azure, GCP, K8s, GitHub, Datadog — 3000+ providers |

## When to use Terraform

| Good fit | Consider alternatives |
|----------|------------------------|
| Multi-cloud or multi-service infra | AWS-only shop → CloudFormation/CDK |
| Team needs shared state + review | Small personal project → click-ops OK |
| GitOps-style infra changes | App config on VMs → Ansible (`ansible-and-jenkins/`) |

## Rehearsal

- Terraform vs CloudFormation — who makes each, lock-in?
- Why never commit `terraform.tfstate`?
- What does `terraform plan` show?
