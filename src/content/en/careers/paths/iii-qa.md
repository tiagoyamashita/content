---
label: "III"
subtitle: "QA"
group: "Paths"
order: 3
---
QA / test engineering
**QA** protects users from bad releases: risk-based testing, automation, and clear bug reports. Titles vary — QA engineer, SDET, quality engineer.

## Day-to-day

| Activity | Examples |
|----------|----------|
| Plan | Test strategy per feature / release |
| Explore | Edge cases, permissions, i18n (important in Japan) |
| Automate | E2E / API / unit where ROI is clear |
| Gate | CI red builds; release sign-off |
| Partner | Sit with FE/BE; shift-left reviews |

```mermaid
flowchart TD
  Story[User story] --> Risks[Risks]
  Risks --> Manual[Exploratory / cases]
  Risks --> Auto[Automation]
  Manual --> Bug[Bug reports]
  Auto --> CI[CI gate]
  Bug --> Eng[Engineering fix]
  CI --> Release
```

## Skills that matter

| Skill | Level | Notes |
|-------|-------|-------|
| Test design / risk analysis | Core | What to cover vs what to skip |
| Exploratory testing | Core | Find what scripts miss |
| One language + test framework | Core | pytest, JUnit, Playwright, Cypress… |
| API testing | Core | Contracts, auth, edge payloads |
| CI literacy | Core | Gates, flakes, artifacts |
| Clear bug reports | Core | Steps, expected/actual, env |
| Automation architecture | Stretch | Page objects, shared fixtures, parallelization |
| Performance / a11y basics | Stretch | Smoke for CWV, keyboard, screen readers |
| Security smoke checks | Stretch | AuthZ gaps, injection basics |
| Japanese | Market | Useful for domestic UX/copy issues |

## Japan notes

- Domestic firms may still lean **manual QA**; product / gaishikei lean **SDET**.
- Strong automation + English can land foreigner-friendly roles even without N1.
- Gaming and embedded have specialized QA cultures.

## Study path (this repo)

| Priority | Track |
|----------|-------|
| 1 | [SWE101](../../swe101/i-overview.md) — language + Git |
| 2 | [SRE101 CI/CD](../../sre101/i-overview.md) — pipelines |
| 3 | Frontend or backend track matching the product |
| 4 | [Cybersecurity](../../cybersecurity/i-overview.md) — basic threat thinking |

Build: automate login + critical path for an open-source app; show flake handling.

## Compensation (illustrative Tokyo)

Mid QA / SDET roughly **¥5–10M**; senior automation at strong product cos can approach SWE bands. Manual-only tracks usually cap lower.

## Career moves

| From QA | Toward |
|---------|--------|
| Automation depth | SDET / toolsmith |
| Product risk sense | PM |
| Infra + flaky systems | SRE |
| Feature ownership | Backend / FE (needs portfolio) |

## Next

[Frontend](iv-frontend.md) · [Backend](v-backend.md).
