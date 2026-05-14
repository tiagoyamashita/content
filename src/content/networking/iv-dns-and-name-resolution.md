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

| Type | Role |
|------|------|
| **A** | IPv4 address |
| **AAAA** | IPv6 address |
| **CNAME** | Canonical name — another hostname (often restricted at zone apex) |
| **TXT** | Arbitrary text — ACME challenges, SPF, DKIM |
| **NS** | Delegates a zone to authoritative servers |

## 4. TTL and caching

**TTL** (time to live) on each answer tells resolvers how long they may cache. **Low TTL** speeds failover and migrations; **high TTL** reduces load and can improve resilience to resolver issues but slows cutover.

## 5. Kubernetes and ingress

Inside a cluster, **CoreDNS** serves **cluster.local** names for **Services**. **External** names still use upstream resolvers. **Ingress** resources rely on DNS in the real world pointing **A/AAAA/CNAME** to your **load balancer** or **anycast** edge so clients reach the right IP before HTTP/TLS applies.

## 6. Operational footguns

- **Stale cache** after IP changes.
- **Split-horizon DNS** — different answers inside corp vs internet (debugging surprises).
- **DNSSEC** — authenticity chain for DNS itself (adoption varies).

Next: **Ingress** and edge routing (HTTP routing on top of names and IPs).
