---
label: "V"
subtitle: "アプリをDocker化する"
group: "SRE"
order: 5
---
SRE ツール — Kubernetes: アプリの Docker 化

イメージは Kubernetes が実行するものであり、ポッドが **小型**、**安全**、**プローブに優しい**状態を保つように **Dockerファイル**を設計します。

## 1. Kubernetes がイメージに期待するもの

- A **long-running process** (or batch Job/CronJob exit 0) as **PID 1** or wrapped so signals propagate correctly.
- The app **listens on a port** (often **`0.0.0.0`**, not only **`localhost`**) matching **`containerPort`** in the Pod spec.
- **Configurable via env vars / mounted files**—12-factor style—so the **same image** serves dev/stage/prod.
- **Readiness** and **liveness** paths or TCP checks your app exposes consistently (see **Workloads & health** in this folder).

## 2. Dockerファイルのパターン

### マルチステージビルド

**ビルダー** ステージでコンパイル/テストします。アーティファクトのみを **ランタイム** ステージにコピーします。攻撃対象領域が小さくなり、ノードへのプルが高速になります。

```dockerfile
# build
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app
COPY . .
RUN ./mvnw -q -DskipTests package

# run
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
USER nobody
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
```

Adjust for Node (`npm ci` + `node dist`), Go (`FROM scratch` + static binary), Python (`venv` + slim base), etc.

### `.dockerignore`

Exclude **`target/`**, **`node_modules/`**, **`.git`**, local **`*.env`** so **`COPY`** stays deterministic and builds stay fast.

## 3. PID 1、シグナル、および正常なシャットダウン

Kubernetes **`terminationGracePeriodSeconds`** sends **SIGTERM** then **SIGKILL**. If PID 1 does not forward signals, shutdown stalls draining connections.

- Prefer **`exec`** form **`ENTRYPOINT`** so the runtime receives signals (`ENTRYPOINT ["java", …]` not **`sh -c`** unless wrapped carefully).
- For shells/scripts wrapping binaries, use **`dumb-init`** or **`tini`** as PID 1.
- Implement **`SIGTERM`** handling in apps—finish in-flight HTTP requests within grace budget.

## 4. ユーザーとファイルシステム

- Run **non-root** (`USER` in Dockerfile + **`securityContext.runAsNonRoot`** in Pod spec).
- Prefer **`readonlyRootFilesystem: true`** in Pods when possible—mount **`tmp`**/`writable-volume`s only where needed.
- Avoid baking secrets into images—inject via **Secrets**/CSI/`envFrom`.

## 5. 基本イメージ

Balance patch cadence vs size: **`distroless`**, **`alpine`**, **`wolfi`**/`chainguard`, or vendor hardened bases—scan regularly (**`trivy`**, **`grype`**, registry scanners).

Pin digests (**`image@sha256:…`**) in production manifests once promoted—not only `:latest`.

## 6. 可観測性フック

- **Structured logs** to **stdout/stderr** (Kubernetes aggregates **`kubectl logs`** / agents avoid parsing arbitrary files).
- **Expose metrics** on **`/metrics`** if Prometheus scrapes the Pod (**Instrumentation** under Tooling → Prometheus).
- Align **`EXPOSE`**/listening port with **Service** **`targetPort`** and probes (**`/healthz`**, **`/readyz`**).

## 7. リソースヒントは Kubernetes に変換されます

Profile locally (`docker run`) rough RSS/CPU at modest load—use numbers as starting **`requests`** / **`limits`** in Deployments (iterate after observing kube-metrics).

## 8. CI チェックリスト

1. **`docker build`** on every merge; tag **`git sha`** + semver.
2. Push to registry **near** the cluster region.
3. Scan image; block critical CVEs per policy.
4. Smoke **run container** + **`curl`** readiness endpoint before deploy promotion.

これにより、**コンテナのビルド** から **ポッド仕様** の調整までの橋渡しが行われます。次のステップは、このフォルダーの **ワークロードと健全性** および **GitOps と運用** にあります。
