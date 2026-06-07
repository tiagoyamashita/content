---
label: "V"
subtitle: "Network"
group: "System design"
order: 5
---
Network bottlenecks
**Physics and protocol choices** cap throughput and add latency between services and regions.

## 1. Signals

| Signal | Detection |
|--------|-----------|
| NIC bandwidth maxed | `sar -n DEV`, cloud NIC metrics |
| TCP **retransmits** high | `ss -ti`, `netstat -s` |
| Cross-AZ / cross-region latency | Trace span between services |
| **Ephemeral port exhaustion** | `TIME_WAIT` storm, connect errors |
| TLS handshake CPU | CPU on edge during spike |

## 2. Causes and fixes

| Cause | Fix |
|-------|-----|
| Chatty RPC (many round trips) | Batch APIs; gRPC streaming |
| Large JSON payloads | gzip/Brotli; protobuf |
| New TCP conn per request | **Connection pool**; keep-alive |
| HTTP/1.1 head-of-line blocking | **HTTP/2** multiplex; **HTTP/3** (QUIC) |
| Cross-region RTT | CDN; regional deploy; cache at edge |
| Service mesh sidecar ~1 ms each hop | Mesh on critical paths only; bypass for internals |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 110" role="img" aria-label="Chatty vs batched network calls">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Chatty vs batched</text>
  <text x="12" y="38" fill="#f87171" font-size="9">10 × 1 RTT = 10 × latency</text>
  <path d="M12 50 H40" stroke="#f87171" stroke-width="1"/><path d="M12 58 H40" stroke="#f87171" stroke-width="1"/><path d="M12 66 H40" stroke="#f87171" stroke-width="1"/>
  <text x="12" y="88" fill="#86efac" font-size="9">1 batch call = 1 RTT + server-side join</text>
  <path d="M200 58 H280" stroke="#86efac" stroke-width="2"/>
</svg></figure>

## 3. Latency budget (example)

| Hop | Typical |
|-----|---------|
| Same AZ | 0.1–0.5 ms |
| Cross-AZ | 1–3 ms |
| Cross-region (US↔EU) | 80–120 ms |
| Mobile last mile | 20–200 ms |

Design APIs so **critical path** minimizes cross-region hops.

## 4. Connection management

| Practice | Why |
|----------|-----|
| Pool size tuned to DB/API limits | Avoid exhaustion |
| Idle timeout aligned with LB | No stale sockets |
| HTTP/2 one conn many streams | Fewer handshakes |

## 5. CDN and edge

Offload **static** and **cacheable API** responses — see scalable patterns CDN note.

**Related:** Networking track (TCP, HTTP, TLS), [Application-level](vii-application-level.md) (timeouts, circuit breakers).
