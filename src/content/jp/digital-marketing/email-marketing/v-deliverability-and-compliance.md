---
label: "V"
subtitle: "Deliverability & compliance"
group: "Digital marketing"
order: 5
---
Deliverability & compliance
**Deliverability** is whether inbox providers accept your mail. **Compliance** is legal permission to send. Both fail silently until bounce rates and spam complaints spike.

Not legal advice — confirm requirements with counsel for your markets.

## 1. DNS authentication trio

| Record | Purpose |
|--------|---------|
| **SPF** | Which servers may send as your domain |
| **DKIM** | Cryptographic signature per message |
| **DMARC** | Policy when SPF/DKIM fail + reporting |

ESP setup wizards (Resend, Brevo, SendGrid) give exact DNS records. Propagation can take 24–48 hours.

See also [Startups — don't self-host email day one](../../startups/i-overview.md).

## 2. Sender reputation signals

| Positive | Negative |
|----------|----------|
| Consistent volume | Sudden list imports |
| Low bounce/complaint | Purchased lists |
| Engaged readers | Spammy words, bad HTML |
| Authenticated domain | Shared IP with spammers (cheap ESPs) |

**Dedicated sending domain** for marketing (e.g. `mail.yourdomain.com`) protects main domain if issues occur.

## 3. Content and technical spam triggers

| Avoid | Prefer |
|-------|--------|
| ALL CAPS subject | Normal casing |
| Shortened URL only | Full branded links |
| Image-only emails | Text + images balanced |
| Broken HTML | Test in Litmus or send to Gmail/Outlook |

## 4. CAN-SPAM (US) — awareness

| Requirement | Practice |
|-------------|----------|
| Don't deceive | Honest subject and from-name |
| Identify as ad if promotional | Clear when selling |
| Physical address | Footer in marketing emails |
| Unsubscribe | Honor within 10 business days |

## 5. GDPR / UK GDPR — awareness

| Theme | Practice |
|-------|----------|
| **Lawful basis** | Consent or legitimate interest (document which) |
| **Clear opt-in** | No pre-ticked boxes for marketing |
| **Data access / delete** | Process in privacy policy |
| **Record keeping** | When/how they subscribed |

Double opt-in helps prove consent.

## 6. Monitoring

| Check | Tool |
|-------|------|
| DNS records valid | MXToolbox, ESP verifier |
| Inbox placement | Mail-tester.com before big sends |
| Bounce/complaint rates | ESP dashboard |

Pause campaigns if complaint rate jumps.

## 7. Rehearsal questions

- What do SPF, DKIM, and DMARC do?
- Why use a dedicated subdomain for marketing sends?
- Name one CAN-SPAM requirement.

**Next:** [Paid advertising — Overview](../paid-advertising/i-overview.md).
