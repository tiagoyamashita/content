---
label: "II"
subtitle: "リポジトリとプルリクエスト"
group: "GitHub"
order: 2
---
リポジトリとプルリクエスト

**リポジトリ** には、コードと履歴が GitHub に保存されます。 **プル リクエスト (PR)** は、レビューとチェックを使用して、あるブランチを別のブランチにマージすることを提案します。

## 1. リポジトリを作成する

| Option | Steps |
|--------|--------|
| **New repo on GitHub** | `+` → New repository → add README optional |
| **Push existing local** | `git remote add origin …` → `git push -u origin main` |
| **Template / fork** | Use org template or Fork button |

```bash
git clone git@github.com:org/myapp.git
cd myapp
```

## 2. リポジトリのレイアウト

```text
myapp/
  .github/
    workflows/ci.yml      # GitHub Actions
    PULL_REQUEST_TEMPLATE.md
  src/
  README.md
  LICENSE
```

**README** — 訪問者が最初に目にするもの。ドキュメントのセットアップと環境変数。

## 3. プル リクエストのライフサイクル

```text
1. Create branch locally:  git switch -c feature/oauth
2. Commit and push:        git push -u origin feature/oauth
3. GitHub: "Compare & pull request"
4. Fill title + description; link issue (#42)
5. Reviewers comment; CI runs
6. Address feedback → push more commits (PR updates)
7. Merge → delete branch (optional checkbox)
8. Local: git switch main && git pull
```

## 4. PR 説明テンプレート

```markdown
## Summary
- Add Google OAuth login

## Test plan
- [ ] Sign in with Google on staging
- [ ] Existing email login still works

## Screenshots
(if UI)
```

## 5. コードレビュー

|査読者はそうする |著者はそうします |
|--------------|---------------|
| diff を読み取り、必要に応じてテストします。応答して修正をプッシュ |
|承認、変更リクエスト、またはコメント |会話を解決する |
| CI ステータスを確認する | PR を小規模かつ集中的に保つ |

**Required approvals** — set in branch protection [Actions, issues & settings](iii-actions-issues-and-settings.md).

## 6. マージオプション

|ボタン |結果 |
|----------|----------|
| **マージコミットを作成** |ベースブランチでコミットをマージ |
| **スカッシュとマージ** |ベースで 1 つのコミット |
| **リベースとマージ** |コミットのリニアリプレイ |

チームはリポジトリ設定のデフォルトを選択します。一貫性が重要です。

## 7. フォークの貢献

オープンソースのパターン:

1. Fork repo to your account
2. Clone fork, add `upstream` remote
3. Branch on fork, push, PR **to upstream**

メンテナにはフォークからの PR が表示されます。大きな変更の前にアップストリームと同期します。

## 8. 問題とリンク

```text
PR description: Fixes #123
Commit message:  fix: handle timeout (#123)
```

Closing keywords (`Fixes`, `Closes`) auto-close issues on merge.

## 9. リリース

**Releases** page → **Draft new release** → choose tag `v1.0.0`, notes, attach binaries.

Pairs with Git tags from [Remotes & collaboration](../essentials/v-remotes-and-collaboration.md).

## 10. 権限 (組織リポジトリ)

|役割 |一般的なアクセス |
|------|----------------|
| **読む** |プライベート リポジトリのクローンを作成する |
| **書く** |ブランチをプッシュする (保護されていない場合) |
| **メンテナンス** |問題、一部の設定を管理する |
| **管理者** |ブランチ保護、秘密 |

全員を個別に管理するのではなく、組織内で **チーム** を使用します。

**関連:** **Git** ブランチとリモート、CI/CD GitHub アクションのメモ。
