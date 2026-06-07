---
label: "II"
subtitle: "Supply chain & SLSA"
group: "CI/CD"
order: 2
---
Supply chain & SLSA
**Supply chain attacks** target dependencies, build tools, and registries — not just your application code. **SLSA** (Supply-chain Levels for Software Artifacts) defines maturity levels for trustworthy builds.

## 1. Common risks

| Risk | Example |
|------|---------|
| **Typosquatting** | `reqeusts` instead of `requests` on PyPI |
| **Dependency confusion** | Private package name published publicly |
| **Compromised action/plugin** | Malicious update to a CI action |
| **Registry takeover** | Unsigned image replaced in registry |
| **Build script injection** | Untrusted PR modifies workflow YAML |

## 2. SLSA levels

| Level | Requirement | Typical CI capability |
|-------|-------------|------------------------|
| **L1** | Build process documented and logged | Any CI with history |
| **L2** | Hosted build service + signed provenance | GitHub/GitLab attestations |
| **L3** | Hardened, isolated, reproducible build | Dedicated build cluster, hermetic deps |
| **L4** | Two-person review + hermetic, reproducible | Highest assurance (rare in practice) |

Most teams target **L2** with signed provenance and pinned dependencies; **L3** for security-sensitive releases.

## 3. Pin actions and dependencies

**Bad** — tag can move:

```yaml
- uses: actions/checkout@v4
```

**Better** — immutable commit SHA:

```yaml
- uses: actions/checkout@b4ffde65f46336ab88eb625be47e5b2ead783297 # v4.1.1
```

Use **Renovate** or **Dependabot** to open PRs when SHAs/tags update — you still review before merge.

**Maven / npm** — commit lock files (`package-lock.json`, `pom.xml` with BOM):

```xml
<!-- pom.xml — pin dependency versions explicitly -->
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
  <version>3.4.0</version>
</dependency>
```

## 4. SBOM generation

**SBOM** (Software Bill of Materials) lists every component in a build.

```yaml
# GitHub Actions — Syft SBOM
- name: Generate SBOM
  uses: anchore/sbom-action@v0
  with:
    path: .
    format: spdx-json

- name: Upload SBOM artifact
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: sbom.spdx.json
```

| Tool | Output | Use |
|------|--------|-----|
| **Syft** | SPDX, CycloneDX | General SBOM |
| **Trivy** | CVE + SBOM | Scan + inventory |
| **Gradle SBOM plugin** | CycloneDX | JVM builds |

Store SBOMs with release artifacts for audit and incident response.

## 5. Sign and verify artifacts

**Cosign** (sigstore) signs container images:

```bash
# Sign after push
cosign sign --yes registry.example.com/myapp:1.2.3

# Verify before deploy (in cluster or deploy script)
cosign verify registry.example.com/myapp:1.2.3 \
  --certificate-identity=... \
  --certificate-oidc-issuer=...
```

GitHub **artifact attestations** tie a build to a commit and workflow — consumers verify provenance before promotion.

## 6. Scan in CI

```yaml
# Trivy — filesystem + image
- name: Scan repo
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: fs
    severity: CRITICAL,HIGH
    exit-code: 1

- name: Scan image
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: myapp:${{ github.sha }}
    severity: CRITICAL,HIGH
    exit-code: 1
```

| Scan type | Catches |
|-----------|---------|
| **Dependency (SCA)** | Known CVEs in libraries |
| **SAST** | Code patterns (Semgrep, CodeQL) |
| **Container** | OS packages in image layers |
| **IaC** | Misconfig in Terraform/K8s manifests |

Gate merges on **CRITICAL/HIGH**; track MEDIUM in backlog.

## 7. Renovate / Dependabot example

```json
// renovate.json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "matchManagers": ["github-actions"],
      "pinDigests": true
    },
    {
      "matchUpdateTypes": ["major"],
      "dependencyDashboardApproval": true
    }
  ]
}
```

## 8. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| `curl \| bash` in Dockerfile without checksum | Pin version + verify hash |
| Private registry creds in image layers | BuildKit secrets, multi-stage |
| Ignoring scan failures | `exit-code: 1` on HIGH+ |
| No lock file in repo | Commit lockfile; fail CI if out of sync |

**Related:** [Docker in CI](../tools-and-platforms/v-docker-in-ci.md), [Secrets & OIDC](iii-secrets-and-oidc.md).
