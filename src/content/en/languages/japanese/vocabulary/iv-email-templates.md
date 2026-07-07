---
label: "IV"
subtitle: "Email templates"
group: "Japanese"
order: 4
---
Email templates — Japanese business & IT
Copy-ready **件名 (subject)** and **本文 (body)** patterns for **社内 (internal)** and **社外 (client/vendor)** email. Replace `○○`, `△△`, `□□` with company name, person name, and your name. Honorific rules: [Keigo](iii-keigo.md). Quick replies: [Verbs & office replies](../day2day/i-beginner.md).

## How to use these templates

| Placeholder | Replace with |
|-------------|--------------|
| `○○株式会社` | Recipient company |
| `△△` | Recipient surname (before 様) |
| `□□` | Your full name |
| `◇◇` | Your company name |
| `【】` | Ticket ID, project code, env name |

**Standard structure:**

```text
[Company — external only]
[Name]様

[Opener — お世話になっております / お疲れ様です]
[Thanks or apology — optional]
[Body — facts, dates, actions]
[Close — よろしくお願いいたします]
[Signature block]
```

| Audience | Opener | Close |
|----------|--------|-------|
| **Client / vendor** | いつもお世話になっております。 | 何卒よろしくお願いいたします。 |
| **Internal (any level)** | お疲れ様です。 | よろしくお願いします。 |
| **Boss** | お疲れ様です。 | よろしくお願いいたします。 |

---

## Subject lines (件名)

| Situation | 件名 example |
|-----------|--------------|
| First contact | 【◇◇】ご挨拶（□□） |
| Reply / FYI | Re: 【課題番号】〇〇について |
| Review request | 【ご確認依頼】基本設計書 v1.2 |
| Approval | 【ご承認依頼】本番リリース申請（3/15 18:00） |
| Incident | 【障害連絡】〇〇サービス 応答遅延 |
| Recovery | 【復旧連絡】〇〇サービス 障害対応完了 |
| Delivery | 【納品】〇〇機能 リリース完了のご報告 |
| Meeting | 【打合せ調整】要件定義レビュー（3/20） |
| Delay | 【お詫び】納期遅延のご連絡 |
| Document share | 【資料共有】週次進捗報告（W12） |

**Tips:** Put **action** (ご確認, 障害連絡) and **date/ID** early. Internal mail can be shorter: `【確認】API仕様 3章`.

---

## 1. Internal — colleague (same team)

**件名:** 【確認】ログ調査のお願い

```text
田中さん

お疲れ様です。◇◇の□□です。

本番でエラーが出ているため、
14:00〜15:00の applog を共有いただけますか。

お手数ですが、よろしくお願いします。

□□
```

**件名:** 【共有】対応完了

```text
皆様

お疲れ様です。◇◇の□□です。

先ほどの事象について、修正を本番に反映しました。
問題ないか、ご確認をお願いします。

以上、よろしくお願いします。

□□
```

---

## 2. Internal — to boss (上長)

**件名:** 【ご報告】リリース完了

```text
部長

お疲れ様です。□□です。

本日18:00予定の本番リリースを完了しました。
特に問題は発生しておりません。

引き続き監視いたします。
以上、よろしくお願いいたします。

□□
```

**件名:** 【ご相談】スケジュール遅延

```text
部長

お疲れ様です。□□です。

〇〇機能の開発について、
テストで不具合が見つかったため、
納期を1週間後ろにずらしたいと考えております。

代替案として、機能を分割リリースする案もあります。
ご都合のよろしい時間にご相談させてください。

よろしくお願いいたします。

□□
```

**件名:** 【ご承認依頼】本番デプロイ

```text
部長

お疲れ様です。□□です。

下記の内容で本番デプロイを実施したく、
ご承認をお願いいたします。

・対象：〇〇サービス
・日時：3/15（金）18:00〜18:30
・内容：バグ修正（課題【12345】）
・ロールバック：前バージョンへ15分以内

問題なければ、ご返信ください。
よろしくお願いいたします。

□□
```

