---
label: "VI"
subtitle: "Git sync & team workflows"
group: "Obsidian"
order: 6
---
Obsidian — Part VI
Because a vault is a **folder of Markdown files**, **Git** is a natural sync and collaboration layer. The **Obsidian Git** plugin automates commit/pull/push; teams treat the vault like a small docs repo.

For Git basics, see [Everyday commands](../git/essentials/iii-everyday-commands.md). For `.gitignore` conventions, see [Workflows & conventions](../git/essentials/vii-workflows-and-conventions.md). For CI on a docs repo, see [Fundamentals](../../sre101/cicd/i-fundamentals.md).

## 1. Vault as a Git repository

```bash
cd ~/notes/engineering-vault
git init
git remote add origin git@github.com:you/engineering-vault.git
```

Or use a **subfolder** of an existing repo:

```text
my-product/
  src/
  docs/              ← open this folder as vault in Obsidian
  .git/
```

Same **Git** track — [Overview](../git/i-overview.md) rules apply: meaningful commits, branches for large restructures, PRs for team vaults.

## 2. Obsidian Git plugin

Install **Obsidian Git** from community plugins. Typical settings:

| Setting | Suggestion |
|---------|------------|
| **Vault backup interval** | e.g. 10–30 min auto-commit (optional) |
| **Auto pull on startup** | On for single-user; careful with conflicts on shared vaults |
| **Commit message** | Template: `vault backup: {{date}}` or manual messages for real work |
| **Pull before push** | Enabled — reduces rejected pushes |

Manual workflow from the command palette: **Obsidian Git: Commit all changes**, **Push**, **Pull**.

## 3. What to commit

| Commit | Skip or gitignore |
|--------|-------------------|
| `*.md` notes | `.trash/` |
| `attachments/` (if not huge binaries) | Large video files — use LFS or external storage |
| `.obsidian/plugins/`, shared config | `workspace.json` (personal layout) |
| `templates/` | Machine-specific cache |

Example `.gitignore`:

```gitignore
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.trash/
*.tmp
.DS_Store
```

Never commit **API keys**, **`.env`**, or **tokens** — see [Secrets in history](../git/essentials/viii-secrets-and-sensitive-files-in-history.md).

## 4. Merge conflicts in Markdown

Conflicts appear like any text file:

```markdown
<<<<<<< HEAD
Decision: use Redis for sessions.
=======
Decision: use JWT stateless sessions.
>>>>>>> branch
```

| Approach | When |
|----------|------|
| **Edit manually** | Small vaults, rare overlap |
| **One note per author per day** | Reduces daily-note collisions |
| **Branch per project** | Large restructures |
| **Lock sections** | Social rule: "I own `runbooks/payments/` this week" |

Obsidian does not merge notes automatically — resolve in Git or an external merge tool, then reopen the vault.

## 5. Team vault conventions

| Convention | Detail |
|------------|--------|
| **Naming** | `adr-NNN-slug.md`, `runbook-service-x.md` |
| **Frontmatter schema** | Same `status`, `tags`, `owner` keys for Dataview |
| **Plugin lockfile** | Commit enabled plugins so CI and peers match |
| **PR review** | Treat ADR and runbook changes like code docs |
| **README** | Landing note: how to open vault, required plugins |

## 6. Mobile and other sync options

| Method | Trade-off |
|--------|-----------|
| **Git + mobile Git app** | Free; manual; conflict-prone on daily notes |
| **Obsidian Sync** (paid) | Official; E2E encryption option; low friction |
| **iCloud / Dropbox folder vault** | Easy; weak conflict resolution for simultaneous edits |
| **Working Copy (iOS) + Obsidian** | Common Git-on-mobile pattern |

Pick **one** source of truth — mixing Sync and Git on the same vault causes pain.

## 7. CI on a vault repo (optional)

Light checks on push:

```yaml
# .github/workflows/docs.yml
name: vault-lint
on:
  push:
    paths: ['**.md']
jobs:
  markdown:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: DavidAnson/markdownlint-cli2-action@v16
        with:
          globs: '**/*.md'
```

Add link checking or Mermaid validation if the vault embeds many diagrams.

## Rehearsal

- Why gitignore **`workspace.json`**?
- One risk of **auto-commit every 10 minutes** on a shared vault?

## Next

Continue with [Engineering workflows](vii-engineering-workflows.md) for ADRs, runbooks, and note-taking systems.
