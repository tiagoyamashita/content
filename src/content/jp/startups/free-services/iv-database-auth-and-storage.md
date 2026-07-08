---
label: "IV"
subtitle: "データベース、認証、ストレージ"
group: "スタートアップ"
order: 4
---
データベース、認証、ストレージ

VM への Postgres のインストールはスキップします。 **管理された無料利用枠** により、データベース、認証、バックアップと TLS を備えたファイル ストレージが提供されます。

## 1. データベース + サービスとしてのバックエンド

| Provider | Free tier (typical) | Includes |
|----------|---------------------|----------|
| **[Supabase](https://supabase.com)** | Project limits | Postgres, auth, storage, realtime |
| **[Firebase](https://firebase.google.com)** | Spark plan | Firestore/Realtime DB, auth, hosting |
| **[Neon](https://neon.tech)** | Serverless Postgres | Branching, scale-to-zero |
| **[PlanetScale](https://planetscale.com)** | Hobby | MySQL-compatible (check current offering) |
| **[MongoDB Atlas](https://www.mongodb.com/atlas)** | M0 cluster | Document DB |

```text
Supabase quick mental model:
  Postgres  ←  SQL migrations, RLS policies
  Auth      ←  email magic link, OAuth (Google, GitHub)
  Storage   ←  S3-like buckets with policies
```

## 2. 認証

| Option | When |
|--------|------|
| **Supabase / Firebase Auth** | BaaS already chosen |
| **[Clerk](https://clerk.com)** | Polished UI components; free MAU cap |
| **[Auth0](https://auth0.com)** | Free tier for dev; enterprise later |
| **NextAuth / Auth.js** | Self-hosted OAuth in your app |

**OAuth** (Google でサインイン/GitHub) を使用して、早期にパスワードを保存しないようにします。

## 3. ファイルとオブジェクトのストレージ

|サービス |無料ノート |
|-----------|-----------|
| **スーパーベース ストレージ** |プロジェクトにバンドルされています |
| **Cloudflare R2** |無料のストレージ。 Cloudflare への下り料金なし |
| **AWS S3** | 5 GB 無料枠 (新規アカウントの場合は 12 か月) |
| **Firebase ストレージ** |スパーク制限 |

アップロードをサーバーレス **一時ディスク**に保存しないでください。署名された URL を持つオブジェクト ストレージを使用してください。

## 4. 秘密

|アプローチ | MVP |
|----------|-----|
|プラットフォーム環境変数 | Vercel / レンダリング ダッシュボード |
| **GitHub の秘密** | CI のみ |
| **ドップラー / 非フィジカル** |同期用の無料チーム層 |

Do not commit `.env` with production keys.

## 5. 環境レイアウトの例

```bash
DATABASE_URL=postgresql://...
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=eyJ...          # public, RLS protects data
SUPABASE_SERVICE_ROLE_KEY=...     # server only — never expose to browser
RESEND_API_KEY=re_...
```

## 6. 無料の BaaS をやめるべき場合

|信号 |検討してください |
|----------|----------|
|接続プールの制限 |専用 Postgres (RDS、Neon 有料) |
|複雑なクエリ / RLS の痛み |独自のバックエンド + ORM |
|ベンダーロックインの懸念 |データをエクスポートします。標準 Postgres が役に立ちます。

**関連:** CS101 **データベース** サブメニュー、RLS/auth 深さの Supabase スキル。
