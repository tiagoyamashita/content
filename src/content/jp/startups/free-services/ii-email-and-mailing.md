---
label: "II"
subtitle: "電子メールと郵送"
group: "スタートアップ"
order: 2
---
電子メールと郵送

スタートアップにとって、**電子メール**は、**トランザクション** (パスワードのリセット、領収書、アラート) と **マーケティング** (ニュースレター、お知らせ) の 2 つの仕事を意味します。 VPS 上の自己ホスト型 SMTP サーバーではなく、**API プロバイダー** を使用してください。

## 1. トランザクションとマーケティング

|タイプ |トリガー |例 |要件 |
|-----|----------|----------|--------------|
| **トランザクション** |ユーザーアクション |サインアップの確認、パスワードのリセット、請求書 |高い配信性、迅速な API |
| **マーケティング** |キャンペーン |毎週のダイジェスト、製品発表 |購読解除リンク、同意リスト (GDPR/CAN-SPAM) |

多くのプロバイダーは両方を行っています。一部のチームは、評判を分離するためにベンダーを分割します (例: Resend + MailerLite)。

## 2. 推奨される無料利用枠プロバイダー (トランザクション)

| Provider | Free tier (typical) | Best for |
|----------|---------------------|----------|
| **[Resend](https://resend.com)** | ~3,000 emails/month | Developer-first API, React Email, good DX |
| **[Brevo](https://www.brevo.com)** (Sendinblue) | ~300 emails/day | Transactional + marketing in one |
| **[SendGrid](https://sendgrid.com)** | ~100 emails/day forever | Mature API, wide docs |
| **[Mailjet](https://www.mailjet.com)** | ~200 emails/day | EU-friendly option |
| **[Amazon SES](https://aws.amazon.com/ses/)** | Very low cost; free tier with EC2 | Already on AWS; sandbox until verified |

ベンダーの価格ページで現在の制限を常に確認してください。

## 3. 例 — 再送信で送信 (ノード)

```javascript
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

await resend.emails.send({
  from: "Acme <onboarding@mail.yourdomain.com>",
  to: ["user@example.com"],
  subject: "Verify your email",
  html: "<p>Click <a href='https://app.example.com/verify?token=...'>here</a>.</p>",
});
```

Store **`RESEND_API_KEY`** in env vars — never commit keys (see CI/CD secrets notes).

## 4. 例 — SendGrid (HTTP API スケッチ)

```bash
curl -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [{"to": [{"email": "user@example.com"}]}],
    "from": {"email": "noreply@yourdomain.com"},
    "subject": "Password reset",
    "content": [{"type": "text/plain", "value": "Reset link: ..."}]
  }'
```

## 5. DNS — 到達性の要点

電子メールプロバイダーの指定どおりに、DNS ホスト (Cloudflare、Route 53 など) に **正確に** レコードを追加します。

|記録 |目的 |
|--------|--------|
| **SPF** (TXT) |あなたのドメインにメールを送信できるサーバー |
| **DKIM** (TXT/CNAME) |メッセージごとの暗号化署名 |
| **DMARC** (TXT) |失敗した SPF/DKIM に対するポリシー + レポート |

```text
Example (conceptual — use provider's exact values):

yourdomain.com   TXT   v=spf1 include:_spf.resend.com ~all
resend._domainkey.yourdomain.com   CNAME   ... (from Resend dashboard)
_dmarc.yourdomain.com   TXT   v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

Start DMARC with **`p=none`** while monitoring; tighten to **`quarantine`** / **`reject`** once confident.

## 6. 差出人アドレスとドメイン

| Pattern | Notes |
|---------|--------|
| `noreply@yourdomain.com` | OK for transactional; don't expect replies |
| `hello@yourdomain.com` | Use for support — monitor inbox |
| Shared sandbox domain | Provider default (e.g. `onboarding@resend.dev`) — **dev only** |
| Custom domain | Required for production trust |

運用トラフィックを送信する前に、プロバイダー UI のドメインを確認してください。

## 7. 受信メール (無料オプション)

| Service | What you get | Cost |
|---------|--------------|------|
| **[Cloudflare Email Routing](https://developers.cloudflare.com/email-routing/)** | Forward `you@domain` → Gmail | Free with CF DNS |
| **Zoho Mail** | Limited free mailboxes on custom domain | Free tier (check seat limits) |
| **ImprovMX** | Forward-only aliases | Free tier available |

**Google Workspace** はカスタム ドメインの Gmail の料金を支払っています。多くのスタートアップ企業は、収益が確保されるまで、代わりに Cloudflare 経由で個人の Gmail に転送しています。

## 8. ニュースレターとメーリングリスト

|プロバイダー |無料利用枠 (通常) |メモ |
|----------|---------------------|----------|
| **ブレボ** | 1 日あたりの送信上限にはマーケティングが含まれます |同一アカウントで取引可能 |
| **メーラーライト** |無料の購読者数制限 |シンプルなニュースレターに最適 |
| **ボタンダウン** |小さなリストは無料 | Markdown ニュースレター、インディーズ向け |
| **ConvertKit / Beehiiv** |限られた無料枠 |クリエイター重視 |

法的な基本:

- **オプトインのみ** — 購入済みリストはありません
- すべてのマーケティング電子メールの **購読解除** リンク
- EU ユーザー (GDPR) の場合は **同意タイムスタンプ** を保存します

## 9. MVP で避けるべきこと

| Anti-pattern | Why |
|--------------|-----|
| Postfix on a $5 VPS | IP reputation, port 25 blocks, no time for it |
| Sending from `@gmail.com` via API | Forgery filters, ToS issues |
| Same domain cold outreach + product mail | Marketing spam hurts transactional deliverability |
| No bounce handling | Providers throttle or suspend you |

**バウンス**と**苦情**には Webhook を使用します。それらのアドレスにメールを送信するのをやめてください。

## 10. 最小限のメールチェックリスト

- [ ] Domain verified with provider
- [ ] SPF + DKIM + DMARC published
- [ ] Transactional templates (verify, reset, welcome)
- [ ] API key in secrets manager / env — not in repo
- [ ] Unsubscribe for any marketing list
- [ ] Test with [mail-tester.com](https://www.mail-tester.com) or similar before launch

## 11. アップグレードする場合

|信号 |有料/専用への移行 |
|----------|--------------------------|
|日次/月次の上限に達する |次の層または SES ボリューム |
|スパムに一貫してランディング |専任の IP、配信可能性コンサルタント |
| SLA または専用のサポートが必要 |エンタープライズプラン |
|大量の製品メール | SES + 構成セット、または消印 |

**Related:** [Hosting, domains & CDN](iii-hosting-domains-and-cdn.md) (DNS host), networking DNS notes, CI/CD secrets.
