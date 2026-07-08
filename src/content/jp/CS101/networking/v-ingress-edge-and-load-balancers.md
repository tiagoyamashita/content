---
label: "V"
subtitle: "Ingress、エッジ、ロードバランサー"
group: "ネットワーク"
order: 5
---
ネットワーキング — パート V: Ingress、エッジ、ロード バランサー

トラフィックがクラスターまたはデータセンターに到達するまでに、**TCP** が確立され、**TLS** がすでに終了している可能性があります。

### Ingress とは何ですか?

**Ingress** は、同じ IP 上のすべてのリクエストを単一のアプリに送信するのではなく、**ホスト名**、**URL パス**、および場合によっては **ヘッダー**に基づいて **HTTP および HTTPS** リクエストを正しいバックエンドにルーティングする **アプリケーション層 (L7) エントリ ポイント**です。

**Kubernetes** では具体的には次のようになります。

- **Ingress** オブジェクトは **構成** (ルール + オプションの TLS) です。
- **Ingress コントローラー** は、これらのルール (nginx Ingress コントローラー、Traefik、AWS ロード バランサー コントローラーなど) を適用する **実行中のプロキシ ** です。

|用語 |レイヤー |仕事 |
|------|-------|-----|
| **ロードバランサー (L4)** | TCP/UDP |ノード間で接続を分散します。 URL | は見ないかもしれません。
| **イングレス (L7)** | HTTP/HTTPS | 「`api.example.com/v1` → このサービス; `www.example.com` → そのサービス」 |
| **サービス** |クラスター内 |ポッドのセットへの安定したアドレス |

Kubernetes 以外のシステムは、**リバース プロキシ**、**API ゲートウェイ**、**エッジ ルーター** などの名前で同じアイデアを使用します。Kubernetes は、構成リソースの名前 **Ingress** を標準化しました。

## 1. ロード バランサーとリバース プロキシの比較

- **ネットワーク / L4 ロード バランサー** — IP/ ポート (場合によっては TLS パススルー) によって **TCP/UDP** フローを分散します。高速で、アプリケーションをあまり意識しません。
- **アプリケーション / L7 リバース プロキシ** — **HTTP** (ホスト、パス、ヘッダー) を理解し、**IT3__ 終了**、圧縮、レート制限、WAF 統合を実行できます。

**Ingress コントローラー** (nginx、Traefik、HAProxy、Envoy ベースのゲートウェイ、クラウド ベンダー コントローラー) は通常、**NodePort/ClusterIP** またはクラウド LB 統合の前にある **L7** プロキシです。

## 2. Kubernetes Ingress (概念的)

- **Ingress** リソースはルールを宣言します: **ホスト**、**パス** → **バックエンド サービス** (およびポート)。
- **コントローラー** は Ingress オブジェクトを監視し、プロキシ (ルート、証明書) をプログラムします。
- **TLS** は、Ingress によって参照される **Secret** を介して接続されることがよくあります。 **cert-manager** は **ACME** 証明書を自動化します。

トラフィック パス (通常):

```text
Internet → cloud LB (optional TLS) → Ingress controller → Service → Pod
```

## 3. エッジの TLS

- **入口で TLS を終了** — ポッドは HTTP を参照します。より単純ですが、**mTLS** または **バックエンド TLS** を追加しない限り、クラスター内のトラフィックはプレーンテキストになる可能性があります。
- **パススルー TLS** — LB は暗号化された TCP を転送します。イングレスまたはアプリが終了します。 SNI ルーティングがよりスマートな LB で実行される場合に便利です。

## 4. ヘッダープロキシセット

クライアントには 1 ホップが見えます。バックエンドにはコンテキストが必要です。

- **X-Forwarded-For** — 元のクライアント IP (プロキシのチェーン)。
- **X-Forwarded-Proto** — 最初のプロキシによって認識される `http` または `https`。
- **X-Forwarded-Host** — 元のホスト ヘッダー。

これらを解釈するときは、**信頼できる** プロキシのみを信頼します (そうでない場合はスプーフィング)。

