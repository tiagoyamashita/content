---
label: "I"
subtitle: "Core concepts"
group: "Networking"
order: 1
---
Networking — Part I
Layers, addressing, reliability, and common protocols.

## 1. Goals & layered models
- Split concerns: physical bits → frames → packets → segments → messages.
- OSI 7 layers vs TCP/IP stack — names differ; focus on responsibilities.
- Encapsulation: each layer adds headers; peer layers talk logically.
- Why layers: swap technologies (Wi‑Fi vs Ethernet) without rewriting apps.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 168" role="img" aria-label="TCP IP stack with encapsulation">
  <text x="96" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Layered stack (TCP/IP shape)</text>
  <rect x="110" y="30" width="160" height="22" rx="4" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="118" y="45" fill="#e4e4e7" font-size="10">application (HTTP, DNS, …)</text>
  <rect x="100" y="56" width="180" height="22" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="124" y="71" fill="#e4e4e7" font-size="10">transport (TCP / UDP, ports)</text>
  <rect x="90" y="82" width="200" height="22" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="118" y="97" fill="#e4e4e7" font-size="10">internet (IP, routing, ICMP)</text>
  <rect x="80" y="108" width="220" height="22" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="118" y="123" fill="#e4e4e7" font-size="10">link (Ethernet, Wi‑Fi, MAC)</text>
  <rect x="70" y="134" width="240" height="22" rx="4" fill="rgba(63,63,70,0.9)" stroke="#71717a"/>
  <text x="135" y="149" fill="#a1a1aa" font-size="10">physical (bits on wire / air)</text>
  <text x="12" y="164" fill="#71717a" font-size="9">each layer adds headers → encapsulation; peers interpret same layer only</text>
</svg></figure>


## 2. Link layer essentials
- Frames between neighbors on the same link; MAC addresses (LAN identity).
- Switches learn MAC→port; broadcast domains vs collision domains.
- ARP resolves IP → MAC on local subnet (ties L3 to L2).


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 116" role="img" aria-label="LAN with switch and MAC addressing">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Same LAN — frames & MAC addresses</text>
  <rect x="40" y="40" width="88" height="44" rx="6" fill="rgba(34,197,94,0.1)" stroke="#86efac"/>
  <text x="56" y="60" fill="#e4e4e7" font-size="10">host A</text>
  <text x="48" y="76" fill="#a1a1aa" font-size="9">MAC-A</text>
  <rect x="292" y="40" width="88" height="44" rx="6" fill="rgba(96,165,250,0.1)" stroke="#60a5fa"/>
  <text x="308" y="60" fill="#e4e4e7" font-size="10">host B</text>
  <text x="300" y="76" fill="#a1a1aa" font-size="9">MAC-B</text>
  <rect x="176" y="48" width="68" height="56" rx="4" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="186" y="72" fill="#e4e4e7" font-size="9">switch</text>
  <text x="178" y="88" fill="#71717a" font-size="8">MAC→port</text>
  <path d="M128 62 H174 M246 62 H292" stroke="#a1a1aa" stroke-width="2"/>
  <text x="96" y="106" fill="#71717a" font-size="9">frames hop link‑local; ARP maps IP→MAC before sending</text>
</svg></figure>


