---
label: "V"
subtitle: "Interactive architecture canvas"
group: "System Design"
order: 98
---
System Design — Interactive architecture canvas

Drag **nodes** (app server, Redis, Kibana, load balancer, …), connect them, export SVG. The tool is a **standalone HTML page** — notes apps render **Markdown**, not a full `<html>` document with embedded scripts, so the canvas lives in a sibling file you open in a **browser beside** this note.

## Open the canvas next to your notes

1. In the file tree, open **`system-design-canvas.html`** (same folder as this note).
2. **Right‑click** the file → **Reveal in File Explorer** (or **Copy Path**), then **double‑click** the `.html` file so it opens in Chrome / Edge / Firefox.
3. Put the browser window **next to** Cursor (or on a second monitor) so you can read the written notes while sketching.

**Relative link** (works when browsing the repo on GitHub: open the file, then use **Raw** or download and open locally):

[System design canvas → `system-design-canvas.html`](system-design-canvas.html)

If your viewer blocks local links, paste the full path to `system-design-canvas.html` into the browser address bar, or use **Simple Browser** / **Live Preview** in the editor pointed at that file.

## What's in the canvas

- Palette of common **system design** building blocks (e.g. app tier, cache, broker, observability).
- **Connections** between nodes, **clear**, **auto layout**, **export SVG**.