## 5. gRPC と WebSocket

Ingress は、**gRPC** の **HTTP/2** と、**WebSockets** の **アップグレード** / 長期接続をサポートする必要があります。すべてのデフォルトのアノテーションが両方をサポートしているわけではありません。コントローラーのドキュメントを確認してください。

## 6. DNS + 一緒に進入する

1. **DNS** `A`/`AAAA` または `CNAME` → **ロード バランサー** クラウドまたはベアメタル LB によって提供される IP またはホスト名。
2. **Ingress** ルールは **ホスト**と一致し、正しい **サービス**にルーティングします。
3. **TLS** 証明書は、**ホスト** (証明書上の SAN) をカバーする必要があります。

### 例 — Kubernetes 上の REST API (本番環境)

仮定する：

- パブリック REST API: **`https://api.example.com`**
- ステージング API: **`https://api.staging.example.com`**
- イングレス コントローラーからのクラウド ロード バランサーのホスト名: **`k8s-prod-abc123.eu-west-1.elb.amazonaws.com`** (AWS スタイル。GCP/Azure は独自の LB ホスト名または静的 IP を使用します)
- クラスター内 **サービス**: `rest-api-prod` (ポート **8080**)、`rest-api-staging` (ポート **8080**)

**ステップ 1 — DNS レコード** (ゾーン **`example.com`** の DNS プロバイダーで作成します):

|レコード名 (ホスト名) |タイプ |値 / へのポイント | TTL |目的 |
|--------------------------|------|---------------------|-----|----------|
| **`api.example.com`** | **CNAME** | `k8s-prod-abc123.eu-west-1.elb.amazonaws.com` | 300 |実稼働 REST API — 名前は **入力ロード バランサー** に解決されます。
| **`api.staging.example.com`** | **CNAME** | `k8s-prod-abc123.eu-west-1.elb.amazonaws.com` | 300 |ステージング API — 同じ LB。 **Ingress Host** ヘッダーはバックエンドを選択します。
| **`_acme-challenge.api.example.com`** | **TXT** | (cert-manager / Let’s Encrypt からの値) | 60 | TLS 証明書発行のドメイン制御を証明 |
| **`api.example.com`** (オプションの頂点エイリアス) | **A** | `203.0.113.50` | 300 |クラウドが CNAME ターゲットではなく **安定した IPv4** を提供する場合にのみ **A** を使用します。

レコード名に関する注意:

- 多くの UI では、**名前** 列はゾーンに関連しています。`api.example.com` の完全な FQDN ではなく、**`api`** を入力してください。 `api.staging.example.com` には **`api.staging`** と入力します。
- ほとんどのプロバイダーでは、ゾーンの頂点 (`example.com` 自体) に CNAME を付けないでください**。ルートが LB に到達する必要がある場合は、**A/AAAA** または **ALIAS/ANAME** を使用してください。
- **PTR** は API 用に作成するものではありません。逆引き DNS は IP アロケーター (クラウド プロバイダー) によって所有されます。

**ステップ 2 — イングレス ルール** (DNS が LB に解決された後に何が起こるか):

| `Host` ヘッダー (DNS 名と一致する必要があります) |パス |バックエンドサービス |サービスポート | TLS 証明書 SAN |
|-------------------------------------|------|--------------|--------------|--------------|
| **`api.example.com`** | `/` (プレフィックス) | `rest-api-prod` | 8080 | `api.example.com` |
| **`api.staging.example.com`** | `/` | `rest-api-staging` | 8080 | `api.staging.example.com` |
| **`api.example.com`** | `/health` | `rest-api-prod` | 8080 |同じ証明書 |

クライアントは常に **同じ LB IP/ホスト名** に接続します。 **Host** ヘッダー (URL から) は、どの **Service** が HTTP リクエストを受信するかをイングレス コントローラーに伝えます。

**ステップ 3 — 1 つの REST 呼び出しのエンドツーエンド パス**

