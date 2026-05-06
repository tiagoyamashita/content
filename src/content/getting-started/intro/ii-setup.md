---
label: "II"
subtitle: "Setup"
group: "Getting started"
order: 2
---
Getting started — Intro: Setup
Connect Cursor Notes (or your viewer) to this repo so the sidebar loads **`src/content`**.

## 1. Branch

This repo tracks **`main`**. If your default branch differs, use that branch in settings instead.

## 2. Content path

Set the content root to:

```text
src/content
```

So the app loads **`src/content/_meta.json`** and every topic folder under it (including nested folders such as **`getting-started/intro/`**).

## 3. GitHub settings in Cursor

1. Open **GitHub** settings from the Notes menu.
2. Set **owner** / **repository** to match **`origin`**.
3. Set **branch** to **`main`** (try **`master`** only if your repo still uses it).
4. Paste a **personal access token** with repo read access if the repository is private.

## 4. Refresh

After you push new folders or files, refresh or resync notes so the tree updates.
