---
label: "VIII"
subtitle: "When to use & tradeoffs"
group: "HTMX"
order: 8
---
HTMX — when to use & tradeoffs
HTMX is a **deliberate architectural choice**: hypermedia on the server, minimal client state. It shines for many web apps and fails for others — choose based on product constraints, not hype.

## 1. Decision matrix

| Factor | Favor HTMX | Favor SPA (React/Vue/Svelte) |
|--------|------------|------------------------------|
| Team strength | Backend-heavy, strong templates | Deep frontend specialists |
| UI complexity | Forms, tables, dashboards | Rich client editors, maps, drag-drop canvases |
| SEO for public pages | Server HTML already indexable | Need SSR/SSG layer anyway |
| Offline / mobile shell | Limited | React Native / Flutter |
| API reuse | HTML + optional JSON | JSON API first, web is one client |
| Time to MVP | Few moving parts | More tooling, state management |

## 2. Compared to full MPAs

| | **Classic MPA** | **HTMX MPA** |
|---|-----------------|--------------|
| Navigation | Full reload | Partial swap, optional **`hx-boost`** |
| UX | Simpler | Smoother, less flicker |
| Complexity | Lowest | + one JS library + partial templates |
| Fallback | N/A | Works without JS if routes return full pages |

HTMX is an **upgrade path** from server-rendered apps, not a rewrite.

## 3. Compared to SPAs

```text
SPA cost:  API design + client router + state store + component library + build pipeline
HTMX cost: Partial templates + HX-Request branching + swap tuning
```

| SPA advantage | HTMX counter |
|---------------|--------------|
| Instant client transitions | **`hx-boost`**, prefetch extensions |
| Shared mobile/web API | You may still want JSON for native apps |
| Component ecosystem | Use Web Components or sprinkles of Alpine/JS |
| Complex client validation | Server-first; add **`htmx:validate`** + small JS |

Many teams use **“HTMX + Alpine.js”** for local UI state (toggle, dropdown) without a full SPA.

## 4. Hybrid architectures

Common production pattern:

```text
Marketing site     →  static / SSR pages
App shell (HTMX)   →  authenticated CRUD, admin
Public API         →  JSON for partners / mobile
Heavy widget       →  embedded React island in one div
```

Do not force one paradigm for the entire product.

## 5. Operational concerns

| Topic | Notes |
|-------|-------|
| **Observability** | Log `HX-Request` like API calls; same backends |
| **Performance** | Small HTML fragments beat large JSON + client render for simple lists |
| **Caching** | Fragment endpoints uncached; static assets on [CDN](../cdn/i-overview.md) |
| **Versioning** | Template changes deploy with server — no separate frontend deploy |
| **Load testing** | More requests than one fat SPA load, but lighter payloads |

## 6. Team workflow

| Practice | Why |
|----------|-----|
| **One template per UI state** | Avoid duplicate HTML in JSON DTOs |
| **Contract tests for partials** | Prevent broken swaps on refactor |
| **Design system in CSS** | Less need for component frameworks |
| **Document swap targets** | `#main`, `#modal-body` — stable IDs |

## 7. When not to use HTMX

- **Collaborative editing** (OT/CRDT) — client owns document model.
- **Media editors**, **CAD**, **games** — canvas/WebGL lifecycle.
- **App store mobile app** — HTMX is web; use native or cross-platform SDK.
- **Strict “API-only backend” policy** — HTMX couples UI to server templates.

## 8. Learning path in SWE101

| Related track | Connection |
|---------------|------------|
| [Java / Spring Boot](../java/springboot/i-intro-and-project-layout.md) | Thymeleaf + `@Controller` partials |
| [Python](../python/i-basics-and-syntax.md) | Flask/FastAPI + Jinja2 |
| [Postgres](../postgres/i-overview.md) | Same data layer as any web stack |
| [CDN](../cdn/v-static-assets-and-spas.md) | Static JS/CSS vs dynamic HTML |
| [API gateway](../api-gateway/i-overview.md) | Route HTML and JSON on same host or split |

## 9. Checklist before adopting

- [ ] Primary users on modern browsers (HTMX 2.x)?
- [ ] Team comfortable maintaining server templates?
- [ ] Product is form/list/dashboard heavy?
- [ ] Auth model works with cookie sessions?
- [ ] Plan for partials testing and stable `hx-target` IDs?
- [ ] Identified any “islands” needing a full client framework?

If most answers are yes, HTMX is a strong default for internal and B2B web apps.

## Further reading

- [htmx.org documentation](https://htmx.org/docs/) — authoritative attribute reference
- [hypermedia.systems](https://hypermedia.systems/) — design philosophy behind HTMX
