---
label: "I"
subtitle: "Overview"
group: "SWE101"
order: 0
---
SWE101 — overview
**Software engineering** is building and operating systems that solve problems reliably — not only writing code. This curriculum covers languages, **frameworks**, databases, delivery tooling, and design patterns. Start here for **what kinds of software exist** and **how teams ship them**; then dive into the submenu that matches your stack.

## Map of SWE101

| Area | Examples in this track |
|------|-------------------------|
| **Version control** | [Git](git/i-overview.md) |
| **Languages** | [Java](java/intro/i-basics-and-syntax.md), [Python](python/i-basics-and-syntax.md), [Rust](rust/i-basics-and-toolchain.md), [JavaScript](javascript/i-overview.md) |
| **Frameworks** | [Spring Boot](java/springboot/i-intro-and-project-layout.md), [React](javascript/react/i-overview.md), [Angular](javascript/angular/i-overview.md), [React Native](javascript/react-native/i-overview.md), [Flutter](flutter/i-overview.md), [jQuery](javascript/jquery/i-overview.md), [HTMX](htmx/i-overview.md), [Bootstrap](javascript/bootstrap/i-overview.md) |
| **Web UI & styling** | [HTMX](htmx/i-overview.md), [CSS](css/i-overview.md), [Sass/Less](css/sass/i-overview.md) |
| **Backend & data** | [Postgres](postgres/i-overview.md), [MongoDB](mongodb/i-overview.md), [Redis](redis/i-overview.md), [Kafka](kafka/i-overview.md), [PL/SQL](plsql/i-overview.md) |
| **Infrastructure & delivery** | [CDN](cdn/i-overview.md), [API gateway](api-gateway/i-overview.md) |
| **Design** | [System design](sysdesign/scalable-patterns/i-overview.md), [PlantUML](plantuml/i-overview.md) |

## 1. Types of software

Software is grouped by **who uses it**, **where it runs**, and **how it is sold** — the same engineer skills apply; the constraints differ.

| Type | Runs on | Typical examples | Common frameworks | Key constraints |
|------|---------|------------------|-------------------|-----------------|
| **Web application** | Browser + server | SaaS dashboards, e-commerce, admin tools | [React](javascript/react/i-overview.md), [Angular](javascript/angular/i-overview.md), [Spring Boot](java/springboot/i-intro-and-project-layout.md), [HTMX](htmx/i-overview.md), Django, Next.js | Latency, auth, SEO (public sites), responsive UI |
| **Mobile app** | Phone/tablet (iOS, Android) | Banking, social, field service | [React Native](javascript/react-native/i-overview.md), [Flutter](flutter/i-overview.md), SwiftUI, Jetpack Compose | App store rules, offline, push notifications |
| **Desktop application** | Windows, macOS, Linux | IDEs, creative tools, point-of-sale | Electron, .NET WPF/MAUI, Qt, Tauri | Installers, auto-update, local file access |
| **API / backend service** | Servers, containers | REST/GraphQL microservices, webhooks | [Spring Boot](java/springboot/i-intro-and-project-layout.md), FastAPI, Express, NestJS, ASP.NET Core | Uptime, scaling, versioning, idempotency |
| **Embedded / firmware** | Microcontrollers, devices | Appliances, sensors, automotive ECU | FreeRTOS, Zephyr, Arduino (sketch model) | Memory limits, real-time, safety |
| **CLI / developer tool** | Terminal, CI | `git`, build tools, linters | Click (Python), Cobra (Go), Clap ([Rust](rust/i-basics-and-toolchain.md)) | Scriptability, cross-platform, fast startup |
| **Batch / data pipeline** | Schedulers, Spark, warehouses | ETL, reports, ML training jobs | Apache Spark, Airflow, dbt | Throughput, cost, data correctness |
| **Internal tool** | Company network | Support consoles, ops dashboards | Same as web — often [React](javascript/react/i-overview.md) + [Spring Boot](java/springboot/i-intro-and-project-layout.md) or [HTMX](htmx/i-overview.md) | SSO, audit logs, low polish OK |
| **Platform / infrastructure** | Cloud, k8s | Databases, queues, CDNs | Kubernetes, Terraform, Spring Cloud (see **SRE101**) | Reliability, multi-tenant isolation |

