---
label: "V"
subtitle: "Ingress, edge, and load balancers"
group: "Networking"
order: 5
---
Networking — Part V: Ingress, edge, and load balancers

By the time traffic hits your cluster or data center, **TCP** is established and **TLS** may already be terminated.

### What is Ingress?

**Ingress** is an **application-layer (L7) entry point** that routes **HTTP and HTTPS** requests to the correct backend based on **hostname**, **URL path**, and sometimes **headers** — instead of sending every request on the same IP to a single app.

In **Kubernetes** specifically:

- An **Ingress** object is **configuration** (rules + optional TLS).
- An **Ingress controller** is the **running proxy** that applies those rules (nginx Ingress Controller, Traefik, AWS Load Balancer Controller, …).

| Term | Layer | Job |
|------|-------|-----|
| **Load balancer (L4)** | TCP/UDP | Spread connections across nodes; may not look at URL |
| **Ingress (L7)** | HTTP/HTTPS | “`api.example.com/v1` → this Service; `www.example.com` → that Service” |
| **Service** | In-cluster | Stable address to a set of pods |

Non-Kubernetes systems use the same idea under names like **reverse proxy**, **API gateway**, or **edge router** — Kubernetes standardized the name **Ingress** for the config resource.

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

| Protocol | LB must… |
|----------|----------|
| **WebSocket** | Allow **101 Switching Protocols**, long timeouts, often **session affinity** |
| **SSE** | Disable response buffering; long-lived **GET** |
| **gRPC** | **HTTP/2** end-to-end or grpc-aware proxy |

Deep dive: [WebSockets, SSE, and gRPC](vii-websockets-sse-grpc-and-realtime.md). Layer placement: [L4/L7 layers and where to balance](vi-l4-l7-layers-and-where-to-balance.md).

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

### Example — zoning a REST API by region (global deploy)

When you run **multiple regional clusters** (EU, US, APAC), you need clients to reach the **nearest** ingress and, for compliance, sometimes **only** data in that **jurisdiction**. Two common DNS patterns:

| Pattern | Public URL | How routing works | Best when |
|---------|------------|-------------------|-----------|
| **Geo DNS on one name** | `api.example.com` | Resolver returns **different A/CNAME** by client geography | Mobile/web apps use a **single** API hostname |
| **Regional subdomains** | `api.eu.example.com`, `api.us.example.com` | Client (or config) picks the zone explicitly | B2B integrations, **data residency** contracts, debugging |
| **Both** | `api.example.com` + regional aliases | Geo DNS for default; subdomains for override / failover | Large products with compliance + convenience |

Assume three production clusters:

| Region | Kubernetes cluster | Ingress LB hostname | Primary data store |
|--------|-------------------|---------------------|-------------------|
| **EU** | `prod-eu-west-1` | `k8s-eu-aaa111.eu-west-1.elb.amazonaws.com` | RDS / DB in **eu-west-1** |
| **US** | `prod-us-east-1` | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` | RDS in **us-east-1** |
| **APAC** | `prod-ap-southeast-1` | `k8s-ap-ccc333.ap-southeast-1.elb.amazonaws.com` | RDS in **ap-southeast-1** |

**Option A — Geo DNS on `api.example.com`** (Route 53 Geolocation, Cloudflare Load Balancing, Azure Traffic Manager, etc.):

| Record name | Type | Routing policy | Value / points to | Purpose |
|-------------|------|----------------|-------------------|---------|
| **`api.example.com`** | **CNAME** | Geolocation: **Europe** | `k8s-eu-aaa111.eu-west-1.elb.amazonaws.com` | EU users → EU ingress |
| **`api.example.com`** | **CNAME** | Geolocation: **North America** | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` | US/Canada → US ingress |
| **`api.example.com`** | **CNAME** | Geolocation: **Asia Pacific** | `k8s-ap-ccc333.ap-southeast-1.elb.amazonaws.com` | APAC → AP ingress |
| **`api.example.com`** | **CNAME** | Geolocation: **Default** | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` | Fallback if geo unknown |

Each regional **Ingress** uses the **same** `Host: api.example.com` rule — only the **backend cluster** differs:

| Region | `Host` | Path | Backend Service | Notes |
|--------|--------|------|-----------------|-------|
| EU | `api.example.com` | `/v1/` | `rest-api` | Reads/writes **EU** database only |
| US | `api.example.com` | `/v1/` | `rest-api` | **US** database replica or primary |
| APAC | `api.example.com` | `/v1/` | `rest-api` | **APAC** database |

TLS: one certificate with SAN **`api.example.com`** (same name everywhere); terminate at **each regional** ingress with the same cert (or regional cert-manager issuers).

**Option B — explicit regional subdomains** (clearer for compliance and partner docs):

| Record name | Type | Value / points to | Purpose |
|-------------|------|-------------------|---------|
| **`api.eu.example.com`** | **CNAME** | `k8s-eu-aaa111.eu-west-1.elb.amazonaws.com` | EU REST API — GDPR / EU data residency |
| **`api.us.example.com`** | **CNAME** | `k8s-us-bbb222.us-east-1.elb.amazonaws.com` | Americas API |
| **`api.ap.example.com`** | **CNAME** | `k8s-ap-ccc333.ap-southeast-1.elb.amazonaws.com` | Asia-Pacific API |
| **`api.example.com`** | **CNAME** | Geo policy or **CNAME** → `api.us.example.com` | Global marketing URL; or geo-routed as in Option A |

| Region | `Host` (Ingress) | TLS cert SAN | Client config |
|--------|------------------|--------------|---------------|
| EU | `api.eu.example.com` | `api.eu.example.com` | EU mobile app build points here |
| US | `api.us.example.com` | `api.us.example.com` | US app / default SDK base URL |
| APAC | `api.ap.example.com` | `api.ap.example.com` | APAC tenant onboarding |

**Request flow (EU user, Option A)**

```text
GET https://api.example.com/v1/orders

