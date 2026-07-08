---
label: "VI"
subtitle: "Requests & handoffs"
group: "Daily conversations"
order: 6
---
Requests & handoffs — conversations
**依頼**, **承認**, **引き継ぎ**, and **納品** — spoken versions of patterns in [Email templates](../iv-email-templates.md). Use **いただけますか** toward clients; **お願いします** internal.

---

## 1. Asking 課長 for approval (spoken)

**Context:** Before production deploy. **Internal.**

| | |
|---|---|
| **あなた** | 鈴木さん、お時間よろしいですか。本番デプロイの承認をお願いしたいです。 |
| | — Do you have a moment? I need approval for prod deploy. |
| **鈴木課長** | リスクは？ |
| **あなた** | 軽微なバグ修正です。ロールバック手順も準備済みです。 |
| **鈴木課長** | わかった。進めていいよ。 |
| **あなた** | ありがとうございます。18時にデプロイします。完了したらご連絡します。 |
| | — Thanks. Deploying at 18:00. I'll contact you when done. |

---

## 2. Asking client for sign-off (meeting)

**Context:** UAT complete. **External.**

| | |
|---|---|
| **あなた** | 佐藤様、本日はお時間をいただきありがとうございます。 |
| **あなた** | 受入試験はすべて完了しております。本番リリースのご承認をいただけますでしょうか。 |
| | — UAT is complete. May we have your approval for production release? |
| | [尊敬: **ご承認をいただけますでしょうか** — their approval elevated] |
| **佐藤様** | 問題ないです。進めてください。 |
| **あなた** | ありがとうございます。では、3月15日18時にリリースさせていただきます。 |
| | — Thank you. We'll release on March 15 at 18:00. |
| | [謙譲: **リリースさせていただきます**] |
| **佐藤様** | よろしくお願いします。 |
| **あなた** | 引き続きよろしくお願いいたします。 |

---

## 3. Handoff to another team (引き継ぎ)

**Context:** You finish phase; ops takes over. **Internal — cross-team.**

| | |
|---|---|
| **あなた** | 情報システム部の皆様、お疲れ様です。開発部の□□です。 |
| **あなた** | 〇〇システムの引き継ぎ資料を共有しました。ご確認いただけますでしょうか。 |
| | — Shared handoff docs for XX system. Could you review? |
| **情シス担当** | 確認します。来週の定例で質問してもいい？ |
| **あなた** | はい、もちろんです。不明点があれば、いつでもご連絡ください。 |
| | — Yes. Contact us anytime if anything is unclear. |
| | [尊敬: **ご連絡ください** — their contact elevated] |
| **情シス担当** | よろしく。 |
| **あなた** | こちらこそ、よろしくお願いいたします。 |

---

## 4. Delivering to client (completion meeting)

**Context:** Final delivery. **External.**

| | |
|---|---|
| **あなた** | 佐藤様、本日は納品のご説明のため、お時間をいただきありがとうございます。 |
| **あなた** | ご契約いただきました〇〇機能について、本番環境へ反映が完了しております。 |
| | — The contracted XX feature has been deployed to production. |
| | [尊敬: **ご契約いただきました** — their contract elevated] |
| **あなた** | 操作説明は資料の通りですが、ご不明点はございますか。 |
| | — Operation is per the manual — any questions? |
| | [尊敬: **ご不明点はございますか**] |
| **佐藤様** | 特にありません。お疲れ様でした。 |
| **あなた** | こちらこそ、長らくお世話になりありがとうございました。 |
| | — Thank you for your long support. |
| **あなた** | 保守期間中も、引き続きよろしくお願いいたします。 |

---

## 5. Vendor asks you to change scope

**Context:** Vendor wants spec change on call. **External — push back politely.**

| | |
|---|---|
| **山田（ベンダー）** | 仕様変更をお願いしたいのですが、来週までにいただけますか。 |
| | — We'd like a spec change by next week. |
| **あなた** | ご連絡ありがとうございます。内容を確認させていただきます。 |
| **あなた** | 恐れ入りますが、来週は社内レビューの都合で難しいです。再来週はいかがでしょうか。 |
| | — Sorry — next week is hard due to internal review. How about the week after? |
| | [丁寧: **恐れ入りますが** + soft no] |
| **山田** | わかりました。では再来週でお願いします。 |
| **あなた** | ありがとうございます。変更内容をメールでいただけますでしょうか。 |
| | — Thank you. Could you send the changes by email? |
| | [尊敬: **いただけますでしょうか**] |

---

## 6. Asking senior to review your document

**Context:** 詳細設計書 before client send. **Internal — 部長.**

| | |
|---|---|
| **あなた** | 部長、詳細設計書のドラフトができました。ご確認いただけますでしょうか。 |
| | — Director, detailed design draft is ready. Could you review? |
| | [尊敬: **ご確認いただけますでしょうか**] |
| **田村部長** | いつまでに必要？ |
| **あなた** | クライアント送付が金曜のため、木曜午前までにいただけると助かります。 |
| | — Client send is Friday — by Thursday AM would help. |
| **田村部長** | わかった。明日見る。 |
| **あなた** | ありがとうございます。よろしくお願いいたします。 |

---

## 7. Daily check-in with client PM (短い電話)

**Context:** Weekly ritual. **External — routine.**

| | |
|---|---|
| **あなた** | 佐藤様、お世話になっております。□□です。先週の進捗、ご報告させていただきます。 |
| **佐藤様** | ええ、お願いします。 |
| **あなた** | 基本設計は完了し、今週は詳細設計に入ります。課題は外部APIの仕様待ちです。 |
| **佐藤様** | APIの件、こちらで確認します。 |
| **あなた** | ありがとうございます。ご確認いただき次第、進めさせていただきます。 |
| | — Thank you. We'll proceed once you confirm. |
| **佐藤様** | よろしく。 |
| **あなた** | 引き続きよろしくお願いいたします。失礼いたします。 |

---

## Practice drill

1. Pick one dialogue; read **your** lines aloud twice.
2. Label each line 尊敬 / 謙譲 / 丁寧 using [Keigo](../iii-keigo.md).
3. Rewrite the same scene as a short email using [Email templates](../iv-email-templates.md).
4. Swap 佐藤様 ↔ 田村部長 and notice which verbs change.

## Next steps

- Verb tables: [Keigo](../iii-keigo.md)
- Written versions: [Email templates](../iv-email-templates.md)
- Titles in scenes: [Corporate structure](../ii-corporate-structure.md)
- Back to map: [Overview](i-overview.md)
