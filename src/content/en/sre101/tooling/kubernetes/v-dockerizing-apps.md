---
label: "V"
subtitle: "Dockerizing apps"
group: "SRE"
order: 5
---
SRE tooling — Kubernetes: Dockerizing apps
Images are what Kubernetes runs—design **Dockerfiles** so Pods stay **small**, **secure**, and **probe-friendly**.

## 1. What Kubernetes expects from your image

- A **long-running process** (or batch Job/CronJob exit 0) as **PID 1** or wrapped so signals propagate correctly.
- The app **listens on a port** (often **`0.0.0.0`**, not only **`localhost`**) matching **`containerPort`** in the Pod spec.
- **Configurable via env vars / mounted files**—12-factor style—so the **same image** serves dev/stage/prod.
- **Readiness** and **liveness** paths or TCP checks your app exposes consistently (see **Workloads & health** in this folder).

## 2. Dockerfile patterns

### Multi-stage builds

Compile/test in a **builder** stage; copy only artifacts into the **runtime** stage—smaller attack surface and faster pulls to Nodes.

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

## 3. PID 1, signals, and graceful shutdown

Kubernetes **`terminationGracePeriodSeconds`** sends **SIGTERM** then **SIGKILL**. If PID 1 does not forward signals, shutdown stalls draining connections.

- Prefer **`exec`** form **`ENTRYPOINT`** so the runtime receives signals (`ENTRYPOINT ["java", …]` not **`sh -c`** unless wrapped carefully).
- For shells/scripts wrapping binaries, use **`dumb-init`** or **`tini`** as PID 1.
- Implement **`SIGTERM`** handling in apps—finish in-flight HTTP requests within grace budget.

## 4. Users and filesystem

- Run **non-root** (`USER` in Dockerfile + **`securityContext.runAsNonRoot`** in Pod spec).
- Prefer **`readonlyRootFilesystem: true`** in Pods when possible—mount **`tmp`**/`writable-volume`s only where needed.
- Avoid baking secrets into images—inject via **Secrets**/CSI/`envFrom`.

## 5. Base images

Balance patch cadence vs size: **`distroless`**, **`alpine`**, **`wolfi`**/`chainguard`, or vendor hardened bases—scan regularly (**`trivy`**, **`grype`**, registry scanners).

Pin digests (**`image@sha256:…`**) in production manifests once promoted—not only `:latest`.

## 6. Observability hooks

- **Structured logs** to **stdout/stderr** (Kubernetes aggregates **`kubectl logs`** / agents avoid parsing arbitrary files).
- **Expose metrics** on **`/metrics`** if Prometheus scrapes the Pod (**Instrumentation** under Tooling → Prometheus).
- Align **`EXPOSE`**/listening port with **Service** **`targetPort`** and probes (**`/healthz`**, **`/readyz`**).

## 7. Resource hints translate to Kubernetes

Profile locally (`docker run`) rough RSS/CPU at modest load—use numbers as starting **`requests`** / **`limits`** in Deployments (iterate after observing kube-metrics).

## 8. CI checklist

1. **`docker build`** on every merge; tag **`git sha`** + semver.
2. Push to registry **near** the cluster region.
3. Scan image; block critical CVEs per policy.
4. Smoke **run container** + **`curl`** readiness endpoint before deploy promotion.

This bridges **container build** to **Pod spec** tuning—next steps live in **Workloads & health** and **GitOps & operations** in this folder.
