---
label: "III"
subtitle: "TLS handshake and certificates"
group: "Networking"
order: 3
---
Networking — Part III: TLS handshake and certificates

**TLS** (successor to SSL) provides **confidentiality** (encryption), **integrity** (tamper detection), and usually **server authentication** (and optionally **client authentication**) using **public-key cryptography** and **X.509 certificates**.

## 1. What the handshake achieves

Before application data (e.g. HTTP):

1. **Agree on TLS version and cipher suite** — algorithms for key exchange, encryption, and MAC/AEAD.
2. **Authenticate the server** — client verifies the server’s certificate chain against trusted **CAs** (certificate authorities).
3. **Establish shared secrets** — often via **Diffie–Hellman** (or ECDH) so **forward secrecy** is possible: compromise of the server’s long-term key does not decrypt old sessions if ephemeral keys were used.
4. **Derive session keys** — symmetric keys used for bulk encryption of the rest of the connection.

## 2. Classic full handshake (conceptual)

Modern TLS 1.2/1.3 differ in detail; a simplified story:

1. **ClientHello** — supported versions, cipher suites, random nonce, key share (TLS 1.3), **SNI** (Server Name Indication: which hostname the client wants — critical for shared IPs).
2. **ServerHello** — chosen parameters, server **certificate chain**, optional **CertificateRequest** (for mutual TLS).
3. **Client** verifies certificates, finishes key exchange, sends **Finished** (proof of handshake transcript).
4. **Server Finished** — both sides now derive **traffic keys** and send **encrypted** application data (HTTP).

**TLS 1.3** reduces round trips (often **1-RTT** for first connection; **0-RTT** resumption exists but has replay trade-offs).

### Sequence diagram (TLS 1.2–style, simplified)

Diagram below: **TCP is already up**; then the **TLS record layer** exchanges handshake messages. Cipher names and optional messages (**ServerKeyExchange**, **client auth**) are omitted for clarity. **TLS 1.3** encrypts most of the server’s first flight and usually completes in fewer round trips—same goals (agree keys, authenticate server, **Finished** proves transcript integrity).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 520" role="img" aria-label="TLS 1.2 simplified handshake sequence after TCP is established">
  <defs>
    <marker id="net-iii-tls-r" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
    <marker id="net-iii-tls-l" markerWidth="7" markerHeight="7" refX="1" refY="3.5" orient="auto"><path d="M7 0 L0 3.5 L7 7 Z" fill="#60a5fa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">TLS handshake (after TCP established)</text>
  <rect x="12" y="28" width="456" height="22" rx="3" fill="rgba(113,113,122,0.15)" stroke="#71717a"/>
  <text x="24" y="43" fill="#a1a1aa" font-size="9">TCP already up — SYN / SYN-ACK / ACK complete</text>
  <text x="72" y="68" fill="#86efac" font-size="10" font-weight="600">Client</text>
  <line x1="96" y1="74" x2="96" y2="500" stroke="#52525b" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="312" y="68" fill="#60a5fa" font-size="10" font-weight="600">Server (TLS stack)</text>
  <line x1="336" y1="74" x2="336" y2="500" stroke="#52525b" stroke-width="2" stroke-dasharray="4 3"/>
  <path d="M96 92 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="86" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ClientHello</text>
  <text x="128" y="98" fill="#a1a1aa" font-size="8">versions, cipher suites, random, SNI, key-share</text>
  <path d="M330 118 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="112" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ServerHello</text>
  <text x="148" y="124" fill="#a1a1aa" font-size="8">chosen version, cipher suite, random</text>
  <path d="M330 144 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="138" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Certificate</text>
  <text x="148" y="150" fill="#a1a1aa" font-size="8">server chain (leaf → intermediates)</text>
  <path d="M330 168 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="168" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ServerHelloDone</text>
  <rect x="108" y="182" width="216" height="58" rx="4" fill="rgba(251,191,36,0.1)" stroke="#fbbf24"/>
  <text x="118" y="198" fill="#fbbf24" font-size="8" font-weight="600">Client verifies</text>
  <text x="118" y="212" fill="#a1a1aa" font-size="8">chain to trusted root · hostname vs SAN</text>
  <text x="118" y="224" fill="#a1a1aa" font-size="8">key agreement (RSA / DH / ECDH) → session keys</text>
  <path d="M96 254 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="250" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ClientKeyExchange</text>
  <path d="M96 274 H330" stroke="#86efac" stroke-width="1.5" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="270" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ChangeCipherSpec</text>
  <path d="M96 294 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="290" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Finished</text>
  <text x="128" y="302" fill="#a1a1aa" font-size="8">HMAC / PRF over handshake transcript</text>
  <path d="M330 322 H102" stroke="#60a5fa" stroke-width="1.5" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="318" fill="#e4e4e7" font-size="9" font-family="ui-monospace">ChangeCipherSpec</text>
  <path d="M330 342 H102" stroke="#60a5fa" stroke-width="2" marker-end="url(#net-iii-tls-l)"/>
  <text x="148" y="338" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Finished</text>
  <rect x="120" y="352" width="192" height="20" rx="3" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="148" y="366" fill="#86efac" font-size="9" font-weight="600">Handshake complete</text>
  <path d="M96 388 H330" stroke="#86efac" stroke-width="2" marker-end="url(#net-iii-tls-r)"/>
  <text x="128" y="384" fill="#e4e4e7" font-size="9" font-family="ui-monospace">Application data</text>
  <text x="128" y="396" fill="#a1a1aa" font-size="8">e.g. HTTP — encrypted with negotiated AEAD</text>
  <rect x="348" y="412" width="120" height="52" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="356" y="428" fill="#71717a" font-size="8">After both Finished</text>
  <text x="356" y="440" fill="#71717a" font-size="8">match, traffic keys</text>
  <text x="356" y="452" fill="#71717a" font-size="8">protect all records</text>
  <text x="12" y="508" fill="#71717a" font-size="10">Alert records signal errors; TLS 1.3 shortens this flight — same authentication and key goals.</text>
</svg></figure>

## 3. Certificates and trust

- A **leaf certificate** binds a **public key** to names (**CN** / **SAN**: DNS names like `api.example.com`).
- The client chains to a **root CA** in its trust store (OS or browser).
- **Validity period**, revocation (**OCSP** / **CRL**), and **pinning** (rare, brittle) affect real-world security.

## 4. TLS termination

**Edge termination:** load balancer or **ingress** decrypts TLS and may forward **plain HTTP** to pods (cluster-internal) or re-encrypt to backends (**mTLS**). Implications:

- Backends see **X-Forwarded-Proto: https** or similar when the edge sets it.
- **End-to-end TLS** to the app requires configuring the proxy to **pass-through** or **re-encrypt** with its own certs.

## 5. Common pitfalls

- **Mixed content** — HTTPS page loading HTTP subresources (blocked or warned).
- **SNI** missing or wrong — virtual hosting on one IP fails or serves the wrong cert.
- **Expired or mis-issued certs** — monitoring and automation (**ACME** / Let’s Encrypt) reduce outages.

Next: **DNS** (how names become addresses before TCP/TLS), then **ingress** and edge routing.
