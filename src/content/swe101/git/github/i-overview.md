---
label: "I"
subtitle: "概要"
group: "GitHub"
order: 1
---
GitHub — 概要

**GitHub** は Git リポジトリをホストし、**プル リクエスト**、**レビュー**、**アクション**、**問題**、**プロジェクト** ツールを追加します。 Git 自体はローカルで実行されます。GitHub はソーシャル層と自動化層です。

## このトピックのマップ

|注 |フォーカス |
|------|----------|
| **Git → Essentials** |ローカル Git コマンド、ブランチ、リモート |
| [リポジトリとプルリクエスト](ii-repositories-and-pull-requests.md) |リポジトリ、フォーク、PR、レビュー |
| [アクション、問題、設定](iii-actions-issues-and-settings.md) | CI、問題、ブランチ保護、トークン |
| [寄与グラフ](activity-contribution-graph.md) |このサイトの投稿グリッドのデモ |

## Git + GitHub フロー

```text
local:  branch → commit → push
GitHub: Pull Request → review → merge → Actions CI
```

## アカウントの必需品

|タスク |どこ |
|------|----------|
| SSH キー |設定 → SSH および GPG キー |
|パーソナルアクセストークン |設定 → 開発者設定 (きめ細かい設定を推奨) |
|コミットの電子メール |設定 → 電子メール (`git config user.email` と一致) |
| 2FA |設定 → パスワードと認証 |

## リハーサル

- **Git** と **GitHub** の違いは何ですか?
- PR の **マージ**では何が起こりますか?

**関連:** **Git** トラック、CI/CD **GitHub アクション**、セットアップの開始 (メモ アプリの OAuth)。
