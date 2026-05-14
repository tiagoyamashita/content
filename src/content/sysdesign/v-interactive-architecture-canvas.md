---
label: "V"
subtitle: "Interactive architecture canvas"
group: "System Design"
order: 98
---
System Design — Interactive architecture canvas

Drag **nodes** (app server, Redis, Kibana, load balancer, …), connect them, export SVG. The tool is a **standalone HTML page** — notes apps render **Markdown**, not a full `<html>` document with embedded scripts, so the canvas lives in a sibling file you open in a **browser beside** this note.

## Open the canvas next to your notes

**Why a Markdown link does not work here:** Cursor Notes (and similar GitHub-backed viewers) only treat **`.md` notes** as in-app destinations. A click on something like `system-design-canvas.html` is not opened as a file — the app often **drops you back on the root / menu**. The HTML must be opened **outside** the notes pane (browser or editor preview).

**Path in this repo** (from the workspace root):

```text
src/content/sysdesign/system-design-canvas.html
```

### Option A — File Explorer

1. In Cursor’s **Explorer**, open **`src/content/sysdesign/system-design-canvas.html`**.
2. **Right‑click** the tab or file → **Reveal in File Explorer**.
3. **Double‑click** the `.html` file so your default browser opens it.

### Option B — Terminal from repo root (fastest)

**Windows (PowerShell or cmd):**

```bat
start "" "src\content\sysdesign\system-design-canvas.html"
```

**macOS:**

```bash
open src/content/sysdesign/system-design-canvas.html
```

Run that with the **terminal’s current folder** set to the **`content`** repo root (the folder that contains `src`).

### Option C — Simple Browser / Live Preview

If you use **Simple Browser** or **Live Preview**, paste a **`file:///`** URL to that same path after you copy it from Explorer (**Copy path**), or point the preview at the file from the command palette.

Dock the browser (or second window) **beside** Notes so you can read this page while using the canvas.

## What's in the canvas

- Palette of common **system design** building blocks (e.g. app tier, cache, broker, observability).
- **Connections** between nodes, **clear**, **auto layout**, **export SVG**.
