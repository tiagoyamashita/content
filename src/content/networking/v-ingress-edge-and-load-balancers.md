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

## 7. Study order recap

**TCP/UDP** → **HTTP** → **TLS** → **DNS** (name → address) → **Ingress/LB** (HTTP routing and TLS at the edge). Together they describe how a browser request reaches a pod.
