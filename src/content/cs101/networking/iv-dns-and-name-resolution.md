---
label: "IV"
subtitle: "DNS と名前解決"
group: "ネットワーク"
order: 4
---
インターネット — 作業パート IV: DNS と名前解決





**DNS** マップ **人間が判読できる名前** (`api.example.com`) から接続時に使用される **レコード**: 主に **A/AAAA** (アドレス)、**CNAME** (エイリアス)、**MX** (メール)、**TXT** (検証、SPF など)。

## 1. TCP および TLS よりも DNS が重要である理由

**TCP** を開くには`api.example.com:443`の場合、リゾルバーは **IP アドレス**を取得する必要があります。 TLS **ClientHello** には、サーバーが正しい証明書を選択できるように、同じホスト名の **SNI** が含まれることがよくあります。

## 2. 再帰還と言うのは

- **スタブ リゾルバー** (ラップトップ、コンテナ) が **再帰リゾルバー** (ISP、`8.8.8.8`、企業 DNS、Kubernetes の CoreDNS)。
- 再帰リゾルバーは、**root** → **TLD** からツリーをたどります (`.com`) → **権限のある**ネームサーバー`example.com`最終的な答えが得られるまで、**TTL** に従って **キャッシュ**します。

## 3. レコードタイプ (実用的なサブセット)

|タイプ |役割 |名前 |値 |
|------|------|------|------|
| **A** | IPv4 アドレス |`api`|`203.0.113.50`|
| **AAAA** | IPv6 アドレス |`api`|`2001:db8::1`|
| **CNAME** |正規名 — 別のホスト名のエイリアス |`api`|`k8s-lb.eu-west-1.elb.amazonaws.com`|
| **TXT** |任意のテキスト |`_acme-challenge.api`|`xK8f9Qm2vP7L3nR8wT1sY0uJ5hF4gD6cB2aE`|
| **TXT** |任意のテキスト |`@`|`v=spf1 include:_spf.google.com ~all`|
| **NS** |ゾーンを権限のあるサーバーに委任します。`@`|`ns1.cloudflare.com`|
| **NS** |ゾーンを権限のあるサーバーに委任します。`@`|`ns2.cloudflare.com`|

### Hostinger hPanel — DNS ゾーン リスト (ゾーン`myrestapp.com`)

**Web サイト → myrestapp.com → DNS / DNS レコード** に表示されるのと同じレコード (列 **タイプ**、**名前**、**ポイント先**、**TTL**):

|タイプ |名前 | | を指すTTL |
|------|------|-----------|-----|
|あ | @ | 185.248.155.42 | 14400 |
|あ | ftp | 185.248.155.42 | 14400 |
| CNAME | www | myrestapp.com | 14400 |
| CNAME |アピ | lb-1847293021.eu-west-1.elb.amazonaws.com | 300 |
| AAAA |アピ | 2001:db8:5ca8:1::42 | 300 |
| TXT | _acme-challenge.api | 300 | 300 | 300 | xK8f9Qm2vP7L3nR8wT1sY0uJ5hF4gD6cb2aE 300 |
| TXT | @ | v=spf1 include:_spf.google.com ~all | 14400 |
| NS | @ | ns1.dns-parking.com | 14400 |
| NS | @ | ns2.dns-parking.com | 14400 |

## 4. TTL とキャッシュ

各回答の **TTL** (生存時間) は、リゾルバーがキャッシュできる期間を示します。 **低 TTL** はフェイルオーバーと移行を高速化します。 **TTL** が高いと負荷が軽減され、リゾルバーの問題に対する回復力が向上しますが、カットオーバーが遅くなります。

## 5. Kubernetes、DNS、および Ingress

Kubernetes は **2 つの異なる DNS システム**を使用します。これらを混同すると、「クラスター内では動作するが、ラップトップでは動作しない」というバグが発生する一般的な原因になります。

| DNS スコープ |誰が答えますか |例名 |使用者 |
|----------|---------------|--------------|----------|
| **パブリック (インターネット)** | Hostinger、Cloudflare、Route 53、… |`api.myrestapp.com`|ブラウザ、モバイル アプリ、パートナー |
| **クラスター内** | **コアDNS** |`rest-api.default.svc.cluster.local`|サービスと通信するポッド |

パブリック DNS は **クラウド ロード バランサー**で停止します。 **Ingress** は、TCP がクラスターに到達し、HTTP を使用した後**のみ実行されます。`Host`** ヘッダー — DNS は Kubernetes サービスについて知りません。

### Ingressって何ですか?

**Ingress** (Kubernetes 内) は、クラスター内で実行されているアプリの **HTTP/HTTPS のフロント ドア**です。これには 2 つの部分があります。

|ピース |それは何ですか |
|------|-----------|
| **Ingress リソース** |ルールをリストする構成オブジェクト (YAML): 「if **`Host`** は`api.myrestapp.com`そしてパスは`/v1/…`、**サービス**にトラフィックを送信します`rest-api`ポート **8080** です。」 |
| **イングレス コントローラー** |これらのルールを**読み取り**し、それらを強制するように**リバース プロキシ**を構成する実行中のプログラム (nginx、Traefik など)。 |

