---
label: "II"
subtitle: "インストール"
group: "SRE"
order: 2
---
SRE ツール — Grafana: インストール

ラボおよび本番環境向けのセットアップで Grafana を実行する一般的な方法。

## 1. 公式パッケージとバイナリ

- VM を簡単にインストールする必要がある場合は、OS 固有のパッケージ (**APT/YUM/RPM**) に従うか、Grafana の配布ページからバイナリをダウンロードします。
- HTTP ポートの **`grafana.ini`** (または環境変数)、リバース プロキシの背後の **`root_url`**、および管理者の資格情報を構成します。デフォルトはすぐにローテーションされます。

## 2. ドッカー

```text
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

永続化のために **`/var/lib/grafana`** をマウントします。非対話型ブートストラップの場合は **`GF_SECURITY_ADMIN_PASSWORD`** を挿入します。

## 3. Kubernetes (ヘルム)

Grafana のチャート リポジトリから **Grafana Helm チャート** を使用します。ピン チャート バージョン、**`persistence.enabled`** を設定し、**`datasources`** YAML またはサイドカー構成を介してデータソースを挿入して、ポッドが再スケジュールに耐えられるようにします。

## 4. グラファナクラウド

マネージド Grafana は運用オーバーヘッドを除去します。 Prometheus 互換のエンドポイントとベンダーのドキュメントごとにホストされたログ/トレースを接続します。バイナリを実行せずに SSO とスケーリングが必要な場合に適しています。

## 5. 最初のデータソース

Grafana が起動したら、**接続 → データソースの追加 → Prometheus** (または Loki)、URL (クラスター内サービス DNS またはゲートウェイ) を設定し、**保存してテスト**します。一貫した名前を付けて環境ごとに繰り返します (`prometheus-prod`、`loki-prod`)。
