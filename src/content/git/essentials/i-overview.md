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
| `ii-install-and-configure.md` | Install, `user.name`, SSH keys |
| `iii-everyday-commands.md` | init, clone, add, commit, status, log |
| `iv-branching-and-merging.md` | branch, merge, conflicts |
| `v-remotes-and-collaboration.md` | push, pull, fetch, pull with rebase |
| `vi-undo-and-history.md` | restore, reset, revert, stash |
| `vii-workflows-and-conventions.md` | GitHub flow, commits, `.gitignore` |

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
