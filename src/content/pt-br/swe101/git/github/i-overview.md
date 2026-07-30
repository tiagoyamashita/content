---
label: "I"
subtitle: "Overview"
group: "GitHub"
order: 1
---
GitHub — overview
**GitHub** hosts Git repositories and adds **pull requests**, **reviews**, **Actions**, **Issues**, and **project** tooling. Git itself runs locally — GitHub is the social and automation layer.

## Map of this topic

| Note | Focus |
|------|--------|
| **Git → Essentials** | Local Git commands, branches, remotes, **`~/.ssh/config`** |
| [Repositories & pull requests](ii-repositories-and-pull-requests.md) | Repos, forks, PRs, reviews |
| [Actions, issues & settings](iii-actions-issues-and-settings.md) | CI, issues, branch protection, tokens |
| [SSH keys](iv-ssh-keys.md) | Add keys on GitHub, test `ssh -T`, deploy keys, SSO |
| [Contribution graph](activity-contribution-graph.md) | This site's contribution grid demo |

## Git + GitHub flow

```text
local:  branch → commit → push
GitHub: Pull Request → review → merge → Actions CI
```

## Account essentials

| Task | Where |
|------|--------|
| SSH keys | [SSH keys](iv-ssh-keys.md) · Settings → SSH and GPG keys |
| Personal access token | Settings → Developer settings (prefer fine-grained) |
| Email for commits | Settings → Emails (match `git config user.email`) |
| 2FA | Settings → Password and authentication |

## Rehearsal

- Difference between **Git** and **GitHub**?
- What happens on **merge** of a PR?

**Related:** **Git** track, CI/CD **GitHub Actions**, Getting started setup (OAuth for notes app).
