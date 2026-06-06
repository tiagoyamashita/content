---
label: "V"
subtitle: "ネットワーク"
group: "システム設計"
order: 5
---
ネットワークのボトルネック

**物理的およびプロトコルの選択**により、スループットが制限され、サービスとリージョン間の遅延が増加します。

## 1. 信号

| Signal | Detection |
|--------|-----------|
| NIC bandwidth maxed | `sar -n DEV`, cloud NIC metrics |
| TCP **retransmits** high | `ss -ti`, `netstat -s` |
| Cross-AZ / cross-region latency | Trace span between services |
| **Ephemeral port exhaustion** | `TIME_WAIT` storm, connect errors |
| TLS handshake CPU | CPU on edge during spike |

## 2. 原因と解決策

|原因 |修正 |
|------|-----|
|おしゃべり RPC (往復が多い) | API をバッチ処理します。 gRPC ストリーミング |
|大きな JSON ペイロード | gzip/ブロトリ;プロトブフ |
|リクエストごとの新しい TCP 接続 | **接続プール**;キープアライブ |
| HTTP/1.1 行頭ブロック | **HTTP/2** マルチプレックス。 **HTTP/3** (QUIC) |
|クロスリージョン RTT | CDN;地域展開。エッジでのキャッシュ |
|サービス メッシュ サイドカー 各ホップ ~1 ミリ秒 |クリティカル パス上のメッシュのみ。内部のバイパス |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 110" role="img" aria-label="Chatty vs batched network calls">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Chatty vs batched</text>
  <text x="12" y="38" fill="#f87171" font-size="9">10 × 1 RTT = 10 × latency</text>
  <path d="M12 50 H40" stroke="#f87171" stroke-width="1"/><path d="M12 58 H40" stroke="#f87171" stroke-width="1"/><path d="M12 66 H40" stroke="#f87171" stroke-width="1"/>
  <text x="12" y="88" fill="#86efac" font-size="9">1 batch call = 1 RTT + server-side join</text>
  <path d="M200 58 H280" stroke="#86efac" stroke-width="2"/>
</svg></figure>

## 3. レイテンシーバジェット (例)

|ホップ |典型的な |
|-----|----------|
|同じ AZ | 0.1 ～ 0.5 ミリ秒 |
|クロスAZ | 1 ～ 3 ミリ秒 |
|クロスリージョン (US↔EU) | 80 ～ 120 ミリ秒 |
|モバイルのラストワンマイル | 20 ～ 200 ミリ秒 |

**クリティカル パス**がクロスリージョン ホップを最小限に抑えるように API を設計します。

## 4. 接続管理

|練習 |なぜ |
|----------|-----|
| DB/API 制限に合わせて調整されたプール サイズ |疲労を避ける |
| LB に合わせたアイドル タイムアウト |古いソケットはありません |
| HTTP/2 1 つの接続が多数のストリーム |握手の減少 |

## 5. CDN とエッジ

**静的** および **キャッシュ可能な API** 応答をオフロードします。スケーラブル パターン CDN の注記を参照してください。

**Related:** Networking track (TCP, HTTP, TLS), [Application-level](vii-application-level.md) (timeouts, circuit breakers).