Many products combine types: a **mobile app** talks to a **backend API** backed by **Postgres**, with a **web admin** for operators.

```text
User-facing          →  Web / mobile / desktop  (React, Angular, Flutter, …)
Business logic       →  Services (Spring Boot, FastAPI, Node, …)
Data                 →  SQL, document, cache, queue
Delivery             →  Git, CI/CD, containers, CDN
```

## 2. Deployment & ownership models

| Model | Meaning | You care about |
|-------|---------|----------------|
| **SaaS** | Vendor hosts; customers use via browser/API | Multi-tenancy, upgrades, SLAs |
| **On-premise** | Customer runs your software in their datacenter | Install docs, air-gapped updates |
| **Open source** | Source public; support/commercial optional | Licensing, community, security patches |
| **Licensed shrink-wrap** | Rare today; installed product + license key | Updates, compatibility |
| **In-house** | Built for one organization | Integration with legacy systems |

## 3. Development lifecycle types

A **lifecycle** is how work moves from idea → running software. Teams mix pieces; labels are guides, not religions.

| Lifecycle | Flow | Best when | Tradeoffs |
|-----------|------|-----------|-----------|
| **Waterfall** | Requirements → design → build → test → deploy (sequential phases) | Fixed scope, contracts, regulated docs | Late feedback; hard to pivot |
| **Agile (umbrella)** | Short iterations, working software, change welcome | Most product software | Needs discipline; can become chaos without rituals |
| **Scrum** | Fixed-length **sprints**, roles (PO, SM), ceremonies (planning, retro) | Cross-functional team on one product | Ceremony overhead if team is tiny |
| **Kanban** | Continuous flow, WIP limits on a board | Ops, support, steady stream of tasks | Less predictable delivery dates |
| **Iterative / incremental** | Ship thin slices early, expand features | MVPs, learning what users want | Requires deployable increments each cycle |
| **DevOps / CI/CD** | Build, test, deploy **automated** on every change | Any team shipping frequently | Upfront pipeline investment |
| **Shape Up** | 6-week cycles, betting table, cool-down | Product companies (Basecamp-style) | Not sprint-based; fixed appetite |

```text
Waterfall:     Req ──► Design ──► Build ──► Test ──► Release
Agile loop:    Plan → Build → Review → Deploy → repeat (weeks)
DevOps loop:   Commit → CI test → staging → prod (hours/days)
```

## 4. Environments across the lifecycle

| Environment | Purpose |
|-------------|---------|
| **Local** | Developer machine — fast feedback |
| **Dev / shared** | Integrate branches; unstable OK |
| **Staging / pre-prod** | Production-like; QA and demos |
| **Production** | Real users — change control, monitoring |

Code promotion: [Git](git/i-overview.md) branches and tags map to these stages; pipelines (see **SRE101 / CI/CD**) automate the path.

## 5. Roles you will meet (brief)

| Role | Focus |
|------|--------|
| **Software engineer** | Features, bugs, design, tests |
| **Frontend / backend / full-stack** | UI vs server vs both |
| **QA / SDET** | Test plans, automation |
| **DevOps / SRE** | Deploy, monitor, incident response |
| **Product manager** | Priorities, requirements |
| **Designer** | UX, visual design |

Small teams blur roles; large orgs specialize.

## 6. How this track fits the lifecycle

| Phase | SWE101 topics that help |
|-------|-------------------------|
| **Design** | [System design](sysdesign/classic-designs/i-overview.md), [PlantUML](plantuml/i-overview.md) |
| **Implement** | Languages, [Java Spring Boot](java/springboot/i-intro-and-project-layout.md), [React](javascript/react/i-overview.md) |
| **Store data** | [Postgres](postgres/i-overview.md), [MongoDB](mongodb/i-overview.md), [Redis](redis/i-overview.md) |
| **Integrate & ship** | [Git](git/i-overview.md), [API gateway](api-gateway/i-overview.md) |
| **Scale & operate** | [CDN](cdn/i-overview.md), bottleneck analysis in sysdesign |

For cloud delivery and CI/CD depth, see **SRE101**.

## Next

Pick a submenu from the sidebar — [Git essentials](git/essentials/i-overview.md) and a language track are common starting points.
