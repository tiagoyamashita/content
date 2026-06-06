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

|ルール |詳細 |
|------|----------|
| **`main` 保護されています** |直接的なプッシュはありません。 PR + CI が必要 |
| **寿命の短いブランチ** |数か月ではなく数日 |
| **小規模な PR** |より簡単なレビュー |

代替案: **Gitflow** (ブランチをリリース) — より重い。 **トランクベース** (機能フラグ) — 成熟した CI 用。

## 2. ブランチの命名

```text
feature/add-oauth-login
fix/null-pointer-checkout
docs/api-readme
chore/deps-bump
```

Jira/Linear を使用する場合はチケット ID を含めます: `feature/PROJ-123-oauth`。

## 3. 従来のコミット

```text
feat: add password reset email
fix: prevent double submit on checkout
docs: document env vars
chore: bump eslint
refactor: extract mail service
test: cover auth controller
```

形式: **`type(scope): description`**

利点: 読み取り可能なログ、自動変更ログ ツール、セマンティック リリース。

## 4. プルリクエストのチェックリスト

- [ ] `main` で最新のブランチ (リベースまたはマージ)
- [ ] CI グリーン
- [ ] セルフレビューの差分
- [ ] 説明では、内容だけではなく **なぜ** も説明されています
- [ ] UI変更のスクリーンショット
- [ ] DB/API が壊れた場合の移行メモ

## 5. `.gitattributes` (オプション)

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

| |モノレポ |ポリレポ |
|---|----------|----------|
|構造 |多くのプロジェクト、1 つの Git リポジトリ |サービスごとに 1 つのリポジトリ |
| CI |パスフィルター (アクションの `paths:`) |リポジトリごとのパイプライン |
|ギット |共有履歴、大規模なクローン |より小さいクローン |

Git も同様に機能します。Git の機能ではなく、組織の選択です。

## 8. コミットしてはいけないこと

|決して |代わりに |
|------|-----------|
| `.env`、API キー |環境変数、シークレットマネージャー |
| `node_modules/`、`target/` | `.gitignore` + CI インストール |
|大規模なバイナリ | Git LFS またはオブジェクト ストレージ |
|生成されたビルド出力 | CI ビルドアーティファクト |

## 9. リハーサルの答え

- **GitHub フロー** — デプロイ可能な `main` に PR を追加します。
- **元に戻すとリセット** — 共有/プッシュの場合は元に戻します。ローカルクリーンアップのためにリセットします。
- **従来のコミット** — 明確さとツールのために構造化された `type: message`。

**関連:** **GitHub** (ブランチ保護、PR)、CI/CD の基礎。
