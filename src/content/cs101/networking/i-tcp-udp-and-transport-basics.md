---
label: "I"
subtitle: "TCP、UDP、トランスポートの基本"
group: "働いています"
order: 1
---
インターネット作業 — パート I: TCP、UDP、およびトランスポートの基本

アプリケーションがネットワーク上でバイトを送信する方法: アドレス指定、ポート、および 2 つの主要なトランスポート プロトコル。

## 1. アドレスとポート

- **IP アドレス** (IPv4 または IPv6) は、ネットワーク上の **ホスト** を識別します。
- **ポート** (0 ～ 65535) は、そのホスト上の **アプリケーションまたはサービス**を識別します。 **IP:port** は、クライアントがサーバーにアクセスするために使用するソケット エンドポイントです。

ポートがないと、OS はどのプロセスが受信トラフィックを受信するかを逆多重化できません。

<figure class="notes-diagram"><svg xmlns="0 viewBox="0 0 440 200" role="img" aria-label="One host IP with multiple processes on different ports; client targets a specific IP port pair">
  <defs>
    <marker id="net-i-port-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Host 203.0.113.10 — one IP, many services</text>
  <rect x="24" y="32" width="180" height="128" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="72" y="54" fill="#a1a1aa" font-size="10" font-family="ui-monospace">203.0.113.10</text>
  <rect x="40" y="66" width="148" height="24" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="52" y="82" fill="#e4e4e7" font-size="10" font-family="ui-monospace">:443  HTTPS server</text>
  <rect x="40" y="96" width="148" height="24" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="52" y="112" fill="#e4e4e7" font-size="10" font-family="ui-monospace">:5432 PostgreSQL</text>
  <rect x="40" y="126" width="148" height="24" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="52" y="142" fill="#e4e4e7" font-size="10" font-family="ui-monospace">:53   DNS resolver</text>
  <rect x="280" y="72" width="120" height="48" rx="6" fill="rgba(24,24,27,0.95)" stroke="#71717a"/>
  <text x="304" y="92" fill="#d4d4d8" font-size="10" font-family="system-ui,sans-serif">Client app</text>
  <text x="296" y="108" fill="#a1a1aa" font-size="9" font-family="ui-monospace">ephemeral :52418</text>
  <path d="M280 96 H204" stroke="#86efac" stroke-width="2" marker-end="url(#net-i-port-mk)"/>
  <text x="196" y="88" fill="#86efac" font-size="9" font-weight="600">connect</text>
  <text x="196" y="100" fill="#fbbf24" font-size="9" font-family="ui-monospace">203.0.113.10:443</text>
  <text x="12" y="182" fill="#71717a" font-size="10">OS routes by destination port → correct process (demultiplexing).</text>
</svg></figure>

## 2. UDP — ユーザーデータグラム プロトコル

**特徴**

- **コネクションレス:** セットアップ ハンドシェイクはありません。準備ができたらデータグラムを送信します。
- **再順序付けなし / ベストエフォート:** 再送信または順序付けの保証は組み込まれていません (アプリケーションは独自の保証を追加できます)。
- **ヘッダーが小さく、遅延が少ない:** DNS クエリ、VoIP、ゲーム、時折損失が許容されるメトリクスに適しています。

**UDPを選択する場合**

- **低レイテンシー**が必要で、損失を許容できるか、独自の信頼性を実装している場合 (例: UDP 上に構築された QUIC)。

<figure class="notes-diagram"><svg xmlns="1 viewBox="0 0 440 176" role="img" aria-label="UDP sends independent datagrams with no handshake; one may be lost or arrive out of order">
  <defs>
    <marker id="net-i-udp-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
    <marker id="net-i-udp-lost" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#f87171"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">UDP — fire-and-forget datagrams</text>
  <rect x="24" y="36" width="88" height="40" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="44" y="60" fill="#e4e4e7" font-size="11">Sender</text>
  <rect x="328" y="36" width="88" height="40" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="340" y="60" fill="#e4e4e7" font-size="11">Receiver</text>
  <rect x="108" y="88" width="52" height="22" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="118" y="103" fill="#e4e4e7" font-size="9" font-family="ui-monospace">#1</text>
  <path d="M112 99 H328" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-i-udp-mk)"/>
  <rect x="108" y="114" width="52" height="22" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="118" y="129" fill="#e4e4e7" font-size="9" font-family="ui-monospace">#2</text>
  <path d="M112 125 H240" stroke="#f87171" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#net-i-udp-lost)"/>
  <text x="244" y="128" fill="#f87171" font-size="9">lost</text>
  <rect x="108" y="140" width="52" height="22" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="118" y="155" fill="#e4e4e7" font-size="9" font-family="ui-monospace">#3</text>
  <path d="M112 151 H328" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-i-udp-mk)"/>
  <text x="328" y="108" fill="#fbbf24" font-size="9">may arrive as #1, #3</text>
  <text x="12" y="168" fill="#71717a" font-size="10">No connection state; no automatic retry or ordering.</text>
