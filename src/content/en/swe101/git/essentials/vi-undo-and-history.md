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

## 7. Remove file from history (secrets)

If you committed a **password**:

1. Rotate the secret immediately
2. Remove from history: `git filter-repo` or BFG Repo-Cleaner
3. Force push (coordinate with team)

Prevention: `.gitignore`, pre-commit hooks, secret scanning on GitHub.

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

**Related:** [Workflows & conventions](vii-workflows-and-conventions.md), CI/CD security (no secrets in repo).
