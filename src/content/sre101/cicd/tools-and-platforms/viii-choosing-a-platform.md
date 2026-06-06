---
label: "VIII"
subtitle: "Choosing a platform"
group: "CI/CD"
order: 8
---
Choosing a CI/CD platform
No single “best” tool — match **hosting**, **compliance**, **team skills**, and **budget**.

## 1. Decision checklist

| # | Question | Lean toward |
|---|----------|-------------|
| 1 | Where is Git hosted? | GitHub → Actions; GitLab → GitLab CI |
| 2 | Cloud or **on-prem** runners only? | Jenkins, self-hosted GitLab/GitHub runners |
| 3 | Budget for **managed minutes**? | Self-host or flat SaaS plan |
| 4 | Need integrated registry, security, pages? | GitLab |
| 5 | Already on **Kubernetes** for everything? | Tekton |
| 6 | Maximum plugins / legacy Groovy? | Jenkins |
| 7 | Fast cache, minimal ops? | CircleCI, GitHub Actions |

## 2. Comparison table

| Platform | Hosting | Config | Runners | Best for |
|----------|---------|--------|---------|----------|
| **GitHub Actions** | GitHub | `.github/workflows/` | GitHub + self-hosted | OSS & GitHub-centric teams |
| **GitLab CI** | GitLab | `.gitlab-ci.yml` | Shared + self-hosted | Self-managed DevOps platform |
| **Jenkins** | Self | `Jenkinsfile` | Your agents | On-prem, air-gap, plugins |
| **CircleCI** | SaaS | `.circleci/config.yml` | Cloud | Cache-heavy polyrepos |
| **Tekton** | K8s | CRDs | Pod per step | Platform eng on Kubernetes |

## 3. Scenario examples

### Startup on GitHub, deploy to AWS

```text
GitHub Actions → OIDC to AWS → ECR push → ECS/EKS deploy
```

Minimal ops; use Marketplace actions; secrets in GitHub Environments.

### Enterprise on-prem GitLab

```text
GitLab CI → internal registry → Ansible/K8s deploy to private DC
```

Single vendor; runners on your VMs; compliance data stays inside.

### Bank air-gapped

```text
Jenkins controller + agents → Artifactory → manual promote to prod
```

No SaaS; plugins for mainframe, legacy SCM; change windows with approval steps.

### Internal developer platform team

```text
Tekton Pipelines + Triggers → Kaniko → Helm to shared K8s
```

Golden paths as Templates; devs trigger via service catalog.

## 4. Migration path

| From | To | Tip |
|------|-----|-----|
| Jenkins freestyle | Declarative Jenkinsfile | One repo at a time |
| Jenkins | GitHub Actions | Map stages → jobs; replace plugins with actions |
| CircleCI | GitLab | Orbs → `include` templates |
| Ad-hoc shell | Any CI | Extract `scripts/ci.sh`; call from YAML |

Run **parallel** pipelines during migration; compare artifacts and test results.

## 5. Anti-patterns

| Anti-pattern | Why |
|--------------|-----|
| CI without cache | Slow feedback → devs skip CI |
| `latest` only deploy tag | Can't roll back |
| Secrets in repo | Rotate and incident |
| One giant Jenkins job | No parallelisation, brittle |
| Different CI locally vs cloud | Use same Dockerfile / compose |

## 6. Rehearsal answers

- **GitHub Actions minimal workflow:** checkout → setup runtime → install deps → test [GitHub Actions](ii-github-actions.md).
- **GitLab `needs:`:** DAG edges — job starts when dependencies finish, not entire previous stage.
- **Jenkins over SaaS:** on-prem control, air-gap, plugin legacy, existing controller investment.
- **Multi-stage Docker:** builder stage discarded — runtime image only has JAR/binary [Docker in CI](v-docker-in-ci.md).

**Related:** Part I fundamentals, **Security & best practices** submenu, tools overview [Overview](i-overview.md).
