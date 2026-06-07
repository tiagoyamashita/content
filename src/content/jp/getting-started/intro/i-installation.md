---
label: "I"
subtitle: "インストール"
group: "はじめに"
order: 1
---
はじめに — はじめに: インストール

ディスク上のメモを開いて編集する方法、またはアプリがボールトをホストできるように GitHub に接続する方法。

## 1. 2 つの作業方法

**Browse your files (local)**  
Clone or download this repository and **open the folder in Cursor**. Your notes are Markdown under **`src/content/`**. You do **not** need to sign in to GitHub just to read or edit files on your machine—Explorer and search behave like any project.

**Sign in with GitHub (vault)**  
Use **GitHub login** in the Notes flow when you want the program to **create your vault** and **manage notes** against your repository—creating folders, `_meta.json`, and Markdown through the UI while staying in sync with GitHub. You grant access so the client can read (and write, if you enable it) the repo that backs your vault.

完全なオフライン編集にはローカル ブラウジングを選択し、ターミナルから Git を選択します。すべてのパスを手動で管理せずに、統合されたコンテナーの作成とリモート同期が必要な場合は、GitHub ログインを選択します。

## 2. Git

Install **[Git](https://git-scm.com/downloads)** when you plan to clone, branch, commit, or push (required for both workflows if you use a remote).

チェック：

```text
git --version
```

## 3. エディター/カーソル

Use **Cursor** (or VS Code) with Markdown preview for comfortable editing of `.md` files and YAML frontmatter.

## 4. リポジトリのクローンを作成します (ローカル コピー)

後で GitHub サインインを使用する場合でも、**ローカル クローン** はバックアップ、差分、および一括編集に役立ちます。

```text
git clone https://github.com/<owner>/<repo>.git
cd <repo>
```

Replace **`<owner>`** / **`<repo>`** with your GitHub path.

## 5. 次へ

Continue with **Setup** in this Intro folder for branch, **`src/content`** path, tokens, and OAuth scopes when using GitHub-backed notes.