## 3. Network layer — IP & routing
- IP delivers packets host-to-host across networks (best-effort, unreliable).
- IPv4 / IPv6 addressing; CIDR prefixes; longest-prefix routing.
- Routers forward by destination prefix; NAT rewrites addresses at boundaries.
- ICMP: errors and diagnostics (e.g. unreachable, ping echo).


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 124" role="img" aria-label="IP packets routed across networks">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">IP — host‑to‑host across subnets</text>
  <rect x="28" y="44" width="72" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="40" y="66" fill="#e4e4e7" font-size="10">host</text>
  <rect x="176" y="40" width="68" height="44" rx="4" fill="rgba(39,39,42,0.95)" stroke="#fbbf24"/>
  <text x="186" y="62" fill="#fbbf24" font-size="10">router</text>
  <text x="184" y="76" fill="#a1a1aa" font-size="8">forward</text>
  <rect x="320" y="44" width="72" height="36" rx="6" fill="rgba(96,165,250,0.12)" stroke="#60a5fa"/>
  <text x="328" y="66" fill="#e4e4e7" font-size="10">host</text>
  <path d="M100 62 H172 M248 62 H318" stroke="#86efac" stroke-width="2" stroke-dasharray="6 4"/>
  <circle cx="118" cy="62" r="5" fill="#86efac"/>
  <circle cx="298" cy="62" r="5" fill="#86efac"/>
  <text x="44" y="102" fill="#71717a" font-size="9">packets carry dest IP; routers pick next hop by longest‑prefix match</text>
  <text x="44" y="116" fill="#71717a" font-size="9">NAT may rewrite addresses at an edge; ICMP carries control/error messages</text>
</svg></figure>


## 4. Transport — TCP & UDP
- TCP: connections, retransmissions, ordering, flow & congestion control.
- UDP: datagrams, minimal overhead — good for latency-sensitive / simple apps.
- Ports multiplex processes on a host (well-known vs ephemeral ports).


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 118" role="img" aria-label="TCP versus UDP and ports on a host">
  <text x="68" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Transport — pick TCP or UDP</text>
  <rect x="24" y="36" width="168" height="72" rx="6" fill="rgba(34,197,94,0.08)" stroke="#86efac"/>
  <text x="72" y="54" fill="#86efac" font-size="10" font-weight="600">TCP</text>
  <text x="36" y="72" fill="#a1a1aa" font-size="9">connection · reliable · ordered</text>
  <text x="36" y="88" fill="#a1a1aa" font-size="9">flow & congestion control</text>
  <rect x="228" y="36" width="168" height="72" rx="6" fill="rgba(96,165,250,0.08)" stroke="#60a5fa"/>
  <text x="286" y="54" fill="#93c5fd" font-size="10" font-weight="600">UDP</text>
  <text x="244" y="72" fill="#a1a1aa" font-size="9">datagrams · minimal state</text>
  <text x="244" y="88" fill="#a1a1aa" font-size="9">good for latency / simplicity</text>
  <rect x="140" y="96" width="140" height="18" rx="3" fill="#27272a" stroke="#52525b"/>
  <text x="148" y="108" fill="#71717a" font-size="9">ports demux sockets on one IP</text>
</svg></figure>


## 5. Application — HTTP & DNS
- HTTP: request/response over TCP/TLS; methods, status codes, headers.
- DNS: name → record (A/AAAA, CNAME, …); hierarchical and cached.
- TLS sits above TCP: handshake, certificates, symmetric encryption for HTTP.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 112" role="img" aria-label="DNS then HTTP over TLS">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Typical web fetch — DNS then HTTP(S)</text>
  <rect x="24" y="36" width="96" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="44" y="58" fill="#e4e4e7" font-size="10">browser</text>
  <path d="M122 54 H168" stroke="#a1a1aa" stroke-width="2"/><text x="126" y="48" fill="#fbbf24" font-size="9">DNS</text>
  <rect x="172" y="36" width="96" height="36" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="188" y="58" fill="#e4e4e7" font-size="10">resolver</text>
  <path d="M270 54 H318" stroke="#a1a1aa" stroke-width="2"/><text x="278" y="48" fill="#86efac" font-size="9">IP</text>
  <rect x="322" y="36" width="96" height="36" rx="6" fill="rgba(96,165,250,0.12)" stroke="#60a5fa"/>
  <text x="336" y="58" fill="#e4e4e7" font-size="10">origin</text>
  <text x="24" y="88" fill="#71717a" font-size="9">① resolve name → address · ② TCP connect (often :443) · ③ TLS handshake · ④ HTTP</text>
  <text x="24" y="104" fill="#71717a" font-size="9">HTTPS = HTTP over TLS; DNS itself often uses UDP (and TCP for large responses).</text>