1. DNS (geo)   resolver in Germany → api.example.com → EU LB IP
2. TLS         SNI api.example.com
3. Ingress EU  Host api.example.com → rest-api:8080 (EU cluster)
4. App         uses EU DB connection string; no cross-region DB hop on hot path
```

**Request flow (partner pins EU subdomain, Option B)**

```text
GET https://api.eu.example.com/v1/orders

1. DNS         api.eu.example.com → EU LB only (no geo guesswork)
2. Ingress EU  Host api.eu.example.com → rest-api:8080
```

**Global deploy checklist**

| Concern | Practice |
|---------|----------|
| **Latency** | Geo DNS or regional subdomain so RTT stays low; avoid EU user → US cluster by default |
| **Data residency** | Prefer **Option B** or shard IDs in tokens; document which hostname stores PII where |
| **Sessions / JWT** | Region-specific issuers or `region` claim; don’t share sticky sessions across oceans |
| **Writes across regions** | Async replication or **single write region** per entity; REST API docs state consistency model |
| **Health checks** | Per-region LB health; geo DNS **failover** record to next region if EU LB unhealthy |
| **Observability** | Tag metrics/logs with `region=eu-west-1`; one global dashboard, regional alerts |

**Anti-patterns**

| Anti-pattern | Why it hurts |
|--------------|--------------|
| One global cluster, one DB, geo DNS only | DNS sends user to a **nearby edge** but **app + DB** may still be one region — see fixes below |
| Same `Host` rule, shared DB across regions | Compliance failure; cross-region latency on every query |
| CNAME all regions to **one** LB | Defeats zoning — all traffic hits a single region |

#### Can replication or sharding fix “geo DNS only”?

**Partly — but only if data and compute move with the user**, not DNS alone.

| Fix | What you add | What it solves | What it does **not** solve |
|-----|--------------|----------------|----------------------------|
| **Regional app tier** | Ingress + API pods in **EU, US, APAC** (Option A/B above) | TLS/HTTP handled locally; app code runs near the client | Nothing about data by itself |
| **Read replication** | **Primary** in one region + **read replicas** in others; regional API uses **local replica** for reads | **Read latency** for `GET /v1/orders`, dashboards, caches | **Writes** still hit primary (cross-ocean RTT) unless you accept async replication lag |
| **Multi-primary / active-active** | CockroachDB, Spanner, Aurora Global, Cassandra, etc. | Writes closer to some users; built-in conflict handling | Complexity, cost, **eventual consistency** trade-offs; not all SQL apps migrate easily |
| **DB sharding by region** | Shard key = `region` or `tenant_region`; EU rows live on **EU-primary** shard | **Reads and writes** stay in-region when routing is correct | Cross-region queries/joins; re-sharding pain; wrong shard key sends EU user to US data |
| **Geo DNS only + CDN** | Cache `GET` at edge | Static assets and **cacheable** API responses | Personalized or `POST`/`PUT` still reach origin + DB far away |

**Minimal viable fix (common REST pattern)**

```text
Geo DNS → regional ingress → regional API pods → local read replica (reads)
                                              → primary or regional writer (writes)
```

1. Deploy **regional clusters** (not just geo DNS to one global LB).
2. Add **read replicas** per region; configure connection pools: **read** → `replica.eu.internal`, **write** → `primary` or region-local writer.
3. Document **replication lag** on reads (`GET` may be stale for N seconds) or use **read-your-writes** routing for the session.
4. For **strict residency**, shard or pin **primary** data in that jurisdiction (`api.eu` → EU-primary only) — replication for DR, not as the only copy abroad.

**Sharding example (region in the key)**

| Shard | Primary location | Serves |
|-------|------------------|--------|
| `region=eu` | `eu-west-1` RDS | `api.eu.example.com` and EU geo-DNS traffic |
| `region=us` | `us-east-1` RDS | `api.us.example.com` and Americas traffic |
| `region=ap` | `ap-southeast-1` RDS | APAC traffic |

Ingress sends traffic to the regional API; the API resolves tenant/user → **shard** and opens a DB connection **in that region**. Geo DNS without this stack only optimizes the **first network hop**.

**Rule of thumb:** replication fixes **read distance**; sharding (or regional primaries) fixes **write distance and residency**; geo DNS fixes **which front door** the client knocks on — you need all three aligned for a global REST API.

## 7. Study order recap

**TCP/UDP** → **HTTP** → **TLS** → **DNS** (name → address) → **Ingress/LB** (HTTP routing and TLS at the edge) → **L4/L7 placement** → **WebSockets / SSE / gRPC**. Together they describe how a browser request reaches a pod — and stays connected when the app is realtime.

- [L4/L7 layers and where to balance](vi-l4-l7-layers-and-where-to-balance.md)
- [WebSockets, SSE, and gRPC](vii-websockets-sse-grpc-and-realtime.md)
