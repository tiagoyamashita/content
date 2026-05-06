---
label: "II"
subtitle: "Tools & Platforms"
group: "CI/CD"
order: 2
---
CI/CD — Part II: Tools & Platforms
GitHub Actions, GitLab CI, Jenkins, Docker.

## 1. GitHub Actions
Workflow file: .github/workflows/*.yml
- Triggered by on: [push, pull_request, schedule, workflow_dispatch].
- Jobs run on github-hosted runners (ubuntu-latest, windows-latest, macos-latest)
or self-hosted runners.

Key concepts:
- Action: reusable step packaged as a Docker container or JS module.

```yaml
uses: actions/checkout@v4
uses: actions/setup-node@v4
```

- Matrix strategy: fan-out across multiple OS / version combos.

```yaml
strategy:
  matrix:
    node: [18, 20, 22]
```

- Reusable workflows: call one workflow from another (DRY).
- Environments + required reviewers gate production deploys.

## 2. GitLab CI
Config: .gitlab-ci.yml at repo root.
- Stages declared at the top; jobs assigned to a stage.
- Runners: shared (GitLab.com) or self-hosted via runner registration.

Unique features:
- include: — split pipeline config across files.
- extends: — YAML anchors for DRY job definitions.
- DAG (needs:) — skip stage ordering for faster pipelines.
- Environments with auto-stop after inactivity.
- Built-in container registry and package registry.

## 3. Jenkins
Self-hosted; highly customizable via plugins (1800+).

Pipeline types:
- Scripted (Groovy DSL) — full flexibility, steeper learning curve.
- Declarative — structured syntax, preferred for new pipelines.

Declarative skeleton:

```groovy
pipeline {
  agent any
  stages {
    stage('Build') { steps { sh 'make' } }
    stage('Test')  { steps { sh 'make test' } }
  }
}
```

Shared Libraries: package Groovy helpers in a separate repo.

## 4. Docker in CI
- Build image → push to registry → deploy from registry.
- Layer caching: pull previous image as cache-from to speed builds.
- Multi-stage builds: builder stage compiles → final stage copies only
the binary — tiny production image.

docker buildx bake — advanced: build multiple platforms in one command.
SBOM generation: attest supply-chain provenance in the image manifest.

## 5. Choosing a platform
GitHub Actions  — best for GitHub repos; huge marketplace; generous free tier.
GitLab CI       — best when self-hosting matters; integrated DevSecOps.
Jenkins         — maximum control; on-prem; large plugin ecosystem.
CircleCI        — fast caching; good DX; SaaS.
Tekton          — Kubernetes-native; composable; no GUI by default.

Decision checklist:
1. Where is the code hosted?
2. Cloud or on-prem runners needed?
3. Budget for managed runner minutes?
4. Team's existing tooling?

## 6. Remember & rehearse
- Write a minimal GitHub Actions workflow: checkout → install → test.
- What does needs: do in GitLab CI?
- When would you pick Jenkins over a SaaS CI tool?
- Explain multi-stage Docker builds and why they shrink image size.
