---
label: "I"
subtitle: "Overview"
group: "CI/CD"
order: 1
---
Security & best practices — overview
Secure CI/CD protects **source**, **build**, **artifacts**, and **deploy targets**. Treat the pipeline as part of your **attack surface** — not just app code.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Supply chain & SLSA](ii-supply-chain-and-slsa.md) | SLSA, SBOM, signing, dependency pinning |
| [Secrets & OIDC](iii-secrets-and-oidc.md) | Vaults, rotation, OIDC to cloud |
| [Least-privilege runners](iv-least-privilege-runners.md) | Token scope, self-hosted runners, fork PRs |
| [Testing strategy](v-testing-strategy.md) | Test pyramid, gates, sharding, flaky tests |
| [Pipeline observability & DORA](vi-pipeline-observability-and-dora.md) | DORA metrics, alerts, pipeline tracing |
| [Release gates & rollbacks](vii-release-gates-and-rollbacks.md) | Approvals, immutable deploys, rollback |

**Related:** Part I fundamentals, **Tools & platforms** submenu, **Terraform** submenu → [Terraform in CI/CD](../terraform/vii-terraform-in-cicd.md) (OIDC in apply jobs).

## Secure pipeline layers

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" role="img" aria-label="CI/CD security layers from source to deploy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Defense in depth across the pipeline</text>
  <rect x="12" y="36" width="88" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="20" y="54" fill="#e4e4e7" font-size="8">Source &amp; deps</text>
  <path d="M100 50 H120" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="120" y="36" width="88" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="128" y="54" fill="#e4e4e7" font-size="8">Build &amp; scan</text>
  <path d="M208 50 H228" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="228" y="36" width="88" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="236" y="54" fill="#e4e4e7" font-size="8">Secrets &amp; IAM</text>
  <path d="M316 50 H336" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="336" y="36" width="88" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="344" y="54" fill="#e4e4e7" font-size="8">Deploy gates</text>
  <text x="12" y="88" fill="#71717a" font-size="9">Pin actions · SBOM · least privilege · OIDC · signed images · prod approval</text>
</svg></figure>

## Quick checklist

| Layer | Do this |
|-------|---------|
| Dependencies | Lock files, Renovate/Dependabot, scan CVEs |
| Actions / plugins | Pin to **commit SHA**, not floating `@v4` tag |
| Credentials | OIDC or short-lived tokens; never keys in repo |
| Runners | Ephemeral VMs; no prod network from PR jobs |
| Artifacts | Sign images (Cosign); verify before deploy |
| Production | Environment protection, manual approval, rollback path |

## Rehearsal

- What is SLSA L2 vs L3?
- Why pin a GitHub Action to a SHA?
- Name the four DORA metrics.
- Why not run fork PRs on self-hosted runners with secrets?
