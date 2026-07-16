#!/usr/bin/env python3
"""Inject top-folder percentage breakdown into graphify-out/graph.html.

Reads node `source_file` paths from the HTML (or graph.json), groups by the
first curriculum track folder (ai101, swe101, …), and adds a sidebar panel:

  Top folders
  SWE101  ████████░░  34.2%

Usage:
  python scripts/patch-graphify-folder-stats.py
  python scripts/patch-graphify-folder-stats.py --html graphify-out/graph.html
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_HTML = REPO_ROOT / "graphify-out" / "graph.html"
DEFAULT_GRAPH = REPO_ROOT / "graphify-out" / "graph.json"

KNOWN_TRACKS = {
    "ai101",
    "swe101",
    "sre101",
    "cs101",
    "cybersecurity",
    "digital-marketing",
    "cryptocurrency101",
    "startups",
    "food",
    "languages",
    "getting-started",
}

TRACK_TITLES = {
    "ai101": "AI101",
    "swe101": "SWE101",
    "sre101": "SRE101",
    "cs101": "CS101",
    "cybersecurity": "Cybersecurity",
    "digital-marketing": "Digital marketing",
    "cryptocurrency101": "Cryptocurrency101",
    "startups": "Startups",
    "food": "Food",
    "languages": "Languages",
    "getting-started": "Getting started",
    ".obsidian": "Obsidian config",
    "misc": "Other",
}

PALETTE = [
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
    "#BAB0AC",
    "#86BCB6",
    "#F1A340",
]


def track_of(source_file: str) -> str:
    parts = [p for p in source_file.replace("\\", "/").split("/") if p and p not in (".", "..")]
    for i, p in enumerate(parts):
        pl = p.lower()
        if pl in KNOWN_TRACKS:
            return pl
        if pl in ("en", "jp") and i + 1 < len(parts):
            nxt = parts[i + 1].lower()
            if nxt in KNOWN_TRACKS:
                return nxt
        if pl == ".obsidian":
            return ".obsidian"
    for p in parts:
        if p.lower() not in ("src", "content") and not p.startswith("."):
            return p.lower()
    return "misc"


def title_of(track: str) -> str:
    return TRACK_TITLES.get(track, track.replace("-", " ").title())


def load_source_files(html: str, graph_path: Path) -> list[str]:
    if graph_path.is_file():
        data = json.loads(graph_path.read_text(encoding="utf-8"))
        files = []
        for n in data.get("nodes", []):
            sf = n.get("source_file")
            if sf:
                files.append(sf)
        if files:
            return files

    m = re.search(r"const RAW_NODES = (\[.*?\]);\s*\nconst RAW_EDGES", html, re.S)
    if not m:
        raise SystemExit("error: could not find RAW_NODES in HTML and no graph.json")
    nodes = json.loads(m.group(1))
    return [n["source_file"] for n in nodes if n.get("source_file")]


def folder_stats(source_files: list[str]) -> list[dict]:
    counts = Counter(track_of(sf) for sf in source_files)
    total = sum(counts.values()) or 1
    rows = []
    for i, (track, count) in enumerate(counts.most_common()):
        rows.append(
            {
                "id": track,
                "label": title_of(track),
                "count": count,
                "percent": round(100.0 * count / total, 1),
                "color": PALETTE[i % len(PALETTE)],
            }
        )
    return rows


def build_panel_html(rows: list[dict], total: int) -> str:
    items = []
    for r in rows:
        pct = r["percent"]
        items.append(
            f"""    <div class="folder-row" data-track="{r['id']}" role="button" tabindex="0"
         title="Show {r['label']} nodes and linked pages">
      <div class="folder-head">
        <span class="folder-dot" style="background:{r['color']}"></span>
        <span class="folder-label">{r['label']}</span>
        <span class="folder-pct">{pct}%</span>
      </div>
      <div class="folder-bar"><div class="folder-fill" style="width:{pct}%;background:{r['color']}"></div></div>
    </div>"""
        )
    body = "\n".join(items)
    return f"""  <div id="folder-stats-wrap">
    <h3>Top folders</h3>
    <div class="folder-meta">{total} nodes by curriculum track · click a folder to focus it + linked pages</div>
    <button type="button" id="folder-show-all" class="folder-show-all">Show all</button>
    <div id="folder-stats">
{body}
    </div>
  </div>
