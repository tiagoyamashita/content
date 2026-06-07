---
label: "V"
subtitle: "モニタリング、分析、開発ツール"
group: "スタートアップ"
order: 5
---
モニタリング、分析、開発ツール

**故障の時期を知る**と**配送コード**のための無料枠 - MVP には十分で、オンコールが現実になったらアップグレードします。

## 1. エラーの追跡

| Service | Free tier | Notes |
|---------|-----------|-------|
| **[Sentry](https://sentry.io)** | Developer plan | Stack traces, releases, alerts |
| **[GlitchTip](https://glitchtip.com)** | Self-host OSS | Sentry-compatible API |
| **Highlight.io** | Session replay + errors | Frontend-heavy apps |

```javascript
// Sentry (conceptual)
Sentry.init({ dsn: process.env.SENTRY_DSN, environment: "production" });
```

## 2. 稼働時間とステータス

| Service | Free |
|---------|------|
| **[UptimeRobot](https://uptimerobot.com)** | ~50 monitors, 5-min interval |
| **[Better Stack](https://betterstack.com)** | Uptime + incident basics |
| **GitHub Actions cron** | DIY HTTP ping |

Monitor **`/health`** endpoint — not just homepage.

## 3. 分析

| Service | Privacy / notes |
|---------|-----------------|
| **[Plausible](https://plausible.io)** | Paid but lightweight; trial |
| **[Umami](https://umami.is)** | Self-host or cloud — OSS |
| **Cloudflare Web Analytics** | Free, no cookie banner in many cases |
| **Google Analytics** | Free; heavier, consent banners in EU |

製品分析 (ファネル): **PostHog** クラウド無料枠 (小規模向け)。

## 4. CI/CD とコード

|サービス |スタートアップには無料 |
|----------|--------|
| **GitHub** |プライベート リポジトリ、アクション分/月 |
| **Gitラボ** |無料枠 CI |
| **依存ボット / 改修** |依存関係の更新 |

パイプライン パターンについては、**CI/CD** トラックを参照してください。

## 5. デザインとコラボレーション

|ツール |無料 |
|------|------|
| **フィグマ** |スターター ファイル |
| **概念** |個人/小規模チーム |
| **線形** |小規模チームには無料 |
| **Discord / Slack** |無料枠 |

## 6. 最小限の運用スタック

```text
Deploy (Vercel) → Sentry (errors) → UptimeRobot (ping)
                → Cloudflare Analytics (traffic)
                → GitHub Actions (test on PR)
```

## 7. 支払い時期

|必要 |アップグレード |
|-----|----------|
| 24 時間年中無休のオンコール ページング | PagerDuty、有料のベタースタック |
|ログの保存期間 > 7 日 | Datadog、Axiom、CloudWatch 有料 |
| SOC2 / 監査 |エンタープライズプラン |

**関連:** CI/CD **セキュリティと可観測性**、クラウド パターン **SLO** に関するメモ。
