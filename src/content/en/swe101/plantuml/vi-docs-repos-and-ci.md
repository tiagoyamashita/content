---
label: "VI"
subtitle: "Docs, repos & CI"
group: "PlantUML"
order: 6
---
PlantUML — Part VI
How to keep **`.puml` files** in Git, embed them in **Markdown**, split large designs with **`!include`**, and **render or validate** in **CI** so broken diagrams fail the build.

For Git workflow basics, see [Everyday commands](../git/essentials/iii-everyday-commands.md). For CI concepts, see [CI/CD fundamentals](../../sre101/cicd/i-fundamentals.md).

## 1. Store source in the repo

| Approach | Pros | Cons |
|----------|------|------|
| **`.puml` only** | Single source; small repo | GitHub preview needs plugin or CI artifact |
| **`.puml` + committed `.svg`** | Visible in PR diffs and on GitHub | Must regenerate on change |
| **Generated in docs build** | Always fresh on site | Requires build step for readers |

**Recommended:** commit **`.puml`**; commit **`.svg`** if your audience reads raw GitHub without a renderer.

```text
docs/
  diagrams/
    checkout.puml
    checkout.svg    ← optional, generated
```

Add to **`.gitignore`** if you never commit outputs:

```gitignore
docs/diagrams/*.png
docs/diagrams/*.svg
```

## 2. Markdown embedding

GitHub **does not** natively render PlantUML in Markdown (unlike Mermaid). Options:

| Method | How |
|--------|-----|
| **Link to SVG** | `![Checkout flow](diagrams/checkout.svg)` |
| **Link to source** | `[source](diagrams/checkout.puml)` |
| **HTML img tag** | `<img src="diagrams/checkout.svg" alt="Checkout flow">` |
| **Docs site plugin** | MkDocs, Docusaurus, or Antora PlantUML extensions render at build time |

Example in a service README:

```markdown
## Architecture

![Order flow](docs/diagrams/order-sequence.svg)

Source: [order-sequence.puml](docs/diagrams/order-sequence.puml) — regenerate with `make diagrams`.
```

## 3. `!include` and modular design

Split by **bounded context** or **diagram type**:

```text
docs/diagrams/
  _shared/
    colors.puml
    services.puml
  ordering/
    context.puml
    container.puml
    seq-place-order.puml
```

**`services.puml`** (fragments only — no `@startuml`):

```plantuml
!define SVC_API [Order API]
!define SVC_PAY [Payment Service]
```

**`seq-place-order.puml`**:

```plantuml
@startuml
!include ../_shared/colors.puml
!include ../_shared/services.puml
actor User
SVC_API --> SVC_PAY : charge
@enduml
```

| Rule | Detail |
|------|--------|
| **Relative paths** | Resolved from the file containing `!include` |
| **No `@startuml` in includes** | Included files are fragments |
| **Pin stdlib** | Vendor C4-PlantUML instead of live `raw.githubusercontent.com` URLs |

## 4. Makefile / script (local render)

```makefile
PLANTUML = java -jar tools/plantuml.jar
SRC = docs/diagrams
OUT = docs/diagrams

diagrams:
	$(PLANTUML) -tsvg -o $(OUT) $(SRC)/**/*.puml
```

Or a small script in `scripts/render-diagrams.sh` invoked before `mkdocs build` or `npm run docs`.

## 5. CI: validate and publish

### Validate only (fast PR check)

```yaml
# .github/workflows/diagrams.yml (excerpt)
jobs:
  plantuml:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "17"
      - run: sudo apt-get install -y graphviz
      - run: |
          curl -L -o plantuml.jar https://github.com/plantuml/plantuml/releases/download/v1.2024.8/plantuml-1.2024.8.jar
          java -jar plantuml.jar -checkonly docs/diagrams/**/*.puml
```

**`-checkonly`** fails on syntax errors without writing files — good gate for PRs.

### Render and upload

```yaml
      - run: java -jar plantuml.jar -tsvg -o out docs/diagrams
      - uses: actions/upload-artifact@v4
        with:
          name: diagrams
          path: out/
```

Commit bot or docs pipeline can attach artifacts to static sites.

## 6. Review checklist (PRs that touch `.puml`)

| Check | Question |
|-------|----------|
| **Names** | Match services/env vars in code and infra? |
| **Scope** | One scenario per sequence file? |
| **Secrets** | No real hostnames, keys, or internal-only URLs in public repos? |
| **Includes** | New fragments referenced with correct relative paths? |
| **Output** | If SVG is committed, was it regenerated? |
| **Alt paths** | Error and timeout paths shown where relevant? |

## 7. PlantUML vs Mermaid in the same repo

| Use PlantUML | Use Mermaid |
|--------------|-------------|
| UML sequence with `alt`/`opt`/`par` | Simple flowcharts in GitHub README |
| C4 context/container | Native GitHub rendering |
| Large multi-file `!include` trees | Quick inline diagram in a single MD file |

Both can coexist — pick per doc audience and renderer.

## Track complete

You now have overview → toolchain → sequence → component/deployment → class/activity/state → docs/CI. Apply these to your next RFC, service README, or [system design](../sysdesign/classic-designs/ii-url-shortener.md) walkthrough.
