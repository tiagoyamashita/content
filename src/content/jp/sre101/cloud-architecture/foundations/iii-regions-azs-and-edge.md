---
label: "III"
subtitle: "リージョン、AZ、エッジ"
group: "クラウドアーキテクチャ"
order: 3
---
リージョン、AZ、エッジ

クラウドの容量は**地理的に**整理されます。ここでの設計の選択は、**レイテンシー**、**コンプライアンス**、**フォールト トレランス**に影響します。

## 1. 地域

A **region** is an independent geographic area (e.g. `us-east-1`, `eu-west-1`, `ap-southeast-1`).

|プロパティ |詳細 |
|----------|----------|
|隔離 |あるリージョン内のリソースは別のリージョンに自動複製されません**。
|レイテンシ |ユーザーに近い地域を選択 |
|コンプライアンス |データ常駐 (GDPR — EU 地域) |
|サービス |すべてのサービスがすべての地域に存在するわけではありません。

```text
AWS (example)
  us-east-1 (N. Virginia)
  eu-west-1 (Ireland)
  ap-northeast-1 (Tokyo)
```

## 2. アベイラビリティーゾーン (AZ)

**AZ** は、**低遅延のプライベート ファイバー** でリンクされた、リージョン内の 1 つ以上の物理的に分離されたデータ センターです。

```text
Region: eu-west-1
  ├── eu-west-1a   (datacenter campus A)
  ├── eu-west-1b   (datacenter campus B)
  └── eu-west-1c   (datacenter campus C)
```

| Rule | Why |
|------|-----|
| Deploy across **≥ 2 AZs** | Survive single DC failure |
| Same region, different AZ | Low latency, synchronous options |
| Don't assume AZ names match across accounts | `1a` in account A ≠ same building as `1a` in account B |

## 3. メンタルモデル図

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 110" role="img" aria-label="Region with three AZs">
  <rect x="12" y="24" width="376" height="72" rx="4" fill="none" stroke="#52525b"/>
  <text x="20" y="40" fill="#d4d4d8" font-size="10" font-weight="600">Region (eu-west-1)</text>
  <rect x="28" y="52" width="96" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="52" y="72" fill="#e4e4e7" font-size="9">AZ-a</text>
  <rect x="152" y="52" width="96" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="176" y="72" fill="#e4e4e7" font-size="9">AZ-b</text>
  <rect x="276" y="52" width="96" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="300" y="72" fill="#e4e4e7" font-size="9">AZ-c</text>
  <text x="12" y="108" fill="#71717a" font-size="9">Load balancer spans AZs · RDS Multi-AZ standby in another AZ</text>
</svg></figure>

## 4. エッジ/PoP (Point of Presence)

**CDN エッジ ノード** は、ユーザーの近くにコンテンツをキャッシュします。領域全体ではなく、グローバルに分散されます (数百の場所)。

|サービス |プロバイダー |
|----------|----------|
|クラウドフロント | AWS |
|アズール CDN / フロントドア |アズール |
|クラウド CDN | GCP |
|クラウドフレア |マルチクラウドエッジ |

**用途:** 静的アセット (JS、CSS、画像)、キャッシュ可能な API GET 応答、エッジでの TLS 終端。

## 5. マルチリージョン vs マルチ AZ

| |マルチ AZ |マルチリージョン |
|---|----------|--------------|
|から保護します |単一の DC 障害 |リージョン全体の停止 |
|レイテンシ |同じ領域 (AZ 間で約 1 ～ 2 ミリ秒) |地域を超えて高い |
|複雑さ |標準 HA | DNS フェイルオーバー、レプリケーションの遅延 |
|コスト |中程度 |高 (インフラの複製 + 転送) |

Start with **multi-AZ**; add **multi-region** when RTO/RPO or compliance requires it [HA & disaster recovery](vii-ha-and-disaster-recovery.md).

## 6. データ常駐の例

| Requirement | Design |
|-------------|--------|
| EU personal data stays in EU | Deploy in `eu-west-1`, restrict replication |
| Global product, local compliance | Per-region stacks + geo-routing |
| DR in second region | Async replication — understand RPO |

## 7. ローカル ゾーンと波長 (AWS コンテキスト)

|拡張子 |目的 |
|----------|----------|
| **ローカルゾーン** |地域の拡張 — 都市までの超低遅延 |
| **波長** | 5G エッジ — モバイル/ゲームの遅延 |

特殊 — 特定のメトロにとってミリ秒が重要な場合に使用します。

## 8. 地域の選択チェックリスト

- [ ] プライマリ ユーザーへの待ち時間
- [ ] 必要なサービスが利用可能
- [ ] 法的/データの所在地
- [ ] 価格 (地域によって異なります)
- [ ] DR 領域がペアになっているか、明示的に選択されています

**Related:** [Networking, VPC & LB](vi-networking-vpc-and-lb.md), [HA & disaster recovery](vii-ha-and-disaster-recovery.md), patterns **CDN** note.
