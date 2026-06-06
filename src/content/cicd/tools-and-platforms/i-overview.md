---
label: "I"
subtitle: "Overview"
group: "CI/CD"
order: 1
---
Tools & platforms — overview
**CI/CD platforms** run your pipeline on **runners** (agents): checkout code, build, test, scan, deploy. Pick based on **where code lives**, **hosting**, and **team skills**.

## Map of this submenu

| Note | Platform | Config file |
|------|----------|-------------|
| `ii-github-actions.md` | GitHub Actions | `.github/workflows/*.yml` |
| `iii-gitlab-ci.md` | GitLab CI/CD | `.gitlab-ci.yml` |
| `iv-jenkins.md` | Jenkins | `Jenkinsfile` |
| `v-docker-in-ci.md` | Docker (all platforms) | `Dockerfile`, build args |
| `vi-circleci.md` | CircleCI | `.circleci/config.yml` |
| `vii-tekton.md` | Tekton (Kubernetes) | `Pipeline`, `Task` CRDs |
| `viii-choosing-a-platform.md` | Decision guide | — |

**Related:** Part I fundamentals, **Security & best practices** submenu, **Ansible & Jenkins** submenu, **Terraform** submenu.

## Typical pipeline on any platform

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 100" role="img" aria-label="CI pipeline stages checkout build test publish deploy">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Same stages, different YAML syntax</text>
  <rect x="12" y="36" width="56" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="20" y="54" fill="#e4e4e7" font-size="8">checkout</text>
  <path d="M68 50 H88" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="88" y="36" width="48" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="96" y="54" fill="#e4e4e7" font-size="8">build</text>
  <path d="M136 50 H156" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="156" y="36" width="48" height="28" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="164" y="54" fill="#e4e4e7" font-size="8">test</text>
  <path d="M204 50 H224" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="224" y="36" width="56" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="232" y="54" fill="#e4e4e7" font-size="8">publish</text>
  <path d="M280 50 H300" stroke="#a1a1aa" stroke-width="1"/>
  <rect x="300" y="36" width="56" height="28" rx="3" fill="rgba(248,113,113,0.12)" stroke="#f87171"/>
  <text x="308" y="54" fill="#e4e4e7" font-size="8">deploy</text>
</svg></figure>

## Rehearsal

- Minimal GitHub Actions: checkout → install → test?
- GitLab `needs:` vs stages?
- Why multi-stage Docker in CI?
