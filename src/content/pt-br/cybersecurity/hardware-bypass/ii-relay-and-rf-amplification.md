---
label: "II"
subtitle: "Relay & RF amplification"
group: "Hardware bypass"
order: 2
---
Relay & RF amplification

**Relay attacks** (sometimes sold as “signal amplifiers”) defeat systems that equate **radio presence** with **physical presence**. The car, door, or payment terminal thinks the legitimate token is nearby; it is actually far away, with attackers bridging two radio links in real time.

## 1. How a relay works

```text
[Key fob in house]  ←——RF——→  [Attacker device A]
                                      │
                               (internet or wired link)
                                      │
[Car at curb]       ←——RF——→  [Attacker device B]
```

| Step | What happens |
|------|----------------|
| 1 | Car pings for key (LF wake-up or UHF challenge) |
| 2 | Device B receives car’s signal, forwards to A |
| 3 | Key responds; A forwards response to B |
| 4 | Car accepts — crypto verified, **distance not** |

Latency matters: links must be fast enough to complete the protocol before timeouts. Modern attacks use SDRs, dedicated relay boxes, or phone apps — not “magic amplifiers” alone.

## 2. Keyless vehicle entry (passive entry)

| Property | Weak designs | Stronger designs |
|----------|--------------|------------------|
| **Presence check** | “Key responded” only | Ultra-wideband (UWB) distance bounding |
| **User action** | Walk up → auto unlock | Phone-as-key with biometric + ranging |
| **Sleep behavior** | Key always listening | Motion sensor sleep (key sleeps in drawer) |

**Rolling codes** stop **replay** of a captured unlock frame later. They do **not** stop a **live** relay — the real key signs a fresh challenge in real time.

### Typical theft chain (defender view)

1. Scout driveway / parking (target vehicle, key hung near door).
2. Relay at night — unlock + start (if push-start, same proximity trust).
3. Drive away — no broken window, no OBD hack required.

## 3. RFID & NFC

| System | Relay risk | Notes |
|--------|------------|-------|
| **125 kHz prox cards** | High | Low data rate; easy long-range read in some setups |
| **MIFARE Classic** | Historical crypto breaks + cloning | Legacy building access |
| **13.56 MHz NFC (payments)** | Relay possible in theory | Time limits, cryptograms, risk engines; not “tap from miles away” in practice for EMV |
| **Building badges** | Medium | Depends on reader protocol; many lack ranging |

**Amplifier** in marketing often means **relay** or **high-gain antenna** to read a badge from farther than designed — still a **policy failure** (single factor at the door).

## 4. Bluetooth LE

Phones-as-keys (cars, locks, laptops) use BLE. Relay attacks on BLE have been demonstrated in research; mitigations mirror automotive:

- **Ranging** (UWB companion, channel sounding in newer BLE)
- **Require user gesture** on phone (tap, Face ID)
- **Background relay detection** (Apple/Google platform work in progress)

## 5. Signal amplification vs relay

| Term (colloquial) | Usually means |
|-------------------|---------------|
| **Amplifier** | Boost RF so reader reaches farther — or mislabeled relay kit |
| **Relay** | Two coupled radios — real-time protocol bridge |
| **Replay** | Record then play — blocked by rolling codes if implemented |
| **Rolljam** | Jam + capture rolling code, use previous — hybrid RF attack on some remotes |

Defenders should ask vendors: **Which threat model was tested — relay, replay, or jam?**

## 6. Detection and indicators

| Signal | Possible meaning |
|--------|------------------|
| Unlock event while key holder asleep / away (phone GPS elsewhere) | Relay or compromised digital key |
| Multiple failed proximity attempts then success | Relay tuning |
| Fleet vehicles leaving geofence without driver app login | Physical relay theft |

## 7. Mitigations (summary)

| Layer | Action |
|-------|--------|
| **User** | Faraday pouch for fobs; store keys away from doors/windows |
| **OEM** | UWB distance bounding; disable passive entry at night (some apps) |
| **Fleet** | GPS + immobilizer policy; video at lot perimeter |
| **Facilities** | Upgrade to modern credential + PIN; anti-passback |

Detail: [Defenses, legal & detection](v-defenses-legal-and-detection.md).

## Rehearsal questions

- Why is “encrypted key fob” not enough against relay?
- What is the difference between replay and relay in one sentence?
- Name one mitigation that measures distance, not just signal strength.

**Next:** [Telecom floods & messaging abuse](iii-telecom-floods-and-messaging-abuse.md).
