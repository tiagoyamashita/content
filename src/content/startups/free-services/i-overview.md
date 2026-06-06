---
label: "I"
subtitle: "概要"
group: "スタートアップ"
order: 1
---
無料サービス — 概要

初期段階の製品に役立つ厳選された**無料枠**。制限の変更 - 本番環境の数値に依存する前に、必ずベンダーのサイトを確認してください。

## このサブメニューのマップ

|注 |フォーカス |
|------|----------|
| [電子メールと郵送](ii-email-and-mailing.md) |トランザクション電子メール、ニュースレター、DNS — **ここから始めてください** |
| [ホスティング、ドメイン、CDN](iii-hosting-domains-and-cdn.md) |静的サイト、サーバーレス、DNS、TLS |
| [データベース、認証、ストレージ](iv-database-auth-and-storage.md) | Postgres、認証、ファイル、シークレット |
| [監視、分析、開発ツール](v-monitoring-analytics-and-devtools.md) |エラー、稼働時間、分析、CI |

## 独自のメールサーバーを実行しないでください

```text
❌  EC2 + Postfix on port 25  →  spam folder, blacklists, ops pain
✅  Resend / Brevo / SES API  →  they handle reputation + bounces
```

あなたは引き続き **ドメインを所有しており**、プロバイダーが提供する **SPF、DKIM、DMARC** レコードを追加します。

## 必要に応じて簡単に選択

|必要 |無料の出発点 |
|------|---------------------|
|パスワードのリセット/ウェルカムメール |再送信、Brevo、SendGrid |
|マーケティング ニュースレター | Brevo、MailerLite、ボタンダウン |
| `hello@` を Gmail に転送 | Cloudflareの電子メールルーティング |
| Web アプリのホスティング | Vercel、Netlify、Cloudflare ページ |
|データベース + 認証 |スーパーベース、ファイアベース |
|ファイルのアップロード | Cloudflare R2 (CF への無料下り)、Supabase ストレージ |
|エラー追跡 | Sentry (開発層)、GlitchTip (セルフホスト) |
|稼働時間チェック | UptimeRobot、より良いスタックを無料で提供 |

## コストの現実

| MVP では通常無料 |通常は支払われます |
|---------------------|--------------|
|趣味のホスティング、小規模 DB |カスタム ドメインのメール シート（Google Workspace） |
|電子メールの量が少ない |大量のメール、専用 IP |
|コミュニティサポート |契約 + SLA |

## リハーサル

- トランザクション電子メールとマーケティング電子メール — 同じプロバイダーですか?
- 電子メールの到達性に役立つ 3 つの DNS レコードはどれですか?
