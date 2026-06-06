---
label: "VI"
subtitle: "元に戻すと履歴"
group: "Git"
order: 6
---
元に戻すと履歴

Git が作業をすぐに削除することはほとんどありませんが、**リセット**、**復元**、**元に戻す**の動作は異なります。コミットを共有する前に、どちらを使用するかを確認してください。

## 1. アンステージして破棄する (安全)

```bash
git restore --staged file.js     # unstage (keep file changes)
git restore file.js              # discard working tree changes (tracked file)
git clean -fd                    # remove untracked files/dirs — destructive
```

最新の Git は **`restore`** を使用します。古いドキュメントでは **`checkout -- file`** を使用します。

## 2. 最後のコミットを修正します (プッシュされません)

```bash
git add forgotten-file.js
git commit --amend -m "feat: complete login flow"
```

**プッシュしていない** (またはチームが同意した) コミットのみを修正し、履歴を書き換えます。

## 3. リセット — 分岐ポインタを移動する

```bash
git reset --soft HEAD~1    # undo commit, keep staged
git reset --mixed HEAD~1   # undo commit, unstage (default)
git reset --hard HEAD~1    # undo commit AND discard changes — dangerous
```

|モード |コミット |ステージング |ワーキングツリー |
|------|-------|-----------|--------------|
| `--soft` |削除されました |保管 |保管 |
| `--mixed` |削除されました |クリア済み |保管 |
| `--hard` |削除されました |クリア済み |クリア済み |

**チームの調整なしに共有ブランチでは絶対に `--hard`** しないでください。

## 4. revert — 元に戻す新しいコミット

**公開済み**の履歴に対して安全:

```bash
git revert abc1234           # one commit
git revert HEAD              # last commit
git revert -m 1 merge_commit # merge revert — pick mainline parent
```

フォワードコミットを作成します - 履歴の書き換えはありません。

## 5. 隠し場所 — 棚の作業が進行中

```bash
git stash push -m "wip login form"
git stash list
git stash pop                # apply + remove from stash
git stash apply stash@{0}    # apply, keep stash
git stash drop
```

中途半端な作業をコミットせずにブランチを切り替えます。

## 6.「失われた」コミットを回復する

```bash
git reflog                     # every HEAD movement ~90 days
git switch -c recover abc1234  # branch at lost commit
```

Reflog は、間違った **`reset --hard`** (ローカルで) の後にあなたを救います。

## 7. 履歴 (シークレット) からファイルを削除します。

**パスワード**をコミットした場合:

1. シークレットをすぐにローテーションします
2. 履歴から削除: `git filter-repo` または BFG Repo-Cleaner
3. フォースプッシュ（チームとの連携）

防止: `.gitignore`、コミット前フック、GitHub でのシークレット スキャン。

## 8. 意思決定ガイド

|状況 |コマンド |
|----------|----------|
|ファイルのステージングを解除 | `git restore --staged` |
|ローカル編集を破棄する | `git restore` |
|最後のコミットメッセージを修正 (ローカル) | `git commit --amend` |
|最後のコミットを元に戻し、ファイルを保持します | `git reset --soft HEAD~1` |
|メインでプッシュされたコミットを元に戻す | `git revert` |
|仕事を一時停止する | `git stash` |
|失われたコミットを見つける | `git reflog` |

**関連:** [ワークフローと規約](vii-workflows-and-conventions.md)、CI/CD セキュリティ (リポジトリにシークレットはありません)。
