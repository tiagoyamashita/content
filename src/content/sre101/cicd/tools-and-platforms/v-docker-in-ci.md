---
label: "V"
subtitle: "CI の Docker"
group: "CI/CD"
order: 5
---
CI の Docker

標準パターン: **イメージのビルド** → **レジストリへのプッシュ** → **タグによるデプロイ**。 GitHub アクション、GitLab、Jenkins、CircleCI でも同じフロー。

## 1. パイプラインの流れ

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 100" role="img" aria-label="Docker build push deploy in CI">
  <rect x="12" y="40" width="64" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="60" fill="#e4e4e7" font-size="9">git commit</text>
  <path d="M76 56 H96" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="96" y="40" width="64" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="108" y="60" fill="#e4e4e7" font-size="9">docker build</text>
  <path d="M160 56 H180" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="180" y="40" width="64" height="32" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="192" y="60" fill="#e4e4e7" font-size="9">push registry</text>
  <path d="M244 56 H264" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="264" y="40" width="64" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="276" y="60" fill="#e4e4e7" font-size="9">deploy tag</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Immutable artifact = image digest or semver tag</text>
</svg></figure>

## 2. 多段階の Docker ファイル (Spring Boot の例)

```dockerfile
# syntax=docker/dockerfile:1

FROM eclipse-temurin:22-jdk AS builder
WORKDIR /app
COPY mvnw pom.xml ./
COPY .mvn .mvn
RUN ./mvnw -B dependency:go-offline
COPY src ./src
RUN ./mvnw -B package -DskipTests

FROM eclipse-temurin:22-jre
WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar
USER 1000
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

|ステージ |サイズへの影響 |
|------|-----------|
|ビルダー | JDK + Maven キャッシュ — 破棄 |
|ランタイム | JRE + JAR のみ — **小さい** 製品イメージ |

## 3. CI でのレイヤーキャッシュ

```bash
docker pull myregistry/myapp:cache || true
docker build \
  --cache-from myregistry/myapp:cache \
  -t myregistry/myapp:$GIT_SHA \
  -t myregistry/myapp:cache \
  .
docker push myregistry/myapp:$GIT_SHA
docker push myregistry/myapp:cache
```

GitHub **`docker/build-push-action`** および GitLab **BuildKit** はキャッシュ バックエンドをサポートしています。

## 4. タグと不変性

|タグ |使用 |
|-----|-----|
|`$GIT_SHA`|コミットまで追跡可能 |
|`$BRANCH-$SHA`|人間が読める |
|`latest`|利便性 — 製品内で単独で使用することは避けてください |
|センバー`v1.4.2`|タグからのリリース |

展開する **`digest@sha256:…`** 最大限の不変性を実現します。

## 5. buildx とマルチプラットフォーム

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myregistry/myapp:1.0.0 \
  --push .
```

**Apple Silicon** 開発 + **AMD64** クラウド、または **Graviton** ARM ノードに必要です。

## 6. CIのセキュリティ

|練習 |ツール |
|----------|------|
| CVE のスキャン画像 |トリビー、グライプ、スニック |
| **SBOM** を生成 | syft、証明書を構築する |
|サイン画像 |余符号、記法 |
| Dockerfile 内の非ルート USER |コンテナ脱出の影響を軽減 |
|`.dockerignore`|除外する`.git`、秘密、`target/`|

```yaml
# GitHub Actions — Trivy scan after build
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/org/app:${{ github.sha }}
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
```

## 7. __​​ IT0__-in-Docker (DinD) メモ

Gitラボ`docker:dind`サービスと Jenkins Docker エージェントには **特権** モードが必要です (セキュリティのトレードオフ)。ポリシーが必要な場合は、**Kaniko** または **buildkit rootless** を優先します。

## 8. ローカルパリティ

```bash
docker compose -f docker-compose.ci.yml run --rm test
```

CI が使用しているのと同じイメージ → 「私のマシンで動作します」が縮小されます。

**関連:** [GitHub アクション](ii-github-actions.md)、[Gitラボ CI](iii-gitlab-ci.md)、[サプライ チェーンと SLSA](../security-and-best-practices/ii-supply-chain-and-slsa.md）。
