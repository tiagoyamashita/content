---
label: "II"
subtitle: "Install & configure"
group: "Git"
order: 2
---
Install & configure
Install Git once per machine, set identity, and prefer **SSH** (or HTTPS with credential helper) for GitHub/GitLab.

## 1. Install

| OS | Command / source |
|----|------------------|
| **Windows** | [git-scm.com](https://git-scm.com) or `winget install Git.Git` |
| **macOS** | Xcode CLT or `brew install git` |
| **Linux** | `sudo apt install git` / `dnf install git` |

Verify:

```bash
git --version
```

## 2. Identity (required for commits)

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the **same email** as your GitHub account if you want commits linked on your profile.

View settings:

```bash
git config --global --list
```

| Scope | Flag | Use |
|-------|------|-----|
| System | `--system` | All users |
| Global | `--global` | Your user (`~/.gitconfig`) |
| Local | `--local` | Current repo only (overrides global) |

## 3. Default branch name

```bash
git config --global init.defaultBranch main
```

## 4. SSH key for GitHub

```bash
ssh-keygen -t ed25519 -C "you@example.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub   # paste into GitHub → Settings → SSH keys
ssh -T git@github.com
```

Clone with SSH:

```bash
git clone git@github.com:owner/repo.git
```

Step-by-step on the **GitHub website** (deploy keys, SSO, multiple keys): [GitHub — SSH keys](../github/iv-ssh-keys.md).

## 5. SSH config for Git remotes

When **any program** runs Git against a remote — terminal, **Cursor**, VS Code, GUI client, hook script — Git invokes **SSH** for `git@github.com:…` URLs. SSH reads **`~/.ssh/config`** to decide **which private key** to use. Without this file, SSH may offer the wrong key and you get **`Permission denied (publickey)`**.

**File:** `~/.ssh/config` (create if missing). Permissions: **`chmod 600 ~/.ssh/config`** (and `700` on `~/.ssh/`).

### Single GitHub key (most common)

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  AddKeysToAgent yes
```

| Directive | Purpose |
|-----------|---------|
| **`HostName`** | Real server (always `github.com` for GitHub) |
| **`User git`** | GitHub’s Git user — required |
| **`IdentityFile`** | Path to **private** key (not `.pub`) |
| **`IdentitiesOnly yes`** | Use only this key for this host — avoids trying every key in the agent |
| **`AddKeysToAgent yes`** | Load key into `ssh-agent` (Linux/macOS; see Windows below) |

Test (same as before):

```bash
ssh -T git@github.com
git ls-remote git@github.com:owner/repo.git
```

### Multiple GitHub identities (work + personal)

Use **Host aliases** — same `HostName`, different keys:

```sshconfig
Host github.com-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal
  IdentitiesOnly yes

Host github.com-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
  IdentitiesOnly yes
```

Point **remotes** at the alias (not `github.com`):

```bash
git clone git@github.com-work:mycompany/project.git
git remote set-url origin git@github.com-personal:me/side-project.git
```

SSH matches the **`Host`** line; GitHub still sees a normal connection to `github.com`.

### Per-repo override (Git config)

When one repo must always use a specific key:

```bash
git config core.sshCommand "ssh -i ~/.ssh/id_ed25519_work -o IdentitiesOnly=yes"
```

Stored in **`.git/config`** for that repo only — overrides default SSH config for all remote operations in that clone.

### One-off shell override

```bash
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes" git push
```

Useful in scripts when you cannot rely on `~/.ssh/config`.

### How apps pick this up

```text
IDE / script / terminal
    → git fetch | push | pull
        → ssh git@github.com (or git@github.com-work)
            → reads ~/.ssh/config
            → uses IdentityFile for matching Host
```

| Environment | Notes |
|-------------|--------|
| **macOS** | Add `UseKeychain yes` under `Host` to store passphrase in Keychain |
| **Windows (Git Bash / OpenSSH)** | Config at **`C:\Users\you\.ssh\config`** — same syntax |
| **WSL** | Use WSL’s `~/.ssh/config`; Windows Git and WSL do not share keys unless you link files |
| **CI (GitHub Actions)** | Uses **`GITHUB_TOKEN`** or deploy keys — not your laptop `~/.ssh/config` |

**macOS Keychain example:**

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  IdentitiesOnly yes
  AddKeysToAgent yes
  UseKeychain yes
```

After editing config, re-test:

```bash
ssh -T git@github.com
# or
ssh -T git@github.com-work
```

## 6. HTTPS alternative

```bash
git clone https://github.com/owner/repo.git
```

Use **credential manager** (Git for Windows includes one) or **fine-grained PAT** — avoid embedding passwords in URLs.

## 7. Useful global defaults

```bash
git config --global pull.rebase false    # merge on pull (default); see v-remotes
git config --global fetch.prune true     # drop stale remote-tracking branches
git config --global color.ui auto
git config --global core.editor "code --wait"   # VS Code / Cursor
```

## 8. First repo

```bash
mkdir myproject && cd myproject
git init
echo "# My project" > README.md
git add README.md
git commit -m "Initial commit"
```

Link to GitHub (after creating empty repo on site):

```bash
git remote add origin git@github.com:you/myproject.git
git push -u origin main
```

**Related:** [Everyday commands](iii-everyday-commands.md), [GitHub — SSH keys](../github/iv-ssh-keys.md), **GitHub** → repositories note.
