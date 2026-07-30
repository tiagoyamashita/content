---
label: "V"
subtitle: "Remotes & collaboration"
group: "Git"
order: 5
---
Remotes & collaboration
A **remote** is a named URL to another repository — usually **`origin`** on GitHub. **Fetch** downloads; **pull** fetches + integrates; **push** uploads your commits.

## 1. Remote commands

```bash
git remote -v
git remote add origin git@github.com:you/app.git
git remote set-url origin git@github.com:you/app.git

git fetch origin              # download branches/tags — no merge
git pull origin main          # fetch + merge into current branch
git push origin main          # upload commits
git push -u origin feature/x  # first push — set upstream
```

After `-u`, plain **`git push`** / **`git pull`** use the tracking branch.

## 2. Fetch vs pull

```mermaid
flowchart LR
  subgraph fetch
    F1[download origin] --> F2[branch unchanged]
  end
  subgraph pull
    P1[fetch] --> P2[merge or rebase into current]
  end
```

Safer workflow for shared branches:

```bash
git fetch origin
git log HEAD..origin/main --oneline   # what's new upstream?
git merge origin/main                 # or rebase
```

## 3. Pull with rebase

Keeps feature branch linear before push:

```bash
git config --global pull.rebase true
# or per pull:
git pull --rebase origin main
```

On feature branch before opening PR:

```bash
git switch feature/api
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**`--force-with-lease`** — safer than `--force`; fails if remote moved unexpectedly.

## 4. Tracking branches

```bash
git branch -vv
# feature/api  abc1234 [origin/feature/api] latest commit msg
```

Set upstream if missing:

```bash
git push -u origin feature/api
```

## 5. Collaboration flow

```mermaid
flowchart TB
  P1[pull latest main] --> P2[create feature branch]
  P2 --> P3[commit locally]
  P3 --> P4[push branch]
  P4 --> P5[open Pull Request]
  P5 --> P6[review and merge]
  P6 --> P7[pull main and delete branch]
```

See **GitHub** topic for PR UI, reviews, branch protection.

## 6. Fork workflow

Contributing to someone else's repo:

```bash
# clone your fork
git clone git@github.com:you/upstream-project.git
cd upstream-project
git remote add upstream git@github.com:original/upstream-project.git

git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

PR goes **from your fork** → **upstream**.

## 7. Tags and releases

```bash
git tag v1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
git push origin --tags
```

GitHub **Releases** attach binaries and notes to tags.

## 8. Troubleshooting push

| Error | Fix |
|-------|-----|
| `rejected (non-fast-forward)` | Pull/rebase first, then push |
| `permission denied` | SSH key or token — check [SSH config](ii-install-and-configure.md#5-ssh-config-for-git-remotes) and [GitHub SSH keys](../github/iv-ssh-keys.md) |
| `protected branch` | Use PR; cannot push directly to `main` |

**Related:** [Branching & merging](iv-branching-and-merging.md), CI/CD (workflows on `push`).
