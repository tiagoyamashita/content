---
label: "IV"
subtitle: "分岐とマージ"
group: "Git"
order: 4
---
分岐とマージ

**ブランチ**は安価なポインタです。すべての機能や修正に使用してください。 **マージ** は履歴を結合します。同じ行が変更された場合に **競合** を解決します。

## 1. ブランチの基本

```bash
git branch                    # list local branches
git branch feature/login      # create branch (does not switch)
git switch feature/login      # checkout branch (Git 2.23+)
git switch -c feature/login   # create + switch

git switch main
git merge feature/login       # merge into current branch
git branch -d feature/login   # delete after merge
```

レガシー: `git checkout -b feature/login` — `switch -c`と同じ。

## 2. 分岐図

```text
main:     A --- B --- C ----------- M
                      \           /
feature/login:         D --- E ---

merge M combines E into main
```

## 3. マージタイプ

|タイプ |いつ |結果 |
|------|------|----------|
| **早送り** |ブランチ以降、メインに新しいコミットはありません |線形履歴 |
| **3 者間マージ** |両方とも移動しました | 2 つの親とコミットをマージ |

```bash
git merge feature/login
# if conflicts → edit files → git add → git commit
```

## 4. 競合の解決

ファイル内の競合マーカー:

```text
<<<<<<< HEAD
const timeout = 5000;
=======
const timeout = 10000;
>>>>>>> feature/login
```

手順:

1. 最終的に必要なコードに編集します (マーカーを削除します)。
2. `git add conflicted-file`
3. `git commit` (またはマージを続行)

マージを中止します:

```bash
git merge --abort
```

## 5. リベース (線形履歴)

更新されたメインに加えてコミットを再生します。

```bash
git switch feature/login
git fetch origin
git rebase origin/main
```

```text
Before rebase:
  main:    A - B - C
  feature: A - B - D - E

After rebase onto C:
  main:    A - B - C
  feature: A - B - C - D' - E'
```

**黄金律:** すでに **プッシュ**され共有されているコミットをリベースしないでください。履歴が書き換えられます。ローカルのみ、または PR マージ前の機能ブランチの場合は OK。

## 6. PR でのマージとリベース

|戦略 |歴史 |使用 |
|----------|-----------|-----|
| **コミットをマージ** |正確な枝の形状を保持 | GitHub のデフォルト「マージ コミットの作成」 |
| **スカッシュマージ** |メインで 1 つのコミット |メインログをクリーンアップ |
| **リベースマージ** |リニアコミットのリプレイ |リニアメイン |

チームは 1 つの規則を選択します。[ワークフローと規則](vii-workflows-and-conventions.md) の文書です。

## 7. ヘッドの取り外し

(ブランチではなく) コミットを直接チェックアウトすると、**切り離された HEAD** 状態になり、コミットが失われる可能性があります。修理：

```bash
git switch -c recover-work
```

## 8. リハーサルの答え

- **ブランチ** — コミットへのポインタ。新しいコミットごとに移動します。
- **早送り** — メインは単純にブランチの先端に進みます。マージコミットはありません。
- **競合** — 同じ領域が別々に編集されました。 Git は自動選択できません。

**関連:** [リモートとコラボレーション](v-remotes-and-collaboration.md)、**GitHub** PR のメモ。
