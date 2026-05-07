---
label: "II"
subtitle: "Installation"
group: "SRE"
order: 2
---
SRE tooling — Grafana: Installation
Common ways to run Grafana for labs and production-shaped setups.

## 1. Official packages & binary

- Follow OS-specific packages (**APT/YUM/RPM**) or download the binary from Grafana’s distribution pages when you need a quick VM install.
- Configure **`grafana.ini`** (or env vars) for HTTP port, **`root_url`** behind reverse proxies, and admin credentials—rotate defaults immediately.

## 2. Docker

```text
docker run -d -p 3000:3000 --name=grafana grafana/grafana
```

Mount **`/var/lib/grafana`** for persistence; inject **`GF_SECURITY_ADMIN_PASSWORD`** for non-interactive bootstrap.

## 3. Kubernetes (Helm)

Use the **Grafana Helm chart** from Grafana’s chart repo: pin chart version, set **`persistence.enabled`**, and inject datasources via **`datasources`** YAML or sidecar configs so Pods survive reschedules.

## 4. Grafana Cloud

Managed Grafana removes ops overhead; connect Prometheus-compatible endpoints and hosted logs/traces per vendor docs—good when you want SSO and scaling without running the binary.

## 5. First datasource

After Grafana is up: **Connections → Add datasource → Prometheus** (or Loki), set URL (in-cluster service DNS or gateway), **Save & test**. Repeat per environment with consistent naming (`prometheus-prod`, `loki-prod`).
