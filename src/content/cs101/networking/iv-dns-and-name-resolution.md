---
label: "IV"
subtitle: "DNS and name resolution"
group: "Networking"
order: 4
---
Networking — Part IV: DNS and name resolution

**DNS** maps **human-readable names** (`api.example.com`) to **records** used at connection time: mostly **A/AAAA** (addresses), **CNAME** (alias), **MX** (mail), **TXT** (verification, SPF, etc.).

## 1. Why DNS matters before TCP and TLS

To open **TCP** to `api.example.com:443`, the resolver must obtain an **IP address**. The TLS **ClientHello** often includes **SNI** with the same hostname so the server can pick the right certificate.

## 2. Recursive vs authoritative

- **Stub resolver** (your laptop, container) asks a **recursive resolver** (ISP, `8.8.8.8`, corporate DNS, CoreDNS in Kubernetes).
- The recursive resolver walks the tree from **root** → **TLD** (`.com`) → **authoritative** nameservers for `example.com` until it gets the final answer, then **caches** it according to **TTL**.

## 3. Record types (practical subset)

| Type | Role | Name | Value |
|------|------|------|-------|
| **A** | IPv4 address | `api` | `203.0.113.50` |
| **AAAA** | IPv6 address | `api` | `2001:db8::1` |
| **CNAME** | Canonical name — alias to another hostname | `api` | `k8s-lb.eu-west-1.elb.amazonaws.com` |
| **TXT** | Arbitrary text | `_acme-challenge.api` | `xK8f9Qm2vP7L3nR8wT1sY0uJ5hF4gD6cB2aE` |
| **TXT** | Arbitrary text | `@` | `v=spf1 include:_spf.google.com ~all` |
| **NS** | Delegates zone to authoritative servers | `@` | `ns1.cloudflare.com` |
| **NS** | Delegates zone to authoritative servers | `@` | `ns2.cloudflare.com` |

### Hostinger hPanel — DNS zone list (zone `myrestapp.com`)

Same records as they appear under **Websites → myrestapp.com → DNS / DNS records** (columns **Type**, **Name**, **Points to**, **TTL**):

| Type | Name | Points to | TTL |
|------|------|-----------|-----|
| A | @ | 185.248.155.42 | 14400 |
| A | ftp | 185.248.155.42 | 14400 |
| CNAME | www | myrestapp.com | 14400 |
| CNAME | api | lb-1847293021.eu-west-1.elb.amazonaws.com | 300 |
| AAAA | api | 2001:db8:5ca8:1::42 | 300 |
| TXT | _acme-challenge.api | xK8f9Qm2vP7L3nR8wT1sY0uJ5hF4gD6cB2aE | 300 |
| TXT | @ | v=spf1 include:_spf.google.com ~all | 14400 |
| NS | @ | ns1.dns-parking.com | 14400 |
| NS | @ | ns2.dns-parking.com | 14400 |

## 4. TTL and caching

**TTL** (time to live) on each answer tells resolvers how long they may cache. **Low TTL** speeds failover and migrations; **high TTL** reduces load and can improve resilience to resolver issues but slows cutover.

## 5. Kubernetes, DNS, and Ingress

Kubernetes uses **two different DNS systems**. Confusing them is a common source of “works in the cluster, fails from my laptop” bugs.

| DNS scope | Who answers | Example name | Used by |
|-----------|-------------|--------------|---------|
| **Public (internet)** | Hostinger, Cloudflare, Route 53, … | `api.myrestapp.com` | Browsers, mobile apps, partners |
| **In-cluster** | **CoreDNS** | `rest-api.default.svc.cluster.local` | Pods talking to Services |

Public DNS stops at your **cloud load balancer**. **Ingress** only runs **after** TCP reaches the cluster and uses the HTTP **`Host`** header — DNS does not know about Kubernetes Services.

### What is Ingress?

**Ingress** (in Kubernetes) is the **HTTP/HTTPS front door** for apps running in a cluster. It has two parts:

| Piece | What it is |
|-------|------------|
| **Ingress resource** | A config object (YAML) that lists rules: “if **`Host`** is `api.myrestapp.com` and path is `/v1/…`, send traffic to **Service** `rest-api` on port **8080**.” |
| **Ingress controller** | A running program (nginx, Traefik, …) that **reads** those rules and configures a **reverse proxy** to enforce them. |