</svg></figure>


## 6. Security & TLS (overview)
- Threats: eavesdropping, tampering, spoofing — TLS aims at confidentiality & integrity.
- Certificates bind public keys to identities (chain to trusted roots).
- Know TLS vs “HTTPS”: TLS protects arbitrary TCP apps, not only the web.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 118" role="img" aria-label="TLS protects data in transit with certificates">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">TLS — confidentiality & integrity</text>
  <rect x="40" y="44" width="88" height="40" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="58" y="68" fill="#e4e4e7" font-size="10">client</text>
  <rect x="154" y="48" width="112" height="32" rx="16" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="166" y="68" fill="#bbf7d0" font-size="10">encrypted tunnel</text>
  <rect x="292" y="44" width="88" height="40" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="308" y="68" fill="#e4e4e7" font-size="10">server</text>
  <text x="40" y="96" fill="#71717a" font-size="9">cert proves identity (chain to roots); keys negotiate session crypto</text>
  <text x="40" y="110" fill="#71717a" font-size="9">TLS works over any stream (HTTP, SMTP, …), not only browsers.</text>
</svg></figure>



<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 248" role="img" aria-label="TLS handshake message sequence">
  <text x="72" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">TLS handshake (simplified 1.3-style)</text>
  <text x="52" y="44" fill="#86efac" font-size="10" font-weight="600">client</text>
  <text x="332" y="44" fill="#93c5fd" font-size="10" font-weight="600">server</text>
  <line x1="72" y1="52" x2="72" y2="210" stroke="#52525b" stroke-dasharray="4 4"/>
  <line x1="368" y1="52" x2="368" y2="210" stroke="#52525b" stroke-dasharray="4 4"/>
  <defs>
    <marker id="net-tls-h1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
    <marker id="net-tls-h2" markerWidth="8" markerHeight="8" refX="1" refY="4" orient="auto"><path d="M8 0 L0 4 L8 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <path d="M72 72 H352" stroke="#a1a1aa" stroke-width="2" fill="none" marker-end="url(#net-tls-h1)"/>
  <text x="116" y="66" fill="#e4e4e7" font-size="9">ClientHello (suites, key share)</text>
  <path d="M368 100 H88" stroke="#a1a1aa" stroke-width="2" fill="none" marker-end="url(#net-tls-h2)"/>
  <text x="96" y="94" fill="#e4e4e7" font-size="9">ServerHello + certificate chain + verify + Finished</text>
  <path d="M72 132 H352" stroke="#86efac" stroke-width="2" fill="none" marker-end="url(#net-tls-h1)"/>
  <text x="132" y="126" fill="#bbf7d0" font-size="9">Finished (keys derived)</text>
  <path d="M72 176 H352" stroke="#71717a" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#net-tls-h1)"/>
  <path d="M368 188 H72" stroke="#71717a" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#net-tls-h2)"/>
  <text x="118" y="170" fill="#a1a1aa" font-size="9">encrypted records (HTTP, …)</text>
  <text x="118" y="184" fill="#a1a1aa" font-size="9">authenticated encryption · replay protection</text>
  <text x="16" y="232" fill="#71717a" font-size="9">Exact flights differ by TLS version & extensions; goal is agree keys + authenticate server (mutual TLS adds client cert).</text>
</svg></figure>


## 7. Remember & rehearse
- Trace a browser request: DNS → TCP connect → TLS → HTTP GET.
- Compare when you’d pick UDP vs TCP for a new service.
- Sketch home LAN: ISP modem, router/NAT, DNS resolution path.

| Command | Purpose |
|---------|---------|
| `ping` | Test connectivity (uses ICMP) |
| `traceroute` | Show packet route |
| `netstat` | Display active connections |
| `ipconfig` / `ifconfig` | Show network configuration |
| `nslookup` / `dig` | DNS queries |