</svg></figure>

## 3. TCP — 中継制御プロトコル

**特徴**

- **接続指向:** **3 ウェイ ハンドシェイク** により、アプリケーション データの前に状態が確立されます (クラシック モデルの場合)。
- **信頼性の高い、順序付けられたバイト ストリーム:** 再送信、シーケンス、フロー制御、輻輳制御。
- **全二重:** 接続が確立された後、双方が送信できます。

**ラフなスリーウェイ ハンドシェイク (簡易)**

1. クライアントは **SYN** (シーケンス番号を同期) を送信します。
2. サーバーは **SYN-ACK** を応答します。
3. クライアントは **ACK** を送信します — データ転送のために確立された接続とみなされます (詳細はスタックと TCP オプションによって異なります)。

<figure class="notes-diagram"><svg xmlns="2 viewBox="0 0 440 220" role="img" aria-label="TCP three-way handshake SYN SYN-ACK ACK then bidirectional data stream">
  <defs>
    <marker id="net-i-tcp-r" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
    <marker id="net-i-tcp-l" markerWidth="7" markerHeight="7" refX="1" refY="3.5" orient="auto"><path d="M7 0 L0 3.5 L7 7 Z" fill="#60a5fa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">TCP — three-way handshake, then data</text>
  <text x="72" y="44" fill="#86efac" font-size="10" font-weight="600">Client</text>
  <line x1="96" y1="50" x2="96" y2="200" stroke="#52525b" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="312" y="44" fill="#60a5fa" font-size="10" font-weight="600">Server</text>
  <line x1="336" y1="50" x2="336" y2="200" stroke="#52525b" stroke-width="2" stroke-dasharray="4 3"/>
  <path d="M96 68 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-i-tcp-r)"/>
  <text x="168" y="62" fill="#e4e4e7" font-size="10" font-family="ui-monospace">SYN  seq=100</text>
  <path d="M330 88 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-i-tcp-l)"/>
  <text x="148" y="82" fill="#e4e4e7" font-size="10" font-family="ui-monospace">SYN-ACK  seq=300 ack=101</text>
  <path d="M96 108 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-i-tcp-r)"/>
  <text x="168" y="102" fill="#e4e4e7" font-size="10" font-family="ui-monospace">ACK  ack=301</text>
  <rect x="120" y="118" width="192" height="20" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="148" y="132" fill="#86efac" font-size="9" font-weight="600">ESTABLISHED — both sides may send</text>
  <path d="M96 152 H330" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-i-tcp-r)"/>
  <text x="168" y="146" fill="#a1a1aa" font-size="9">HTTP request bytes…</text>
  <path d="M330 172 H102" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#net-i-tcp-l)"/>
  <text x="168" y="166" fill="#a1a1aa" font-size="9">HTTP response bytes…</text>
  <text x="12" y="212" fill="#71717a" font-size="10">Kernel buffers reorder, retransmit, and pace sends — app sees one ordered byte stream.</text>
</svg></figure>

**TCPを選択する場合**

- **HTTP/1.1 と HTTP/2** は歴史的に TCP 上にありました。スタックがバイト ストリームの損失と順序付けを処理できるようにする必要があります。

<figure class="notes-diagram"><svg xmlns="3 viewBox="0 0 440 120" role="img" aria-label="TCP vs UDP comparison">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">TCP vs UDP at a glance</text>
  <rect x="12" y="30" width="200" height="78" rx="5" fill="rgba(34,197,94,0.08)" stroke="#86efac"/>
  <text x="24" y="50" fill="#86efac" font-size="11" font-weight="600">TCP</text>
  <text x="24" y="66" fill="#a1a1aa" font-size="9">✓ handshake  ✓ ordered stream</text>
  <text x="24" y="80" fill="#a1a1aa" font-size="9">✓ retransmit  ✓ flow control</text>
  <text x="24" y="96" fill="#71717a" font-size="9">HTTP, APIs, file transfer</text>
  <rect x="228" y="30" width="200" height="78" rx="5" fill="rgba(59,130,246,0.08)" stroke="#60a5fa"/>
  <text x="240" y="50" fill="#60a5fa" font-size="11" font-weight="600">UDP</text>
  <text x="240" y="66" fill="#a1a1aa" font-size="9">✗ no setup  ✗ best-effort</text>
  <text x="240" y="80" fill="#a1a1aa" font-size="9">✓ low latency  ✓ small header</text>
  <text x="240" y="96" fill="#71717a" font-size="9">DNS, VoIP, gaming, QUIC base</text>
