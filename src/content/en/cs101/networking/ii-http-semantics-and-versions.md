---
label: "II"
subtitle: "HTTP semantics and versions"
group: "Networking"
order: 2
---
Networking — Part II: HTTP semantics and versions

HTTP is an **application-layer** protocol: **methods**, **URLs**, **headers**, and **bodies** describe requests and responses. It usually runs over **TCP** (and today often inside **TLS**, i.e. HTTPS).

## 1. Request / response model

- **Client** opens a connection (typically to port **80** for HTTP, **443** for HTTPS) and sends a **request**.
- **Server** returns a **response** with a **status code**, headers, and optional body.

**Common methods**

- **GET** — read a resource; should be safe and idempotent when used correctly.
- **POST** — submit data, create actions; not assumed idempotent.
- **PUT / PATCH** — replace or partially update resources.
- **DELETE** — remove a resource.

## 2. Status codes (families)

- **1xx** — informational (e.g. `100 Continue`).
- **2xx** — success (`200 OK`, `201 Created`, `204 No Content`).
- **3xx** — redirection (`301`, `302`, `304 Not Modified`).
- **4xx** — client error (`400`, `401`, `403`, `404`).
- **5xx** — server error (`500`, `502`, `503`).

## 3. Headers you see everywhere

- **Host** — which virtual host on the server (required in HTTP/1.1).
- **Content-Type** — MIME type of the body (`application/json`, `text/html`, …).
- **Content-Length** / **Transfer-Encoding** — how the body is framed.
- **Connection** — keep-alive behavior (HTTP/1.1 defaults differ from HTTP/1.0).

## 4. HTTP/1.1 vs HTTP/2 vs HTTP/3 (high level)

| Version | Transport | Multiplexing | Typical note |
|---------|-----------|--------------|--------------|
| HTTP/1.1 | TCP | One request per connection unless pipelining (rare); often many parallel TCP connections | Head-of-line blocking at connection level |
| HTTP/2 | TCP | Many streams multiplexed on one TCP connection | Header compression (HPACK); server push (rare in practice) |
| HTTP/3 | QUIC (UDP-based) | Multiplexed with improved loss recovery vs TCP+H2 | Growing CDN and browser support |

## 5. HTTPS is not “a different HTTP”

**HTTPS** means HTTP over **TLS**. The **TLS handshake** (next note) runs first; then HTTP messages are encrypted on the wire.

## 6. Relation to ingress and proxies

**Reverse proxies** and **ingress controllers** terminate HTTP(S), route by **Host** and path, and forward to backends. Understanding **Host**, **X-Forwarded-For**, and **TLS termination** at the edge is essential for correct logging and security headers.

For **where** to place L4 vs L7 balancers, see [L4/L7 layers and where to balance](vi-l4-l7-layers-and-where-to-balance.md). For **WebSockets, SSE, and gRPC**, see [WebSockets, SSE, and gRPC](vii-websockets-sse-grpc-and-realtime.md).

Next: **TLS handshake** and certificates.
