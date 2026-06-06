---
label: "II"
subtitle: "サービスモデル"
group: "クラウドアーキテクチャ"
order: 2
---
サービスモデル — IaaS、PaaS、SaaS

クラウド プロバイダーはハードウェアを **レイヤー** で抽象化します。上位レイヤーは、**運用の負担が軽減**され、**低レベルの制御が軽減される**ことを意味します。

## 1. 3 つのモデル

|モデル |あなたが管理します |プロバイダーが管理 |例 |
|----------|-----------|----------|----------|
| **IaaS** | OS、ランタイム、アプリ、データ |ハイパーバイザー、ハードウェア、DC | EC2、Azure VM、GCE |
| **PaaS** |アプリのコードとデータ | OS、ランタイム、スケーリング | App Engine、Elastic Beanstalk、Heraku |
| **SaaS** |設定とデータ |その他すべて | Gmail、Salesforce、GitHub |

```text
Responsibility stack (bottom = always provider):

  SaaS     │████████████████│  you: config only
  PaaS     │████████░░░░░░░░│  you: app + data
  IaaS     │████░░░░░░░░░░░░│  you: OS through app
           └────────────────┘
           Hardware / virtualization
```

<figure class="notes-diagram"><svg xmlns="1 viewBox="0 0 440 140" role="img" aria-label="IaaS PaaS SaaS responsibility stack">
  <rect x="20" y="10" width="120" height="24" rx="4" fill="#27272a"/>
  <text x="80" y="27" fill="#86efac" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">IaaS</text>
  <rect x="160" y="10" width="120" height="24" rx="4" fill="#27272a"/>
  <text x="220" y="27" fill="#fbbf24" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">PaaS</text>
  <rect x="300" y="10" width="120" height="24" rx="4" fill="#27272a"/>
  <text x="360" y="27" fill="#60a5fa" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">SaaS</text>
  <text x="220" y="68" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">← more control          less ops burden →</text>
  <rect x="20" y="82" width="400" height="18" rx="3" fill="#18181b"/>
  <text x="220" y="95" fill="#52525b" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Physical hardware / data center (always provider-managed)</text>
  <rect x="20" y="106" width="400" height="18" rx="3" fill="#1c1c1f"/>
  <text x="220" y="119" fill="#52525b" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Hypervisor / virtualization</text>
</svg></figure>

## 2. 責任共有モデル

セキュリティとコンプライアンスは**常に共有**されます。SaaS であってもアクセスを構成し、資格情報を保護します。

|エリア | IaaS | PaaS | SaaS |
|------|------|------|------|
|物理的なセキュリティ |プロバイダー |プロバイダー |プロバイダー |
|ネットワークパッチ適用 |プロバイダー |プロバイダー |プロバイダー |
| OSパッチ適用 | **あなた** |プロバイダー |プロバイダー |
|アプリの脆弱性 | **あなた** | **あなた** |共有 |
|アイデンティティとアクセス | **あなた** | **あなた** | **あなた** |
|データ暗号化 | **あなた** | **あなた** |よく共有される |

## 3. モデルの選択

|状況 | | に向かって傾ける
|----------|---------------|
|レガシー アプリのリフトアンドシフト | IaaS (EC2) |
|標準 Web アプリ、最小限の操作 | PaaS (Cloud Run、Elastic Beanstalk) |
|電子メール、CRM、ソース管理 | SaaS |
|カスタム カーネル モジュールが必要 | IaaS |
|スパイキーなイベント処理 |サーバーレス/FaaS (PaaS ファミリ) |

## 4. PaaS の極みとしての FaaS

**Functions as a Service** (Lambda、Cloud Functions) — コードをアップロードします。プロバイダーがそれを実行し、スケーリングします。 [計算オプション](iv-compute-options.md)を参照してください。

## 5. ハイブリッドとマルチクラウド

|用語 |意味 |
|-----|----------|
| **ハイブリッド** |オンプレミス + クラウド (VPN/ダイレクト接続) |
| **マルチクラウド** |冗長性またはベンダーミックスのための AWS + Azure |
| **クラウドネイティブ** |最初からクラウド API 向けに設計 |

IaaS の柔軟性はハイブリッドに役立ちます。 SaaS は統合の負担を軽減します。

## 6. コストへの影響

|モデル |一般的な請求 |
|------|------|
| IaaS |時間/秒あたりの VM、接続されたディスク |
| PaaS |アプリ インスタンス時間またはリクエスト単位 |
| SaaS |シートごと / 機能層ごと |

抽象度が高くなると、**使用率**が向上することがよくあります。料金は、アイドル状態の OS パッチ適用時間ではなく、使用した分に対して支払うことになります。

## 7. マッピングされた例

|ワークロード |モデル |サービス |
|----------|----------|----------|
| Linux 上のカスタム Java | IaaS | EC2 + EBS |
| Spring Boot コンテナ | IaaS/PaaS 境界 | EKS、クラウドラン |
|静的サイト + API | PaaS | S3 + API ゲートウェイ + Lambda |
|会社メール | SaaS | Google ワークスペース |

**関連:** [コンピューティング オプション](iv-compute-options.md)、[適切に設計されたフレームワーク](viii-well-architected-framework.md)。
