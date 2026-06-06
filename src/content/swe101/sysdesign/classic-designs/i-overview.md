---
label: "I"
subtitle: "概要"
group: "システム設計"
order: 1
---
クラシックなデザイン — 概要

**パート I** (キャッシュ、DB、シャーディング) と **スケーラブル パターン** (API、キュー、CDN、検索) を組み合わせた正規の **インタビューと本番**の問題。

## このサブメニューのマップ

|注 |システム |コアテンション |
|------|--------|--------------|
| [短縮URL](ii-url-shortener.md) | Bitly スタイルのリダイレクト |読み取りが多い。鍵の生成。 301 対 302 |
| [ニュースフィードとタイムライン](iii-news-feed-timeline.md) |ツイッター/インスタグラムフィード |書き込み時と読み取り時のファンアウト。有名人 |
| [チャットとリアルタイムメッセージング](iv-chat-realtime-messaging.md) | WhatsApp/Slack スタイルのチャット | WebSocket;面前;メッセージの順序 |
| [ビデオストリーミング](v-video-streaming.md) | YouTube/Netflix スタイルのビデオ |アップロード/トランスコード パイプラインと CDN 再生 |
| [ライドシェアリングとロケーション](vi-ride-sharing-location.md) | Uber/Lyft スタイルのマッチング |高周波GPS;地理空間インデックス |
| [Web クローラー](vii-web-crawler.md) | Googlebot スタイルのクローラー |礼儀正しさ。フロンティア;重複排除 |

## デザインがどのように接続されるか

<figure class="notes-diagram"><svg xmlns="0 viewBox="0 0 520 160" role="img" aria-label="Classic design problems mapped to building blocks">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Shared building blocks across classic designs</text>
  <rect x="12" y="36" width="88" height="28" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="24" y="54" fill="#e4e4e7" font-size="9">Cache (Redis)</text>
  <rect x="108" y="36" width="88" height="28" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="120" y="54" fill="#e4e4e7" font-size="9">Queue (Kafka)</text>
  <rect x="204" y="36" width="88" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="216" y="54" fill="#e4e4e7" font-size="9">CDN / object store</text>
  <rect x="300" y="36" width="88" height="28" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="312" y="54" fill="#e4e4e7" font-size="9">Search index</text>
  <rect x="396" y="36" width="88" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="408" y="54" fill="#e4e4e7" font-size="9">Sharded DB</text>
  <text x="12" y="82" fill="#a1a1aa" font-size="9">URL shortener → cache + shard · Feed → Redis ZSET · Video → CDN · Crawler → frontier + Bloom</text>
  <text x="12" y="110" fill="#d4d4d8" font-size="10" font-weight="600">Interview flow</text>
  <text x="12" y="128" fill="#71717a" font-size="9">Requirements → estimate QPS/storage → high-level diagram → deep dive hot path → bottlenecks</text>
  <text x="12" y="148" fill="#71717a" font-size="9">Part I → Scalable patterns → Classic designs → Bottleneck analysis</text>
</svg></figure>

## リハーサルの質問

- URL短縮データモデルと読み取りスケーリング?
- ファンアウト書き込みと読み取り — 有名人向けのハイブリッド?
- チャットの WebSocket とロングポーリングは?
- スノーフレーク ID プロパティ?
- ビデオのアップロード → トランスコード → HLS 再生パス?
- ライドマッチングのための Geohash vs S2?
- クローラーにおけるブルームフィルターの役割?
