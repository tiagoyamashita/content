---
label: "VI"
subtitle: "L4/L7 layers and where to balance"
group: "Networking"
order: 6
---
Networking — Part VI: L4/L7 layers and where to balance

**Load balancing** is not one decision — it depends on **which layer** of the stack your balancer understands. A **Layer 4 (L4)** device spreads **TCP/UDP flows**; a **Layer 7 (L7)** proxy routes **HTTP semantics** (Host, path, headers). Put the balancer in the wrong place and **WebSockets stick**, **gRPC breaks**, or **TLS certs** do not match.

For ingress rules and DNS examples, see [Ingress, edge, and load balancers](v-ingress-edge-and-load-balancers.md). For transport basics, see [TCP, UDP, and transport basics](i-tcp-udp-and-transport-basics.md).

## 1. Two layer models (practical view)

Engineers usually mix **OSI** names with the **TCP/IP** stack:

| OSI (conceptual) | TCP/IP stack | What you configure | Examples |
|------------------|--------------|-------------------|----------|
| **L7 Application** | Application | URLs, headers, cookies, RPC methods | HTTP, HTTPS, gRPC, WebSocket frames |
| **L6 Presentation** | (folded into app/TLS) | Encoding, TLS record encryption | TLS ciphertext after handshake |
| **L5 Session** | (often folded into app) | Long-lived sessions | WebSocket connection, JDBC pool |
| **L4 Transport** | Transport | IP + port, TCP connection | `:443`, `:5432`, SYN/ACK |
| **L3 Network** | Internet | Routing, IP addresses | `203.0.113.50`, VPC routes |
| **L2 Data link** | Network access | MAC, VLAN, ARP | Switch ports, NIC |

**Rule of thumb:** when someone says **“L7 load balancer”** they mean **application-aware HTTP(S) routing**. **“L4 load balancer”** means **connection distribution without parsing HTTP**.

```text
Client
  │
  ▼  L7 — Host: api.example.com  Path: /v1/users  (HTTP)
  ▼  L6 — TLS encrypts bytes (HTTPS)
  ▼  L4 — TCP to 203.0.113.50:443
  ▼  L3 — IP routing across the internet
```

## 2. What each balancer type sees

| Balancer type | Sees on the wire | Typical routing key | Does **not** see |
|---------------|------------------|---------------------|------------------|
| **L4 (NLB, hardware LB, `kube-proxy` in some modes)** | IP, port, protocol; optional TLS **SNI** if passthrough | 5-tuple `(src IP, src port, dst IP, dst port, proto)` | URL path, `Authorization` header, JSON body |
| **L7 (reverse proxy, Ingress, API gateway)** | HTTP request line, headers, sometimes body | `Host`, path prefix, header rules, cookie | SQL queries inside the app (unless you add custom L7 rules) |
| **DNS load balancing** | Client geography, health (via probes) | Geo, weighted records | Individual HTTP requests — only picks **which front door** |

**TLS termination changes the picture:**

| Mode | Where TLS ends | L4 LB role | L7 proxy role |
|------|----------------|------------|---------------|
| **Terminate at edge** | Cloud LB or Ingress | Forwards **plain HTTP** to backends (or re-encrypts) | Reads Host/path; sets `X-Forwarded-*` |
| **TLS passthrough (L4)** | Backend or dedicated TLS proxy | Forwards **encrypted TCP**; may use **SNI** to pick backend | Cannot inspect HTTP until something terminates TLS |
| **Re-encrypt (SSL bridging)** | Edge terminates, new TLS to backend | Often L4 to edge only | Edge → backend over HTTPS or mTLS |

## 3. Where to load balance — decision guide

| Traffic | Prefer balance at | Why |
|---------|-------------------|-----|
| **Public REST/JSON API** (`GET/POST /v1/...`) | **L7 Ingress / API gateway** | Route by **Host** and **path**; rate limits; WAF; one IP, many services |
| **Static site + API on same domain** | **L7** | `/` → CDN or static bucket; `/api` → app Service |
| **Raw TCP (Postgres, Redis, custom binary)** | **L4** | No HTTP to parse; connection-level spread |
| **TLS passthrough to many backends on one IP** | **L4 with SNI** or **dedicated TLS proxy** | Encrypted until backend; SNI picks cert/backend |
| **WebSockets / SSE / gRPC streaming** | **L7 that supports the protocol** + often **session affinity** | Long-lived connections; see [WebSockets, SSE, and gRPC](vii-websockets-sse-grpc-and-realtime.md) |
| **Microservices inside a VPC** | **L7 service mesh / sidecar** or **L4** between tiers | mTLS and path rules in mesh; DB stays L4 |
| **Global users, one hostname** | **DNS (geo/ latency)** → **regional L7/L4** | DNS picks region; LB spreads inside region — see Part V regional examples |

