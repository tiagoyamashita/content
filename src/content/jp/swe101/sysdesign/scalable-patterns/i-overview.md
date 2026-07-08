---
label: "I"
subtitle: "概要"
group: "システム設計"
order: 1
---
スケーラブルなパターン — 概要

**APIs**、**非同期メッセージング**、**レート制限**、**検索**、**CDN**、**分散トランザクション**、**可観測性**のパターン — コア構成要素 (**パート I** のキャッシュ、DB、レプリケーション) の上の層。

## このサブメニューのマップ

|注 |トピック |核心的な質問 |
|------|--------|---------------|
| [API デザイン](ii-api-design.md) | REST、gRPC、GraphQL |クライアントはどのようにして大規模なサービスと通信するのでしょうか? |
| [メッセージキューと非同期](iii-message-queues-and-async.md) |キュー、パブリッシュ/サブスクライブ、送信トレイ |スパイクをどのように分離して吸収するのでしょうか? |
| [レート制限](iv-rate-limiting.md) |トークンバケット、スライディングウィンドウ |バックエンドを過負荷から保護するにはどうすればよいでしょうか? |
| [検索システム](v-search-systems.md) |逆インデックス、CDC、ベクトル |高速な全文検索とセマンティック検索をどのように提供しますか? |
| [CDN & エッジ キャッシュ](vi-cdn-and-edge-caching.md) | CDN、キャッシュの無効化 |静的コンテンツとキャッシュ可能なコンテンツをグローバルに提供するにはどうすればよいですか? |
| [分散トランザクション](vii-distributed-transactions.md) |サーガ、2PC、冪等 |サービス間で書き込みをどのように調整しますか? |
| [大規模な可観測性](viii-observability-at-scale.md) | SLO、トレース、カオス |スケールが何かを壊すとき、どうやってそれを知ることができますか? |
| [データベースシャーディング](ix-database-sharding.md) |シャードキー、ルーティング、再シャーディング |1 つのプライマリを超えて書き込みをスケールするには? |

##これらが一般的なアーキテクチャのどこに配置されるか

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 200" role="img" aria-label="Client through CDN API gateway services queue search and databases">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Request path (simplified)</text>
  <rect x="12" y="36" width="64" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="56" fill="#e4e4e7" font-size="9">Client</text>
  <rect x="88" y="36" width="56" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="98" y="56" fill="#e4e4e7" font-size="9">CDN</text>
  <rect x="156" y="36" width="72" height="32" rx="3" fill="rgba(244,114,182,0.12)" stroke="#f472b6"/>
  <text x="164" y="56" fill="#e4e4e7" font-size="9">API / GW</text>
  <rect x="240" y="36" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="252" y="56" fill="#e4e4e7" font-size="9">Service</text>
  <rect x="316" y="36" width="56" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="324" y="56" fill="#e4e4e7" font-size="9">Queue</text>
  <rect x="384" y="36" width="56" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="388" y="56" fill="#e4e4e7" font-size="9">Search</text>
  <rect x="452" y="36" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="460" y="56" fill="#e4e4e7" font-size="9">DB</text>
  <path d="M76 52 H88" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M144 52 H156" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M228 52 H240" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M304 52 H316" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M372 52 H384" stroke="#a1a1aa" stroke-width="1.5"/>
  <path d="M440 52 H452" stroke="#a1a1aa" stroke-width="1.5"/>
  <text x="12" y="92" fill="#71717a" font-size="10">Rate limiting usually sits at API gateway. Async work fans out via queue. Search index syncs from DB (CDC).</text>
  <text x="12" y="120" fill="#d4d4d8" font-size="10" font-weight="600">Study order</text>
  <text x="12" y="138" fill="#a1a1aa" font-size="9">Part I → this submenu → Classic designs submenu → bottleneck analysis</text>
</svg></figure>

## リハーサルの質問

- カーソルとオフセットのページネーション — それぞれがいつ中断されるか?
- トランザクション送信ボックス — DB とブローカーへの二重書き込みを行ってみませんか?
- トークンバケットとリーキーバケット — バースト動作?
- 逆インデックスとリレーショナル テーブル スキャンの違いは何ですか?
- サーガの振り付けとオーケストレーションは？
- 症状と原因に関する警告 – たとえば?
