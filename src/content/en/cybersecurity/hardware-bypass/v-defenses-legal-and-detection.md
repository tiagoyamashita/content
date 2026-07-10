---
label: "V"
subtitle: "Defenses, legal & detection"
group: "Hardware bypass"
order: 5
---
Defenses, legal & detection

Hardware bypass defenses span **product design**, **user habits**, **carrier/platform policy**, and **operations**. Few issues are fixed by a single app patch.

## 1. Defense matrix

| Attack family | Product / OEM | Enterprise | Individual |
|---------------|---------------|------------|------------|
| **Relay (vehicle)** | UWB ranging; sleep motion key | Fleet GPS + immobilizer; secure parking | Faraday pouch; key away from entry |
| **RFID/NFC** | Modern cred + anti-clone | PIN + badge; upgrade readers | Report lost badge immediately |
| **SMS flood** | N/A | Abuse desk with carriers; exec protection | Filter unknown senders |
| **OTP bombing** | WebAuthn; rate limits | SSO everywhere | Use hardware key for email |
| **Jamming** | Wired sensor paths | RF monitoring at critical sites | Wired alarm backup |
| **Smishing** | In-app only comms | User training | Never tap SMS links |

## 2. Distance bounding and UWB

**Distance bounding** cryptographically estimates **time of flight** — relay adds too much latency to fake “near.”

| Tech | Role |
|------|------|
| **UWB (IEEE 802.15.4z)** | Car phone-as-key, precise ranging |
| **BLE channel sounding** | Emerging phone-lock ranging |
| **LF + HF dual band** | Some OEMs require LF wake at car + HF response |

When buying fleet or consumer devices, ask: **Is proximity cryptographically bounded or only “RF received”?**

## 3. Faraday and physical OPSEC

| Item | Limits |
|------|--------|
| **Faraday pouch / box** | Blocks relay to fob inside — must actually seal (test) |
| **Key placement** | Far from windows/doors — reduces relay gain |
| **PIN to drive** | Second factor after relay unlock — OEM dependent |

Faraday does not help if user takes fob out at door while attacker relays.

## 4. Telecom and auth policy

| Policy | Rationale |
|--------|-----------|
| **Ban SMS as sole MFA** for admin, billing, crypto | SIM swap + floods |
| **FIDO2 / passkeys** | Phishing-resistant |
| **Rate-limit OTP** per account + IP + device fingerprint | OTP bombing |
| **Number matching on push MFA** | Stops blind approve |
| **Registered A2P senders only** (business) | Reduces spoof SMS |

Coordinate with **carrier abuse** teams for floods — provide UTC timestamps, sample headers, victim MSISDN.

## 5. Detection and IR playbooks

### Vehicle / physical relay (fleet)

1. Alert: vehicle moving with no driver app unlock event.
2. Correlate: key last seen at home geofence (phone location).
3. Preserve: telematics log, CCTV, insurance timeline.
4. Law enforcement: report VIN; many thefts are export chains.

### SMS / voice flood

1. User reports unusable device — check inbound rate.
2. Open carrier abuse ticket; enterprise may have direct CPaaS contact.
3. Temporarily route critical comms to alternate channel (email, authenticator app).
4. If OTP bombing — lock account pending out-of-band verify.

### Jamming (facilities)

1. Sensor mass offline event — not always jamming (outage).
2. RF survey if repeated; document for regulators if safety-critical.

## 6. Legal and compliance notes

| Activity | Typical status |
|----------|----------------|
| Unauthorized jamming | Illegal (spectrum law) |
| Relay theft | Criminal property crime |
| Bulk SMS harassment | Telecom abuse / stalking laws |
| IMSI catchers | Restricted to authorized agencies in many countries |
| Security research on **owned** devices | Often legal with consent — check local law |

Document **authorized** pen tests (vehicle OEM, facility RFID) with written scope.

## 7. Threat modeling prompt (for new products)

Add to [Threat modeling](../ii-threat-modeling-and-risk.md) sessions:

| Question | If “yes” → |
|----------|------------|
| Does “near” mean RF only? | Model relay |
| Is SMS used for security? | Model flood + SIM swap |
| Does device fail open when RF lost? | Model jamming |
| Is there a legacy radio mode? | Model downgrade |
| Can attacker amplify without breaking crypto? | Physical layer review |

## 8. Further reading (concepts)

| Topic | Search terms |
|-------|--------------|
| Relay attacks | “IEEE RFID relay”, “CCC car relay” |
| UWB secure ranging | FiRa Consortium, 802.15.4z |
| SMS abuse | A2P 10DLC, GSMA SMS firewall |
| GNSS | GPS spoofing detection RAIM |

## Rehearsal questions

- What question do you ask an OEM about “passive entry”?
- Name three controls that do **not** require changing phone OS.
- When should you involve a carrier abuse desk?

**Back:** [Hardware bypass overview](i-overview.md) · [Cybersecurity overview](../i-overview.md).