```text
GET https://api.example.com/v1/users/42

1. DNS     api.example.com  CNAME → k8s-prod-abc123…elb.amazonaws.com → 203.0.113.50
2. TCP     client → 203.0.113.50:443
3. TLS     SNI = api.example.com  (cert must list this name)
4. HTTP    Host: api.example.com  Path: /v1/users/42
5. Ingress rule matches host api.example.com → Service rest-api-prod:8080
6. Pod     Spring Boot / Express / etc. handles GET /v1/users/42
```

**よくある間違い**

|間違い |症状 |
|----------|----------|
| DNS **A** は **pod** IP を指します |ポッドが再起動すると中断します。常に **LB / ingress** を指します |
| Ingress の **ホスト** ≠ DNS 名 | 404 またはデフォルトのバックエンド。証明書の不一致 |
|証明書 SAN がありません **`api.staging.example.com`** |ステージング URL のみでのブラウザ TLS エラー |
|移行中に忘れられた低 TTL |クライアントが古い IP に何時間もアクセスする |

### 例 — リージョンごとに REST API をゾーニングする (グローバル展開)

**複数のリージョン クラスタ** (EU、US、APAC) を実行する場合、クライアントは**最も近い**入力に到達する必要があり、コンプライアンスのため、場合によってはその**管轄区域**内の**のみ**のデータに到達する必要があります。 2 つの一般的な DNS パターン:

|パターン |公開 URL |ルーティングの仕組み |最適な時期 |
|-----------|-----------|-----------|----------|
| **1 つの名前の地理 DNS** | `api.example.com` |リゾルバーはクライアントの地域によって **異なる A/CNAME** を返します |モバイル/Web アプリは **単一** API ホスト名を使用します |
| **地域のサブドメイン** | `api.eu.example.com`、`api.us.example.com` |クライアント (または構成) がゾーンを明示的に選択します。 B2B 統合、**データ常駐** 契約、デバッグ |
| **両方** | `api.example.com` + 地域別名 |デフォルトの地理 DNS。オーバーライド/フェイルオーバー用のサブドメイン |コンプライアンス＋利便性を備えた大型製品 |

3 つの実稼働クラスターを想定します。

|地域 | Kubernetes クラスター |イングレス LB ホスト名 |プライマリ データ ストア |
|----------|-------------------|---------------------|--------|
| **EU** | `prod-eu-west-1` | `k8s-eu-aaa111.eu-west-1.elb.amazonaws.com` | **eu-west-1** の RDS / DB |
| **米国** | `prod-us-east-1` | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` | **us-east-1** の RDS |
| **アジア太平洋** | `prod-ap-southeast-1` | `k8s-ap-ccc333.ap-southeast-1.elb.amazonaws.com` | **ap-southeast-1** の RDS |

**オプション A — `api.example.com`** の地理 DNS (Route 53 地理位置情報、Cloudflare 負荷分散、Azure Traffic Manager など):

|レコード名 |タイプ |ルーティングポリシー |値 / へのポイント |目的 |
|-----------|------|----------------|--------|-----------|
| **`api.example.com`** | **CNAME** |地理的位置: **ヨーロッパ** | `k8s-eu-aaa111.eu-west-1.elb.amazonaws.com` | EU ユーザー → EU 進入 |
| **`api.example.com`** | **CNAME** |地理的位置: **北米** | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` |米国/カナダ → 米国の入力 |
| **`api.example.com`** | **CNAME** |地理的位置: **アジア太平洋** | `k8s-ap-ccc333.ap-southeast-1.elb.amazonaws.com` | APAC → AP イングレス |
| **`api.example.com`** | **CNAME** |地理位置情報: **デフォルト** | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` |地域が不明な場合のフォールバック |

各リージョン **Ingress** は **同じ** `Host: api.example.com` ルールを使用します。**バックエンド クラスター** のみが異なります。

|地域 | `Host` |パス |バックエンドサービス |メモ |
|----------|----------|------|---------------------|----------|
| EU | `api.example.com` | `/v1/` | `rest-api` | **EU** データベースのみ読み取り/書き込み |
|米国 | `api.example.com` | `/v1/` | `rest-api` | **US** データベースのレプリカまたはプライマリ |
|アジア太平洋 | `api.example.com` | `/v1/` | `rest-api` | **APAC** データベース |

TLS: SAN **`api.example.com`** を持つ 1 つの証明書 (どこでも同じ名前)。同じ証明書 (または地域の証明書マネージャー発行者) を使用して **各地域** のイングレスで終了します。

**オプション B — 明示的な地域サブドメイン** (コンプライアンスとパートナーのドキュメントが明確になります):

|レコード名 |タイプ |値 / へのポイント |目的 |
|-------------|------|--------|----------|
| **`api.eu.example.com`** | **CNAME** | `k8s-eu-aaa111.eu-west-1.elb.amazonaws.com` | EU REST API — GDPR / EU データ常駐 |
| **`api.us.example.com`** | **CNAME** | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` |アメリカAPI |
| **`api.ap.example.com`** | **CNAME** | `k8s-ap-ccc333.ap-southeast-1.elb.amazonaws.com` |アジア太平洋 API |
| **`api.example.com`** | **CNAME** |地域ポリシーまたは **CNAME** → `api.us.example.com` |グローバル マーケティング URL。または、オプション A | のように地理的ルートで指定されます。

