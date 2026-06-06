---
label: "V"
subtitle: "ネットワーク"
group: "システム設計"
order: 5
---
ネットワークのボトルネック

**物理的およびプロトコルの選択**により、スループットが制限され、サービスとリージョン間の遅延が増加します。

## 1. 信号

|信号 |検出 |
|----------|----------|
| NIC 帯域幅が最大に達しました | `sar -n DEV`、クラウド NIC メトリクス |
| TCP **再送信** 高 | `ss -ti`、`netstat -s` |
|クロス AZ / クロスリージョン レイテンシ |サービス間のトレース スパン |
| **一時的なポート枯渇** | `TIME_WAIT` ストーム、接続エラー |
| TLS ハンドシェイク CPU |スパイク中にエッジ上の CPU |

## 2. 原因と解決策

|原因 |修正 |
|------|-----|
|おしゃべりな RPC (多くの往復) |バッチ API。 gRPC ストリーミング |
|大きな JSON ペイロード | gzip/ブロトリ;プロトブフ |
|リクエストごとの新しい TCP 接続 | **接続プール**;キープアライブ |
| HTTP/1.1 行頭ブロック | **HTTP/2** マルチプレックス。 **HTTP/3** (QUIC) |
|クロスリージョン RTT | CDN;地域展開。エッジでのキャッシュ |
|サービス メッシュ サイドカー 各ホップ ~1 ミリ秒 |クリティカル パス上のメッシュのみ。内部のバイパス |

<figure class="notes-diagram"><svg xmlns="4 viewBox="0 0 460 110" role="img" aria-label="Chatty vs batched network calls">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Chatty vs batched</text>
  <text x="12" y="38" fill="#f87171" font-size="9">10 × 1 RTT = 10 × latency</text>
  <path d="M12 50 H40" stroke="#f87171" stroke-width="1"/><path d="M12 58 H40" stroke="#f87171" stroke-width="1"/><path d="M12 66 H40" stroke="#f87171" stroke-width="1"/>
  <text x="12" y="88" fill="#86efac" font-size="9">1 batch call = 1 RTT + server-side join</text>
  <path d="M200 58 H280" stroke="#86efac" stroke-width="2"/>
</svg></figure>

## 3. レイテンシーバジェット (例)

|ホップ |典型的な |
|-----|----------|
|同じアリゾナ州 | 0.1 ～ 0.5 ミリ秒 |
|クロスアリゾナ | 1 ～ 3 ミリ秒 |
|クロスリージョン (米国↔EU) | 80 ～ 120 ミリ秒 |
|モバイルのラストワンマイル | 20 ～ 200 ミリ秒 |

**クリティカル パス**がリージョン間のホップを最小限に抑えるように API を設計します。

## 4. 接続管理

|練習 |なぜ |
|----------|-----|
| DB/API の制限に合わせて調整されたプール サイズ |疲労を避ける |
| LB に合わせたアイドル タイムアウト |古いソケットはありません |
| HTTP/2 1 つの接続で多数のストリーム |握手の減少 |

## 5. CDN とエッジ

**静的** および **キャッシュ可能な API** 応答をオフロードします。スケーラブル パターンの CDN ノートを参照してください。

**関連:** ネットワーク トラック (TCP、HTTP、TLS)、[アプリケーション レベル](vii-application-level.md) (タイムアウト、サーキット ブレーカー)。
