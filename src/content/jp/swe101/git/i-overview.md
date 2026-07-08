---
label: "I"
subtitle: "概要"
group: "Git"
order: 1
---
Git — 概要

**Git** は **分散バージョン管理システム (DVCS)** です。プロジェクト履歴の完全なコピーをマシンに保存します。スナップショットを**コミット**し、並行作業のために**ブランチ**し、変更を統合するために**マージ** (またはリベース) を行います。

## このトラックの地図

|サブメニュー |フォーカス |
|----------|----------|
| **必需品** |インストール、毎日のコマンド、ブランチ、リモート、元に戻す、ワークフロー |

Start: **Essentials** → [Overview](essentials/i-overview.md).

ホスティング プラットフォーム (**GitHub**、GitLab、Bitbucket) は Git の上に位置します。PR、アクション、およびこのサイトの貢献グラフについては、**GitHub** トピックを参照してください。

## なぜ Git なのか

| Benefit | Explanation |
|---------|-------------|
| **History** | Every commit is a recoverable snapshot |
| **Branches** | Experiment without breaking `main` |
| **Collaboration** | Push/pull between machines and teammates |
| **Audit** | Who changed what, when, and why (messages) |

## コアオブジェクト (メンタルモデル)

```text
Working tree  →  staging (index)  →  commit  →  branch pointer
     │                │                │
  edit files      git add         git commit    main, feature/login
```

| Object | Role |
|--------|------|
| **Commit** | Snapshot + parent + author + message |
| **Branch** | Movable pointer to a commit |
| **Tag** | Fixed pointer (often for releases) |
| **Remote** | Named link to another repo (`origin`) |

## 分散型と集中型

```text
Centralized (SVN):     one server holds history; checkout is a slice

Distributed (Git):   every clone is a full repo
  your laptop ◄────► origin (GitHub)
  teammate    ◄────► origin
```

You can commit offline; sync with **`git push`** / **`git pull`** when connected.

## Git 対 GitHub

| | Git | GitHub |
|---|-----|--------|
|何を |ツール (CLI) |ホスティング + UI + PR + アクション |
|走る |ローカル |クラウド |
|必須 |はい、バージョン管理のため |いいえ — 代替案: GitLab、セルフホスト |

## リハーサル

- **作業ツリー**、**ステージング**、**コミット**の違いは何ですか?
- **支店**は何を指しますか?
- Git はなぜ **配布**されているのですか?
