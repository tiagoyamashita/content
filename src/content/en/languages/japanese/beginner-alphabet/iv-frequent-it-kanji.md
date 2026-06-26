---
label: "IV"
subtitle: "Frequent IT kanji"
group: "Japanese"
order: 4
---
Kanji for programming — frequent IT kanji
How we will learn the kanji that matter for everyday programming work in Japan: reading docs, UI labels, logs, and ticket comments.

## How we will learn

Japanese IT text is mostly **compound words** built from a small set of recurring kanji. Instead of memorizing thousands of characters, we focus on **high-frequency building blocks** that appear in technical vocabulary.

**Study order for this track**

1. **Core IT kanji (this page)** — Single characters you will see in menus, buttons, and error messages (`設`, `定`, `情`, `報`, `処`, `理`, …), plus obvious calendar and date kanji (`年`, `月`, `日`, `曜`, …).
2. **Compound terms** — Combine those kanji into words you already know in English (`設定` = settings, `情報` = information, `処理` = processing).
3. **Context drills** — Read real UI strings and log lines; map each kanji back to meaning before guessing the whole word.
4. **Design docs** — Read 基本設計書 and 詳細設計書 section headings; map kanji like `詳`, `基`, `遷`, `仕様` before reading full paragraphs.
5. **Spaced review** — Revisit the table weekly; add compounds from your own codebase, Jira tickets, or vendor docs.

**Rules of thumb**

- Learn **meaning**, not every reading. In IT compounds, on-yomi (Chinese-derived readings) dominate (`設定` → せってい).
- When you see an unknown word, **split it into kanji** and translate piece by piece (`設定` → set + fix → configuration/settings).
- Prioritize kanji that change **behavior** (actions, states, permissions) over decorative or rare characters.

## Calendar & everyday time

Obvious kanji from calendars, date pickers, schedules, and timestamps — common in meeting invites, cron docs, SLA windows, and HR tools.

| Kanji | English | Example compound |
|-------|---------|------------------|
| 年 | year | 今年 (ことし — this year), 年次 (ねんじ — annual) |
| 月 | month | 今月 (こんげつ — this month), 月次 (げつじ — monthly) |
| 日 | day, sun | 今日 (きょう — today), 日付 (ひづけ — date) |
| 曜 | weekday | 曜日 (ようび — day of the week), 日曜日 (にちようび — Sunday) |
| 週 | week | 今週 (こんしゅう — this week), 週次 (しゅうじ — weekly) |
| 今 | now, current | 現在 (げんざい — current), 今回 (こんかい — this time) |
| 昨 | previous (day/year) | 昨日 (きのう — yesterday), 昨年 (さくねん — last year) |
| 明 | next, clear | 明日 (あした — tomorrow), 明後日 (あさって — day after tomorrow) |
| 来 | come, next | 来年 (らいねん — next year), 来月 (らいげつ — next month) |
| 毎 | every | 毎日 (まいにち — daily), 毎時 (まいじ — hourly) |
| 午 | noon | 午前 (ごぜん — AM), 午後 (ごご — PM) |
| 秒 | second | 秒 (びょう — second), 秒単位 (びょうたんい — per second) |
| 半 | half | 30分 (さんじゅっぷん — 30 minutes), 半年 (はんとし — half year) |
| 間 | interval, span | 時間 (じかん — time), 期間 (きかん — period) |
| 朝 | morning | 朝 (あさ — morning), 朝会 (ちょうかい — stand-up meeting) |
| 昼 | midday | 昼休み (ひるやすみ — lunch break) |
| 夕 | evening | 夕方 (ゆうがた — evening) |
| 夜 | night | 夜間 (やかん — at night), 夜間バッチ (やかんばっち — nightly batch) |
| 予 | beforehand, plan | 予定 (よてい — schedule), 予約 (よやく — reservation) |
| 祝 | celebrate, holiday | 祝日 (しゅくじつ — public holiday) |
| 休 | rest, closed | 休日 (きゅうじつ — day off), 休憩 (きゅうけい — break) |
| 締 | close, cutoff | 締切 (しめきり — deadline), 締め日 (しめび — closing date) |
| 季 | season, quarter | 四半期 (しはんき — quarter), 季節 (きせつ — season) |
| 暦 | calendar | 西暦 (せいれき — Western calendar), 和暦 (われき — Japanese era calendar) |
| 火 | fire (Tuesday) | 火曜日 (かようび — Tuesday) |
| 水 | water (Wednesday) | 水曜日 (すいようび — Wednesday) |
| 木 | tree (Thursday) | 木曜日 (もくようび — Thursday) |
| 金 | gold / Friday | 金曜日 (きんようび — Friday) |
| 土 | earth (Saturday) | 土曜日 (どようび — Saturday) |
| 番 | number, turn | 番号 (ばんごう — number), 順番 (じゅんばん — order/turn) |

