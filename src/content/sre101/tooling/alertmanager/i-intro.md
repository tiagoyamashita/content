---
label: "I"
subtitle: "イントロ"
group: "SRE"
order: 1
---
SRE ツール — アラートマネージャー: はじめに

Prometheus アラートを人間とシステムに重複排除、グループ化、ルーティングします。

## 1. 役割

**Alertmanager** は **Prometheus** (または互換性のあるソース) からアラートを受信し、**重複を抑制**し、関連する通知を **グループ** して 1 つの通知にし、ラベル (チーム、重大度、地域) ごとに**ルーティング**します。


<figure class="notes-diagram"><svg xmlns="2 viewBox="0 0 560 148" role="img" aria-label="Prometheus evaluates alerting rules and sends firing alerts to Alertmanager; Alertmanager dedupes groups routes then notifies Slack PagerDuty email webhook">
  <defs>
    <marker id="am-flow-arr" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto">
      <path d="M0 0 L8 4 L0 8 Z" fill="#71717a"/>
    </marker>
  </defs>
  <!-- Prometheus -->
  <rect x="16" y="36" width="132" height="52" rx="6" fill="#27272a" stroke="#52525b" stroke-width="1"/>
  <text x="82" y="58" fill="#86efac" font-size="12" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Prometheus</text>
  <text x="82" y="74" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">evaluates alerting rules</text>
  <!-- Arrow 1 -->
  <line x1="148" y1="62" x2="198" y2="62" stroke="#71717a" stroke-width="2" marker-end="url(#am-flow-arr)"/>
  <text x="172" y="54" fill="#71717a" font-size="9" font-family="system-ui,sans-serif" text-anchor="middle">HTTP</text>
  <!-- Alertmanager -->
  <rect x="206" y="28" width="156" height="68" rx="6" fill="#27272a" stroke="#60a5fa" stroke-width="1"/>
  <text x="284" y="52" fill="#93c5fd" font-size="12" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Alertmanager</text>
  <text x="284" y="68" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">dedupe · group · route</text>
  <text x="284" y="84" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">inhibit · silence</text>
  <!-- Arrow 2 -->
  <line x1="362" y1="62" x2="408" y2="62" stroke="#71717a" stroke-width="2" marker-end="url(#am-flow-arr)"/>
  <!-- Receivers -->
  <rect x="416" y="36" width="132" height="52" rx="6" fill="#27272a" stroke="#52525b" stroke-width="1"/>
  <text x="482" y="56" fill="#fbbf24" font-size="12" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Receivers</text>
  <text x="482" y="74" fill="#a1a1aa" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Slack · PagerDuty · …</text>
  <!-- Caption -->
  <text x="280" y="118" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Firing alerts are grouped then delivered — escalation apps live behind receivers.</text>
</svg></figure>

## 2. 中心となる概念

- **ルート ツリー** — マッチャーは、どの **受信者** (Slack、PagerDuty、電子メール、Webhook) がどのアラートを取得するかを決定します。
- **禁止ルール** — 例:同じクラスターに対する重大なアラートがすでに発生している場合、警告を抑制します。
- **Silences** — メンテナンス中の一時的なミュート (監査証跡あり)。
- **グループ化 /repeat_interval** — ノイズの多いアラートをバッチ処理します。リマインダーを繰り返す頻度を制御します。

## 3. Alertmanager と PagerDuty (および同様のもの)

**Alertmanager** は、Prometheus エコシステムのオープンソース **ルーティング** ソフトウェアです。アラートを**どのようにグループ化するか**、アラートを**どこに送信するかを決定します。

**PagerDuty**、Opsgenie、VictorOps などは**宛先**です。これらは **`receivers`** で構成します (例: **`pagerduty_configs`**)。これらは**オンコール スケジュール**、エスカレーション、モバイル プッシュを処理しますが、Alertmanager と同じものではありません。これらは、Alertmanager (または他のツール) から**通知を**消費**します。

このフォルダーで **展開**、**構成と受信機**、**統合と実践**に進みます。
