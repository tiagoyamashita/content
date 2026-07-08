---
label: "I"
subtitle: "概要"
group: "スタートアップ"
order: 1
---
無料サービス — 概要

初期段階の製品に役立つ厳選された**無料枠**。制限の変更 - 本番環境の数値に依存する前に、必ずベンダーのサイトを確認してください。

## このサブメニューのマップ

| Note | Focus |
|------|--------|
| [Email & mailing](ii-email-and-mailing.md) | Transactional email, newsletters, DNS — **start here** |
| [Hosting, domains & CDN](iii-hosting-domains-and-cdn.md) | Static sites, serverless, DNS, TLS |
| [Database, auth & storage](iv-database-auth-and-storage.md) | Postgres, auth, files, secrets |
| [Monitoring, analytics & devtools](v-monitoring-analytics-and-devtools.md) | Errors, uptime, analytics, CI |

## 独自のメールサーバーを実行しないでください

```text
❌  EC2 + Postfix on port 25  →  spam folder, blacklists, ops pain
✅  Resend / Brevo / SES API  →  they handle reputation + bounces
```

あなたは引き続き **ドメインを所有しており**、プロバイダーが提供する **SPF、DKIM、DMARC** レコードを追加します。

## 必要に応じて簡単に選択

| Need | Free starting point |
|------|---------------------|
| Password reset / welcome email | Resend, Brevo, SendGrid |
| Marketing newsletter | Brevo, MailerLite, Buttondown |
| Forward `hello@` to Gmail | Cloudflare Email Routing |
| Web app hosting | Vercel, Netlify, Cloudflare Pages |
| Database + auth | Supabase, Firebase |
| File uploads | Cloudflare R2 (free egress to CF), Supabase Storage |
| Error tracking | Sentry (dev tier), GlitchTip (self-host) |
| Uptime check | UptimeRobot, Better Stack free |

## コストの現実

|通常は MVP で無料です |通常は支払われます |
|---------------------|--------------|
|趣味のホスティング、小規模 DB |カスタム ドメインのメール シート（Google Workspace） |
|電子メールの量が少ない |大量のメール、専用 IP |
|コミュニティサポート |契約 + SLA |

## リハーサル

- トランザクション電子メールとマーケティング電子メール — 同じプロバイダーですか?
- 電子メールの到達性に役立つ 3 つの DNS レコードはどれですか?
