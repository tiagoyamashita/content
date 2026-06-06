---
label: "VI"
subtitle: "元に戻すと履歴"
group: "Git"
order: 6
---
元に戻すと履歴

Git が作業をすぐに削除することはほとんどありません。ただし、**リセット**、**復元**、**元に戻す**の動作は異なります。コミットを共有する前に、どちらを使用するかを確認してください。

## 1. アンステージして破棄する (安全)

```bash
git restore --staged file.js     # unstage (keep file changes)
git restore file.js              # discard working tree changes (tracked file)
git clean -fd                    # remove untracked files/dirs — destructive
```

Modern Git uses **`restore`**; older docs use **`checkout -- file`**.

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

| Mode | Commits | Staging | Working tree |
|------|---------|---------|--------------|
| `--soft` | Removed | Kept | Kept |
| `--mixed` | Removed | Cleared | Kept |
| `--hard` | Removed | Cleared | Cleared |

**Never `--hard`** on shared branches without team coordination.

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

Reflog saves you after wrong **`reset --hard`** (locally).

## 7. 履歴 (シークレット) からファイルを削除します。

**パスワード**をコミットした場合:

1. Rotate the secret immediately
2. Remove from history: `git filter-repo` or BFG Repo-Cleaner
3. Force push (coordinate with team)

Prevention: `.gitignore`, pre-commit hooks, secret scanning on GitHub.

## 8. 意思決定ガイド

| Situation | Command |
|-----------|---------|
| Unstage file | `git restore --staged` |
| Throw away local edits | `git restore` |
| Fix last commit message (local) | `git commit --amend` |
| Undo last commit, keep files | `git reset --soft HEAD~1` |
| Undo pushed commit on main | `git revert` |
| Pause work | `git stash` |
| Find lost commit | `git reflog` |

**Related:** [Workflows & conventions](vii-workflows-and-conventions.md), CI/CD security (no secrets in repo).
