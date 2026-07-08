---
label: "III"
subtitle: "アクション、問題、設定"
group: "GitHub"
order: 3
---
アクション、問題、設定


GitHub **Actions** run CI/CD on events. **Issues** track work. **Settings** lock down `main` and secrets.

## 1. GitHub アクション (CI スケッチ)

Workflow file: **`.github/workflows/ci.yml`**

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
          cache: npm
      - run: npm ci
      - run: npm test
```

| Concept | Meaning |
|---------|---------|
| **Workflow** | YAML file |
| **Trigger** | `push`, `pull_request`, `schedule` |
| **Job** | Runs on one runner |
| **Step** | Command or action |

詳細: CI/CD **ツールとプラットフォーム → GitHub アクション**。

## 2. アクションの秘密

**設定 → シークレットと変数 → アクション**

```yaml
env:
  API_KEY: ${{ secrets.API_KEY }}
```

| Scope | Use |
|-------|-----|
| Repository secret | One repo |
| Environment secret | `production` deploy only |
| Organization secret | Shared across repos |

秘密は決して記録しないでください。フォーク PR は、デフォルトではリポジトリ シークレットを受け取りません。

## 3. ブランチ保護

**Settings → Branches → Add rule** for `main`:

|ルール |なぜ |
|------|-----|
|プルリクエストが必要 |直接プッシュはありません |
|ステータスチェックが必要 | CI を渡す必要があります |
|レビューが必要 |人間の門 |
|線形履歴が必要 |オプション - マージコミットなし |
|プッシュできる人を制限する |管理者のみがバイパス |

## 4. 問題とプロジェクト

| Feature | Use |
|---------|-----|
| **Issues** | Bugs, features, tasks |
| **Labels** | `bug`, `enhancement`, `good first issue` |
| **Milestones** | Release grouping |
| **Projects** | Kanban board across repos |

Link PRs with `Fixes #N` to auto-close.

## 5. GitHub コパイロットとコードスペース (オプション)

|製品 |メモ |
|----------|----------|
| **副操縦士** | AI は IDE をサポート — サブスクリプション |
| **コードスペース** |クラウド開発環境 — 使用量の請求 |
| **.devcontainer** |再現可能なコードスペース構成 |

基本的な GitHub の使用には必要ありません。

## 6. トークンとセキュリティ

| Token type | When |
|------------|------|
| **Fine-grained PAT** | Scripts, Notes app — minimal repo scope |
| **Classic PAT** | Legacy — broad `repo` scope |
| **GitHub App** | Integrations, org-wide — preferred for tools |
| **SSH key** | Git push/pull |

アカウントで **2FA** を有効にします。組織がそれを要求する場合があります。

「**セットアップ** の開始」メモでは、このメモ アプリの OAuth スコープについて説明しています。

## 7. 通知

リポジトリを見る → **参加および @メンション** または **すべてのアクティビティ**。 **[設定] → [通知]** でメールとウェブを調整します。

## 8. GitHub ページ

リポジトリからの無料の静的ホスティング:

**Settings → Pages** → source branch `main` / `/docs` or Actions workflow.

代替案: Vercel/Netlify (スタートアップの無料サービスに関する注記)。

## 9. 新しいリポジトリのチェックリスト

- [ ] README with setup
- [ ] `.gitignore` appropriate to stack
- [ ] LICENSE file
- [ ] Branch protection on `main`
- [ ] CI workflow on PR
- [ ] Dependabot or Renovate (optional)
- [ ] Secret scanning enabled (public repos default)

**Related:** CI/CD security (pin actions, OIDC), **Git** workflows note, [Contribution graph](activity-contribution-graph.md).