"""


CSS = """
  #folder-stats-wrap { padding: 12px 14px; border-bottom: 1px solid #2a2a4e; max-height: 42vh; overflow-y: auto; }
  #folder-stats-wrap h3 { font-size: 13px; color: #aaa; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
  .folder-meta { font-size: 11px; color: #666; margin-bottom: 8px; line-height: 1.35; }
  .folder-show-all {
    display: none; width: 100%; margin-bottom: 10px; padding: 6px 8px;
    background: #0f0f1a; border: 1px solid #3a3a5e; color: #ccc;
    border-radius: 6px; cursor: pointer; font-size: 12px;
  }
  .folder-show-all:hover { border-color: #4E79A7; color: #fff; }
  .folder-show-all.visible { display: block; }
  .folder-row { margin-bottom: 8px; cursor: pointer; padding: 4px 4px 6px; border-radius: 6px; }
  .folder-row:hover { background: #2a2a4e; }
  .folder-row.active { background: #243044; outline: 1px solid #3a5a7a; }
  .folder-row.dimmed { opacity: 0.4; }
  .folder-head { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 3px; }
  .folder-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .folder-label { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .folder-pct { color: #9aa; font-variant-numeric: tabular-nums; font-size: 11px; }
  .folder-bar { height: 6px; background: #0f0f1a; border-radius: 3px; overflow: hidden; }
  .folder-fill { height: 100%; border-radius: 3px; opacity: 0.85; }
"""

FOLDER_FILTER_JS = r"""
<script id="folder-filter-js">
(function () {
  const KNOWN = new Set([
    "ai101","swe101","sre101","cs101","cybersecurity","digital-marketing",
    "cryptocurrency101","startups","food","languages","getting-started"
  ]);
  const TITLES = {
    "ai101":"AI101","swe101":"SWE101","sre101":"SRE101","cs101":"CS101",
    "cybersecurity":"Cybersecurity","digital-marketing":"Digital marketing",
    "cryptocurrency101":"Cryptocurrency101","startups":"Startups","food":"Food",
    "languages":"Languages","getting-started":"Getting started",
    ".obsidian":"Obsidian config","misc":"Other"
  };

  function trackOf(sf) {
    if (!sf) return "misc";
    const parts = String(sf).replace(/\\/g, "/").split("/").filter(Boolean);
    for (let i = 0; i < parts.length; i++) {
      const pl = parts[i].toLowerCase();
      if (KNOWN.has(pl)) return pl;
      if ((pl === "en" || pl === "jp") && i + 1 < parts.length) {
        const nxt = parts[i + 1].toLowerCase();
        if (KNOWN.has(nxt)) return nxt;
      }
      if (pl === ".obsidian") return ".obsidian";
    }
    for (const p of parts) {
      const pl = p.toLowerCase();
      if (pl !== "src" && pl !== "content" && !pl.startsWith(".")) return pl;
    }
    return "misc";
  }

  function titleOf(t) { return TITLES[t] || t; }

  // Build adjacency from RAW_EDGES
  const adj = new Map();
  function addEdge(a, b) {
    if (!adj.has(a)) adj.set(a, new Set());
    if (!adj.has(b)) adj.set(b, new Set());
    adj.get(a).add(b);
    adj.get(b).add(a);
  }
  for (const e of RAW_EDGES) addEdge(e.from, e.to);

  let activeTrack = null;
  const showAllBtn = document.getElementById("folder-show-all");
  const rows = [...document.querySelectorAll(".folder-row[data-track]")];

  function setInfo(html) {
    const el = document.getElementById("info-content");
    if (el) el.innerHTML = html;
  }

  function clearFolderFilter() {
    activeTrack = null;
    rows.forEach(r => { r.classList.remove("active", "dimmed"); });
    if (showAllBtn) showAllBtn.classList.remove("visible");
    const updates = RAW_NODES.map(n => ({
      id: n.id,
      hidden: hiddenCommunities.has(n.community),
    }));
    nodesDS.update(updates);
    if (typeof network !== "undefined" && network.fit) {
      network.fit({ animation: true });
    }
    setInfo('<span class="empty">Click a node to inspect it</span>');
  }

  function focusFolder(track) {
    if (activeTrack === track) {
      clearFolderFilter();
      return;
    }
    activeTrack = track;

    const inFolder = new Set();
    for (const n of RAW_NODES) {
      if (trackOf(n.source_file) === track) inFolder.add(n.id);
    }

    // Include 1-hop linked neighbors (pages linked to/from this folder)
    const visible = new Set(inFolder);
    for (const id of inFolder) {
      const neighbors = adj.get(id);
      if (!neighbors) continue;
      for (const nb of neighbors) visible.add(nb);
    }

    const linkedOnly = [...visible].filter(id => !inFolder.has(id)).length;

    rows.forEach(r => {
      const t = r.getAttribute("data-track");
      r.classList.toggle("active", t === track);
      r.classList.toggle("dimmed", t !== track);
    });
    if (showAllBtn) showAllBtn.classList.add("visible");

    const updates = RAW_NODES.map(n => ({
      id: n.id,
      // Respect community toggles too
      hidden: !visible.has(n.id) || hiddenCommunities.has(n.community),
    }));
    nodesDS.update(updates);

    const fitIds = [...visible].filter(id => {
      const n = nodesDS.get(id);
      return n && !n.hidden;
    });
    if (fitIds.length && typeof network !== "undefined") {
      network.fit({ nodes: fitIds, animation: true });
    }

    setInfo(`
      <div class="field"><b>${titleOf(track)}</b></div>
      <div class="field">${inFolder.size} nodes in folder</div>
      <div class="field">${linkedOnly} linked pages outside folder</div>
      <div class="field" style="color:#888;margin-top:6px;font-size:11px">Click the folder again or Show all to reset</div>
    `);
  }

  rows.forEach(row => {
    row.addEventListener("click", () => focusFolder(row.getAttribute("data-track")));
    row.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        focusFolder(row.getAttribute("data-track"));
      }
    });
  });
  if (showAllBtn) showAllBtn.addEventListener("click", clearFolderFilter);

  // Expose for debugging
  window.focusGraphifyFolder = focusFolder;
  window.clearGraphifyFolderFilter = clearFolderFilter;
})();
</script>
"""


def patch_html(html: str, panel: str) -> str:
    # Remove previous injections if re-run
    html = re.sub(
        r"\s*/\* folder-stats-css \*/.*?/\* /folder-stats-css \*/\s*",
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'\n?\s*<div id="folder-stats-wrap">[\s\S]*?<div id="folder-stats">[\s\S]*?</div>\s*</div>\s*',
        "\n",
        html,
        count=1,
    )
    html = re.sub(
        r'\s*<script id="folder-filter-js">[\s\S]*?</script>\s*',
        "\n",
        html,
        count=1,
    )

    html = html.replace(
        "</style>",
        f"  /* folder-stats-css */{CSS}  /* /folder-stats-css */\n</style>",
        1,
    )

    if '<div id="legend-wrap">' in html:
        html = html.replace(
            '<div id="legend-wrap">',
            panel + "  <div id=\"legend-wrap\">",
            1,
        )
    elif '<div id="stats">' in html:
        html = html.replace('<div id="stats">', panel + '  <div id="stats">', 1)
    else:
        raise SystemExit("error: could not find sidebar insertion point")

    # Inject filter JS after network is created (before </body>)
    if "</body>" in html:
        html = html.replace("</body>", FOLDER_FILTER_JS + "\n</body>", 1)
    else:
        html += FOLDER_FILTER_JS

    return html


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML)
    parser.add_argument("--graph", type=Path, default=DEFAULT_GRAPH)
    args = parser.parse_args()

    if not args.html.is_file():
        print(f"error: HTML not found: {args.html}", file=sys.stderr)
        return 1

    html = args.html.read_text(encoding="utf-8")
    sources = load_source_files(html, args.graph)
    rows = folder_stats(sources)
    total = sum(r["count"] for r in rows)
    panel = build_panel_html(rows, total)
    patched = patch_html(html, panel)
    args.html.write_text(patched, encoding="utf-8")

    print(f"Patched {args.html.relative_to(REPO_ROOT)} — click a top folder to focus it + linked pages")
    for r in rows[:12]:
        print(f"  {r['percent']:5.1f}%  {r['label']} ({r['count']})")
    if len(rows) > 12:
        print(f"  … +{len(rows) - 12} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