## Frequent kanji in IT

These characters appear often in software UI, documentation, and operations vocabulary. The **English** column gives the core meaning in technical context; **Example compound** shows a word with its reading and gloss.

| Kanji | English | Example compound |
|-------|---------|------------------|
| 情 | information | 情報 (じょうほう — information) |
| 報 | report, news | 情報 (じょうほう — information) |
| 処 | handle, process | 処理 (しょり — processing) |
| 理 | manage, reason | 処理 (しょり — processing), 管理 (かんり — management) |
| 設 | design, set up | 設定 (せってい — settings), 設計 (せっけい — design) |
| 定 | fix, decide | 設定 (せってい — settings), 確定 (かくてい — confirm) |
| 保 | preserve, protect | 保存 (ほぞん — save), 保護 (ほご — protection) |
| 存 | exist, store | 保存 (ほぞん — save), 存在 (そんざい — existence) |
| 読 | read | 読み込み (よみこみ — load) |
| 書 | write | 書き込み (かきこみ — write) |
| 入 | enter, input | 入力 (にゅうりょく — input) |
| 出 | exit, output | 出力 (しゅつりょく — output) |
| 送 | send | 送信 (そうしん — send), 配信 (はいしん — delivery) |
| 受 | receive, accept | 受信 (じゅしん — receive), 受付 (うけつけ — acceptance) |
| 接 | connect | 接続 (せつぞく — connection) |
| 断 | sever, cut off | 切断 (せつだん — disconnect) |
| 通 | pass through, communicate | 通信 (つうしん — communication) |
| 信 | trust, message | 通信 (つうしん — communication), 認証 (にんしょう — authentication) |
| 網 | network | 通信網 (つうしんもう — communication network) |
| 端 | terminal, edge | 端末 (たんまつ — terminal) |
| 機 | machine | 機能 (きのう — function), 稼働 (かどう — operation) |
| 能 | ability, capability | 機能 (きのう — function), 性能 (せいのう — performance) |
| 動 | move, operate | 動作 (どうさ — behavior), 自動 (じどう — automatic) |
| 作 | create, work | 作成 (さくせい — create), 動作 (どうさ — operation) |
| 成 | become, complete | 成功 (せいこう — success), 生成 (せいせい — generate) |
| 生 | generate, raw | 生成 (せいせい — generate) |
| 実 | implement, real | 実装 (じっそう — implementation), 実行 (じっこう — execute) |
| 装 | install, equip | 実装 (じっそう — implementation) |
| 行 | execute, row | 実行 (じっこう — execute), 実行中 (じっこうちゅう — running) |
| 始 | start | 開始 (かいし — start), 初期化 (しょきか — initialize) |
| 終 | end | 終了 (しゅうりょう — terminate), 最終 (さいしゅう — final) |
| 止 | stop | 停止 (ていし — stop), 中止 (ちゅうし — cancel) |
| 再 | again, re- | 再起動 (さいきどう — restart), 再実行 (さいじっこう — retry) |
| 起 | rise, boot | 起動 (きどう — boot/start), 再起動 (さいきどう — restart) |
| 開 | open | 開始 (かいし — start), 公開 (こうかい — publish) |
| 閉 | close | 閉じる (とじる — close), 終了 (しゅうりょう — shutdown) |
| 更 | renew, update | 更新 (こうしん — update), 変更 (へんこう — change) |
| 変 | change | 変更 (へんこう — change), 変換 (へんかん — convert) |
| 換 | exchange, convert | 変換 (へんかん — convert), 置換 (ちかん — replace) |
| 移 | move, migrate | 移行 (いこう — migration), 移動 (いどう — move) |
| 転 | transfer | 転送 (てんそう — transfer) |
| 配 | distribute, deploy | 配布 (はいふ — distribution), 配信 (はいしん — delivery) |
| 展 | expand, deploy | 展開 (てんかい — deployment), 拡張 (かくちょう — extension) |
| 構 | structure | 構造 (こうぞう — structure), 構築 (こうちく — build) |
| 築 | build | 構築 (こうちく — build) |
| 部 | part, section | 内部 (ないぶ — internal), 部署 (ぶしょ — department) |
| 分 | divide, minute | 分析 (ぶんせき — analysis), 部分 (ぶぶん — partial) |
| 割 | split, allocate | 分割 (ぶんかつ — split), 割当 (わりあて — allocation) |
| 合 | fit, combine | 統合 (とうごう — integration), 適合 (てきごう — compliance) |
| 統 | unify | 統合 (とうごう — integration), 統計 (とうけい — statistics) |
| 整 | adjust, organize | 整合性 (せいごうせい — consistency), 整理 (せいり — organize) |
| 検 | inspect, search | 検索 (けんさく — search), 検証 (けんしょう — verification) |
| 索 | search, index | 検索 (けんさく — search), 索引 (さくいん — index) |
| 確 | confirm, certain | 確認 (かくにん — confirm), 確定 (かくてい — finalize) |
| 認 | recognize, auth | 認証 (にんしょう — authentication), 承認 (しょうにん — approval) |
| 許 | permit | 許可 (きょか — permission) |
| 拒 | reject | 拒否 (きょひ — deny) |
| 権 | authority, rights | 権限 (けんげん — permissions), 認可 (にんか — authorization) |
| 限 | limit | 制限 (せいげん — restriction), 上限 (じょうげん — upper limit) |
| 制 | control, restrict | 制御 (せいぎょ — control), 制限 (せいげん — restriction) |
| 規 | rule, standard | 規約 (きやく — terms), 規格 (きかく — specification) |
| 準 | conform, standard | 準拠 (じゅんきょ — compliance), 標準 (ひょうじゅん — standard) |
| 標 | mark, standard | 標準 (ひょうじゅん — standard), 目標 (もくひょう — target) |
| 必 | necessary | 必須 (ひっす — required), 必要 (ひつよう — necessary) |
| 要 | need, require | 必要 (ひつよう — necessary), 要求 (ようきゅう — requirement) |
| 任 | responsibility | 任意 (にんい — optional), 責任 (せきにん — responsibility) |
| 意 | intention, meaning | 任意 (にんい — optional), 意味 (いみ — meaning) |
| 正 | correct | 正常 (せいじょう — normal), 修正 (しゅうせい — fix) |
| 誤 | error, mistake | 誤り (あやまり — error) |
| 失 | lose, failure | 失敗 (しっぱい — failure), 消失 (しょうしつ — loss) |
| 敗 | defeat, failure | 失敗 (しっぱい — failure) |
| 警 | warn | 警告 (けいこく — warning), 監視 (かんし — monitoring) |
| 告 | inform, report | 警告 (けいこく — warning), 通知 (つうち — notification) |
| 障 | obstacle, fault | 障害 (しょうがい — incident/failure) |
| 復 | restore | 復旧 (ふっきゅう — recovery), 復元 (ふくげん — restore) |
| 修 | repair | 修正 (しゅうせい — fix), 保守 (ほしゅ — maintenance) |
| 監 | monitor | 監視 (かんし — monitoring), 監査 (かんさ — audit) |
| 視 | view, inspect | 監視 (かんし — monitoring), 表示 (ひょうじ — display) |
| 表 | display, table | 表示 (ひょうじ — display), 一覧 (いちらん — list view) |
| 示 | show, indicate | 表示 (ひょうじ — display), 指示 (しじ — instruction) |
| 画 | screen, image | 画面 (がめん — screen), 画像 (がぞう — image) |
| 像 | image | 画像 (がぞう — image) |
| 記 | record, write | 記録 (きろく — log/record), 登録 (とうろく — register) |
| 録 | record | 記録 (きろく — log), 登録 (とうろく — registration) |
| 登 | register | 登録 (とうろく — registration) |
| 追 | trace, add | 追加 (ついか — add), 追跡 (ついせき — trace) |
| 加 | add | 追加 (ついか — add), 参加 (さんか — join) |
| 削 | shave, delete | 削除 (さくじょ — delete) |
| 除 | remove | 削除 (さくじょ — delete), 解除 (かいじょ — release) |
| 消 | erase, consume | 削除 (さくじょ — delete), 消去 (しょうきょ — clear) |
| 選 | select | 選択 (せんたく — select), 選定 (せんてい — choose) |
| 択 | choose | 選択 (せんたく — select) |
| 値 | value | 数値 (すうち — numeric value), 設定値 (せっていち — setting value) |
| 数 | number | 数値 (すうち — number), 変数 (へんすう — variable) |
| 型 | type | 型 (かた — type), データ型 (データがた — data type) |
| 式 | format, expression | 形式 (けいしき — format) |
| 名 | name | 名前 (なまえ — name), ファイル名 (ファイルめい — filename) |
| 称 | call, label | 名称 (めいしょう — name/title), 通称 (つうしょう — common name) |
| 文 | text, sentence | 文字 (もじ — character), 文書 (ぶんしょ — document) |
| 字 | character | 文字 (もじ — character), 文字列 (もじれつ — string) |
| 列 | row, series | 一覧 (いちらん — list), 配列 (はいれつ — array) |
| 行 | row, execute | 実行 (じっこう — execute), 一行 (いちぎょう — one line) |
| 項 | item, term | 項目 (こうもく — item/field), 条件 (じょうけん — condition) |
| 目 | item, eye | 項目 (こうもく — item), 目的 (もくてき — purpose) |
| 件 | matter, case | 条件 (じょうけん — condition), 事件 (じけん — incident) |
| 条 | clause, article | 条件 (じょうけん — condition), 条項 (じょうこう — clause) |
| 版 | version, edition | 初版 (しょはん — first edition) |
| 新 | new | 新規 (しんき — new), 更新 (こうしん — update) |
| 旧 | old | 旧版 (きゅうはん — old version), 復旧 (ふっきゅう — recovery) |
| 初 | initial, first | 初期化 (しょきか — initialize), 初回 (しょかい — first time) |
| 次 | next | 次回 (じかい — next time), 順次 (じゅんじ — sequential) |
| 前 | before, previous | 前提 (ぜんてい — prerequisite), 以前 (いぜん — before) |
| 後 | after, behind | 以後 (いご — after), 背後 (はいご — backend context) |
| 同 | same | 同期 (どうき — synchronization), 同一 (どういつ — identical) |
| 異 | different | 異常 (いじょう — abnormal), 相異 (そうい — difference) |
| 常 | normal, usual | 正常 (せいじょう — normal), 異常 (いじょう — abnormal) |
| 未 | not yet | 未定 (みてい — undecided), 未完了 (みかんりょう — incomplete) |
| 済 | done, settled | 済み (すみ — done), 処理済み (しょりずみ — processed) |
| 完 | complete | 完了 (かんりょう — complete), 完全 (かんぜん — complete) |
| 了 | finish | 完了 (かんりょう — complete), 終了 (しゅうりょう — finish) |
| 中 | middle, in progress | 実行中 (じっこうちゅう — running), 処理中 (しょりちゅう — processing) |
| 待 | wait | 待機 (たいき — standby), 待ち時間 (まちじかん — wait time) |
| 遅 | slow, delay | 遅延 (ちえん — latency), 遅延時間 (ちえんじかん — delay) |
| 速 | fast, speed | 高速 (こうそく — high speed), 速度 (そくど — speed) |
| 負 | load, burden | 負荷 (ふか — load), 負担 (ふたん — burden) |
| 荷 | load, cargo | 負荷 (ふか — load) |
| 増 | increase | 増加 (ぞうか — increase) |
| 減 | decrease | 削減 (さくげん — reduction), 短縮 (たんしゅく — shorten) |
| 拡 | expand | 拡張 (かくちょう — extension), 拡張性 (かくちょうせい — scalability) |
| 縮 | shrink | 圧縮 (あっしゅく — compression), 短縮 (たんしゅく — shorten) |
| 圧 | compress, pressure | 圧縮 (あっしゅく — compression) |
| 解 | solve, release | 解析 (かいせき — parse), 解除 (かいじょ — release) |
| 析 | analyze | 解析 (かいせき — parse/analysis), 分析 (ぶんせき — analysis) |
| 暗 | hidden, cipher | 暗号 (あんごう — encryption) |
| 号 | number, code | 暗号 (あんごう — cipher), 番号 (ばんごう — number/id) |
| 鍵 | key | 鍵 (かぎ — key), 秘密鍵 (ひみつかぎ — private key) |
| 密 | secret | 秘密 (ひみつ — secret), 暗号 (あんごう — encryption) |
| 証 | proof, certificate | 証明書 (しょうめいしょ — certificate), 認証 (にんしょう — authentication) |
| 防 | defend, prevent | 防御 (ぼうぎょ — defense), 防止 (ぼうし — prevention) |
| 攻 | attack | 攻撃 (こうげき — attack) |
| 侵 | invade | 侵入 (しんにゅう — intrusion) |
| 安 | safe, secure | 安全 (あんぜん — security/safety), 不安定 (ふあんてい — unstable) |
| 全 | all, whole | 全体 (ぜんたい — whole), 安全 (あんぜん — safety) |
| 危 | danger | 危険 (きけん — danger) |
| 頼 | rely, depend | 依存 (いぞん — dependency), 信頼 (しんらい — trust) |
| 依 | depend | 依存 (いぞん — dependency) |
| 永 | permanent | 永続 (えいぞく — persistence), 恒久 (こうきゅう — permanent) |
| 続 | continue | 継続 (けいぞく — continue), 永続 (えいぞく — persistence) |
| 一 | one, temporary | 一時 (いちじ — temporary), 一致 (いっち — match) |
| 時 | time | 一時 (いちじ — temporary), 実行時間 (じっこうじかん — runtime) |
| 期 | period, phase | 同期 (どうき — sync), 期限 (きげん — deadline) |
| 順 | order, sequence | 順序 (じゅんじょ — order), 準備 (じゅんび — preparation) |
| 並 | parallel, line up | 並列 (へいれつ — parallel), 並行 (へいこう — concurrent) |
| 競 | compete | 競合 (きょうごう — conflict/contention) |
| 排 | exclude | 排他 (はいた — exclusive/mutex) |
| 他 | other | 排他 (はいた — exclusive), その他 (そのた — other) |
| 鎖 | lock, chain | 連鎖 (れんさ — chain) |
| 凍 | freeze | 凍結 (とうけつ — freeze/suspend) |
| 結 | bind, freeze | 凍結 (とうけつ — freeze), 結合 (けつごう — binding) |
| 壊 | break | 破壊 (はかい — destroy) |
| 破 | destroy | 破損 (はそん — corruption), 突破 (とっぱ — breakthrough) |
| 戻 | return, rollback | 戻す (もどす — revert), 復元 (ふくげん — restore) |
| 試 | test, try | 試験 (しけん — test), 試行 (しこう — attempt) |
| 験 | test, experiment | 検証 (けんしょう — verification), 実験 (じっけん — experiment) |
| 査 | investigate, audit | 監査 (かんさ — audit), 調査 (ちょうさ — investigation) |
| 調 | investigate, adjust | 調査 (ちょうさ — investigation), 調整 (ちょうせい — adjustment) |
| 評 | evaluate | 評価 (ひょうか — evaluation) |
| 測 | measure | 計測 (けいそく — measurement) |
| 計 | measure, plan | 設計 (せっけい — design), 統計 (とうけい — statistics) |
| 算 | calculate | 計算 (けいさん — calculation), 演算 (えんざん — computation) |
| 最 | most, optimal | 最新 (さいしん — latest), 最適化 (さいてきか — optimization) |
| 適 | appropriate, optimal | 最適化 (さいてきか — optimization), 適用 (てきよう — apply) |
| 化 | transform, -ize | 最適化 (さいてきか — optimization), 自動化 (じどうか — automation) |
| 空 | empty | 空 (から — empty), 空白 (くうはく — blank) |
| 満 | full | 満杯 (まんぱい — full), 充足 (じゅうそく — sufficiency) |
| 欠 | lack | 欠落 (けつらく — missing), 不足 (ふそく — insufficiency) |
| 足 | sufficient | 不足 (ふそく — insufficient), 補足 (ほそく — supplement) |
| 属 | belong, attribute | 属性 (ぞくせい — attribute), 所属 (しょぞく — affiliation) |
| 性 | nature, property | 属性 (ぞくせい — attribute), 性能 (せいのう — performance) |
| 質 | quality | 品質 (ひんしつ — quality), 性質 (せいしつ — property) |
| 率 | rate, ratio | 効率 (こうりつ — efficiency), 利用率 (りようりつ — utilization) |
| 効 | efficiency | 効率 (こうりつ — efficiency), 有効 (ゆうこう — valid) |
| 有 | possess, exist | 有効 (ゆうこう — valid), 所有 (しょゆう — ownership) |
| 無 | none, without | 無効 (むこう — invalid), 無料 (むりょう — free) |
| 非 | non-, un- | 非同期 (ひどうき — asynchronous) |

