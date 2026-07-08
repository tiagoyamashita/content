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

### Private and public repos

If notes live in a **private** repository (or you switch between private and public repos), whatever loads files from GitHub needs **repository access**, not just profile/email.

- **Consent screen** (“private and public repositories”) for **Sign in with GitHub** is expected when the integration uses OAuth **`repo`** scope so it can call the GitHub API for repo contents.
- **Least privilege alternative:** keep login scopes minimal and use a **fine-grained PAT** with **Contents: Read-only** on selected repos—narrower than classic **`repo`** OAuth scope.

### OAuth scopes (if you build your own GitHub login)

When the server must read **private** repo files via OAuth (classic scopes), request **`repo`** in addition to identity fields, for example **`read:user user:email repo`**.

Auth.js / NextAuth-style provider snippet:

```ts
GitHub({
  authorization: {
    params: {
      scope: "read:user user:email repo",
    },
  },
}),
```

Classic **`repo`** is broad (effectively full repo access for that account). Prefer **fine-grained PATs** or a **GitHub App** with **Contents: Read-only** when you control token issuance.

## 4. Refresh

After you push new folders or files, refresh or resync notes so the tree updates.