|地域 | `Host` (イングレス) | TLS 証明書 SAN |クライアント構成 |
|------|---------------|--------------|---------------|
| EU | `api.eu.example.com` | `api.eu.example.com` | EU モバイル アプリのビルド ポイントはこちら |
|米国 | `api.us.example.com` | `api.us.example.com` |米国のアプリ / デフォルトの SDK ベース URL |
|アジア太平洋 | `api.ap.example.com` | `api.ap.example.com` | APAC テナントのオンボーディング |

**リクエスト フロー (EU ユーザー、オプション A)**

```text
GET https://api.example.com/v1/orders

1. DNS (geo)   resolver in Germany → api.example.com → EU LB IP
2. TLS         SNI api.example.com
3. Ingress EU  Host api.example.com → rest-api:8080 (EU cluster)
4. App         uses EU DB connection string; no cross-region DB hop on hot path
```

**リクエスト フロー (パートナー ピン EU サブドメイン、オプション B)**

```text
GET https://api.eu.example.com/v1/orders

1. DNS         api.eu.example.com → EU LB only (no geo guesswork)
2. Ingress EU  Host api.eu.example.com → rest-api:8080
```

**グローバル展開チェックリスト**

|懸念事項 |練習 |
|----------|----------|
| **レイテンシ** |地域 DNS または地域サブドメインにより、RTT が低く抑えられます。デフォルトで EU ユーザー→ US クラスターを回避 |
| **データ常駐** | **オプション B** またはトークン内のシャード ID を優先します。 PII を保存するホスト名を文書化します。
| **セッション / JWT** |地域固有の発行者または `region` 請求。海を越えてスティッキーなセッションを共有しないでください |
| **リージョン間での書き込み** |非同期レプリケーションまたはエンティティごとの **単一書き込み領域**。 REST API ドキュメントの状態整合性モデル |
| **健康診断** |リージョンごとの LB ヘルス。 EU LB が異常な場合は geo DNS **フェイルオーバー** レコードを次のリージョンに記録します。
| **可観測性** | `region=eu-west-1` を使用してメトリクス/ログにタグを付けます。 1 つのグローバル ダッシュボード、地域別アラート |

**アンチパターン**

|アンチパターン |なぜ痛いのか |
|--------------|--------------|
| 1 つのグローバル クラスター、1 つの DB、地理 DNS のみ | DNS はユーザーを **近くのエッジ**に送信しますが、**アプリ + DB** は依然として 1 つのリージョンである可能性があります。以下の修正を参照してください。
|同じ `Host` ルール、リージョン間で DB を共有 |コンプライアンス違反。すべてのクエリのリージョン間のレイテンシ |
|すべてのリージョンを **1** LB に CNAME |ゾーニングの無効化 - すべてのトラフィックが単一のリージョンに到達します。

#### レプリケーションまたはシャーディングで「地理 DNS のみ」を修正できますか?

