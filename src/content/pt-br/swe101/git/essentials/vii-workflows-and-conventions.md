---
label: "VII"
subtitle: "Workflows & conventions"
group: "Git"
order: 7
---
Workflows & conventions
Team agreement on **branch names**, **commit messages**, and **merge strategy** prevents Git from becoming a source of conflict.

## 1. GitHub Flow (common for startups)

```text
main ── always deployable
  │
  └── feature/* ── PR ── review ── merge ── delete branch
```

| Rule | Detail |
|------|--------|
| **`main` protected** | No direct push; require PR + CI |
| **Short-lived branches** | Days, not months |
| **Small PRs** | Easier review |

Alternatives: **Gitflow** (release branches) — heavier; **trunk-based** (feature flags) — for mature CI.

## 2. Branch naming

```text
feature/add-oauth-login
fix/null-pointer-checkout
docs/api-readme
chore/deps-bump
```

Include ticket ID if using Jira/Linear: `feature/PROJ-123-oauth`.

## 3. Conventional Commits

```text
feat: add password reset email
fix: prevent double submit on checkout
docs: document env vars
chore: bump eslint
refactor: extract mail service
test: cover auth controller
```

Format: **`type(scope): description`**

Benefits: readable log, auto-changelog tools, semantic release.

## 4. Pull request checklist

- [ ] Branch up to date with `main` (rebase or merge)
- [ ] CI green
- [ ] Self-review diff
- [ ] Description explains **why**, not only what
- [ ] Screenshots for UI changes
- [ ] Migration notes if DB/API breaking

## 5. `.gitattributes` (optional)

```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
```

Normalizes line endings on Windows/macOS/Linux teams.

## 6. Hooks (local quality gates)

```bash
# .git/hooks/pre-commit — or use husky / pre-commit framework
#!/bin/sh
npm test
```

**pre-commit** (Python tool) — shared hooks in repo:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

## 7. Monorepo vs polyrepo

| | Monorepo | Polyrepo |
|---|----------|----------|
| Structure | Many projects, one Git repo | One repo per service |
| CI | Path filters (`paths:` in Actions) | Per-repo pipelines |
| Git | Shared history, large clone | Smaller clones |

Git works the same — org choice, not Git feature.

## 8. What not to commit

| Never | Instead |
|-------|---------|
| `.env`, API keys | Env vars, secret manager — if committed, [Secrets in history](viii-secrets-and-sensitive-files-in-history.md) |
| `node_modules/`, `target/` | `.gitignore` + CI install |
| Large binaries | Git LFS or object storage |
| Generated build output | CI builds artifacts |

## 9. Rehearsal answers

- **GitHub Flow** — PRs into deployable `main`.
- **Revert vs reset** — revert for shared/pushed; reset for local cleanup.
- **Conventional Commits** — structured `type: message` for clarity and tooling.

**Related:** **GitHub** (branch protection, PRs), CI/CD fundamentals.
