---
label: "V"
subtitle: "Docker in CI"
group: "CI/CD"
order: 5
---
Docker in CI
Standard pattern: **build image** → **push to registry** → **deploy by tag**. Same flow on GitHub Actions, GitLab, Jenkins, CircleCI.

## 1. Pipeline flow

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

## 2. Multi-stage Dockerfile (Spring Boot example)

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

| Stage | Size impact |
|-------|-------------|
| Builder | JDK + Maven cache — discarded |
| Runtime | JRE + JAR only — **small** prod image |

## 3. Layer caching in CI

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

GitHub **`docker/build-push-action`** and GitLab **BuildKit** support cache backends.

## 4. Tags and immutability

| Tag | Use |
|-----|-----|
| `$GIT_SHA` | Traceable to commit |
| `$BRANCH-$SHA` | Human-readable |
| `latest` | Convenience — **avoid** alone in prod |
| Semver `v1.4.2` | Release from tag |

Deploy **`digest@sha256:…`** for maximum immutability.

## 5. buildx and multi-platform

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myregistry/myapp:1.0.0 \
  --push .
```

Needed for **Apple Silicon** dev + **AMD64** cloud, or **Graviton** ARM nodes.

## 6. Security in CI

| Practice | Tool |
|----------|------|
| Scan image for CVEs | Trivy, Grype, Snyk |
| Generate **SBOM** | syft, build attestations |
| Sign image | cosign, Notation |
| Non-root USER in Dockerfile | Reduce container escape impact |
| `.dockerignore` | Exclude `.git`, secrets, `target/` |

```yaml
# GitHub Actions — Trivy scan after build
- uses: aquasecurity/trivy-action@master
  with:
    image-ref: ghcr.io/org/app:${{ github.sha }}
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
```

## 7. Docker-in-Docker (DinD) notes

GitLab `docker:dind` service and Jenkins Docker agents need **privileged** mode — security trade-off. Prefer **Kaniko** or **buildkit rootless** where policy requires.

## 8. Local parity

```bash
docker compose -f docker-compose.ci.yml run --rm test
```

Same image CI uses → “works on my machine” shrinks.

**Related:** `ii-github-actions.md`, `iii-gitlab-ci.md`, `../security-and-best-practices/ii-supply-chain-and-slsa.md`.
