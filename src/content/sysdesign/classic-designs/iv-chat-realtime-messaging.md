---
label: "IV"
subtitle: "Chat & realtime messaging"
group: "System design"
order: 4
---
Chat and real-time messaging
Deliver messages to online recipients **instantly** with ordering, persistence, and **presence**.

## 1. Transport comparison

| Method | Latency | Server load | Fit |
|--------|---------|-------------|-----|
| Short polling | High (N × interval) | Wasteful | Legacy |
| Long polling | Better | Connection held | Fallback |
| **WebSocket** | Low | Persistent conn | **Chat default** |
| SSE | Server → client only | Simpler | Notifications, not full chat |

## 2. High-level architecture

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 120" role="img" aria-label="Chat architecture WebSocket broker storage presence">
  <rect x="12" y="44" width="56" height="32" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="24" y="64" fill="#e4e4e7" font-size="9">Client</text>
  <path d="M68 60 H108" stroke="#86efac" stroke-width="2"/>
  <rect x="108" y="44" width="72" height="32" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="64" fill="#e4e4e7" font-size="9">Chat WS</text>
  <path d="M180 60 H220" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="220" y="44" width="64" height="32" rx="3" fill="rgba(59,130,246,0.12)" stroke="#60a5fa"/>
  <text x="228" y="64" fill="#e4e4e7" font-size="9">Kafka</text>
  <path d="M284 60 H324" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="324" y="44" width="72" height="32" rx="3" fill="rgba(168,85,247,0.12)" stroke="#a855f7"/>
  <text x="332" y="64" fill="#e4e4e7" font-size="9">Cassandra</text>
  <rect x="108" y="88" width="72" height="24" rx="2" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="118" y="104" fill="#e4e4e7" font-size="8">Presence Redis</text>
  <text x="12" y="24" fill="#d4d4d8" font-size="11" font-weight="600">Message flow</text>
</svg></figure>

| Service | Role |
|---------|------|
| **Chat / connection** | WebSocket terminate; route to recipient’s server |
| **Message broker** | Durability; fan-out to multiple chat nodes |
| **Message store** | Historical messages |
| **Presence** | Online / last seen |
| **Push notifications** | APNS/FCM when recipient offline |

## 3. Message storage

**Cassandra** (wide-column) — partition key design:

| Partition key | Clustering | Query |
|---------------|------------|-------|
| `conversation_id` | `message_id DESC` | Latest N messages in thread |

**Snowflake ID:** timestamp + machine id + sequence → **sortable** without central DB sequence.

| Property | Benefit |
|----------|---------|
| Time-ordered | Range scans by id |
| Unique cluster-wide | No coordination per insert |

## 4. Presence

| Event | Action |
|-------|--------|
| Connect | SET `presence:{user_id}` TTL 30s |
| Heartbeat every 5s | EXPIRE renew |
| Disconnect / timeout | Key expires → offline |

Store in **Redis**; subscribers notify friends via pub/sub or broker.

## 5. Delivery guarantees

- **At-least-once** over broker — client **dedupes** by `message_id`.
- Offline user: persist + **push notification** on next sync.
- Multi-device: fan-out to all active sessions for `user_id`.

## 6. Scale notes

- **Sticky sessions** or **user → server** routing table for WebSocket affinity.
- Shard conversations by `conversation_id`.
- Media: object store + CDN; message holds URL only.

**Related:** Networking Part I (WebSocket/TCP), scalable patterns messaging.
