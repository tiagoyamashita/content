---
label: "I"
subtitle: "Fundamentals"
group: "CI/CD"
order: 1
---
CI/CD — Part I: Fundamentals
Continuous Integration, Delivery, and Deployment.

## 1. What is CI/CD
- CI (Continuous Integration): automatically build & test every commit.
- CD (Continuous Delivery): keep the build always releasable to staging.
- CD (Continuous Deployment): auto-deploy every green build to production.
- Goal: shrink the feedback loop — catch bugs when they are still cheap to fix.
- Key insight: integration pain scales with time between merges.

## 2. Pipeline anatomy
A pipeline is a directed graph of stages → jobs → steps.

- Stage: logical group (build, test, deploy).
- Job: unit of work that runs on one runner/agent.
- Step: individual command or action inside a job.

Typical linear pipeline:

```
┌───────┐   ┌──────┐   ┌──────────┐   ┌────────┐
│ build │ → │ test │ → │ security │ → │ deploy │
└───────┘   └──────┘   └──────────┘   └────────┘
```


- Stages can run jobs in parallel (fan-out) and rejoin (fan-in).
- A failing job stops the stage; downstream stages are skipped.

## 3. Triggers & branches
What kicks off a pipeline run:
- Push to a branch (feature/*, main).
- Pull / merge request opened or updated.
- Schedule (cron — nightly test suites, dependency audits).
- Manual dispatch (release buttons).
- Webhook from another system (e.g., container registry push).

Branch strategies:
- Trunk-based: everyone merges to main frequently; feature flags hide WIP.
- Gitflow: long-lived develop + release branches; heavier merge overhead.
- GitHub flow: main is always deployable; PRs from short-lived branches.

## 4. Artifacts & caching
Artifact: file output that survives the job (JAR, Docker image, test report).

- Upload from one job → download in a later job.
- Retention policy: keep artifacts for N days or N runs.

Cache: re-use expensive inputs across runs (node_modules, .m2, pip).
- Keyed by a hash (lock-file hash) → miss = fresh install, hit = fast restore.
- Never cache build outputs (use artifacts for that).
- Cache + artifact together: restore cache → build → upload artifact.

## 5. Environments & secrets
Environment: named deployment target with its own protection rules.
- dev / staging / production — each can require a reviewer approval gate.

Secrets: sensitive values injected at runtime, never stored in code.
- Stored in the CI platform's secret vault (GitHub Secrets, etc.).
- Masked in logs — treated as opaque strings.
- Scope: org → repo → environment (narrowest scope wins).

Best practices:
- Rotate secrets on a schedule.
- Use OIDC (OpenID Connect) to get short-lived cloud credentials instead of
long-lived API keys — no secret to leak.

## 6. Remember & rehearse
- Sketch a three-stage pipeline (build → test → deploy) with a fan-out test job.
- Explain the difference between Continuous Delivery and Continuous Deployment.
- Name two trigger types and when you would use each.
- Why is OIDC preferred over static API keys in CI?
