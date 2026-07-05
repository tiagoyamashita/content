---
label: "VIII"
subtitle: "Secrets in history"
group: "Git"
order: 8
---
Secrets and sensitive files in history

Adding **`.env`** to **`.gitignore`** only stops **future** commits. If the file was ever committed, it remains in **Git history** — clones, forks, and cached GitHub archives can still expose it. **Rotate the secret first**, then find it, then rewrite history.

Prevention: [Everyday commands — `.gitignore`](iii-everyday-commands.md#5-gitignore), [Workflows — what not to commit](vii-workflows-and-conventions.md#8-what-not-to-commit).

## 1. Files and patterns to hunt for

| Risky path / pattern | Often contains |
|----------------------|----------------|
| **`.env`**, **`.env.local`**, **`.env.production`** | DB URLs, API keys, JWT secrets |
| **`credentials.json`**, **`serviceAccountKey.json`** | Cloud provider keys |
| **`*.pem`**, **`id_rsa`**, **`*.p12`**, **`*.key`** | TLS or SSH private keys |
| **`config/secrets.yml`**, **`appsettings.Development.json`** | App secrets |
| **`.aws/credentials`**, **`.npmrc`** (with token) | CLI auth tokens |
| Hard-coded in source | `password=`, `api_key`, `BEGIN PRIVATE KEY` |

## 2. Find sensitive files in history

Run from the **repo root**. These commands search **all branches and tags**.

### Did a path ever exist?

```bash
git log --all --full-history -- .env
git log --all --full-history -- .env.local
git log --all --oneline --name-only -- '*.env'
```

| Flag | Meaning |
|------|---------|
| **`--all`** | Every branch and tag |
| **`--full-history`** | Include commits before renames/deletes |
| **`-- path`** | Limit to that file or glob |

First commit that added the file:

```bash
git log --all --diff-filter=A --summary -- .env
```

### List every path that ever appeared

```bash
git log --all --pretty=format: --name-only | sort -u | grep -E '\.(env|pem|key)$|^\.env'
```

Broader scan for env-like names:

```bash
git log --all --pretty=format: --name-only | sort -u | grep -iE 'env|secret|credential|password|\.pem|id_rsa'
```

### Search file **contents** in history

When the secret is inside a committed file (or a renamed path):

```bash
git log -p --all -S 'sk_live_' --source --all
git log -p --all -G 'API_KEY\s*=' -- '*.env' '*.json' '*.yml'
```

| Option | Use |
|--------|-----|
| **`-S 'string'`** | Pickaxe — commits that add/remove that exact string |
| **`-G 'regex'`** | Commits where diff matches regex |

Search all blobs (can be slow on large repos):

```bash
git grep -i 'BEGIN RSA PRIVATE KEY' $(git rev-list --all)
git grep -i 'password' $(git rev-list --all) -- '*.env' '*.json'
```

### Show what was in an old revision

```bash
git show abc1234:.env
git show main~10:credentials.json
```

### Automated scanners (recommended for teams)

| Tool | Command / where |
|------|-----------------|
| **[gitleaks](https://github.com/gitleaks/gitleaks)** | `gitleaks detect --source . -v` |
| **[trufflehog](https://github.com/trufflesecurity/trufflehog)** | `trufflehog git file://. --only-verified` |
| **GitHub** | **Settings → Code security** — secret scanning, push protection |

Run locally **before** force-pushing a cleanup so you know nothing remains.

## 3. Stop tracking going forward (not enough alone)

```bash
git rm --cached .env
echo ".env" >> .gitignore
git commit -m "chore: stop tracking .env"
git push
```

The file disappears from **HEAD** but **old commits still contain it**. You must rewrite history (next section) if it was ever pushed.

## 4. Remove files from entire history

**Order of operations:**

1. **Rotate / revoke** every exposed key, password, and token — assume it is public.
2. **Back up** the repo (`git clone --mirror`).
3. **Rewrite history** locally.
4. **Verify** with the find commands again.
5. **`git push --force-with-lease`** — coordinate with anyone else using the repo.
6. Teammates **re-clone** or hard-reset — old clones still have the secret.

### Option A — `git filter-repo` (recommended)

Install: [git-filter-repo](https://github.com/newren/git-filter-repo) (`pip install git-filter-repo` or OS package).

Remove one file everywhere:

```bash
git filter-repo --path .env --invert-paths
```

Remove several paths:

```bash
git filter-repo --path .env --path .env.local --path credentials.json --invert-paths
```

Remove by glob:

```bash
git filter-repo --path-glob '*.env' --path-glob '*.pem' --invert-paths
```

Replace leaked strings inside remaining files (e.g. password in `config.yml`):

```bash
# replacements.txt — one line per replacement: literal==>replacement
# password123==>***REMOVED***
git filter-repo --replace-text replacements.txt
```

`git filter-repo` rewrites commits and **removes the `origin` remote** by default — re-add and force-push:

```bash
git remote add origin git@github.com:owner/repo.git
git push --force-with-lease --all
git push --force-with-lease --tags
```

### Option B — BFG Repo-Cleaner

```bash
# delete file from all history
bfg --delete-files .env
bfg --delete-files '{*.pem,*.key}'

# replace text in blobs
bfg --replace-text secrets.txt   # password123==>REMOVED

git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force-with-lease --all
```

Run BFG on a **fresh mirror clone** for large repos.

### Option C — `git filter-branch` (legacy)

Prefer **filter-repo**. Only if you have no alternative:

```bash
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all
```

Then expire reflog and gc as with BFG.

## 5. Verify cleanup

```bash
git log --all --full-history -- .env          # should show nothing
git grep -i 'sk_live_' $(git rev-list --all)  # should show nothing
gitleaks detect --source . -v
```

On GitHub: check **Security → Secret scanning alerts**; re-run or close alerts after rotation.

## 6. Force push and team coordination

```bash
git push --force-with-lease origin main
```

| | **`--force-with-lease`** | **`--force`** |
|--|---------------------------|---------------|
| Safety | Fails if remote moved since your fetch | Overwrites remote regardless |
| Team | Prefer this | Avoid on shared branches |

After rewrite:

- Open PRs against old history may break — close and reopen.
- CI caches keyed by old SHAs may need clearing.
- **Forks** and **clones** still hold old objects until deleted/refreshed.
- GitHub may retain objects briefly; **rotation** remains mandatory.

## 7. GitHub-specific steps

| Action | Where |
|--------|--------|
| Enable **secret scanning** | Repo → Settings → Code security |
| Enable **push protection** | Blocks commits containing known secret patterns |
| Revoke leaked **PAT** / deploy key | Settings → Developer settings / Deploy keys |
| Report exposed **org** secrets | Rotate in vault; audit Actions secret usage |

If a **public** repo leaked a key, treat it as **compromised** even after history rewrite.

## 8. Prevention checklist

| Layer | Practice |
|-------|----------|
| **`.gitignore`** | `.env`, `*.pem`, local config — [Everyday commands](iii-everyday-commands.md#5-gitignore) |
| **Pre-commit** | `gitleaks protect --staged` or similar hook |
| **CI** | Secret scan on PRs |
| **Config** | Env vars, GitHub Actions **secrets**, vault — not files in Git |
| **Review** | Scan `git diff` before commit for `password`, `token`, `private_key` |

## 9. Quick decision guide

| Situation | Action |
|-----------|--------|
| `.env` never committed | Add to `.gitignore` only |
| Committed, **not pushed** | Remove file, `git reset` or amend, fix `.gitignore` |
| Committed and **pushed** | **Rotate secret** → `git filter-repo` → verify → `--force-with-lease` |
| Secret in **public** repo | Rotate immediately; assume breach; audit access logs |
| Unsure what leaked | `git log -p --all -S`, `gitleaks detect`, GitHub alerts |

**Related:** [Undo & history](vi-undo-and-history.md), [GitHub — Actions, issues & settings](../github/iii-actions-issues-and-settings.md) (repository secrets), [Workflows & conventions](vii-workflows-and-conventions.md).
