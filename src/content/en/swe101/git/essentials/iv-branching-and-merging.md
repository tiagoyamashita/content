---
label: "IV"
subtitle: "Branching & merging"
group: "Git"
order: 4
---
Branching & merging
**Branches** are cheap pointers — use them for every feature or fix. **Merge** combines histories; resolve **conflicts** when the same lines changed.

## 1. Branch basics

```bash
git branch                    # list local branches
git branch feature/login      # create branch (does not switch)
git switch feature/login      # checkout branch (Git 2.23+)
git switch -c feature/login   # create + switch

git switch main
git merge feature/login       # merge into current branch
git branch -d feature/login   # delete after merge
```

Legacy: `git checkout -b feature/login` — same as `switch -c`.

## 2. Branch diagram

```text
main:     A --- B --- C ----------- M
                      \           /
feature/login:         D --- E ---

merge M combines E into main
```

## 3. Merge types

| Type | When | Result |
|------|------|--------|
| **Fast-forward** | No new commits on main since branch | Linear history |
| **Three-way merge** | Both moved | Merge commit with two parents |

```bash
git merge feature/login
# if conflicts → edit files → git add → git commit
```

## 4. Resolving conflicts

Conflict markers in file:

```text
<<<<<<< HEAD
const timeout = 5000;
=======
const timeout = 10000;
>>>>>>> feature/login
```

Steps:

1. Edit to final desired code (remove markers)
2. `git add conflicted-file`
3. `git commit` (or continue merge)

Abort merge:

```bash
git merge --abort
```

## 5. Rebase (linear history)

Replay your commits on top of updated main:

```bash
git switch feature/login
git fetch origin
git rebase origin/main
```

```text
Before rebase:
  main:    A - B - C
  feature: A - B - D - E

After rebase onto C:
  main:    A - B - C
  feature: A - B - C - D' - E'
```

**Golden rule:** do not rebase commits already **pushed** and shared — rewrites history. OK for local-only or your feature branch before PR merge.

## 6. Merge vs rebase on PR

| Strategy | History | Use |
|----------|---------|-----|
| **Merge commit** | Preserves exact branch shape | Default on GitHub "Create merge commit" |
| **Squash merge** | One commit on main | Clean main log |
| **Rebase merge** | Linear commits replayed | Linear main |

Team picks one convention — document in [Workflows & conventions](vii-workflows-and-conventions.md).

## 7. Detached HEAD

Checking out a commit directly (not a branch) puts you in **detached HEAD** — commits can be lost. Fix:

```bash
git switch -c recover-work
```

## 8. Rehearsal answers

- **Branch** — pointer to a commit; moves on each new commit.
- **Fast-forward** — main simply moves forward to branch tip; no merge commit.
- **Conflict** — same region edited differently; Git cannot auto-pick.

**Related:** [Remotes & collaboration](v-remotes-and-collaboration.md), **GitHub** PRs note.
