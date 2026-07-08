---
label: "V"
subtitle: "Incidents & escalation"
group: "Daily conversations"
order: 5
---
Incidents & escalation — conversations
**障害** discussions — spoken updates often precede [Email templates](../iv-email-templates.md). Apologize first (**申し訳ございません**), then facts, then action.

---

## 1. Noticing issue — telling your 課長 first

**Context:** Production alert; internal Slack also fired. **Internal — urgent.**

| | |
|---|---|
| **あなた** | 鈴木さん、すみません。本番でエラー率が上がっています。 |
| | — Suzuki, sorry — error rate is up in prod. |
| **鈴木課長** | 状況わかる？ |
| **あなた** | 今ログを確認しています。15分以内に原因を報告します。 |
| | — Checking logs now. I'll report cause within 15 minutes. |
| **鈴木課長** | わかった。部長にも連絡して。 |
| **あなた** | 承知しました。まず調査してから、部長にご報告いたします。 |
| | — Understood. I'll investigate, then report to the director. |
| | [謙譲: **ご報告いたします**] |

---

## 2. Verbal report to 部長

**Context:** 5 minutes later; boss at desk. **Internal — senior.**

| | |
|---|---|
| **あなた** | 部長、お時間よろしいでしょうか。本番障害のご報告です。 |
| | — Director, do you have a moment? Production incident report. |
| **田村部長** | うん、どうぞ。 |
| **あなた** | 10時15分から、決済APIがタイムアウトしています。影響は一部ユーザーです。 |
| **あなた** | 原因はDB接続プールの枯渇と見ております。再起動で復旧する見込みです。 |
| **田村部長** | 顧客には？ |
| **あなた** | これから佐藤様に電話し、メールでもご連絡いたします。 |
| | — I'll call Mr. Sato and also email. |
| | [謙譲: **ご連絡いたします**] |
| **田村部長** | わかった。復旧したら教えて。 |
| **あなた** | 承知いたしました。 |
| | [謙譲: **承知いたしました** — to 部長] |

---

## 3. First call to client during outage

**Context:** You call 佐藤様. **External — high stakes.**

| | |
|---|---|
| **あなた** | 佐藤様、お世話になっております。◇◇の□□でございます。 |
| **あなた** | 大変申し訳ございません。現在、貴社向けサービスで障害が発生しております。 |
| | — We sincerely apologize. Your service is currently impaired. |
| | [尊敬: **貴社**; apology: **大変申し訳ございません**] |
| **佐藤様** | 状況は？ |
| **あなた** | 10時15分頃より、決済処理が遅延しております。現在、原因を調査しております。 |
| **佐藤様** | いつ直る？ |
| **あなた** | 恐れ入りますが、復旧時刻はまだ確定しておりません。30分以内に、改めてご連絡いたします。 |
| | — Sorry — recovery time not fixed yet. I'll contact you again within 30 minutes. |
| | [謙譲: **ご連絡いたします**] |
| **佐藤様** | わかった。よろしく。 |
| **あなた** | ご迷惑をおかけし、重ね重ねお詫び申し上げます。失礼いたします。 |

---

## 4. Recovery — telling 部長 then client

**Context:** Service restored. **Internal then external.**

**To 部長:**

| | |
|---|---|
| **あなた** | 部長、12時30分に復旧しました。原因は接続プール設定です。 |
| **田村部長** | 顧客には報告した？ |
| **あなた** | これから佐藤様にお電話いたします。 |
| | — I'll call Mr. Sato now. |
| | [謙譲: **お電話いたします**] |

**To 佐藤様 (phone):**

| | |
|---|---|
| **あなた** | 佐藤様、□□です。先ほどの障害につきまして、12時30分に復旧いたしました。 |
| | — Regarding the earlier outage — we recovered at 12:30. |
| | [謙譲: **復旧いたしました** — humble announcement of your team's fix] |
| **あなた** | この度はご不便をおかけし、大変申し訳ございませんでした。 |
| **佐藤様** | 了解。報告書は？ |
| **あなた** | 明日までに障害報告書をメールでお送りいたします。 |
| | — I'll email an incident report by tomorrow. |

---

## 5. Post-mortem meeting (社内)

**Context:** Blameless review; still polite. **Internal.**

| | |
|---|---|
| **鈴木課長** | では、振り返りを始めます。□□さん、経緯からお願いします。 |
| **あなた** | はい。10時15分にアラートを受け、ログで接続エラーを確認しました。 |
| **あなた** | 11時45分にプール設定を変更し、12時30分に復旧しました。 |
| **田村部長** | 再発防止は？ |
| **あなた** | 監視閾値の見直しと、手順書の更新を今週中に実施いたします。 |
| | — We'll revise monitoring thresholds and update the runbook this week. |
| | [謙譲: **実施いたします**] |
| **鈴木課長** | 顧客への説明資料も頼む。 |
| **あなた** | 承知しました。金曜までに共有します。 |

---

## 6. When you caused the incident

**Context:** Your change caused outage. **Internal — accountable.**

| | |
|---|---|
| **あなた** | 部長、申し訳ございません。今回の障害は、私のデプロイミスが原因です。 |
| | — Director, I'm sorry. This outage was caused by my deploy mistake. |
| **田村部長** | 状況は把握した。今は復旧優先。振り返りは後で。 |
| **あなた** | はい。現在、ロールバックを実施しております。完了次第、ご報告いたします。 |
| | — Yes. Rolling back now. I'll report when complete. |

---

## Keigo checklist (this file)

| Situation | Must include |
|-----------|--------------|
| Client outage call | **申し訳ございません** + **ご迷惑をおかけ** |
| Uncertain ETA | **恐れ入りますが** — soften bad news |
| Your update to client | **ご連絡いたします** / **お送りいたします** |
| To 部長 | **ご報告** / **承知いたしました** (not bare うん) |

Written follow-up: [Email templates](../iv-email-templates.md) §6–7.

## Next

[Requests & handoffs](vi-requests-approval-and-handoffs.md) — ご承認 and deliverables.