**Ingress は DNS ではありません。** DNS は、**どの IP** に接続するかをクライアントに指示します。 Ingress は、URL のホスト名とパスを使用して、**接続の到着後**にリクエストを処理する**サービス**をクラスターに指示します。

**Ingress はサービスではありません。** **サービス** は、ポッドへの安定したクラスター内ネットワークです。 **Ingress** は**サービスの前に位置し、**外部** HTTP トラフィックを適切なサービスにルーティングします。

```text
DNS:      api.myrestapp.com  →  203.0.113.50 (load balancer)
Ingress:  Host: api.myrestapp.com  +  path /v1/users  →  Service rest-api:8080  →  Pod
```

### 5.1 クラスター内 DNS (CoreDNS)

すべての **Service** は、クラスター内で安定した DNS 名を取得します。

```text
<service>.<namespace>.svc.cluster.local
```

|サービス |ネームスペース |クラスター DNS 名 | ClusterIP (例) |
|----------|----------|---------------------|---------------------|
|`rest-api`|`default`|`rest-api.default.svc.cluster.local`|`10.96.42.18`|
|`postgres`|`data`|`postgres.data.svc.cluster.local`|`10.96.88.5`|

- ポッドは接続文字列でこの名前を使用します。**ポッド IP ではありません** (ポッドは再起動して IP を変更します)。
- 短い名前は同じ名前空間内で機能します。`rest-api`→`rest-api.default.svc.cluster.local`。
- この DNS は公共のインターネット上では**表示されません**。

### 5.2 パブリック DNS からクラスターへ

REST API の一般的なクラウド設定:

1. **Ingress コントローラー** (nginx、Traefik など) を **LoadBalancer** サービスの背後にデプロイします。
2. クラウドは、ホスト名を使用して **ロード バランサー** を作成します。`lb-1847293021.eu-west-1.elb.amazonaws.com`。
3. **Hostinger** (または任意のパブリック DNS) に ​​* を追加します`api`CNAME → そのホスト名** (§3 の表を参照)。
4. クライアントの解決`api.myrestapp.com`→ LB IP → **TCP :443** → **Ingress コントローラー** ポッド。

|パブリック DNS レコード | | を指すKubernetes オブジェクト |
|---------------------|-----------|---------------------|
|`api`CNAME |`lb-1847293021.eu-west-1.elb.amazonaws.com`|`Service`**LoadBalancer** (または Ingress の前の LB) と入力します。
| (パブリック DNS にはなし) | — | **イングレス** ルール:`Host: api.myrestapp.com`|
| (パブリック DNS にはなし) | — | **サービス**`rest-api`→ **ポッド** |

### 5.3 Ingress の追加内容 (DNS 以降)

**DNS** は次のように答えます。「IP とは何ですか?」`api.myrestapp.com`？」  
**Ingress** の答えは次のとおりです。`Host: api.myrestapp.com`そしてパス`/v1/…`、**サービス**とポートはどれですか?」

|入力フィールド |例 | | と一致する必要があります
|--------------|--------|---------------|
|`host`|`api.myrestapp.com`|クライアントが URL **および** TLS cert SAN で使用する名前。
|`path`|`/`または`/v1`| URL パス接頭辞 |
|`backend.service.name`|`rest-api`| Kubernetes サービス名 |
|`backend.service.port.number`|`8080`|サービスポート (ターゲットコンテナポート) |

もう少しのイングレス (概念 YAML):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rest-api
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.myrestapp.com
      secretName: api-tls-cert
  rules:
    - host: api.myrestapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rest-api
                port:
                  number: 8080
