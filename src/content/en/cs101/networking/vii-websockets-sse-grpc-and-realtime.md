---
label: "VII"
subtitle: "WebSockets, SSE, and gRPC"
group: "Networking"
order: 7
---
Networking — Part VII: WebSockets, SSE, and gRPC

Short **HTTP request/response** is not the only application pattern on the web. **WebSockets**, **Server-Sent Events (SSE)**, and **gRPC** use TCP (or QUIC) differently — and **load balancers must know** which protocol you use or connections fail silently.

For **where** to place L4 vs L7 balancers, see [L4/L7 layers and where to balance](vi-l4-l7-layers-and-where-to-balance.md). For HTTP basics, see [HTTP semantics and versions](ii-http-semantics-and-versions.md).

## 1. Protocol landscape (beyond REST)

| Protocol | Direction | Transport | Typical use |
|----------|-----------|-----------|-------------|
| **HTTP/1.1 REST** | Request → response | TCP (often TLS) | CRUD APIs, forms, most web pages |
| **WebSocket** | **Bidirectional** messages | TCP; starts as HTTP **Upgrade** | Chat, live dashboards, collaborative edits, games |
| **SSE** | **Server → client** stream | Long-lived HTTP response | Live feeds, notifications, AI token streaming |
| **Long polling** | Pseudo-push over HTTP | Repeated HTTP requests | Legacy browsers; prefer SSE or WS when possible |
| **gRPC** | Request/response + **streams** | **HTTP/2** (TCP or TLS) | Microservice RPC, strong contracts (Protobuf) |
| **HTTP/3** | Same roles as H1/H2 | **QUIC (UDP)** | Multiplexing without TCP head-of-line blocking |

```text
REST:     client ──GET──► server ──200 JSON──► client   (connection may close)

WebSocket: client ◄──────► server   (one TCP conn, many frames both ways)

SSE:      client ──GET──► server ──chunk chunk chunk──►  (one response, open)

gRPC:     client ──HTTP/2 stream──► server  ( unary or bidi streams )
```

## 2. WebSockets

### Handshake (still HTTP)

WebSocket begins as a normal **HTTP/1.1** request with an **Upgrade** negotiation:

```http
GET /chat HTTP/1.1
Host: app.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

Server agrees:

```http
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

After **101**, the connection is **no longer HTTP** — both sides send **WebSocket frames** (text/binary, ping/pong, close).

### What the load balancer must do

| Requirement | Why |
|-------------|-----|
| **Support HTTP Upgrade** | Without it, proxy returns 400/502 and WS never starts |
| **Long idle timeouts** | Chat may be quiet for minutes; default 60s LB timeout kills the socket |
| **Session affinity (stickiness)** | Later frames on the **same TCP connection** must reach the **same backend** that accepted the Upgrade |
| **Disable response buffering** | Some proxies buffer “slow” responses — breaks streaming frames |
| **TLS termination** | Usually at **L7 Ingress**; WSS = WebSocket over TLS on `:443` |

**Anti-pattern:** round-robin **L4** spread where each **new TCP** goes random backend — fine for **new** WS connections, but **never** mid-connection. Problem appears when proxies **re-handshake** or **retry** incorrectly.

### Scaling WebSockets across pods

One pod cannot hold every user. Patterns:

| Pattern | How it works | Load balancer |
|---------|--------------|---------------|
| **Sticky sessions** | LB pins client to one pod for life of connection | Cookie or source-IP affinity at **L7** |
| **Pub/sub backplane** | Any pod accepts WS; broadcasts via **Redis**, Kafka, NATS | LB can round-robin **new** connections; messages cross pods |
| **Dedicated WS tier** | `wss://realtime.example.com` → WS cluster; REST stays separate | Separate Ingress rules — cleanest ops split |

## 3. Server-Sent Events (SSE)

**SSE** is **one-way**: server pushes `text/event-stream` over a **single long HTTP GET**.

```http
GET /events HTTP/1.1
Accept: text/event-stream
```

Response stays open:

```text
data: {"price": 42.1}

data: {"price": 42.3}
```

| vs WebSocket | SSE |
|--------------|-----|
| Direction | Server → client only | Same |
| Protocol | Plain HTTP (HTTP/2 multiplexing OK) | WS custom framing after Upgrade |
| Browser API | `EventSource` | `WebSocket` |
| Through proxies | Easier (looks like HTTP) | Needs Upgrade support |
| Binary data | Awkward (base64 in text) | Native binary frames |

**Load balancing SSE:** same as long HTTP — **disable buffering**, **long timeouts**, optional **stickiness** if server holds per-client state in memory.

**Modern overlap:** many **LLM streaming APIs** use SSE (`data: {...}\n\n`) because it works through standard HTTPS proxies.

