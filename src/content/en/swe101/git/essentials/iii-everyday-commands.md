---
label: "III"
subtitle: "Everyday commands"
group: "Git"
order: 3
---
Everyday commands
The commands you run **every day**: inspect state, stage changes, commit, read history.

## 1. Three trees

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 90" role="img" aria-label="Git working tree staging commit">
  <rect x="12" y="36" width="100" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="56" fill="#e4e4e7" font-size="9">Working tree</text>
  <path d="M112 52 H132" stroke="#a1a1aa"/>
  <text x="118" y="48" fill="#71717a" font-size="7">add</text>
  <rect x="132" y="36" width="100" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="152" y="56" fill="#e4e4e7" font-size="9">Staging</text>
  <path d="M232 52 H252" stroke="#a1a1aa"/>
  <text x="238" y="48" fill="#71717a" font-size="7">commit</text>
  <rect x="252" y="36" width="100" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="272" y="56" fill="#e4e4e7" font-size="9">Repository</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Files move left → right into history</text>
</svg></figure>

## 2. Inspect state

```bash
git status              # modified, staged, untracked
git status -sb          # short branch info
git diff                # unstaged changes
git diff --staged       # staged vs last commit
git log --oneline -10   # recent commits
git log --oneline --graph --all   # branch graph
```

## 3. Stage and commit

```bash
git add file.js                 # one file
git add src/                    # directory
git add -p                      # patch — hunk by hunk
git add -A                      # all changes (careful)

git commit -m "fix: handle null user id"
git commit -am "docs: update README"   # skip separate add for tracked files only
```

Write messages in **imperative mood**: "Add feature" not "Added feature".

## 4. Clone existing project

```bash
git clone git@github.com:org/app.git
cd app
```

Clone creates **`origin`** remote and checks out default branch.

## 5. `.gitignore`

Never commit secrets, build output, or OS junk:

```gitignore
# .gitignore
node_modules/
dist/
.env
.env.local
*.log
.DS_Store
target/
.idea/
```

If a file was committed by mistake, see [Secrets in history](viii-secrets-and-sensitive-files-in-history.md) — removing from `.gitignore` alone is not enough.

## 6. Show one commit

```bash
git show abc1234
git show HEAD~1 --stat
```

## 7. Compare branches

```bash
git diff main..feature/login
git log main..feature/login --oneline
```

## 8. Common status lines

| Status | Meaning |
|--------|---------|
| **Untracked** | New file — not in Git yet |
| **Modified** | Changed since last commit |
| **Staged** | Will be in next commit |
| **Clean** | Nothing to commit |

## 9. Quick reference

| Task | Command |
|------|---------|
| What changed? | `git status`, `git diff` |
| Save snapshot | `git add` + `git commit` |
| History | `git log --oneline --graph` |
| Who edited line? | `git blame file.js` |

**Related:** [Branching & merging](iv-branching-and-merging.md), [Workflows & conventions](vii-workflows-and-conventions.md).