```

**cert-manager** は多くの場合、`api-tls-cert`秘密と**`_acme-challenge.api`** 発行中にパブリック DNS に TXT レコードが記録されます。

### 5.4 エンドツーエンドのパス (図)

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 280" role="img" aria-label="Public DNS through load balancer ingress service to pod">
  <defs>
    <marker id="net-iv-k8s-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Internet → cluster (api.myrestapp.com)</text>
  <rect x="12" y="36" width="88" height="44" rx="4" fill="rgba(24,24,27,0.95)" stroke="#71717a"/>
  <text x="28" y="58" fill="#e4e4e7" font-size="10">Client</text>
  <text x="20" y="72" fill="#a1a1aa" font-size="8">browser / app</text>
  <rect x="120" y="36" width="100" height="44" rx="4" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="132" y="54" fill="#fbbf24" font-size="9" font-weight="600">Public DNS</text>
  <text x="128" y="68" fill="#a1a1aa" font-size="8">Hostinger / Route53</text>
  <rect x="240" y="36" width="108" height="44" rx="4" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="252" y="54" fill="#60a5fa" font-size="9" font-weight="600">Cloud LB</text>
  <text x="248" y="68" fill="#a1a1aa" font-size="8">:443 TCP + TLS</text>
  <rect x="368" y="28" width="140" height="120" rx="6" fill="rgba(34,197,94,0.06)" stroke="#86efac" stroke-dasharray="5 3"/>
  <text x="380" y="44" fill="#86efac" font-size="9" font-weight="600">Kubernetes cluster</text>
  <rect x="380" y="52" width="116" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="392" y="68" fill="#e4e4e7" font-size="8">Ingress controller</text>
  <text x="392" y="80" fill="#a1a1aa" font-size="7">Host: api.myrestapp.com</text>
  <rect x="380" y="96" width="116" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="392" y="114" fill="#e4e4e7" font-size="8">Service rest-api:8080</text>
  <rect x="392" y="132" width="92" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="408" y="147" fill="#e4e4e7" font-size="8">Pod (REST app)</text>
  <path d="M100 58 H120" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="102" y="50" fill="#71717a" font-size="7">① query</text>
  <path d="M220 58 H240" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="222" y="50" fill="#71717a" font-size="7">② CNAME→IP</text>
  <path d="M348 58 H368" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="350" y="50" fill="#71717a" font-size="7">③ connect</text>
  <path d="M438 88 V96" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <path d="M438 124 V132" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="12" y="100" fill="#d4d4d8" font-size="10" font-weight="600">Inside the cluster (pod → pod)</text>
  <rect x="12" y="112" width="72" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="134" fill="#e4e4e7" font-size="9">Pod A</text>
  <rect x="120" y="112" width="140" height="36" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="128" y="128" fill="#a855f7" font-size="8" font-weight="600">CoreDNS</text>
  <text x="128" y="140" fill="#a1a1aa" font-size="7">rest-api.default.svc…</text>
  <rect x="280" y="112" width="80" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="292" y="134" fill="#e4e4e7" font-size="9">Service</text>
  <rect x="380" y="112" width="72" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="392" y="134" fill="#e4e4e7" font-size="9">Pod B</text>
  <path d="M84 130 H120" stroke="#a855f7" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <path d="M260 130 H280" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <path d="M360 130 H380" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="12" y="168" fill="#71717a" font-size="9">④ Ingress matches Host + path  ⑤ Service picks a ready pod</text>
  <rect x="12" y="182" width="496" height="88" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="200" fill="#d4d4d8" font-size="9" font-weight="600">Checklist</text>
  <text x="24" y="216" fill="#a1a1aa" font-size="8">Public: api CNAME → LB hostname (TTL 300 during migrations)</text>
  <text x="24" y="230" fill="#a1a1aa" font-size="8">Ingress host = api.myrestapp.com · TLS secret covers same name</text>
  <text x="24" y="244" fill="#a1a1aa" font-size="8">Service name/port in Ingress = Service manifest · selector → pod labels</text>
  <text x="24" y="258" fill="#a1a1aa" font-size="8">kubectl get ingress,svc · dig api.myrestapp.com · curl -v https://api.myrestapp.com/health</text>
</svg></figure>

### 5.5 オブジェクトの概要

|レイヤー | Kubernetes 種類 |名前（例） | DNS / アドレス指定 |
|------|---------------|----------------|---------------|
|ワークロード |導入 |`rest-api`| — |
|ネットワーク |サービス |`rest-api`|`rest-api.default.svc.cluster.local`|
|ルーティング |イングレス |`rest-api`| **パブリック** DNS → LB | が必要です
|エントリー |サービス (LB) |`ingress-nginx-controller`| CNAME のクラウド ホスト名 |
|構成 |秘密 |`api-tls-cert`| Ingress の TLS 証明書/キー |

### 5.6 よくある間違い

|症状 |考えられる原因 |
|----------|--------------|
|`curl: Could not resolve host`|パブリック DNS が欠落しているか間違っています **名前** / **ポイント先** |
| TLS 証明書名が一致しません |証明書 SAN ≠ URL ホスト。イングレスを修正`tls.hosts`または DNS 名 |
| nginx イングレスからの 404 |イングレス`host`または`path`リクエストと一致しません |
|クラスタの外部ではなく内部で動作します。使用済み`rest-api.default.svc`ラップトップからの URL — パブリックが必要`api.myrestapp.com`|
| DNS OK しかし接続が拒否されました | LB / ファイアウォール / Ingress コントローラー サービスの準備ができていません |

完全な REST + Hostinger + 地域の例: **パート V — Ingress** [Ingress、エッジ、ロード バランサー](v-ingress-edge-and-load-balancers.md）。

## 6. 運用可能なフットガン

- IP の変更後の **古いキャッシュ**。
- **スプリットホライズン DNS** — 社内とインターネットで異なる答え (デバッグで驚くべきこと)。
- **DNSSEC** — DNS 自体の信頼性チェーン (採用状況は異なります)。

次: **Ingress** とエッジ ルーティング (名前と IP に基づく HTTP ルーティング)。
