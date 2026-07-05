---
label: "IV"
subtitle: "SSH keys"
group: "GitHub"
order: 5
---
GitHub — SSH keys
Use **SSH keys** so `git push`, `git pull`, and `git fetch` authenticate without typing a password. GitHub identifies you by the **public key** you register; your **private key** stays on your machine.

For generating keys locally, see [Install & configure](../essentials/ii-install-and-configure.md). For **`~/.ssh/config`** (pick the right key when apps run Git), see the same note — [SSH config for Git remotes](../essentials/ii-install-and-configure.md#5-ssh-config-for-git-remotes).

## 1. Why SSH for GitHub

| | **SSH** (`git@github.com:…`) | **HTTPS** (`https://github.com/…`) |
|--|-------------------------------|-------------------------------------|
| Auth | Key pair | PAT or credential manager |
| Clone URL | `git@github.com:owner/repo.git` | `https://github.com/owner/repo.git` |
| Typical setup | One key per machine or per identity | Token in OS keychain |

Both work. SSH is common for daily dev once keys are configured.

## 2. Generate a key (local)

On your machine:

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

| Prompt | Suggestion |
|--------|------------|
| **File** | Default `~/.ssh/id_ed25519`, or a named file e.g. `~/.ssh/id_ed25519_github` if you use several keys |
| **Passphrase** | Recommended — unlock with `ssh-agent` / OS keychain so apps can use the key without prompting every time |

Show the **public** key (safe to share):

```bash
cat ~/.ssh/id_ed25519.pub
# or
cat ~/.ssh/id_ed25519_github.pub
```

Copy the full line starting with `ssh-ed25519`.

## 3. Add the key on GitHub

1. Sign in to **GitHub**.
2. Profile photo → **Settings**.
3. **SSH and GPG keys** (under “Access”).
4. **New SSH key**.

| Field | What to enter |
|-------|----------------|
| **Title** | Machine or purpose — e.g. `MacBook Pro`, `Work laptop`, `CI deploy (read-only)` |
| **Key type** | **Authentication Key** (default for dev machines) |
| **Key** | Paste the **`.pub`** file contents (one line) |

5. **Add SSH key** — you may need to confirm password or 2FA.

### Key types on GitHub

| Type | Use |
|------|-----|
| **Authentication Key** | Your user — push/pull any repo your account can access |
| **Signing Key** (GPG/SSH signing) | Verify commit signatures — separate from push auth |
| **Deploy key** (on a **repo**, not account settings) | One repo only — automation or a single server |

**Deploy keys:** repo → **Settings** → **Deploy keys** → **Add deploy key**. Read-only unless you explicitly allow write (use sparingly).

## 4. Test the connection

```bash
ssh -T git@github.com
```

Expected (first time):

```text
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

| Result | Fix |
|--------|-----|
| **`Permission denied (publickey)`** | Wrong key, key not on GitHub, or SSH not using the key you added — check [SSH config](../essentials/ii-install-and-configure.md#5-ssh-config-for-git-remotes) |
| **Wrong GitHub user** | Multiple keys — use `Host` alias in `~/.ssh/config` and matching remote URL |
| **Host key verification failed** | Rare; verify you reach real GitHub (corporate proxy/firewall) |

## 5. Use SSH remotes

```bash
git clone git@github.com:owner/repo.git
```

Existing HTTPS repo:

```bash
git remote -v
git remote set-url origin git@github.com:owner/repo.git
```

Remote format: **`git@github.com:owner/repo.git`** — not `https://`.

## 6. Organization SSO (if prompted)

Some orgs require **SSO authorization** for SSH keys:

1. **Settings** → **SSH and GPG keys**.
2. Find your key → **Configure SSO** → **Authorize** next to the organization.

Without this, push may fail with permission errors even though `ssh -T` works for your user.

## 7. Multiple keys (work vs personal)

GitHub allows **many keys** on one account and many accounts across machines. Locally you choose **which private key** is used via:

- **`~/.ssh/config`** — `Host` + `IdentityFile` (recommended)
- **`GIT_SSH_COMMAND`** or **`core.sshCommand`** — per shell or per repo

Example: work key for `github.com-work`, personal for `github.com-personal` — full setup in [Install & configure — SSH config](../essentials/ii-install-and-configure.md#5-ssh-config-for-git-remotes).

## 8. Security checklist

| Do | Don't |
|----|--------|
| Paste only **`.pub`** files into GitHub | Commit or share **private** keys (no `.pub` suffix) |
| Use a **passphrase** on private keys | Reuse one deploy key for every repo if scopes differ |
| Remove keys when you retire a laptop | Leave ex-employee keys on org repos |
| Prefer **fine-grained PATs** for HTTPS automation | Store PATs in repo source code |

## Related

- [Install & configure](../essentials/ii-install-and-configure.md) — keygen, `ssh-agent`, **`~/.ssh/config`**
- [Remotes & collaboration](../essentials/v-remotes-and-collaboration.md) — `origin`, push/pull
- [Actions, issues & settings](iii-actions-issues-and-settings.md) — tokens vs SSH for CI