---

## 3. Internal — cross-team / project

**件名:** 【依頼】DBマイグレーション実施のお願い

```text
情報システム部 ご担当者様

お疲れ様です。◇◇開発部の□□です。

3/20（水）22:00〜23:00に、
ステージング環境でマイグレーションを実施したく存じます。

影響範囲：orders テーブル（カラム追加）
ロールバック手順：添付の手順書を参照

ご都合をお知らせいただけますと幸いです。
よろしくお願いいたします。

□□
◇◇開発部
```

---

## 4. Client — first reply / acknowledgment

**件名:** Re: お問い合わせ（〇〇について）

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇株式会社の□□でございます。

この度はお問い合わせいただき、ありがとうございます。
内容を確認いたしました。

担当より改めてご連絡いたします。
2営業日以内を目安にご返信いたします。

何卒よろしくお願いいたします。

――――――――――――――
◇◇株式会社
□□
TEL：xxx-xxxx-xxxx
――――――――――――――
```

---

## 5. Client — review / approval request

**件名:** 【ご確認依頼】基本設計書（〇〇システム）v1.0

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇株式会社の□□でございます。

基本設計書 v1.0 を作成いたしましたので、
ご確認をお願いいたします。

・対象：〇〇システム 基本設計
・確認期限：3/25（火）まで
・添付：基本設計書_v1.0.pdf

ご不明点やご修正がございましたら、
本メールへご返信ください。

ご確認のほど、よろしくお願いいたします。

□□
```

**件名:** 【ご承認依頼】本番リリース（3/15）

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇の□□でございます。

下記日程で本番リリースを実施いたします。
ご承認いただけますでしょうか。

・実施日時：3/15（金）18:00〜19:00
・内容：機能A リリース（課題一覧：添付）
・影響：メンテナンス画面 約30分

ご問題ございましたら、3/14（木）までにご連絡ください。

何卒よろしくお願いいたします。

□□
```

---

## 6. Client — incident (initial notice)

**件名:** 【障害連絡】〇〇サービス 障害発生のお知らせ

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇株式会社の□□でございます。

本日10時15分頃より、貴社ご利用の〇〇サービスにおいて
応答遅延が発生しております。

■ 発生日時：3/10（月）10:15〜（継続中）
■ 影響範囲：管理画面の表示遅延
■ 現状：原因調査中

大変ご迷惑をおかけしております。
復旧次第、改めてご報告いたします。

お急ぎのお問い合わせは、本メールへご返信ください。

何卒よろしくお願いいたします。

□□
```

---

## 7. Client — incident (recovery)

**件名:** 【復旧連絡】〇〇サービス 障害対応完了のご報告

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇の□□でございます。

先日ご連絡いたしました障害につきまして、
本日12:30に復旧が完了いたしました。

■ 障害期間：3/10 10:15 〜 3/10 12:30
■ 原因：DB接続プールの枯渇
■ 対応：プール設定の変更、再起動

この度はご不便をおかけし、大変申し訳ございませんでした。
再発防止策として、監視閾値の見直しを進めております。

詳細は別途、障害報告書をお送りいたします。

何卒よろしくお願いいたします。

□□
```

---

## 8. Client — delay apology

**件名:** 【お詫び】納期遅延のご連絡

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇の□□でございます。

この度、〇〇機能の納品予定日（3/20）につきまして、
テスト工程で追加対応が必要となったため、
3/27まで遅延する見込みです。

大変申し訳ございません。

■ 遅延理由：結合試験での不具合3件
■ 新納期：3/27（木）
■ 進捗：修正完了2件、残1件（対応中）

週次で進捗をご報告いたします。
ご不明点がございましたら、お知らせください。

何卒よろしくお願いいたします。

□□
```

---

## 9. Client — delivery / release complete

**件名:** 【納品】〇〇機能 リリース完了のご報告

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇の□□でございます。

〇〇機能の本番リリースが完了いたしましたので、
ご報告申し上げます。

