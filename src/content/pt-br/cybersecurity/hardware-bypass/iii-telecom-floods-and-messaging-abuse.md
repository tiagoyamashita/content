---
label: "III"
subtitle: "Telecom floods & messaging abuse"
group: "Hardware bypass"
order: 3
---
Telecom floods & messaging abuse

Phones are **global identifiers** tied to SMS, voice, and app accounts. Attackers abuse **telecom as a weapon** — not to hack the handset OS, but to **deny service**, **harass**, **bypass weak 2FA**, or **launder fraud** through millions of cheap messages.

## 1. SMS flood (messaging DoS)

```text
Attacker → bulk SMS API / SIM farm / compromised sender
         → millions of messages → one victim number
         → phone unusable, battery drain, notification fatigue
```

| Goal | Effect on victim |
|------|------------------|
| **Harassment** | Psychological; emergency calls harder to place |
| **Distraction** | Hide bank fraud alerts in noise |
| **Extortion** | Pay to stop flood |
| **Competitive sabotage** | Disable executive / support line |

SMS was designed for **delivery**, not **authenticated sender identity** at the handset. Filtering is asymmetric: carriers and aggregators can throttle; end users have limited tools.

## 2. Why SMS is still abused

| Property | Attacker use |
|----------|--------------|
| **Universal** | Every phone accepts SMS by default |
| **No TLS to user** | Phishing links in body |
| **OTP channel** | Intercept via SIM swap (different attack) or trick user in flood chaos |
| **Cheap at scale** | Gray-market routes, open relays, stolen API keys |
| **Weak repudiation** | Sender IDs spoofable in some countries |

**Flash SMS** (class 0 — pop on screen without saving) and **WAP push** variants have been used for **full-screen phishing** without appearing in the inbox history.

## 3. Voice and hybrid floods

| Type | Pattern |
|------|---------|
| **TDoS** | Auto-dial victim; tie up line (911 swatting adjacent — extreme harm) |
| **Robocall storms** | Same as SMS but voice; often paired with caller-ID spoofing |
| **OTP bombing** | Trigger “forgot password” on many sites → flood of legit OTP SMS |

OTP bombing abuses **your own security stack** — each message is “legitimate” from the app’s view.

## 4. SIM farms and bulk messaging infrastructure

```text
[Bulk SMS platform] → [SMPP gateway] → [SIM boxes / IoT SIMs]
                              ↓
                    millions of MSISDNs as senders
```

| Component | Defender relevance |
|-----------|-------------------|
| **SIM box** | Physical device with many SIMs — fraud, arbitrage, spam |
| **SS7 / signaling abuse** | Nation-state / insider — location, intercept (regulated; high impact) |
| **A2P 10DLC / brand registry** | US carrier effort to register business senders — reduces spoof, not all abuse |

You rarely “patch” SS7 as an app developer; you **do not rely on SMS secrecy** for high-value auth.

## 5. Smishing at scale

Hardware bypass meets social engineering:

| Step | Abuse of technology |
|------|---------------------|
| 1 | Million-number blast via short code or rotated sender |
| 2 | “Your package failed” link — few clicks = profit |
| 3 | MFA fatigue — user approves push after SMS noise |

## 6. Who must defend what

| Owner | Controls |
|-------|----------|
| **Carriers / CPaaS** | Rate limits, anomaly detection, sender registration, abuse desk |
| **App platform** | No SMS-only MFA for sensitive ops; WebAuthn, push with number matching |
| **Enterprise** | Protect support numbers; monitor executive SIMs |
| **Individual** | Filter unknown senders (iOS/Android); don’t use SMS OTP for crypto |

## 7. Detection signals

| Metric | Alert |
|--------|-------|
| Inbound SMS rate >> baseline | Active flood |
| Same message body hash from 1000+ senders | Campaign |
| OTP requests spike per user | OTP bombing |
| Support queue + user “can’t use phone” | Possible TDoS/SMS flood |

## 8. Mitigations

| Mitigation | Layer |
|------------|-------|
| **WebAuthn / FIDO2** | App — remove SMS from auth path |
| **Rate limit OTP sends** | App — per user + per IP |
| **Push MFA with context** | App — show map, app name |
| **Carrier abuse ticket** | User — report flood to operator |
| **Filter unknown SMS** | OS setting |
| **Never click SMS links** | User policy for banks, parcels |

Legal: bulk harassment and SWATing are criminal; document for law enforcement with timestamps and sample messages.

## Rehearsal questions

- How is OTP bombing different from a classic SMS flood?
- Why doesn’t fixing your app’s TLS stop smishing?
- Name a stronger replacement for SMS as a second factor.

**Next:** [Jamming, spoofing & downgrade](iv-jamming-spoofing-and-downgrade.md).
