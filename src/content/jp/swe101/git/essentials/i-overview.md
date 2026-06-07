---
label: "I"
subtitle: "概要"
group: "Git"
order: 1
---
Git の要点 — 概要

日常の Git: 一度構成し、**追加 → コミット → プッシュ**、機能に分岐し、**リモート**と同期し、間違いから回復します。

## このサブメニューのマップ

| Note | Focus |
|------|--------|
| [Install & configure](ii-install-and-configure.md) | Install, `user.name`, SSH keys |
| [Everyday commands](iii-everyday-commands.md) | init, clone, add, commit, status, log |
| [Branching & merging](iv-branching-and-merging.md) | branch, merge, conflicts |
| [Remotes & collaboration](v-remotes-and-collaboration.md) | push, pull, fetch, pull with rebase |
| [Undo & history](vi-undo-and-history.md) | restore, reset, revert, stash |
| [Workflows & conventions](vii-workflows-and-conventions.md) | GitHub flow, commits, `.gitignore` |

**関連:** **GitHub** トピック (PR、ホスティング)、CI/CD の基礎 (プッシュ時のトリガー)。

## 毎日の最小ループ

```bash
git status
git add path/to/file
git commit -m "feat: describe change"
git pull --rebase
git push
```

## リハーサル

- `git add` vs `git commit`?
- Merge vs rebase — one sentence each?
