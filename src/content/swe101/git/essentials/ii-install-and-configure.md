---
label: "II"
subtitle: "インストールと設定"
group: "Git"
order: 2
---
インストールと設定

マシンごとに Git を 1 回インストールし、ID を設定し、GitHub/GitLab には **SSH** (または資格情報ヘルパーを備えた HTTPS) を優先します。

## 1. インストール

| OS | Command / source |
|----|------------------|
| **Windows** | [git-scm.com](https://git-scm.com) or `winget install Git.Git` |
| **macOS** | Xcode CLT or `brew install git` |
| **Linux** | `sudo apt install git` / `dnf install git` |

確認する：

```bash
git --version
```

## 2. ID (コミットに必要)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

プロファイルにコミットをリンクしたい場合は、GitHub アカウントと **同じメールアドレス** を使用してください。

設定を表示:

```bash
git config --global --list
```

| Scope | Flag | Use |
|-------|------|-----|
| System | `--system` | All users |
| Global | `--global` | Your user (`~/.gitconfig`) |
| Local | `--local` | Current repo only (overrides global) |

## 3. デフォルトのブランチ名

```bash
git config --global init.defaultBranch main
```

## 4. GitHub の SSH キー

```bash
ssh-keygen -t ed25519 -C "you@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub   # paste into GitHub → Settings → SSH keys
ssh -T git@github.com
```

SSH を使用してクローンを作成します。

```bash
git clone git@github.com:owner/repo.git
```

## 5. HTTPS の代替案

```bash
git clone https://github.com/owner/repo.git
```

**資格情報マネージャー** (Windows の Git には資格情報マネージャーが含まれます) または **きめ細かい PAT** を使用します。URL にパスワードを埋め込むのは避けてください。

## 6. 便利なグローバルデフォルト

```bash
git config --global pull.rebase false    # merge on pull (default); see v-remotes
git config --global fetch.prune true     # drop stale remote-tracking branches
git config --global color.ui auto
git config --global core.editor "code --wait"   # VS Code / Cursor
```

## 7. 最初のリポジトリ

```bash
mkdir myproject && cd myproject
git init
echo "# My project" > README.md
git add README.md
git commit -m "Initial commit"
```

GitHub へのリンク (サイトで空のリポジトリを作成した後):

```bash
git remote add origin git@github.com:you/myproject.git
git push -u origin main
```

**Related:** [Everyday commands](iii-everyday-commands.md), **GitHub** → repositories note.
