---
label: "I"
subtitle: "Overview"
group: "Git"
order: 1
---
Git essentials — overview
Day-to-day Git: configure once, then **add → commit → push**, branch for features, sync with **remotes**, recover from mistakes.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Install & configure](ii-install-and-configure.md) | Install, `user.name`, SSH keys, **`~/.ssh/config`** |
| [Everyday commands](iii-everyday-commands.md) | init, clone, add, commit, status, log |
| [Branching & merging](iv-branching-and-merging.md) | branch, merge, conflicts |
| [Remotes & collaboration](v-remotes-and-collaboration.md) | push, pull, fetch, pull with rebase |
| [Undo & history](vi-undo-and-history.md) | restore, reset, revert, stash |
| [Workflows & conventions](vii-workflows-and-conventions.md) | GitHub flow, commits, `.gitignore` |
| [Secrets in history](viii-secrets-and-sensitive-files-in-history.md) | Find `.env` in history, `git filter-repo`, force push |

**Related:** **GitHub** topic (PRs, hosting), CI/CD fundamentals (triggers on push).

## Minimum daily loop

```bash
git status
git add path/to/file
git commit -m "feat: describe change"
git pull --rebase
git push
```

## Rehearsal

- `git add` vs `git commit`?
- Merge vs rebase — one sentence each?
