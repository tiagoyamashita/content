---
label: "I"
subtitle: "Overview"
group: "Hardware bypass"
order: 1
---
Hardware bypass — overview

**Hardware bypass** is when attackers abuse **how a physical system is built to work** — radios, phones, key fobs, payment terminals — instead of breaking crypto in software. The device or protocol does its job; the attacker **extends, replays, floods, or deceives** the channel.

This track is **defensive**: understand the physics and design flaws so you can threat-model products, homes, fleets, and telecom exposure. It is not a how-to for crime.

## What “technology against itself” means

| Pattern | Idea | Example |
|---------|------|---------|
| **Relay** | Legitimate signal path stretched in space/time | Unlock car in driveway while key is inside house |
| **Replay** | Record valid exchange, play it back later | Clone weak RFID badge |
| **Flood** | Overwhelm a channel the victim must use | Millions of SMS to one number |
| **Jam + downgrade** | Block strong link; force weak fallback | Jam LTE; push 2G-only mode |
| **Spoof** | Impersonate a trusted RF or ID source | Fake cell tower (IMSI catcher — law enforcement / illegal abuse) |

Software security (TLS, passwords) does not help if the **trust decision happens on an unauthenticated radio link** with no proof of distance.

## Map of this submenu

| Note | Focus |
|------|--------|
| [Relay & RF amplification](ii-relay-and-rf-amplification.md) | Keyless entry, NFC, RFID, Bluetooth LE relays |
| [Telecom floods & messaging abuse](iii-telecom-floods-and-messaging-abuse.md) | SMS/voice floods, SIM farms, why phones are still targeted |
| [Jamming, spoofing & downgrade](iv-jamming-spoofing-and-downgrade.md) | GPS/Wi‑Fi/cellular jamming, forced weak modes |
| [Defenses, legal & detection](v-defenses-legal-and-detection.md) | UWB, Faraday, rate limits, fleet policy, law |

**Related:** [Application & network security](../iv-application-and-network-security.md), [Threat modeling](../ii-threat-modeling-and-risk.md), [Networking — transport basics](../../cs101/networking/i-tcp-udp-and-transport-basics.md).

## Mental model

```text
Legitimate design:  "If the key is near the car, unlock."
Attacker twist:     "Near" = radio proximity, not human proximity
                    → relay makes "near" true at two places at once

Legitimate design:  "SMS delivers OTP to user's phone."
Attacker twist:     SMS has no sender authentication at the user edge
                    → flood or social layer bypasses the control
```

## Who this affects

| Role | Why care |
|------|----------|
| **Consumer** | Keyless theft, SIM swap adjacent risks, smishing floods |
| **Product / IoT engineer** | Design choice: passive entry, NFC pairing, OTA keys |
| **Fleet / facilities** | Vehicle relay, gate RFID, warehouse scanners |
| **App / platform** | SMS OTP as sole factor; push notification abuse |
| **SOC / IR** | Anomaly patterns: mass inbound SMS, GPS loss events |

## Attack vs defense stack

```text
Physical layer (RF, SMS, GPS)
  → often NO end-to-end crypto between "thing" and "user token"
Protocol layer (rolling codes, UWB ranging)
  → where modern fixes land
Policy layer (no SMS OTP, rate limits, user education)
  → where most orgs actually win
```

## Ethical and legal boundary

| OK in learning / work | Not OK |
|-----------------------|--------|
| Threat-model relay on **your** test vehicle with owner consent | Relay-stealing stranger's car |
| Lab jammer in **shielded** RF chamber | Jamming airport or emergency bands |
| Read carrier abuse reports, build **inbound** flood detection | Operating SIM farms to harass |

Laws vary by country (telecom abuse, RF transmission, computer fraud). Treat unauthorized RF transmission and messaging floods as **criminal** in most jurisdictions.

## Study order

[Relay & RF amplification](ii-relay-and-rf-amplification.md) → [Telecom floods](iii-telecom-floods-and-messaging-abuse.md) → [Jamming & downgrade](iv-jamming-spoofing-and-downgrade.md) → [Defenses & legal](v-defenses-legal-and-detection.md).

## Rehearsal questions

- Why does a rolling code in a key fob not stop a **live** relay attack?
- Name two attacks that target **availability** of a phone number, not confidentiality.
- What is distance bounding and which wireless tech uses it?

**Next:** [Relay & RF amplification](ii-relay-and-rf-amplification.md).
