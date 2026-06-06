---
label: "II"
subtitle: "リポジトリとプルリクエスト"
group: "GitHub"
order: 2
---
リポジトリとプルリクエスト

**リポジトリ** には、GitHub 上のコードと履歴が保存されます。 **プル リクエスト (PR)** は、レビューとチェックを使用して、あるブランチを別のブランチにマージすることを提案します。

## 1. リポジトリを作成する

|オプション |ステップ |
|----------|----------|
| **GitHub 上の新しいリポジトリ** | `+` → 新しいリポジトリ → README を追加（オプション） |
| **既存のローカルをプッシュ** | `git remote add origin …` → `git push -u origin main` |
| **テンプレート/フォーク** |組織テンプレートまたはフォーク ボタンを使用する |

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
| CI ステータスを確認する | PR は小規模かつ集中的に行う |

**必要な承認** — ブランチ保護 [アクション、問題、設定](iii-actions-issues-and-settings.md) で設定します。

## 6. マージオプション

|ボタン |結果 |
|----------|----------|
| **マージコミットを作成** |ベースブランチでコミットをマージ |
| **スカッシュとマージ** |ベースで 1 つのコミット |
| **リベースとマージ** |コミットのリニアリプレイ |

チームはリポジトリ設定のデフォルトを選択します。一貫性が重要です。

## 7. フォークの貢献

オープンソースのパターン:

1. アカウントにリポジトリをフォークする
2. フォークのクローンを作成し、`upstream` リモートを追加します
3. フォークで分岐、プッシュ、PR **上流へ**

メンテナはフォークからの PR を確認します。大きな変更の前にアップストリームと同期します。

## 8. 問題とリンク

```text
PR description: Fixes #123
Commit message:  fix: handle timeout (#123)
```

終了キーワード (`Fixes`、`Closes`) はマージ時に問題を自動的に終了します。

## 9. リリース

**リリース** ページ → **新しいリリースのドラフト** → タグ `v1.0.0`、メモを選択し、バイナリを添付します。

[リモートとコラボレーション](../essentials/v-remotes-and-collaboration.md) の Git タグとペアリングします。

## 10. 権限 (組織リポジトリ)

|役割 |一般的なアクセス |
|------|----------------|
| **読む** |プライベート リポジトリのクローンを作成する |
| **書く** |ブランチをプッシュする (保護されていない場合) |
| **メンテナンス** |問題、一部の設定を管理する |
| **管理者** |ブランチ保護、秘密 |

全員を個別に管理するのではなく、組織内で **チーム** を使用します。

**関連:** **Git** ブランチとリモート、CI/CD GitHub アクションに関するメモ。