■ リリース日時：3/15（金）18:30
■ 対象環境：本番
■ リリースノート：添付参照

ご確認いただき、問題がございましたらご連絡ください。
ご査収のほど、よろしくお願いいたします。

□□
```

---

## 10. Client — meeting scheduling

**件名:** 【打合せ調整】要件定義レビュー

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇の□□でございます。

要件定義書のレビューについて、
オンライン打合せを設定させていただきたく存じます。

■ 目的：要件定義 v0.9 のご確認
■ 所要時間：60分
■ 候補日時：
  ・3/18（火）14:00〜15:00
  ・3/19（水）10:00〜11:00
  ・3/20（木）15:00〜16:00

ご都合のよろしい日時をお知らせください。
URLは確定後お送りいたします。

何卒よろしくお願いいたします。

□□
```

---

## 11. Client — weekly progress report

**件名:** 【週次報告】〇〇プロジェクト（3/10週）

```text
○○株式会社
△△様

いつもお世話になっております。
◇◇の□□でございます。

今週の進捗をご報告いたします。

■ 今週の実施内容
  ・基本設計書 v1.0 作成完了
  ・API 試験（正常系）完了

■ 来週の予定
  ・詳細設計着手
  ・結合試験準備

■ 課題・リスク
  ・外部API仕様の確認待ち（貴社ご確認依頼中）

添付：進捗報告書_W11.xlsx

ご確認のほど、よろしくお願いいたします。

□□
```

---

## 12. Vendor — request for quote / support

**件名:** 【お見積依頼】クラウド環境構築

```text
○○株式会社
ご担当者様

お世話になっております。◇◇の□□です。

下記内容について、お見積りをお願いいたします。

■ 希望納期：4月末
■ 概要：AWS 上にステージング環境構築
■ 詳細：添付の要件書を参照

ご不明点がございましたら、お知らせください。
何卒よろしくお願いいたします。

□□
```

---

## 13. Reply patterns (short bodies)

Use after the opener; mix internal / external closings as needed.

| Situation | Body |
|-----------|------|
| **Ack + action** | 承知いたしました。本日中に対応いたします。 |
| **Need time** | 確認いたします。明日午前中までにご連絡いたします。 |
| **Soft no** | 恐れ入りますが、ご希望の日程では対応が難しいです。代替案をご提案いたします。 |
| **Thanks** | ご確認ありがとうございます。承知いたしました。 |
| **Follow-up** | 先日お送りしたメールの件、ご確認いただけましたでしょうか。 |
| **Reminder** | お忙しいところ恐縮です。ご確認のほど、お願いいたします。 |
| **Attachment** | 資料を添付いたしました。ご査収ください。 |
| **Question** | 一点確認させてください。〜について、ご教示いただけますでしょうか。 |

---

## 14. Signature block (署名)

**External (formal):**

```text
――――――――――――――
◇◇株式会社
□□部 □□（名前）
TEL：03-xxxx-xxxx
Email：name@example.com
――――――――――――――
```

**Internal (minimal):**

```text
□□
```

---

## 15. Common mistakes

| Avoid | Use instead |
|-------|-------------|
| Subject empty or `Re: Re: Re:` only | Clear 件名 with action + topic |
| 様 missing on client mail | Always `△△様` on first line after company |
| ご苦労様です to boss | お疲れ様です |
| Body with no line breaks | Short paragraphs; bullet ■ for facts |
| できる？ to client | 可能でございます / 対応可能です |
| No apology on incident/delay | 申し訳ございません / ご迷惑をおかけして |
| Reply-all on sensitive incident | Bcc or dedicated distro per policy |

---

## Next steps

- Honorific verb forms: [Keigo](iii-keigo.md)
- One-line chat replies: [Verbs & office replies](../day2day/i-beginner.md)
- Document names in attachments: [Common words](i-common-words.md) — **Development phase & docs**
- Titles in 宛名: [Corporate structure](ii-corporate-structure.md)
