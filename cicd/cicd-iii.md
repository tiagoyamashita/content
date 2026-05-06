---
label: "III"
subtitle: "Security & Best Practices"
group: "CI/CD"
order: 3
---
CI/CD — Part III: Security & Best Practices
Supply chain, SLSA, testing, observability.

## 1. Supply chain security
Dependency confusion, typosquatting, and compromised dependencies are real risks.

SLSA (Supply-chain Levels for Software Artifacts):
- L1: scripted build — build logged.
- L2: build service — signed provenance.
- L3: hardened build — isolated, reproducible.
- L4: two-party review + hermetic build (highest assurance).

Practical steps:
- Pin action versions to a commit SHA, not a tag.
- Use Dependabot / Renovate to auto-update dependencies.
- Run SBOM generation (Syft, Trivy) and upload as attestation.
- Sign images with Cosign (sigstore) — verify before deploy.

## 2. Least-privilege runners
Runner permissions should be narrowed to only what a job needs.

GitHub Actions:
- permissions: block at workflow or job level.

```yaml
permissions:
  contents: read
  id-token: write
```

- GITHUB_TOKEN is scoped per job automatically.

Self-hosted runners:
- Ephemeral runners (new VM per job) prevent workspace pollution.
- Network-segment runners away from production databases.
- Never run untrusted PRs on self-hosted runners.

## 3. Testing strategy
Shift left: test as early and as cheaply as possible.

Test pyramid (fast → slow, cheap → expensive):
- Unit tests     — isolated, milliseconds, run on every commit.
- Integration    — real DB/queue, seconds to minutes.
- E2E / smoke    — full stack, minutes, run on staging.
- Chaos / load   — periodic (nightly), not per-commit.

In CI:
- Gate merges on unit + integration; block on fail.
- Parallelize test shards (pytest-xdist, Jest --shard).
- Publish test reports (JUnit XML) → PR annotations.
- Flaky test quarantine: track, fix, do not ignore.

## 4. Observability in pipelines
A pipeline is itself a distributed system — apply the same principles.

Metrics to track:
- Lead time: commit → production.
- Deployment frequency: how often you ship.
- Change failure rate: % of deploys that cause incidents.
- MTTR: mean time to restore after a failure.
(These are the DORA four key metrics.)

Tooling:
- OpenTelemetry traces for pipeline steps (Honeycomb, Tempo).
- Slack / PagerDuty alerts on pipeline failures in main.
- Dashboard: pipeline duration trend, flaky test count, cache hit rate.

## 5. Remember & rehearse
- What is SLSA and why does it matter?
- How does pinning an action to a SHA protect you?
- Draw the test pyramid and map it to pipeline stages.
- Name the four DORA metrics and what each measures.