**Ingress is not DNS.** DNS tells the client **which IP** to connect to. Ingress tells the cluster **which Service** should handle the request **after** the connection arrives, using the URL’s hostname and path.

**Ingress is not a Service.** A **Service** is stable in-cluster networking to pods. **Ingress** sits **in front of** Services and routes **external** HTTP traffic to the right one.

```text
DNS:      api.myrestapp.com  →  203.0.113.50 (load balancer)
Ingress:  Host: api.myrestapp.com  +  path /v1/users  →  Service rest-api:8080  →  Pod
```

### 5.1 In-cluster DNS (CoreDNS)

Every **Service** gets a stable DNS name inside the cluster:

```text
<service>.<namespace>.svc.cluster.local
```

| Service | Namespace | Cluster DNS name | ClusterIP (example) |
|---------|-----------|------------------|---------------------|
| `rest-api` | `default` | `rest-api.default.svc.cluster.local` | `10.96.42.18` |
| `postgres` | `data` | `postgres.data.svc.cluster.local` | `10.96.88.5` |

- Pods use this name in connection strings — **not** pod IPs (pods restart and change IP).
- Short names work inside the same namespace: `rest-api` → `rest-api.default.svc.cluster.local`.
- This DNS is **not** visible on the public internet.

### 5.2 From public DNS to the cluster

Typical cloud setup for a REST API:

1. You deploy an **Ingress controller** (nginx, Traefik, …) behind a **LoadBalancer** Service.
2. The cloud creates a **load balancer** with a hostname, e.g. `lb-1847293021.eu-west-1.elb.amazonaws.com`.
3. In **Hostinger** (or any public DNS) you add **`api` CNAME → that hostname** (see §3 table).
4. Client resolves `api.myrestapp.com` → LB IP → **TCP :443** → **Ingress controller** pod.

| Public DNS record | Points to | Kubernetes object |
|-------------------|-----------|-------------------|
| `api` CNAME | `lb-1847293021.eu-west-1.elb.amazonaws.com` | `Service` type **LoadBalancer** (or LB in front of Ingress) |
| (none in public DNS) | — | **Ingress** rule: `Host: api.myrestapp.com` |
| (none in public DNS) | — | **Service** `rest-api` → **Pods** |

### 5.3 What Ingress adds (after DNS)

**DNS** answers: “What IP is `api.myrestapp.com`?”  
**Ingress** answers: “For `Host: api.myrestapp.com` and path `/v1/…`, which **Service** and port?”

| Ingress field | Example | Must match |
|---------------|---------|------------|
| `host` | `api.myrestapp.com` | Name clients use in URL **and** TLS cert SAN |
| `path` | `/` or `/v1` | URL path prefix |
| `backend.service.name` | `rest-api` | Kubernetes Service name |
| `backend.service.port.number` | `8080` | Service port (targets container port) |

Minimal Ingress (conceptual YAML):

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: rest-api
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - api.myrestapp.com
      secretName: api-tls-cert
  rules:
    - host: api.myrestapp.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: rest-api
                port:
                  number: 8080
