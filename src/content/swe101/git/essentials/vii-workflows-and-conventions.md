---
label: "VII"
subtitle: "ワークフローと規約"
group: "Git"
order: 7
---
ワークフローと規約

**ブランチ名**、**コミット メッセージ**、**マージ戦略**に関するチームの合意により、Git が競合の原因になるのを防ぎます。

## 1. GitHub フロー (スタートアップに共通)

```text
main ── always deployable
  │
  └── feature/* ── PR ── review ── merge ── delete branch
```

| Rule | Detail |
|------|--------|
| **`main` protected** | No direct push; require PR + CI |
| **Short-lived branches** | Days, not months |
| **Small PRs** | Easier review |

代替案: **Gitflow** (リリースブランチ) — より重い。 **トランクベース** (機能フラグ) — 成熟した CI 向け。

## 2. ブランチの命名

```text
feature/add-oauth-login
fix/null-pointer-checkout
docs/api-readme
chore/deps-bump
```

Include ticket ID if using Jira/Linear: `feature/PROJ-123-oauth`.

## 3. 従来のコミット

```text
feat: add password reset email
fix: prevent double submit on checkout
docs: document env vars
chore: bump eslint
refactor: extract mail service
test: cover auth controller
```

Format: **`type(scope): description`**

利点: 読み取り可能なログ、自動変更ログ ツール、セマンティック リリース。

## 4. プルリクエストのチェックリスト

- [ ] Branch up to date with `main` (rebase or merge)
- [ ] CI green
- [ ] Self-review diff
- [ ] Description explains **why**, not only what
- [ ] Screenshots for UI changes
- [ ] Migration notes if DB/API breaking

## 5. `.gitattributes` (optional)

```gitattributes
* text=auto eol=lf
*.bat text eol=crlf
```

Windows/macOS/Linux チームの行末を正規化します。

## 6. フック (現地品質のゲート)

```bash
# .git/hooks/pre-commit — or use husky / pre-commit framework
#!/bin/sh
npm test
```

**pre-commit** (Python ツール) — リポジトリ内の共有フック:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
```

## 7. モノリポジトリとポリリポジトリ

| | Monorepo | Polyrepo |
|---|----------|----------|
| Structure | Many projects, one Git repo | One repo per service |
| CI | Path filters (`paths:` in Actions) | Per-repo pipelines |
| Git | Shared history, large clone | Smaller clones |

Git も同様に機能します。Git 機能ではなく組織の選択です。

## 8. コミットしてはいけないこと

| Never | Instead |
|-------|---------|
| `.env`, API keys | Env vars, secret manager |
| `node_modules/`, `target/` | `.gitignore` + CI install |
| Large binaries | Git LFS or object storage |
| Generated build output | CI builds artifacts |

## 9. リハーサルの答え

- **GitHub Flow** — PRs into deployable `main`.
- **Revert vs reset** — revert for shared/pushed; reset for local cleanup.
- **Conventional Commits** — structured `type: message` for clarity and tooling.

**関連:** **GitHub** (ブランチ保護、PR)、CI/CD の基本。