**部分的ですが、DNS だけではなく、データとコンピューティングがユーザーとともに移動する場合に限ります**。

|修正 |追加するもの |解決するもの |何が**解決しない** |
|-----|--------------|----------------|----------------------------|
| **リージョン アプリ層** | **EU、米国、APAC** の Ingress + API ポッド (上記のオプション A/B) | TLS/HTTP はローカルで処理されます。アプリのコードはクライアントの近くで実行されます。データそのものについては何もありません |
| **読み取りレプリケーション** | 1 つのリージョンの **プライマリ** + 他のリージョンの **リードレプリカ**。リージョン API は読み取りに **ローカル レプリカ** を使用します | `GET /v1/orders`、ダッシュボード、キャッシュの **読み取り遅延** | **書き込み**は、非同期レプリケーションのラグを受け入れない限り、依然としてプライマリ (クロスオーシャン RTT) に達します。
| **マルチプライマリ/アクティブ-アクティブ** | CockroachDB、Spanner、Aurora Global、Cassandra など |一部のユーザーに近い書き込みを行います。組み込みの競合処理 |複雑さ、コスト、**最終整合性**のトレードオフ。すべての SQL アプリが簡単に移行できるわけではありません。
| **リージョン別の DB シャーディング** |シャードキー = `region` または `tenant_region`; EU 行は **EU プライマリ** シャードに存在します |ルーティングが正しい場合、**読み取りと書き込み**はリージョン内に留まります。クロスリージョンのクエリ/結合。痛みの再分割。間違ったシャード キーにより EU ユーザーが米国のデータに送信される |
| **地域 DNS のみ + CDN** |エッジで `GET` をキャッシュする |静的アセットと **キャッシュ可能な** API 応答 |パーソナライズされたまたは `POST`/`PUT` は依然としてオリジン + DB に遠く離れたところに到達します。

**実行可能な最小限の修正 (一般的な REST パターン)**

```text
Geo DNS → regional ingress → regional API pods → local read replica (reads)
                                              → primary or regional writer (writes)
```

1. **リージョン クラスター** (1 つのグローバル LB への地理 DNS だけではありません) を展開します。
2. リージョンごとに **リードレプリカ** を追加します。接続プールを構成します: **読み取り** → `replica.eu.internal`、**書き込み** → `primary` またはリージョン ローカル ライター。
3. 読み取り時の **レプリケーション ラグ** (`GET` は N 秒間失効する可能性があります) を文書化するか、セッションに対して **read-your-writes** ルーティングを使用します。
4. **厳密な常駐**の場合、その管轄区域内の**プライマリ** データをシャードまたはピン留めします (`api.eu` → EU プライマリのみ) - 海外の唯一のコピーとしてではなく、DR 用のレプリケーション。

**シャーディングの例 (キー内の領域)**

|シャード |主な場所 |サービス |
|------|------|----------|
| `region=eu` | `eu-west-1` RDS | `api.eu.example.com` と EU geo-DNS トラフィック |
| `region=us` | `us-east-1` RDS | `api.us.example.com` とアメリカ大陸の交通 |
| `region=ap` | `ap-southeast-1` RDS | APAC トラフィック |

Ingress はトラフィックを地域 API に送信します。 API はテナント/ユーザー → **シャード**を解決し、**そのリージョン**で DB 接続を開きます。このスタックを使用しない Geo DNS は、**最初のネットワーク ホップ** のみを最適化します。

**経験則:** レプリケーションは **読み取り距離** を修正します。シャーディング (またはリージョン プライマリ) により **書き込み距離と常駐**が修正されます。 geo DNS は、クライアントが **どの玄関ドア** をノックするかを修正します。グローバル REST API では、3 つすべてを調整する必要があります。

## 7. 研究順序の要約

**TCP/UDP** → **HTTP** → **TLS** → **DNS** (名前 → アドレス) → **Ingress/LB** (HTTP ルーティングと TLS エッジ)。これらは一緒に、ブラウザーのリクエストがどのようにポッドに到達するかを説明します。
