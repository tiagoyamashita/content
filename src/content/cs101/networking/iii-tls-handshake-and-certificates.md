---
label: "III"
subtitle: "TLS ハンドシェイクと証明書"
group: "ネットワーク"
order: 3
---
ネットワーキング — パート III: TLS ハンドシェイクと証明書

**TLS** (SSL の後継) は、**機密性** (暗号化)、**完全性** (改ざん検出)、そして通常は **公開キー暗号化** と **X.509 証明書**を使用した **サーバー認証** (およびオプションで **クライアント認証**) を提供します。

## 1. ハンドシェイクによって達成されるもの

アプリケーションデータの前 (例: HTTP):

1. **TLS バージョンと暗号スイートについて同意します** — 鍵交換、暗号化、および MAC/AEAD のアルゴリズム。
2. **サーバーを認証する** - クライアントは、信頼された **CA** (認証局) に対してサーバーの証明書チェーンを検証します。
3. **共有秘密を確立します** - 多くの場合、**Diffie–Hellman** (または ECDH) を介して **前方秘匿** が可能です。一時的なキーが使用されている場合、サーバーの長期キーが侵害されても古いセッションが復号されません。
4. **セッション キーの導出** — 残りの接続の一括暗号化に使用される対称キー。

## 2. 古典的なフル ハンドシェイク (概念的)

最新の TLS 1.2/1.3 は詳細が異なります。単純化した話:

1. **ClientHello** - サポートされているバージョン、暗号スイート、ランダムなノンス、キー共有 (TLS 1.3)、**SNI** (サーバー名表示: クライアントが希望するホスト名 - 共有 IP に重要)。
2. **ServerHello** — 選択されたパラメータ、サーバー **証明書チェーン**、オプションの **CertificateRequest** (相互 TLS 用)。
3. **クライアント**は証明書を検証し、鍵交換を完了し、**Finished** (ハンドシェイク記録の証明) を送信します。
4. **サーバーが完了** — 双方が **トラフィック キー**を取得し、**暗号化された**アプリケーション データ (HTTP) を送信します。

**TLS 1.3** ではラウンドトリップが削減されます (多くの場合、最初の接続では **1-RTT**、**0-RTT** 再開は存在しますが、リプレイのトレードオフがあります)。

### シーケンス図 (TLS 1.2 スタイル、簡略化)

以下の図: **TCP はすでに起動しています**。その後、**TLS レコード層** がハンドシェイク メッセージを交換します。わかりやすくするために、暗号名とオプションのメッセージ (**ServerKeyExchange**、**クライアント認証**) は省略されています。 **TLS 1.3** はサーバーの最初のフライトの大部分を暗号化し、通常はより少ない往復で完了します。同じ目標 (キーの一致、サーバーの認証、**完了** でトランスクリプトの整合性の証明) です。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 520" role="img" aria-label="TLS 1.2 simplified handshake sequence after TCP is established">
  <defs>
    <marker id="net-iii-tls-r" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
    <marker id="net-iii-tls-l" markerWidth="7" markerHeight="7" refX="1" refY="3.5" orient="auto"><path d="M7 0 L0 3.5 L7 7 Z" fill="#60a5fa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">TLS handshake (after TCP established)</text>
  <rect x="12" y="28" width="456" height="22" rx="3" fill="rgba(113,113,122,0.15)" stroke="#71717a"/>
  <text x="24" y="43" fill="#a1a1aa" font-size="9">TCP already up — SYN / SYN-ACK / ACK complete</text>
  <text x="72" y="68" fill="#86efac" font-size="10" font-weight="600">Client</text>
  <line x1="96" y1="74" x2="96" y2="500" stroke="#52525b" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="312" y="68" fill="#60a5fa" font-size="10" font-weight="600">Server (TLS stack)</text>
  <line x1="336" y1="74" x2="336" y2="500" stroke="#52525b" stroke-width="2" stroke-dasharray="4 3"/>
  <path d="M96 92 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="86" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ClientHello</text>
  <text x="128" y="98" fill="#a1a1aa" font-size="8">versions, cipher suites, random, SNI, key-share</text>
  <path d="M330 118 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="112" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ServerHello</text>
  <text x="148" y="124" fill="#a1a1aa" font-size="8">chosen version, cipher suite, random</text>
  <path d="M330 144 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="138" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Certificate</text>
  <text x="148" y="150" fill="#a1a1aa" font-size="8">server chain (leaf → intermediates)</text>
  <path d="M330 168 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="168" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ServerHelloDone</text>
  <rect x="108" y="182" width="216" height="58" rx="4" fill="rgba(251,191,36,0.1)" stroke="#fbbf24"/>
  <text x="118" y="198" fill="#fbbf24" font-size="8" font-weight="600">Client verifies</text>
  <text x="118" y="212" fill="#a1a1aa" font-size="8">chain to trusted root · hostname vs SAN</text>
  <text x="118" y="224" fill="#a1a1aa" font-size="8">key agreement (RSA / DH / ECDH) → session keys</text>
  <path d="M96 254 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="250" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ClientKeyExchange</text>
  <path d="M96 274 H330" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="270" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ChangeCipherSpec</text>
  <path d="M96 294 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="290" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Finished</text>
  <text x="128" y="302" fill="#a1a1aa" font-size="8">HMAC / PRF over handshake transcript</text>
  <path d="M330 322 H102" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="318" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ChangeCipherSpec</text>
  <path d="M330 342 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="338" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Finished</text>
  <rect x="120" y="352" width="192" height="20" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="148" y="366" fill="#86efac" font-size="9" font-weight="600">Handshake complete</text>
  <path d="M96 388 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="384" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Application data</text>
  <text x="128" y="396" fill="#a1a1aa" font-size="8">e.g. HTTP — encrypted with negotiated AEAD</text>
  <rect x="348" y="412" width="120" height="52" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="356" y="428" fill="#71717a" font-size="8">After both Finished</text>
  <text x="356" y="440" fill="#71717a" font-size="8">match, traffic keys</text>
  <text x="356" y="452" fill="#71717a" font-size="8">protect all records</text>
  <text x="12" y="508" fill="#71717a" font-size="10">Alert records signal errors; TLS 1.3 shortens this flight — same authentication and key goals.</text>
</svg></figure>

## 3. 証明書と信頼

- A **leaf certificate** binds a **public key** to names (**CN** / **SAN**: DNS names like `api.example.com`).
- The client chains to a **root CA** in its trust store (OS or browser).
- **Validity period**, revocation (**OCSP** / **CRL**), and **pinning** (rare, brittle) affect real-world security.

## 4. TLS の終了

**エッジ終端:** ロード バランサーまたは **ingress** は TLS を復号化し、**プレーン HTTP** をポッド (クラスター内部) に転送するか、バックエンド (**mTLS**) に再暗号化する場合があります。影響:

- バックエンドは、エッジが設定するときに **X-Forwarded-Proto: https** または同様のものを参照します。
- アプリへの **エンドツーエンド TLS** には、独自の証明書を使用して **パススルー** または **再暗号化**するようにプロキシを構成する必要があります。

## 5. よくある落とし穴

- **混合コンテンツ** — HTTP サブリソースを読み込む HTTPS ページ (ブロックまたは警告)。
- **SNI** が欠落しているか間違っています - 1 つの IP での仮想ホスティングが失敗するか、間違った証明書が提供されます。
- **証明書の期限切れまたは誤発行** - 監視と自動化 (**ACME** / Let's Encrypt) により、停止が軽減されます。

次: **DNS** (TCP/TLS の前に名前がアドレスになる方法)、次に **ingress** とエッジ ルーティング。
