---
label: "V"
subtitle: "Ingress, edge, and load balancers"
group: "Networking"
order: 5
---
Networking — Part V: Ingress, edge, and load balancers

By the time traffic hits your cluster or data center, **TCP** is established and **TLS** may already be terminated. **Ingress** (especially in **Kubernetes**) is the **HTTP(S) routing layer** that maps **hostnames and paths** to **Services** and pods.

## 1. Load balancer vs reverse proxy

- **Network / L4 load balancer** — distributes **TCP/UDP** flows by IP/port (sometimes TLS pass-through). Fast, less application-aware.
- **Application / L7 reverse proxy** — understands **HTTP** (Host, path, headers), can do **TLS termination**, compression, rate limits, WAF integration.

**Ingress controllers** (nginx, Traefik, HAProxy, Envoy-based gateways, cloud vendor controllers) are usually **L7** proxies in front of **NodePort/ClusterIP** or cloud LB integrations.

## 2. Kubernetes Ingress (conceptual)

- An **Ingress** resource declares rules: **host**, **path** → **backend Service** (and port).
- The **controller** watches Ingress objects and programs the proxy (routes, certs).
- **TLS** is often wired via **Secrets** referenced by the Ingress; **cert-manager** automates **ACME** certificates.

Traffic path (typical):

```text
Internet → cloud LB (optional TLS) → Ingress controller → Service → Pod
```

## 3. TLS at the edge

- **Terminate TLS at ingress** — pods see HTTP; simpler, but traffic inside the cluster may be plaintext unless you add **mTLS** or **backend TLS**.
- **Pass-through TLS** — LB forwards encrypted TCP; ingress or app terminates; useful when SNI routing is done at a smarter LB.

## 4. Headers proxies set

Clients see one hop; backends need context:

- **X-Forwarded-For** — original client IP (chain of proxies).
- **X-Forwarded-Proto** — `http` or `https` as seen by the first proxy.
- **X-Forwarded-Host** — original Host header.

Trust only **trusted** proxies when interpreting these (spoofing otherwise).

## 5. gRPC and WebSockets

Ingress must support **HTTP/2** for **gRPC**, and **Upgrade** / long-lived connections for **WebSockets**. Not every default annotation supports both; verify controller docs.

## 6. DNS + Ingress together

1. **DNS** `A`/`AAAA` or `CNAME` → **load balancer** IP or hostname provided by the cloud or bare-metal LB.
2. **Ingress** rules match **Host** to route to the right **Service**.
3. **TLS** cert must cover that **Host** (SAN on certificate).

### Example — REST API on Kubernetes (production)

Assume:

- Public REST API: **`https://api.example.com`**
- Staging API: **`https://api.staging.example.com`**
- Cloud load balancer hostname from the ingress controller: **`k8s-prod-abc123.eu-west-1.elb.amazonaws.com`** (AWS-style; GCP/Azure use their own LB hostnames or static IPs)
- In-cluster **Services**: `rest-api-prod` (port **8080**), `rest-api-staging` (port **8080**)

**Step 1 — DNS records** (create at your DNS provider for zone **`example.com`**):

| Record name (hostname) | Type | Value / points to | TTL | Purpose |
|------------------------|------|-------------------|-----|---------|
| **`api.example.com`** | **CNAME** | `k8s-prod-abc123.eu-west-1.elb.amazonaws.com` | 300 | Production REST API — name resolves to the **ingress load balancer** |
| **`api.staging.example.com`** | **CNAME** | `k8s-prod-abc123.eu-west-1.elb.amazonaws.com` | 300 | Staging API — same LB; **Ingress Host** header picks the backend |
| **`_acme-challenge.api.example.com`** | **TXT** | (value from cert-manager / Let’s Encrypt) | 60 | Proves domain control for TLS certificate issuance |
| **`api.example.com`** (optional apex alias) | **A** | `203.0.113.50` | 300 | Use **A** only if the cloud gives a **stable IPv4** instead of a CNAME target |

Notes on record names:

- In many UIs the **Name** column is relative to the zone: enter **`api`** not the full FQDN for `api.example.com`; enter **`api.staging`** for `api.staging.example.com`.
- **Do not** CNAME the zone apex (`example.com` itself) on most providers — use **A/AAAA** or **ALIAS/ANAME** if the root must hit the LB.
- **PTR** is not something you create for your API; reverse DNS is owned by the IP allocator (cloud provider).

**Step 2 — Ingress rules** (what happens after DNS resolves to the LB):

| `Host` header (must match DNS name) | Path | Backend Service | Service port | TLS cert SAN |
|-------------------------------------|------|-----------------|--------------|--------------|
| **`api.example.com`** | `/` (prefix) | `rest-api-prod` | 8080 | `api.example.com` |
| **`api.staging.example.com`** | `/` | `rest-api-staging` | 8080 | `api.staging.example.com` |
| **`api.example.com`** | `/health` | `rest-api-prod` | 8080 | same cert |

The client always connects to the **same LB IP/hostname**; the **Host** header (from the URL) tells the ingress controller which **Service** receives the HTTP request.

**Step 3 — End-to-end path for one REST call**

```text
GET https://api.example.com/v1/users/42

1. DNS     api.example.com  CNAME → k8s-prod-abc123…elb.amazonaws.com → 203.0.113.50
2. TCP     client → 203.0.113.50:443
3. TLS     SNI = api.example.com  (cert must list this name)
4. HTTP    Host: api.example.com  Path: /v1/users/42
5. Ingress rule matches host api.example.com → Service rest-api-prod:8080
6. Pod     Spring Boot / Express / etc. handles GET /v1/users/42
```

**Common mistakes**

| Mistake | Symptom |
|---------|---------|
| DNS **A** points to a **pod** IP | Breaks when pods restart; always point to **LB / ingress** |
| **Host** in Ingress ≠ DNS name | 404 or default backend; cert mismatch |
| Cert SAN missing **`api.staging.example.com`** | Browser TLS error on staging URL only |
| Low TTL forgotten during migration | Clients hit old IP for hours |

## 7. Study order recap

**TCP/UDP** → **HTTP** → **TLS** → **DNS** (name → address) → **Ingress/LB** (HTTP routing and TLS at the edge). Together they describe how a browser request reaches a pod.
