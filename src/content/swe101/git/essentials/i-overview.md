---
label: "I"
subtitle: "概要"
group: "Git"
order: 1
---
Git の基本事項 — 概要

日常の Git: 一度構成したら、**追加 → コミット → プッシュ**、機能に応じて分岐し、**リモート**と同期し、間違いから回復します。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [インストールと設定](ii-install-and-configure.md) |インストール、`user.name`、SSH キー |
| [日常コマンド](iii-everyday-commands.md) |初期化、クローン、追加、コミット、ステータス、ログ |
| [分岐・結合](iv-branching-and-merging.md) |ブランチ、マージ、競合 |
| [リモートとコラボレーション](v-remotes-and-collaboration.md) |プッシュ、プル、フェッチ、リベースによるプル |
| [元に戻すと履歴](vi-undo-and-history.md) |復元、リセット、元に戻す、隠しておく |
| [ワークフローと規約](vii-workflows-and-conventions.md) | GitHub フロー、コミット、`.gitignore` |

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
- マージとリベース — それぞれ 1 文ですか?
