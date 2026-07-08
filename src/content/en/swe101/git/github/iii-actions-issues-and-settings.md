---
label: "III"
subtitle: "Actions, issues & settings"
group: "GitHub"
order: 3
---
Actions, issues & settings
GitHub **Actions** run CI/CD on events. **Issues** track work. **Settings** lock down `main` and secrets.

## 1. GitHub Actions (CI sketch)

Workflow file: **`.github/workflows/ci.yml`**

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm
      - run: npm ci
      - run: npm test
```

| Concept | Meaning |
|---------|---------|
| **Workflow** | YAML file |
| **Trigger** | `push`, `pull_request`, `schedule` |
| **Job** | Runs on one runner |
| **Step** | Command or action |

Deep dive: CI/CD **Tools & platforms → GitHub Actions**.

## 2. Secrets in Actions

**Settings → Secrets and variables → Actions**

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

| Scope | Use |
|-------|-----|
| Repository secret | One repo |
| Environment secret | `production` deploy only |
| Organization secret | Shared across repos |

Never log secrets; fork PRs do not receive repo secrets by default.

## 3. Branch protection

**Settings → Branches → Add rule** for `main`:

| Rule | Why |
|------|-----|
| Require pull request | No direct push |
| Require status checks | CI must pass |
| Require review | Human gate |
| Require linear history | Optional — no merge commits |
| Restrict who can push | Admins only bypass |

## 4. Issues & projects

| Feature | Use |
|---------|-----|
| **Issues** | Bugs, features, tasks |
| **Labels** | `bug`, `enhancement`, `good first issue` |
| **Milestones** | Release grouping |
| **Projects** | Kanban board across repos |

Link PRs with `Fixes #N` to auto-close.

## 5. GitHub Copilot & Codespaces (optional)

| Product | Notes |
|---------|-------|
| **Copilot** | AI assist in IDE — subscription |
| **Codespaces** | Cloud dev environment — usage billing |
| **.devcontainer** | Reproducible Codespaces config |

Not required for basic GitHub use.

## 6. Tokens and security

| Token type | When |
|------------|------|
| **Fine-grained PAT** | Scripts, Notes app — minimal repo scope |
| **Classic PAT** | Legacy — broad `repo` scope |
| **GitHub App** | Integrations, org-wide — preferred for tools |
| **SSH key** | Git push/pull |

Enable **2FA** on account; orgs can require it.

**Secret scanning & push protection:** Settings → **Code security and analysis** — blocks or alerts on leaked keys in commits. If `.env` was pushed, rotate secrets and rewrite history — [Secrets in history](../essentials/viii-secrets-and-sensitive-files-in-history.md).

Getting started **Setup** note covers OAuth scopes for this notes app.

## 7. Notifications

Watch repo → **Participating and @mentions** or **All activity**. Tune email vs web in **Settings → Notifications**.

## 8. GitHub Pages

Free static hosting from repo:

**Settings → Pages** → source branch `main` / `/docs` or Actions workflow.

Alternative: Vercel/Netlify (startups free-services note).

## 9. Checklist for new repo

- [ ] README with setup
- [ ] `.gitignore` appropriate to stack
- [ ] LICENSE file
- [ ] Branch protection on `main`
- [ ] CI workflow on PR
- [ ] Dependabot or Renovate (optional)
- [ ] Secret scanning enabled (public repos default)

**Related:** CI/CD security (pin actions, OIDC), **Git** workflows note, [Contribution graph](activity-contribution-graph.md).
