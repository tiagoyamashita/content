---
label: "IV"
subtitle: "データベース、認証、ストレージ"
group: "スタートアップ"
order: 4
---
データベース、認証、ストレージ

VM への Postgres のインストールをスキップします。 **管理された無料枠** により、データベース、認証、バックアップと TLS を備えたファイル ストレージが提供されます。

## 1. データベース + サービスとしてのバックエンド

|プロバイダー |無料利用枠 (通常) |含まれるもの |
|----------|----------|----------|
| **[スーパーベース](3)** |プロジェクトの制限 | Postgres、認証、ストレージ、リアルタイム |
| **[Firebase](4)** |スパークプラン | Firestore/リアルタイム DB、認証、ホスティング |
| **[ネオン](5)** |サーバーレス Postgres |分岐、ゼロまでスケール |
| **[プラネットスケール](6)** |趣味 | MySQL 互換 (現在の製品を確認してください) |
| **[MongoDB アトラス](7)** | M0クラスター |ドキュメントDB |

```text
Supabase quick mental model:
  Postgres  ←  SQL migrations, RLS policies
  Auth      ←  email magic link, OAuth (Google, GitHub)
  Storage   ←  S3-like buckets with policies
```

## 2. 認証

|オプション |いつ |
|------|------|
| **Supabase / Firebase 認証** | BaaS はすでに選択されています |
| **[事務員](8)** |洗練された UI コンポーネント。無料の MAU キャップ |
| **[認証0](9)** |開発者向けの無料枠。後でエンタープライズ |
| **NextAuth / Auth.js** |アプリ内のセルフホスト型 OAuth |

**OAuth** (Google/GitHub でサインイン) を使用して、早期にパスワードを保存しないようにします。

## 3. ファイルとオブジェクトのストレージ

|サービス |無料ノート |
|-----------|-----------|
| **スーパーベース ストレージ** |プロジェクトにバンドルされています |
| **Cloudflare R2** |無料のストレージ。 Cloudflare への下り料金なし |
| **AWS S3** | 5 GB の無料枠 (新規アカウントの場合は 12 か月) |
| **Firebase ストレージ** |スパーク制限 |

アップロードをサーバーレス **一時ディスク**に保存しないでください。署名された URL を持つオブジェクト ストレージを使用してください。

## 4. 秘密

|アプローチ | MVP |
|----------|-----|
|プラットフォーム環境変数 | Vercel / レンダリング ダッシュボード |
| **GitHub の秘密** | CI のみ |
| **ドップラー / 非フィジカル** |同期用の無料チーム層 |

実稼働キーを使用して `.env` をコミットしないでください。

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
|ベンダーロックインの懸念 |データをエクスポートします。標準の Postgres が役立つ |

**関連:** CS101 **データベース** サブメニュー、RLS/認証深度の Supabase スキル。
