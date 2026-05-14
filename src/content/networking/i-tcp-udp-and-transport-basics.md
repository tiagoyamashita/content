---
label: "I"
subtitle: "TCP, UDP, and transport basics"
group: "Networking"
order: 1
---
Networking — Part I: TCP, UDP, and transport basics

How applications send bytes across a network: addressing, ports, and the two dominant transport protocols.

## 1. Addresses and ports

- **IP address** (IPv4 or IPv6) identifies a **host** on a network.
- **Port** (0–65535) identifies an **application or service** on that host. Together **IP:port** is a socket endpoint clients use to reach a server.

Without ports, the OS could not demultiplex which process should receive incoming traffic.

## 2. UDP — User Datagram Protocol

**Characteristics**

- **Connectionless:** no setup handshake; you send datagrams when ready.
- **Unreordered / best-effort:** no built-in retransmission or ordering guarantees (applications can add their own).
- **Small header, low latency:** good for DNS queries, VoIP, gaming, metrics where occasional loss is acceptable.

**When to choose UDP**

- You need **low latency** and can tolerate loss, or you implement your own reliability (e.g. QUIC builds on UDP).

## 3. TCP — Transmission Control Protocol

**Characteristics**

- **Connection-oriented:** a **three-way handshake** establishes state before application data (in the classic model).
- **Reliable, ordered byte stream:** retransmissions, sequencing, flow control, congestion control.
- **Full duplex:** both sides can send after the connection is up.

**Rough three-way handshake (simplified)**

1. Client sends **SYN** (synchronize sequence numbers).
2. Server replies **SYN-ACK**.
3. Client sends **ACK** — connection considered established for data transfer (details vary by stack and TCP options).

**When to choose TCP**

- **HTTP/1.1 and HTTP/2** historically sat on TCP; you want the stack to handle loss and ordering for a byte stream.

## 4. Sockets (conceptual)

A **socket** is the API boundary your program uses: bind/listen/accept on servers, connect/send/recv on clients. The kernel ties sockets to **protocol** (TCP or UDP), **local** and **remote** IP/port pairs, and buffers.

## 5. Mental model for what follows

| Layer (conceptual) | Examples |
|--------------------|----------|
| Transport | TCP, UDP, ports |
| Application | HTTP, TLS, DNS message format |
| Security on the wire | TLS (often “on top of” TCP) |
| Naming | DNS maps names → addresses |
| Edge / cluster | Ingress, load balancers, reverse proxies |

Next: **HTTP** (application semantics), then **TLS** (encryption and identity on the wire).