## Design documents (基本設計書 · 詳細設計書)

Kanji from **basic design** (基本設計書) and **detailed design** (詳細設計書) templates — section headings, flow descriptions, and field definitions.

| Kanji | English | Example compound |
|-------|---------|------------------|
| 本 | main, production, book | 本番 (ほんばん — production), 基本 (きほん — basic/foundation) |
| 基 | foundation, base | 基本設計書 (きほんせっけいしょ — basic design document) |
| 詳 | detailed | 詳細設計書 (しょうさいせっけいしょ — detailed design document) |
| 細 | fine, detail | 詳細 (しょうさい — detail), 詳細設計 (しょうさいせっけい — detailed design) |
| 概 | outline, general | 概要 (がいよう — overview) |
| 背 | back, background | 背景 (はいけい — background/context) |
| 景 | scene, circumstance | 背景 (はいけい — background) |
| 的 | target, -ic suffix | 目的 (もくてき — purpose) |
| 業 | business, work | 業務 (ぎょうむ — business operations) |
| 務 | duty, task | 業務 (ぎょうむ — business operations) |
| 対 | target, versus | 対象 (たいしょう — target scope), 対応 (たいおう — handle/respond) |
| 範 | range, scope | 範囲 (はんい — scope) |
| 方 | direction, method | 方針 (ほうしん — policy/direction) |
| 針 | needle, policy | 方針 (ほうしん — policy) |
| 用 | use, employ | 利用 (りよう — use), 用途 (ようと — intended use) |
| 語 | word, language | 用語 (ようご — terminology), 用語集 (ようごしゅう — glossary) |
| 外 | outside, external | 外部連携 (がいぶれんけい — external integration) |
| 内 | inside, internal | 内部処理 (ないぶしょり — internal processing) |
| 連 | link, connect | 連携 (れんけい — cooperation/integration) |
| 携 | carry, cooperate | 連携 (れんけい — cooperation/integration) |
| 関 | relate, concern | 関連 (かんれん — related), 関係 (かんけい — relationship) |
| 参 | participate, reference | 参照 (さんしょう — reference) |
| 照 | reflect, compare | 参照 (さんしょう — reference), 照合 (しょうごう — match/verify) |
| 特 | special | 特記事項 (とっきじこう — special notes) |
| 課 | section, issue | 課題 (かだい — issue/task) |
| 題 | topic, problem | 課題 (かだい — issue), 問題 (もんだい — problem) |
| 約 | agreement, constraint | 制約 (せいやく — constraint) |
| 図 | diagram | 構成図 (こうせいず — structure diagram), 画面遷移図 (がめんせんいず — screen transition diagram) |
| 仕 | serve, specification | 仕様 (しよう — specification) |
| 様 | form, manner | 仕様 (しよう — specification), 様式 (ようしき — format/template) |
| 説 | explain | 説明 (せつめい — explanation) |
| 義 | meaning, definition | 定義 (ていぎ — definition) |
| 遷 | transition | 画面遷移 (がめんせんい — screen transition), 状態遷移 (じょうたいせんい — state transition) |
| 状 | condition, state | 状態 (じょうたい — state), 状況 (じょうきょう — situation) |
| 態 | state, attitude | 状態 (じょうたい — state) |
| 流 | flow | 処理フロー (しょりフロー — processing flow), 業務フロー (ぎょうむフロー — business flow) |
| 引 | pull, argument | 引数 (ひきすう — argument/parameter) |
| 例 | example, exception | 例外 (れいがい — exception), 凡例 (はんれい — legend) |
| 備 | prepare, remarks | 備考 (びこう — remarks/notes) |
| 補 | supplement | 補足 (ほそく — supplement), 補完 (ほかん — complement) |
| 大 | big, maximum | 最大 (さいだい — maximum) |
| 小 | small, minimum | 最小 (さいしょう — minimum) |
| 桁 | digit, column | 桁数 (けたすう — number of digits) |
| 差 | difference | 差分 (さぶん — diff/delta) |
| 改 | revise | 改訂 (かいてい — revision) |
| 訂 | correct, revise | 改訂 (かいてい — revision) |
| 凡 | ordinary, general | 凡例 (はんれい — legend/key) |
| 注 | note, annotate | 注釈 (ちゅうしゃく — annotation) |
| 釈 | explain, interpret | 注釈 (ちゅうしゃく — annotation) |
| 当 | current, applicable | 当該 (とうがい — applicable/the said), 本番相当 (ほんばんそうとう — production-equivalent) |
| 該 | applicable, that | 当該 (とうがい — applicable) |
| 含 | include | 含む (ふくむ — include) |
| 採 | adopt, pick | 採用 (さいよう — adopt/use) |
| 可 | acceptable, can | 可否 (かひ — yes/no), 可能 (かのう — possible) |
| 渡 | hand over, cross | 引き渡し (ひきわたし — delivery/handover), 受け渡し (うけわたし — handoff) |
| 経 | via, pass through | 経由 (けいゆ — via) |
| 由 | reason, via | 経由 (けいゆ — via), 理由 (りゆう — reason) |
| 宛 | address, directed to | 宛先 (あてさき — destination/recipient) |
| 点 | point | 起点 (きてん — starting point), 終点 (しゅうてん — end point) |
| 岐 | branch, fork | 分岐 (ぶんき — branch/fork) |
| 層 | layer, tier | 階層 (かいそう — layer/hierarchy) |
| 序 | order, preface | 順序 (じゅんじょ — order), 序列 (じょれつ — sequence) |
| 役 | role | 役割 (やくわり — role) |
| 担 | carry, responsible | 担当 (たんとう — person in charge) |
| 責 | responsibility | 責任 (せきにん — responsibility) |
| 以 | by means of, since | 以上 (いじょう — or more), 以下 (いか — or less) |

**Total: 281 kanji**

## Next steps

Future lessons in this track will group compounds by domain (networking, databases, security, DevOps) and practice reading real error messages and UI copy character by character.
