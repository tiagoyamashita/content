---
label: "I"
subtitle: "Installation"
group: "Getting started"
order: 1
---
Getting started — Intro: Installation
How to open and edit notes on disk, or connect GitHub so the app can host your vault.

## 1. Two ways to work

**Browse your files (local)**  
Clone or download this repository and **open the folder in Cursor**. Your notes are Markdown under **`src/content/`**. You do **not** need to sign in to GitHub just to read or edit files on your machine—Explorer and search behave like any project.

**Sign in with GitHub (vault)**  
Use **GitHub login** in the Notes flow when you want the program to **create your vault** and **manage notes** against your repository—creating folders, `_meta.json`, and Markdown through the UI while staying in sync with GitHub. You grant access so the client can read (and write, if you enable it) the repo that backs your vault.

Pick local browsing for full offline editing and Git from the terminal; pick GitHub login when you want integrated vault creation and remote sync without hand-maintaining every path.

## 2. Git

Install **[Git](https://git-scm.com/downloads)** when you plan to clone, branch, commit, or push (required for both workflows if you use a remote).

Check:

```text
git --version
```

## 3. Editor / Cursor

Use **Cursor** (or VS Code) with Markdown preview for comfortable editing of `.md` files and YAML frontmatter.

## 4. Clone the repo (local copy)

Even if you later use GitHub sign-in, a **local clone** is useful for backups, diffs, and bulk edits:

```text
git clone https://github.com/<owner>/<repo>.git
cd <repo>
```

Replace **`<owner>`** / **`<repo>`** with your GitHub path.

## 5. Next

Continue with **Setup** in this Intro folder for branch, **`src/content`** path, tokens, and OAuth scopes when using GitHub-backed notes.
