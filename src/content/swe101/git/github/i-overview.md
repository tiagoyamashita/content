---
label: "I"
subtitle: "概要"
group: "GitHub"
order: 1
---
GitHub — 概要

**GitHub** は Git リポジトリをホストし、**プル リクエスト**、**レビュー**、**アクション**、**問題**、**プロジェクト** ツールを追加します。 Git 自体はローカルで実行されます。GitHub はソーシャル層と自動化層です。

## このトピックのマップ

| Note | Focus |
|------|--------|
| **Git → Essentials** | Local Git commands, branches, remotes |
| [Repositories & pull requests](ii-repositories-and-pull-requests.md) | Repos, forks, PRs, reviews |
| [Actions, issues & settings](iii-actions-issues-and-settings.md) | CI, issues, branch protection, tokens |
| [Contribution graph](activity-contribution-graph.md) | This site's contribution grid demo |

## Git + GitHub フロー

```text
local:  branch → commit → push
GitHub: Pull Request → review → merge → Actions CI
```

## アカウントの必需品

| Task | Where |
|------|--------|
| SSH keys | Settings → SSH and GPG keys |
| Personal access token | Settings → Developer settings (prefer fine-grained) |
| Email for commits | Settings → Emails (match `git config user.email`) |
| 2FA | Settings → Password and authentication |

## リハーサル

- **Git** と **GitHub** の違いは何ですか?
- PR の **マージ** では何が起こりますか?

**関連:** **Git** トラック、CI/CD **GitHub アクション**、セットアップの開始 (メモ アプリの場合は OAuth)。