### Stack placement (typical cloud + Kubernetes)

```text
Internet
    │
    ▼
┌─────────────────────────────────────┐
│  DNS (geo / health)                 │  ← name → regional LB hostname
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Cloud L4 LB (optional)             │  ← high PPS, TLS passthrough, fixed IP
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  L7 Ingress / API gateway           │  ← Host, path, TLS terminate, WAF
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  Service / pods (app processes)     │  ← HTTP server, gRPC server, WS handler
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│  L4 to data tier (optional)         │  ← Postgres, Redis — rarely HTTP
└─────────────────────────────────────┘
```

**You do not need every box.** A small app: **DNS → one L7 reverse proxy → one app** is enough. Add **L4** when you need **millions of TCP connections**, **fixed IPs with passthrough**, or **non-HTTP protocols**.

## 4. L4 vs L7 — trade-offs

| | **L4 load balancing** | **L7 reverse proxy / Ingress** |
|--|------------------------|--------------------------------|
| **Speed / scale** | Very high connection rate; simple forwarding | Parses HTTP; more CPU per request |
| **Routing** | By IP/port (and sometimes SNI) | By URL, headers, gRPC service name |
| **TLS** | Passthrough common; terminate only if device supports it | Terminate at edge; cert per Host |
| **Observability** | Bytes, connections, SYN counts | Status codes, latency per route, path metrics |
| **Stickiness** | **Connection** affinity (same TCP → same backend) | **Cookie** or header-based; required for some WS setups |
| **Misconfig symptom** | Wrong backend IP/port | 404 default backend, redirect loops, cert mismatch |

## 5. Common placement mistakes

| Mistake | What goes wrong | Fix |
|---------|-----------------|-----|
| **L4 LB only** for multi-tenant HTTP on one IP | All traffic hits one backend; Host header ignored | Add **L7 Ingress** or SNI-aware TLS router |
| **Terminate TLS at L4** (device cannot) | Garbled HTTP to app expecting TLS | Terminate at **Ingress** or use **passthrough** to TLS-aware backend |
| **Balance Postgres at L7 HTTP proxy** | Protocol mismatch | Use **L4** (or managed DB proxy) for `:5432` |
| **No session affinity** for WebSocket | Connection jumps pods; random disconnects | **Sticky sessions** or shared pub/sub backplane — Part VII |
| **Trust all `X-Forwarded-For`** | Spoofed client IP in logs/auth | Configure **trusted proxy CIDRs** only |
| **Geo DNS without regional backends** | Low RTT to edge, high RTT to single DB | Align **compute + data** per region — Part V |

## 6. HTTP “layers” inside the application tier

Even after traffic reaches your **pod**, useful splits:

| Layer in your service | Responsibility | Load balancing relevance |
|-----------------------|----------------|--------------------------|
| **Edge (Ingress)** | TLS, routing, rate limit | First **L7** routing decision |
| **API gateway** | Auth, versioning, aggregation | Can be same process as Ingress or separate tier |
| **App server** | Business logic, handlers | Assumes correct Host/path already chosen |
| **Sidecar / mesh** | mTLS, retries, circuit break | **L7/L4** between services in cluster |
| **Connection pool** | DB/Redis clients | Not a public LB — internal **L4** to data stores |

**Do not load-balance at every layer.** Usually: **one well-configured L7 edge** + **L4 for stateful TCP data stores** if you run your own DB tier.

## 7. Quick reference — protocol → layer → balance where

| Protocol | Stack layer | Balance at | Notes |
|----------|-------------|------------|-------|
| **HTTP/1.1 REST** | L7 | Ingress / API gateway | Path-based routes |
| **HTTPS** | L6 + L7 | Terminate at Ingress (typical) | Cert must match DNS name |
| **HTTP/2 / gRPC** | L7 | L7 proxy with HTTP/2 enabled | Needs end-to-end H2 or gRPC-aware proxy |
| **WebSocket** | L7 (upgraded HTTP) | L7 + **sticky** + long timeouts | Starts as HTTP `Upgrade` |
| **SSE** | L7 | L7; disable response buffering | One long HTTP response stream |
| **TCP (Postgres)** | L4 | NLB / internal L4 | Not HTTP |
| **UDP (DNS, QUIC)** | L4 | Anycast / UDP-aware LB | HTTP/3 (QUIC) needs UDP-capable edge |
| **TLS passthrough** | L4 (+ SNI) | L4 LB | L7 cannot route until decrypted |

## Next

Continue with [WebSockets, SSE, and gRPC](vii-websockets-sse-grpc-and-realtime.md) — realtime and RPC protocols and how load balancers must treat them differently from short REST calls.
