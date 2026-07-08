---
label: "III"
subtitle: "アイデンティティ・アクセス・シークレット"
group: "Cybersecurity"
order: 3
---
アイデンティティ・アクセス・シークレット
多くの侵害は**盗まれた・悪用された資格情報**が関与します。強い**アイデンティティ**、**最小権限アクセス**、**シークレットの衛生**が現実の攻撃の多くを防ぎます。

## 1. 認証と認可

| 用語 | 問い | 仕組み |
|------|----------|-----------|
| **認証（AuthN）** | あなたは誰？ | パスワード、パスキー、SSO、API キー |
| **認可（AuthZ）** | 何をしてよい？ | RBAC、ABAC、ポリシーエンジン |

```text
Login (AuthN) → session/JWT issued → each request checked against roles/policies (AuthZ)
```

混同しないこと: 有効なログインは**すべてのリソースへのアクセス**を意味しません。

## 2. アイデンティティのパターン

| パターン | 向く用途 | 注意点 |
|---------|-----|-----------|
| **ローカル ID/パスワード** | 小規模アプリ、開発 | 弱いパスワード、MFA なし |
| **SSO（SAML/OIDC）** | 企業、B2B | リダイレクト URI の誤設定 |
| **ソーシャルログイン** | コンシューマ向け | アカウント連携のバグ |
| **サービスアカウント** | マシン間 | リポジトリ内の長寿命キー |
| **ワークロード ID** | K8s、クラウド VM | 広すぎる IAM ロール |

**推奨:** 人間には中央 IdP（Okta、Entra ID、Google Workspace）+ **MFA**。マシンには**短命トークン**。

## 3. MFA とパスキー

| 要素 | 例 |
|--------|---------|
| **知識**（know） | パスワード |
| **所有**（have） | TOTP アプリ、ハードウェアキー、プッシュ承認 |
| **生体**（are） | 生体認証（デバイス紐づけ） |

| 方針 | 推奨 |
|--------|----------------|
| 管理者 / 本番アクセス | **MFA 必須** |
| 顧客アカウント | MFA 任意 → 高価値操作では推奨 |
| API 自動化 | パスワードなし — スコープ付きトークン + ローテーション |

**パスキー（WebAuthn）** はフィッシングを減らします。資格情報はサイトのオリジンに紐づき、再利用可能なパスワードがありません。

## 4. 認可モデル

**RBAC** = **R**ole-**B**ased **A**ccess **C**ontrol（**ロールベースアクセス制御**）。共通の末尾 **BAC** は **Based Access Control**（**ベースドアクセス制御**）— アクセス判断が**ルール**（ロール、属性、関係）に従い、各エンドポイントでユーザーごとの ad-hoc チェックにならないこと、を意味します。

| 略語 | 正式名称 | 「B」の意味 |
|---------|-----------|--------------|
| **RBAC** | Role-**Based** Access Control | **ロール**（例: `editor`、`admin`） |
| **ABAC** | Attribute-**Based** Access Control | **属性**（部署、クリアランス、時刻） |
| **ReBAC** | Relationship-**Based** Access Control | **関係**（ドキュメントの所有者、チームメンバー） |

| モデル | 考え方 | 例 |
|-------|------|---------|
| **RBAC** | ロール → 権限 | `billing_admin` が返金可能 |
| **ABAC** | ユーザー + リソースの属性 | `department=finance` AND `amount<1000` |
| **ReBAC** | 関係（グラフ） | Google Zanzibar 型「ドキュメント X の編集者」 |

原則:

| 原則 | 実践 |
|-----------|----------|
| **最小権限** | デフォルト拒否。必要最小限のみ付与 |
| **職務分離** | デプロイ担当 ≠ 本番承認者 |
| **ブレークグラス** | 緊急 admin は追加ログ付き |
| **定期的アクセスレビュー** | 四半期: まだこのロールが必要な人は誰か？ |

## 5. セッションとトークンの衛生

| 問題 | 緩和 |
|-------|------------|
| 盗まれたセッション Cookie | `HttpOnly`、`Secure`、`SameSite`、短い TTL |
| localStorage の JWT | httpOnly Cookie またはメモリ + リフレッシュローテーションを優先 |
| スコープ過大の JWT | 小さな audience。短い有効期限。`iss`/`aud` を検証 |
| リフレッシュトークン再利用 | 再利用検知 → ファミリー全体を失効 |

```text
Access token:  short (minutes)
Refresh token: longer, rotatable, stored carefully
API key:       scoped, auditable, revocable
```

## 6. シークレット — git に入れない

| 種類 | 保管場所 | アンチパターン |
|-------------|-------|--------------|
| DB パスワード | Vault、クラウドシークレットマネージャー、CI シークレット | リポジトリの `config.yml` |
| API キー | 実行時 env、可能なら OIDC | README の Slack webhook |
| TLS 秘密鍵 | KMS、cert manager | コミットされた `.pem` |
| 暗号化キー | HSM / KMS | ソースにハードコード |

**CI/CD:** 静的 AWS キーの代わりにプラットフォームシークレット + **クラウドへの OIDC**（[シークレットと OIDC](../sre101/cicd/security-and-best-practices/iii-secrets-and-oidc.md)）。

| 検知 | ツール |
|-----------|---------|
| pre-commit | `gitleaks`、`trufflehog` |
| CI | すべての PR でシークレットスキャン |
| 対応 | 漏洩時は即ローテーション |

## 7. クラウドのマシンアイデンティティ

| ワークロード | パターン |
|----------|---------|
| Lambda / Cloud Run | 最小 IAM の実行ロール |
| Kubernetes Pod | IRSA / ワークロード ID — ノード全体の creds は使わない |
| GitHub Actions → AWS | リポジトリ/環境ごとの OIDC `role-to-assume` |

```text
Bad:  one shared "prod-admin" key on every service
Good: service A role can only read queue X; service B only write table Y
```

## 8. アクセスチェックリスト（本番）

| 確認 | 合格基準 |
|-------|---------------|
| 人間の管理者 | SSO + MFA、共有アカウントなし |
| 本番データアクセス | ロールベース、ログ、可能なら時間制限 |
| サービスアカウント | サービスごとに命名。ボットにユーザーパスワードなし |
| シークレット | 中央保管。ローテーションカレンダー |
| 退職 | IdP 無効化で同日アクセス削除 |

## 9. リハーサル問題

- AuthN と AuthZ をそれぞれ 1 文で説明せよ。
- プライベートリポジトリでも git 内の長寿命 API キーが危険な理由は？
- ステージングへデプロイする CI ジョブでの最小権限とは？
- 盗難リスクを下げる Cookie フラグを 2 つ挙げよ。

**関連:** [脅威モデリング](ii-threat-modeling-and-risk.md)、[アプリケーションセキュリティ](iv-application-and-network-security.md)、[CI/CD 最小権限ランナー](../sre101/cicd/security-and-best-practices/iv-least-privilege-runners.md)。