## 4. gRPC

**gRPC** uses **HTTP/2** framing and **Protobuf** payloads. Methods can be:

| Call type | Pattern |
|-----------|---------|
| **Unary** | One request, one response (like REST) |
| **Server streaming** | One request, many responses |
| **Client streaming** | Many requests, one response |
| **Bidirectional streaming** | Both sides stream |

Example path (implementation-dependent):

```text
POST /my.package.UserService/GetUser HTTP/2
content-type: application/grpc
```

### Load balancing gRPC

| Approach | Notes |
|----------|-------|
| **L7 proxy with gRPC / HTTP/2** | Envoy, nginx with grpc module, cloud gRPC-aware LB — routes by **`:authority`** and service name |
| **Client-side load balancing** | gRPC client picks backend from **DNS SRV** or xDS — common in service mesh |
| **TLS** | Often **mTLS** inside cluster; public edge may terminate and re-encrypt |
| **HTTP/1.1-only Ingress** | **Breaks gRPC** — must enable HTTP/2 end-to-end or use grpc-web |

**L4-only LB** works for gRPC if all backends are interchangeable and client reconnects on failure — but you lose **path/method routing** at the edge.

## 5. Other protocols (when you meet them)

| Protocol | Layer | Load balance | One-line note |
|----------|-------|--------------|---------------|
| **MQTT** | L7 (TCP `:1883` / TLS `:8883`) | L4 TCP or MQTT-aware broker cluster | IoT pub/sub; not browser-native |
| **WebRTC** | UDP + STUN/TURN | Media servers, not classic HTTP LB | Video/voice; signaling may use WebSocket |
| **QUIC / HTTP/3** | UDP L4 + L7 | UDP-capable LB (Cloudflare, modern nginx) | Growing; check edge support before adopting |
| **DNS** | UDP/TCP `:53` | Anycast, dedicated DNS | See [DNS and name resolution](iv-dns-and-name-resolution.md) |

## 6. Comparison — what to load balance where

| Traffic type | OSI layer | Balance at | Session affinity | Timeout |
|--------------|-----------|------------|------------------|---------|
| REST `GET/POST` | L7 | Ingress | Usually **no** | Default (60s) OK |
| File upload (large) | L7 | Ingress | No | **Increase** body/read timeout |
| **WebSocket** | L7 | Ingress (WS-aware) | **Yes** (or pub/sub) | **Long** (minutes–hours) |
| **SSE** | L7 | Ingress | If stateful | **Long**; no buffering |
| **gRPC unary** | L7 | gRPC-capable proxy | Optional | Moderate |
| **gRPC bidi stream** | L7 | Same + sticky or mesh | Often **yes** | Long |
| Postgres / Redis | L4 | NLB | Sometimes for TCP | TCP keepalive |
| TLS passthrough | L4 | NLB + SNI | Per connection | TCP |

## 7. End-to-end example — chat app on Kubernetes

```text
Browser  wss://app.example.com/ws
    │
    ▼  DNS → cloud LB IP
    ▼  L7 Ingress (TLS terminate, WS Upgrade enabled, timeout 3600s)
    ▼  Service chat-realtime (sessionAffinity: ClientIP optional)
    ▼  Pod chat-7f3a  ←── Redis pub/sub ──► Pod chat-9b2c
         ▲                                        ▲
         └──────── other WS clients ──────────────┘
```

| Component | Setting |
|-----------|---------|
| **Ingress annotation** | Enable WebSocket, proxy read/send timeout **≥** longest expected idle chat |
| **REST API** | `https://app.example.com/api/...` — same Ingress, different path; **no** stickiness required |
| **Scale-out** | Add Redis (or similar) so new WS connections can land on **any** pod |

## 8. Choosing a protocol (engineering)

| Need | Prefer |
|------|--------|
| Simple CRUD API | **REST + JSON** over HTTPS |
| Server push notifications (one-way) | **SSE** (simpler ops than WS) |
| Chat, games, collaborative UI | **WebSocket** |
| Internal microservices, strong schemas | **gRPC** |
| Public browser client to gRPC backend | **gRPC-Web** + L7 proxy, or REST gateway |
| Lowest latency fan-out at edge | **CDN + SSE/WS** or dedicated realtime vendor |

## Track recap

**TCP/UDP** → **HTTP** → **TLS** → **DNS** → **Ingress/LB** → **L4/L7 placement** → **realtime protocols**. Together they cover how a browser or service connects, names the host, encrypts traffic, reaches the right backend, and stays connected for more than one request.

Related: [Ingress, edge, and load balancers](v-ingress-edge-and-load-balancers.md) · [HTTP semantics and versions](ii-http-semantics-and-versions.md)
