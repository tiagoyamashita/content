---
label: "III"
subtitle: "Meetings & reviews"
group: "Daily conversations"
order: 3
---
Meetings & reviews — conversations
**定例会**, design **レビュー**, and **1on1** with 課長・部長. You **humble** your speech; you **elevate** their questions and decisions. See [Corporate structure](../ii-corporate-structure.md) for titles.

---

## 1. Daily standup (社内)

**Context:** Short status; team + 鈴木課長. **Internal.**

| | |
|---|---|
| **鈴木課長** | では、順番にどうぞ。田中さんから。 |
| | — OK, in order. Tanaka first. |
| **田中** | 昨日はAPIの修正を完了しました。今日は結合試験をします。ブロッカーはありません。 |
| **あなた** | 昨日はログ調査をしました。原因は設定ミスでした。今日は修正をデプロイします。 |
| | — Yesterday I investigated logs. Cause was a config error. Deploying fix today. |
| **鈴木課長** | 了解。デプロイ前に一度声かけて。 |
| | — Got it. Ping me before deploy. |
| **あなた** | 承知しました。デプロイ前にご連絡します。 |
| | — Understood. I'll contact you before deploy. |
| | [丁寧: **ご連絡します** — acceptable internal; external → **ご連絡いたします**] |

---

## 2. Design review — presenting

**Context:** 基本設計レビュー; 部長 and 顧客担当 join. **Mixed — client present.**

| | |
|---|---|
| **あなた** | それでは、基本設計についてご説明させていただきます。 |
| | — I'll explain the basic design now. |
| | [謙譲: **ご説明させていただきます** — humble permission] |
| **あなた** | 画面遷移は資料の3ページ目をご覧ください。 |
| | — Please see page 3 for screen transitions. |
| | [尊敬: **ご覧ください** — respectful "look"] |
| **佐藤様** | ここの認証の部分は、どのように実装されますか。 |
| | — How will this auth part be implemented? |
| | [尊敬: **実装されますか** — passive respectful] |
| **あなた** | ご質問ありがとうございます。OAuth2で実装いたします。 |
| | — Thank you for the question. We'll implement with OAuth2. |
| | [謙譲: **実装いたします**] |
| **田村部長** | 佐藤様、他にご不明な点はございますか。 |
| | — Mr. Sato, anything else unclear? |
| | [尊敬: **ご不明な点はございますか**] |
| **佐藤様** | 大丈夫です。進めてください。 |
| **あなた** | ありがとうございます。詳細設計に進めさせていただきます。 |
| | — Thank you. We'll proceed to detailed design. |

---

## 3. Boss challenges your estimate

**Context:** 1on1 with 鈴木課長. **Internal — manager.**

| | |
|---|---|
| **鈴木課長** | この工数、2週間で終わる？ |
| | — Can this be done in two weeks? |
| **あなた** | 確認したところ、結合試験に3日ほど必要です。2週間だと少し厳しいです。 |
| | — After checking, integration test needs about three days. Two weeks is tight. |
| **鈴木課長** | じゃあどうする？ |
| **あなた** | 機能を分割して、第1弾を2週間でリリースする案はいかがでしょうか。 |
| | — How about splitting — release phase 1 in two weeks? |
| | [丁寧: **いかがでしょうか** — soft proposal] |
| **鈴木課長** | それで部長に説明して。 |
| **あなた** | 承知しました。部長には本日中にご説明いたします。 |
| | — Understood. I'll explain to the director today. |
| | [謙譲: **ご説明いたします**] |

---

## 4. You disagree politely in a review

**Context:** 課長 proposal; you see a risk. **Internal.**

| | |
|---|---|
| **鈴木課長** | このDB、単一インスタンスでいいんじゃない？ |
| **あなた** | おっしゃる通り、コストは抑えられます。 |
| | — As you say, cost would be lower. |
| | [尊敬: **おっしゃる通り** — agree with their point] |
| **あなた** | 一方で、障害時の影響が大きいため、冗長構成もご検討いただければと存じます。 |
| | — On the other hand, outage impact is large — I'd appreciate considering redundancy. |
| | [謙譲: **存じます** — humble "I think"; 尊敬: **ご検討いただければ**] |
| **鈴木課長** | なるほど。資料まとめてくれる？ |
| **あなた** | かしこまりました。明日までに比較表をお送りします。 |
| | — Certainly. I'll send a comparison table by tomorrow. |
| | [丁寧+: **かしこまりました** — formal ack] |

---

## 5. Meeting close — minutes

**Context:** End of client meeting. **External.**

| | |
|---|---|
| **あなた** | 本日はお時間をいただき、ありがとうございました。 |
| | — Thank you for your time today. |
| | [丁寧: **いただき** — humble receive of time] |
| **あなた** | 議事録は明日午前中までにメールでお送りいたします。 |
| | — I'll email minutes by tomorrow morning. |
| | [謙譲: **お送りいたします**] |
| **佐藤様** | よろしくお願いします。 |
| **あなた** | 引き続きよろしくお願いいたします。失礼いたします。 |
| | — We look forward to continuing. Goodbye. |
| | [謙譲: **失礼いたします** — formal leave] |

---

## Keigo checklist (this file)

| Your line | Type | Why |
|-----------|------|-----|
| ご説明させていただきます | 謙譲 | You present — lower yourself |
| ご覧ください | 尊敬 | Client looks — elevate them |
| おっしゃる通り | 尊敬 | Refer to boss/client words |
| 存じます | 謙譲 | Your opinion — humble |
| かしこまりました | 丁寧+ | Formal ack to senior/client |

## Next

[Phone & client calls](iv-phone-and-client-calls.md) — かしこまりました and hold/transfer phrases.
