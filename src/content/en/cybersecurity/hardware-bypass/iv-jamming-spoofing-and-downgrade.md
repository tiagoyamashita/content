---
label: "IV"
subtitle: "Jamming, spoofing & downgrade"
group: "Hardware bypass"
order: 4
---
Jamming, spoofing & downgrade

Some attacks **block** the real signal or **pretend** to be infrastructure so the victim device connects to an attacker-controlled weak path. The technology still “works” — on the attacker’s terms.

## 1. Jamming (denial of RF)

| Target | Effect |
|--------|--------|
| **GPS L1** | Navigation fails; drones/vehicles drift to dead reckoning |
| **Cellular** | No LTE → phone may hunt older RATs |
| **Wi‑Fi 2.4/5 GHz** | Cameras, locks, sensors offline |
| **Garage / alarm RF** | Remote disable of wireless sensors (paired with physical entry) |

Jamming is **broadcast noise** — illegal to operate on licensed bands in most countries without authorization. Defenders care about **resilience when signal is lost**, not building jammers.

```text
Normal:  Device ←——strong signal——→ tower / satellite
Jammed:  Device hears noise floor → link down → fallback behavior?
```

## 2. Downgrade attacks

Force a device from a **strong mode** to a **weak legacy mode**:

| Scenario | Downgrade |
|----------|-----------|
| **Cellular** | Jam 4G/5G → 2G GSM (weak or no encryption on air interface in legacy) |
| **Wi‑Fi** | Deauth flood → client reconnects; evil twin on open SSID |
| **Bluetooth** | Pairing mode confusion → legacy pairing without MITM protection |
| **Payment terminal** | Rare — force mag stripe if chip fails (regions vary) |

Downgrade is **technology against itself**: the stack is designed to **keep working** when conditions are poor.

## 3. Spoofing

| Type | What is faked |
|------|----------------|
| **GPS spoofing** | Fake satellite signals — receiver reports wrong location/time |
| **Caller ID** | Display name/number on PSTN/VoIP |
| **SMS sender ID** | Alphanumeric sender in markets that allow it |
| **Wi‑Fi evil twin** | Same SSID as café — captive portal harvest |
| **Cell IMSI catcher** | Fake tower — device camps; metadata capture (highly regulated) |

Spoofing breaks **identity at the channel**, before app-layer crypto starts.

## 4. Combined tactics

```text
Jam GPS  →  fleet loses tracking
Jam LTE  →  alarm panel uses cellular backup path
Relay fob  →  while camera offline
```

Physical crimes increasingly **stack** RF layers. Threat models that only list “network intrusion” miss the **RF prelude**.

## 5. IoT and physical security products

| Product | Weak fallback |
|---------|----------------|
| **Wireless alarm** | Jam sensor → no alert; or jam panel uplink |
| **Smart lock** | BLE jam → app can’t reach lock; keypad still works? |
| **Fleet tracker** | GPS jam → last known position stale |
| **Drone** | GNSS jam → RTH may fail |

Ask vendors: **What happens when RF is lost for 60 seconds?** Fail open vs fail closed matters for life safety.

## 6. Detection

| Signal | Possible RF attack |
|--------|-------------------|
| GPS fix lost + cellular still up | Local GPS jammer |
| All sensors drop at once | Wideband jamming |
| Rogue AP same BSSID stronger RSSI | Evil twin |
| 2G-only camp in 5G-only area | Forced downgrade (investigate) |

RF spectrum monitoring is **specialist** — airports, prisons, critical sites; consumers rely on **behavioral** cues.

## 7. Mitigations (high level)

| Mitigation | Applies to |
|------------|------------|
| **Wired backup** | Alarms, critical sensors |
| **GNSS anti-spoof (dual freq, RAIM)** | Aviation, high-end fleet |
| **Disable 2G on devices** | Corporate phone policy |
| **WPA3-Enterprise / cert pinning** | Corporate Wi‑Fi |
| **Don’t rely on GPS alone for auth** | Apps — geo-IP is weak too |
| **Local alarm sirens** | Jam uplink ≠ silent premises |

## Rehearsal questions

- What is the difference between jamming and spoofing?
- Why does “always connected” IoT increase jamming risk?
- Name one downgrade from 4G to an older technology.

**Next:** [Defenses, legal & detection](v-defenses-legal-and-detection.md).
