---
label: "V"
subtitle: "リモートとコラボレーション"
group: "Git"
order: 5
---
リモートとコラボレーション

**リモート** は、別のリポジトリ (通常は GitHub 上の **`origin`**) への名前付き URL です。 **ダウンロード**を取得します。 **プル** フェッチ + 統合。 **プッシュ** はコミットをアップロードします。

## 1. リモートコマンド

```bash
git remote -v
git remote add origin git@github.com:you/app.git
git remote set-url origin git@github.com:you/app.git

git fetch origin              # download branches/tags — no merge
git pull origin main          # fetch + merge into current branch
git push origin main          # upload commits
git push -u origin feature/x  # first push — set upstream
```

`-u` 以降、プレーン **`git push`** / **`git pull`** は追跡ブランチを使用します。

## 2. フェッチとプル

```text
fetch:  origin/main updates on your machine — your branch unchanged until merge/rebase
pull:   fetch + merge (or rebase if configured) into current branch
```

共有ブランチのより安全なワークフロー:

```bash
git fetch origin
git log HEAD..origin/main --oneline   # what's new upstream?
git merge origin/main                 # or rebase
```

## 3. リベースでプルする

プッシュする前に機能ブランチを線形に保ちます。

```bash
git config --global pull.rebase true
# or per pull:
git pull --rebase origin main
```

PR を開く前の機能ブランチ:

```bash
git switch feature/api
git fetch origin
git rebase origin/main
git push --force-with-lease
```

**`--force-with-lease`** — `--force` より安全です。リモートが予期せず移動した場合は失敗します。

## 4. ブランチの追跡

```bash
git branch -vv
# feature/api  abc1234 [origin/feature/api] latest commit msg
```

欠落している場合は上流に設定します。

```bash
git push -u origin feature/api
```

## 5. コラボレーションの流れ

```text
1. git fetch / pull latest main
2. git switch -c feature/issue-42
3. commit locally
4. git push -u origin feature/issue-42
5. Open Pull Request on GitHub
6. Review → merge on GitHub
7. git switch main && git pull
8. git branch -d feature/issue-42
```

PR UI、レビュー、ブランチ保護については、**GitHub** トピックを参照してください。

## 6. フォークのワークフロー

他の人のリポジトリに貢献する:

```bash
# clone your fork
git clone git@github.com:you/upstream-project.git
cd upstream-project
git remote add upstream git@github.com:original/upstream-project.git

git fetch upstream
git switch main
git merge upstream/main
git push origin main
```

PR は **フォークから** → **上流**に進みます。

## 7. タグとリリース

```bash
git tag v1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
git push origin --tags
```

GitHub **リリース**はバイナリとメモをタグに添付します。

## 8. プッシュのトラブルシューティング

|エラー |修正 |
|------|-----|
| `rejected (non-fast-forward)` |最初にプル/リベースしてから | を押します。
| `permission denied` | SSH キーまたはトークン |
| `protected branch` | PR を使用する。 `main` に直接プッシュすることはできません |

**関連:** [分岐とマージ](iv-branching-and-merging.md)、CI/CD (`push`のワークフロー)。
