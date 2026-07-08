---
label: "II"
subtitle: "インストール"
group: "SRE"
order: 2
---
SRE ツール — Grafana: インストール

ラボおよび運用形態のセットアップで Grafana を実行する一般的な方法。

## 1. 公式パッケージとバイナリ

- Follow OS-specific packages (**APT/YUM/RPM**) or download the binary from Grafana’s distribution pages when you need a quick VM install.
- Configure **`grafana.ini`** (or env vars) for HTTP port, **`root_url`** behind reverse proxies, and admin credentials—rotate defaults immediately.

## 2. Docker

```text
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

Mount **`/var/lib/grafana`** for persistence; inject **`GF_SECURITY_ADMIN_PASSWORD`** for non-interactive bootstrap.

## 3. Kubernetes (ヘルム)

Use the **Grafana Helm chart** from Grafana’s chart repo: pin chart version, set **`persistence.enabled`**, and inject datasources via **`datasources`** YAML or sidecar configs so Pods survive reschedules.

## 4. Grafana クラウド

マネージド Grafana により、運用オーバーヘッドが除去されます。 Prometheus 互換のエンドポイントとベンダーのドキュメントごとにホストされたログ/トレースを接続します。バイナリを実行せずに SSO とスケーリングが必要な場合に適しています。

## 5. 最初のデータソース

After Grafana is up: **Connections → Add datasource → Prometheus** (or Loki), set URL (in-cluster service DNS or gateway), **Save & test**. Repeat per environment with consistent naming (`prometheus-prod`, `loki-prod`).
