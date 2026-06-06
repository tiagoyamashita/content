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

## 5. HTTPS alternative

```bash
git clone https://github.com/owner/repo.git
```

Use **credential manager** (Git for Windows includes one) or **fine-grained PAT** — avoid embedding passwords in URLs.

## 6. Useful global defaults

```bash
git config --global pull.rebase false    # merge on pull (default); see v-remotes
git config --global fetch.prune true     # drop stale remote-tracking branches
git config --global color.ui auto
git config --global core.editor "code --wait"   # VS Code / Cursor
```

## 7. First repo

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

**Related:** [Everyday commands](iii-everyday-commands.md), **GitHub** → repositories note.
