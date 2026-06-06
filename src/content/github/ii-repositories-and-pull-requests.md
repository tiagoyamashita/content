---
label: "II"
subtitle: "Repositories & pull requests"
group: "GitHub"
order: 2
---
Repositories & pull requests
A **repository** holds your code and history on GitHub. **Pull requests (PRs)** propose merging one branch into another with review and checks.

## 1. Create a repository

| Option | Steps |
|--------|--------|
| **New repo on GitHub** | `+` → New repository → add README optional |
| **Push existing local** | `git remote add origin …` → `git push -u origin main` |
| **Template / fork** | Use org template or Fork button |

```bash
git clone git@github.com:org/myapp.git
cd myapp
```

## 2. Repository layout

```text
myapp/
  .github/
    workflows/ci.yml      # GitHub Actions
    PULL_REQUEST_TEMPLATE.md
  src/
  README.md
  LICENSE
```

**README** — first thing visitors see; document setup and env vars.

## 3. Pull request lifecycle

```text
1. Create branch locally:  git switch -c feature/oauth
2. Commit and push:        git push -u origin feature/oauth
3. GitHub: "Compare & pull request"
4. Fill title + description; link issue (#42)
5. Reviewers comment; CI runs
6. Address feedback → push more commits (PR updates)
7. Merge → delete branch (optional checkbox)
8. Local: git switch main && git pull
```

## 4. PR description template

```markdown
## Summary
- Add Google OAuth login

## Test plan
- [ ] Sign in with Google on staging
- [ ] Existing email login still works

## Screenshots
(if UI)
```

## 5. Code review

| Reviewer does | Author does |
|---------------|-------------|
| Read diff, test if needed | Respond, push fixes |
| Approve, request changes, or comment | Resolve conversations |
| Check CI status | Keep PR small and focused |

**Required approvals** — set in branch protection (`iii-actions-issues-and-settings.md`).

## 6. Merge options

| Button | Result |
|--------|--------|
| **Create merge commit** | Merge commit on base branch |
| **Squash and merge** | One commit on base |
| **Rebase and merge** | Linear replay of commits |

Team picks default in repo settings — consistency matters.

## 7. Fork contributing

Open source pattern:

1. Fork repo to your account
2. Clone fork, add `upstream` remote
3. Branch on fork, push, PR **to upstream**

Maintainers see PR from your fork; you sync with upstream before big changes.

## 8. Issues and linking

```text
PR description: Fixes #123
Commit message:  fix: handle timeout (#123)
```

Closing keywords (`Fixes`, `Closes`) auto-close issues on merge.

## 9. Releases

**Releases** page → **Draft new release** → choose tag `v1.0.0`, notes, attach binaries.

Pairs with Git tags from `git/essentials/v-remotes-and-collaboration.md`.

## 10. Permissions (org repos)

| Role | Typical access |
|------|----------------|
| **Read** | Clone private repo |
| **Write** | Push branches (if not protected) |
| **Maintain** | Manage issues, some settings |
| **Admin** | Branch protection, secrets |

Use **teams** in orgs — not individual admin for everyone.

**Related:** **Git** branching and remotes, CI/CD GitHub Actions note.