```

**cert-manager** often creates the `api-tls-cert` Secret and the **`_acme-challenge.api`** TXT record in public DNS during issuance.

### 5.4 End-to-end path (illustration)

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 280" role="img" aria-label="Public DNS through load balancer ingress service to pod">
  <defs>
    <marker id="net-iv-k8s-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Internet → cluster (api.myrestapp.com)</text>
  <rect x="12" y="36" width="88" height="44" rx="4" fill="rgba(24,24,27,0.95)" stroke="#71717a"/>
  <text x="28" y="58" fill="#e4e4e7" font-size="10">Client</text>
  <text x="20" y="72" fill="#a1a1aa" font-size="8">browser / app</text>
  <rect x="120" y="36" width="100" height="44" rx="4" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="132" y="54" fill="#fbbf24" font-size="9" font-weight="600">Public DNS</text>
  <text x="128" y="68" fill="#a1a1aa" font-size="8">Hostinger / Route53</text>
  <rect x="240" y="36" width="108" height="44" rx="4" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="252" y="54" fill="#60a5fa" font-size="9" font-weight="600">Cloud LB</text>
  <text x="248" y="68" fill="#a1a1aa" font-size="8">:443 TCP + TLS</text>
  <rect x="368" y="28" width="140" height="120" rx="6" fill="rgba(34,197,94,0.06)" stroke="#86efac" stroke-dasharray="5 3"/>
  <text x="380" y="44" fill="#86efac" font-size="9" font-weight="600">Kubernetes cluster</text>
  <rect x="380" y="52" width="116" height="36" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="392" y="68" fill="#e4e4e7" font-size="8">Ingress controller</text>
  <text x="392" y="80" fill="#a1a1aa" font-size="7">Host: api.myrestapp.com</text>
  <rect x="380" y="96" width="116" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="392" y="114" fill="#e4e4e7" font-size="8">Service rest-api:8080</text>
  <rect x="392" y="132" width="92" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="408" y="147" fill="#e4e4e7" font-size="8">Pod (REST app)</text>
  <path d="M100 58 H120" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="102" y="50" fill="#71717a" font-size="7">① query</text>
  <path d="M220 58 H240" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="222" y="50" fill="#71717a" font-size="7">② CNAME→IP</text>
  <path d="M348 58 H368" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="350" y="50" fill="#71717a" font-size="7">③ connect</text>
  <path d="M438 88 V96" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <path d="M438 124 V132" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="12" y="100" fill="#d4d4d8" font-size="10" font-weight="600">Inside the cluster (pod → pod)</text>
  <rect x="12" y="112" width="72" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="134" fill="#e4e4e7" font-size="9">Pod A</text>
  <rect x="120" y="112" width="140" height="36" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="128" y="128" fill="#a855f7" font-size="8" font-weight="600">CoreDNS</text>
  <text x="128" y="140" fill="#a1a1aa" font-size="7">rest-api.default.svc…</text>
  <rect x="280" y="112" width="80" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="292" y="134" fill="#e4e4e7" font-size="9">Service</text>
  <rect x="380" y="112" width="72" height="36" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="392" y="134" fill="#e4e4e7" font-size="9">Pod B</text>
  <path d="M84 130 H120" stroke="#a855f7" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <path d="M260 130 H280" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <path d="M360 130 H380" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#net-iv-k8s-mk)"/>
  <text x="12" y="168" fill="#71717a" font-size="9">④ Ingress matches Host + path  ⑤ Service picks a ready pod</text>
  <rect x="12" y="182" width="496" height="88" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="200" fill="#d4d4d8" font-size="9" font-weight="600">Checklist</text>
  <text x="24" y="216" fill="#a1a1aa" font-size="8">Public: api CNAME → LB hostname (TTL 300 during migrations)</text>
  <text x="24" y="230" fill="#a1a1aa" font-size="8">Ingress host = api.myrestapp.com · TLS secret covers same name</text>
  <text x="24" y="244" fill="#a1a1aa" font-size="8">Service name/port in Ingress = Service manifest · selector → pod labels</text>
  <text x="24" y="258" fill="#a1a1aa" font-size="8">kubectl get ingress,svc · dig api.myrestapp.com · curl -v https://api.myrestapp.com/health</text>
</svg></figure>

### 5.5 Objects at a glance

| Layer | Kubernetes kind | Name (example) | DNS / addressing |
|-------|-----------------|----------------|------------------|
| Workload | Deployment | `rest-api` | — |
| Network | Service | `rest-api` | `rest-api.default.svc.cluster.local` |
| Routing | Ingress | `rest-api` | Needs **public** DNS → LB |
| Entry | Service (LB) | `ingress-nginx-controller` | Cloud hostname for CNAME |
| Config | Secret | `api-tls-cert` | TLS cert/key for Ingress |

### 5.6 Common mistakes

| Symptom | Likely cause |
|---------|--------------|
| `curl: Could not resolve host` | Public DNS missing or wrong **Name** / **Points to** |
| TLS cert name mismatch | Cert SAN ≠ URL host; fix Ingress `tls.hosts` or DNS name |
| 404 from nginx ingress | Ingress `host` or `path` does not match request |
| Works inside cluster, not outside | Used `rest-api.default.svc` URL from laptop — need public `api.myrestapp.com` |
| DNS OK but connection refused | LB / firewall / Ingress controller Service not ready |

Full REST + Hostinger + regional examples: **Part V — Ingress** [Ingress, edge, and load balancers](v-ingress-edge-and-load-balancers.md).

## 6. Operational footguns

- **Stale cache** after IP changes.
- **Split-horizon DNS** — different answers inside corp vs internet (debugging surprises).
- **DNSSEC** — authenticity chain for DNS itself (adoption varies).

Next: **Ingress** and edge routing (HTTP routing on top of names and IPs).
