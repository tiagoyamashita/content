---
label: "VI"
subtitle: "Undo & history"
group: "Git"
order: 6
---
Undo & history
Git rarely deletes work immediately — but **reset**, **restore**, and **revert** behave differently. Know which to use before sharing commits.

## 1. Unstage and discard (safe)

```bash
git restore --staged file.js     # unstage (keep file changes)
git restore file.js              # discard working tree changes (tracked file)
git clean -fd                    # remove untracked files/dirs — destructive
```

Modern Git uses **`restore`**; older docs use **`checkout -- file`**.

## 2. Amend last commit (not pushed)

```bash
git add forgotten-file.js
git commit --amend -m "feat: complete login flow"
```

Only amend commits **you have not pushed** (or team agrees) — rewrites history.

## 3. reset — move branch pointer

```bash
git reset --soft HEAD~1    # undo commit, keep staged
git reset --mixed HEAD~1   # undo commit, unstage (default)
git reset --hard HEAD~1    # undo commit AND discard changes — dangerous
```

| Mode | Commits | Staging | Working tree |
|------|---------|---------|--------------|
| `--soft` | Removed | Kept | Kept |
| `--mixed` | Removed | Cleared | Kept |
| `--hard` | Removed | Cleared | Cleared |

**Never `--hard`** on shared branches without team coordination.

## 4. revert — new commit that undoes

Safe for **published** history:

```bash
git revert abc1234           # one commit
git revert HEAD              # last commit
git revert -m 1 merge_commit # merge revert — pick mainline parent
```

Creates a forward commit — no history rewrite.

## 5. stash — shelf work in progress

```bash
git stash push -m "wip login form"
git stash list
git stash pop                # apply + remove from stash
git stash apply stash@{0}    # apply, keep stash
git stash drop
```

Switch branches without committing half-done work.

## 6. Recover "lost" commits

```bash
git reflog                     # every HEAD movement ~90 days
git switch -c recover abc1234  # branch at lost commit
```

Reflog saves you after wrong **`reset --hard`** (locally).

## 7. Remove secrets from history

If you committed **`.env`**, keys, or passwords:

1. **Rotate / revoke** the secret immediately — history rewrites do not undo exposure.
2. **Find** what leaked — [Secrets in history](viii-secrets-and-sensitive-files-in-history.md) (`git log --all -- .env`, `git grep`, gitleaks).
3. **Rewrite** history — `git filter-repo` or BFG, then **`git push --force-with-lease`** (coordinate with team).

Adding **`.gitignore`** alone is **not** enough once a file was pushed.

Prevention: pre-commit hooks, GitHub secret scanning, never commit `.env`.

## 8. Decision guide

| Situation | Command |
|-----------|---------|
| Unstage file | `git restore --staged` |
| Throw away local edits | `git restore` |
| Fix last commit message (local) | `git commit --amend` |
| Undo last commit, keep files | `git reset --soft HEAD~1` |
| Undo pushed commit on main | `git revert` |
| Pause work | `git stash` |
| Find lost commit | `git reflog` |
| Secret in Git history | [Secrets in history](viii-secrets-and-sensitive-files-in-history.md) |

**Related:** [Workflows & conventions](vii-workflows-and-conventions.md), [Secrets in history](viii-secrets-and-sensitive-files-in-history.md), CI/CD security (no secrets in repo).
