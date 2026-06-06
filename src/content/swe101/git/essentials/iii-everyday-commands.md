---
label: "III"
subtitle: "日常のコマンド"
group: "Git"
order: 3
---
日常のコマンド

**毎日**実行するコマンド: 状態の検査、ステージの変更、コミット、履歴の読み取り。

## 1. 3 本の木

<figure class="notes-diagram"><svg xmlns="15 viewBox="0 0 400 90" role="img" aria-label="Git working tree staging commit">
  <rect x="12" y="36" width="100" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="56" fill="#e4e4e7" font-size="9">Working tree</text>
  <path d="M112 52 H132" stroke="#a1a1aa"/>
  <text x="118" y="48" fill="#71717a" font-size="7">add</text>
  <rect x="132" y="36" width="100" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="152" y="56" fill="#e4e4e7" font-size="9">Staging</text>
  <path d="M232 52 H252" stroke="#a1a1aa"/>
  <text x="238" y="48" fill="#71717a" font-size="7">commit</text>
  <rect x="252" y="36" width="100" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="272" y="56" fill="#e4e4e7" font-size="9">Repository</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Files move left → right into history</text>
</svg></figure>

## 2. 状態を検査する

```bash
git status              # modified, staged, untracked
git status -sb          # short branch info
git diff                # unstaged changes
git diff --staged       # staged vs last commit
git log --oneline -10   # recent commits
git log --oneline --graph --all   # branch graph
```

## 3. ステージングとコミット

```bash
git add file.js                 # one file
git add src/                    # directory
git add -p                      # patch — hunk by hunk
git add -A                      # all changes (careful)

git commit -m "fix: handle null user id"
git commit -am "docs: update README"   # skip separate add for tracked files only
```

**命令的な雰囲気**でメッセージを書きます: 「機能の追加」ではなく「機能の追加」。

## 4. 既存のプロジェクトのクローンを作成します

```bash
git clone git@github.com:org/app.git
cd app
```

クローンは **`origin`** リモートを作成し、デフォルトのブランチをチェックアウトします。

## 5. `.gitignore`

シークレット、ビルド出力、または OS ジャンクを決してコミットしないでください。

```gitignore
# .gitignore
node_modules/
dist/
.env
.env.local
*.log
.DS_Store
target/
.idea/
```

ファイルが誤ってコミットされた場合は、[元に戻すと履歴](vi-undo-and-history.md) を参照してください。`.gitignore` から削除するだけでは十分ではありません。

## 6. 1 つのコミットを表示する

```bash
git show abc1234
git show HEAD~1 --stat
```

## 7. ブランチの比較

```bash
git diff main..feature/login
git log main..feature/login --oneline
```

## 8. 共通のステータス行

|ステータス |意味 |
|--------|--------|
| **未追跡** |新しいファイル - まだ Git にありません |
| **修正済み** |前回のコミット以降に変更されました |
| **段階的** |次のコミットに含まれます |
| **清潔** |コミットするものは何もありません |

## 9. クイックリファレンス

|タスク |コマンド |
|-----|----------|
|何が変わったのでしょうか？ | `git status`、`git diff` |
|スナップショットを保存 | `git add` + `git commit` |
|歴史 | `git log --oneline --graph` |
|ラインを編集したのは誰ですか? | `git blame file.js` |

**関連:** [分岐と結合](iv-branching-and-merging.md)、[ワークフローと規約](vii-workflows-and-conventions.md)。
