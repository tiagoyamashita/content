---
label: "II"
subtitle: "インストールとツールチェーン"
group: "PlantUML"
order: 2
---
PlantUML — Part II
How to **install** PlantUML, render from the **CLI**, use the **VS Code** extension, and run a **local server** for preview and CI.

## 1. Requirements

| Requirement | Notes |
|-------------|-------|
| **Java (JRE 8+)** | PlantUML is a Java JAR — install a JDK or JRE |
| **Graphviz** (recommended) | `dot` on `PATH` — better layouts for component/deployment/class |
| **Editor or CLI** | VS Code extension, IntelliJ plugin, or `java -jar plantuml.jar` |

### Windows

1. Install **Java** — [Eclipse Temurin](https://adoptium.net/) or Oracle JDK.
2. Install **Graphviz** — [graphviz.org](https://graphviz.org/download/) or `winget install Graphviz.Graphviz`.
3. Confirm: `java -version` and `dot -V`.

### macOS

```bash
brew install openjdk graphviz
```

### Linux (Debian/Ubuntu)

```bash
sudo apt install default-jre graphviz
```

## 2. PlantUML JAR (CLI)

Download the latest **`plantuml.jar`** from [plantuml.com](https://plantuml.com/download) or pin a version in your repo under `tools/plantuml.jar` for reproducible CI.

```bash
java -jar plantuml.jar -tsvg docs/diagrams/order-create.puml
java -jar plantuml.jar -tpng -o out/ docs/diagrams/*.puml
```

| Flag | Meaning |
|------|---------|
| **`-tsvg`** | SVG output (scalable, good for docs) |
| **`-tpng`** | PNG output (slides, wikis) |
| **`-o <dir>`** | Output directory |
| **`-DPLANTUML_LIMIT_SIZE=8192`** | Raise size cap for large diagrams |

Exit code **non-zero** on syntax errors — use that in CI to block broken diagrams.

## 3. VS Code

Install **PlantUML** (jebbs.plantuml) from the marketplace.

| Setting | Suggestion |
|---------|------------|
| **`plantuml.render`** | `PlantUMLServer` or `Local` |
| **`plantuml.server`** | `https://www.plantuml.com/plantuml` (quick start) or your own server |
| **`plantuml.exportOutDir`** | `out/diagrams` — keep generated assets out of hand-edited paths |

**Preview:** open a `.puml` file → `Alt+D` (or command **PlantUML: Preview Current Diagram**).

**Export:** **PlantUML: Export Current Diagram** — commit SVG/PNG only if your doc pipeline does not render on the fly.

> **Security:** public PlantUML servers receive your diagram source. For proprietary designs, use **local JAR** or a **self-hosted** server inside your network.

## 4. Local PlantUML server (optional)

For teams that want browser preview without sending source to the internet:

```bash
java -jar plantuml.jar -picoweb
# default http://localhost:8080
```

Point the VS Code extension **`plantuml.server`** at `http://localhost:8080` for local rendering.

## 5. Project layout (suggested)

```text
docs/
  architecture/
    context.puml
    container.puml
    sequences/
      checkout.puml
      auth.puml
  README.md          ← links to rendered SVG or embeds source
out/
  diagrams/          ← gitignored OR committed for static sites
```

| Choice | When |
|--------|------|
| **Commit `.puml` only** | CI or docs site renders on build |
| **Commit `.puml` + `.svg`** | Readers view on GitHub without a renderer |
| **`!include` partials** | Shared `colors.puml`, `sprites.puml`, `boundary.puml` |

Example include:

```plantuml
@startuml
!include ../_styles/colors.puml
!include ../_components/api.puml
@enduml
```

Paths are relative to the **including file**.

## 6. Troubleshooting

| Symptom | Fix |
|---------|-----|
| **`java` not found** | Install JRE; restart terminal |
| **Empty or ugly layout** | Install Graphviz; verify `dot` on PATH |
| **Diagram too large** | Split with `!include`; or raise `PLANTUML_LIMIT_SIZE` |
| **Unicode / font issues** | Set `-charset UTF-8`; specify `skinparam defaultFontName` |
| **Includes not found** | Check relative path from the file that contains `!include` |

## Next

Continue with [Sequence diagrams](iii-sequence-diagrams.md) — the most common diagram type for API and event flows.