</svg></figure>

## 4.ソケット (考え方)

**ソケット** は、プログラムが使用する API 境界です。サーバーではバインド/リッスン/受け入れ、クライアントでは接続/送信/受信します。カーネルは、ソケットを **プロトコル** (TCP または UDP)、**ローカル** および **リモート** の IP/ポート ペア、およびバッファーに結び付けます。

<figure class="notes-diagram"><svg xmlns="4 viewBox="0 0 440 188" role="img" aria-label="Server bind listen accept and client connect socket flow">
  <defs>
    <marker id="net-i-sock-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">TCP server vs client (socket API)</text>
  <rect x="16" y="34" width="188" height="140" rx="5" fill="rgba(24,24,27,0.95)" stroke="#60a5fa"/>
  <text x="28" y="54" fill="#60a5fa" font-size="10" font-weight="600">Server process</text>
  <text x="28" y="74" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1. socket()</text>
  <text x="28" y="90" fill="#e4e4e7" font-size="9" font-family="ui-monospace">2. bind(0.0.0.0:8080)</text>
  <text x="28" y="106" fill="#e4e4e7" font-size="9" font-family="ui-monospace">3. listen()</text>
  <text x="28" y="122" fill="#86efac" font-size="9" font-family="ui-monospace">4. accept() → new socket</text>
  <text x="28" y="138" fill="#e4e4e7" font-size="9" font-family="ui-monospace">5. read / write</text>
  <rect x="236" y="34" width="188" height="140" rx="5" fill="rgba(24,24,27,0.95)" stroke="#86efac"/>
  <text x="248" y="54" fill="#86efac" font-size="10" font-weight="600">Client process</text>
  <text x="248" y="74" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1. socket()</text>
  <text x="248" y="90" fill="#e4e4e7" font-size="9" font-family="ui-monospace">2. connect(host:8080)</text>
  <text x="248" y="114" fill="#e4e4e7" font-size="9" font-family="ui-monospace">3. write request</text>
  <text x="248" y="130" fill="#e4e4e7" font-size="9" font-family="ui-monospace">4. read response</text>
  <path d="M204 122 H236" stroke="#a1a1aa" stroke-width="2" marker-end="url(#net-i-sock-mk)"/>
  <text x="206" y="114" fill="#fbbf24" font-size="8">TCP conn</text>
  <text x="12" y="182" fill="#71717a" font-size="10">accept() returns a connected socket per client; listen socket stays open.</text>
</svg></figure>

## 5. 以下のメンタルモデル

|レイヤー (概念的) |例 |
|---------------------|----------|
|輸送 | TCP、UDP、ポート |
|アプリケーション | HTTP、TLS、DNS メッセージ形式 |
|ネットワーク上のセキュリティ | TLS (多くの場合、TCP の「上に」) |
|ネーミング | DNS マップ名 → アドレス |
|エッジ/クラスター | Ingress、ロードバランサー、リバースプロキシ |

<figure class="notes-diagram"><svg xmlns="5 viewBox="0 0 440 224" role="img" aria-label="Networking stack layers from application down to transport">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Where this note sits in the stack</text>
  <rect x="80" y="32" width="280" height="32" rx="4" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="108" y="52" fill="#e4e4e7" font-size="10">Edge — ingress, load balancer, reverse proxy</text>
  <rect x="80" y="70" width="280" height="32" rx="4" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="108" y="90" fill="#e4e4e7" font-size="10">Naming — DNS (hostname → IP)</text>
  <rect x="80" y="108" width="280" height="32" rx="4" fill="rgba(244,114,182,0.12)" stroke="#f472b6"/>
  <text x="108" y="128" fill="#e4e4e7" font-size="10">Security — TLS (encrypt + verify identity)</text>
  <rect x="80" y="146" width="280" height="32" rx="4" fill="rgba(34,211,238,0.12)" stroke="#22d3ee"/>
  <text x="108" y="166" fill="#e4e4e7" font-size="10">Application — HTTP, DNS message format</text>
  <rect x="80" y="184" width="280" height="32" rx="4" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="108" y="204" fill="#86efac" font-size="10" font-weight="600">Transport — TCP, UDP, ports  ← Part I</text>
  <text x="368" y="52" fill="#71717a" font-size="9">Part V</text>
  <text x="368" y="90" fill="#71717a" font-size="9">Part IV</text>
  <text x="368" y="128" fill="#71717a" font-size="9">Part III</text>
  <text x="368" y="166" fill="#71717a" font-size="9">Part II</text>
</svg></figure>

次: **HTTP** (アプリケーション セマンティクス)、次に **TLS** (ネットワーク上の暗号化と ID)。
