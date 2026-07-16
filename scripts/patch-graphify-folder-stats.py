#!/usr/bin/env python3
"""Inject top-folder % panel + click-to-filter into graphify-out/graph.html.

Clicking a top folder shows only that track's nodes plus one-hop linked pages.

Usage:
  python scripts/patch-graphify-folder-stats.py
  # always safe to re-run after: graphify export html
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

MARK_CSS_START = "/* graphify-folder-stats:css */"
MARK_CSS_END = "/* /graphify-folder-stats:css */"
MARK_PANEL_START = "<!-- graphify-folder-stats:panel -->"
MARK_PANEL_END = "<!-- /graphify-folder-stats:panel -->"
MARK_JS_START = "<!-- graphify-folder-stats:js -->"
MARK_JS_END = "<!-- /graphify-folder-stats:js -->"


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
        files = [n["source_file"] for n in data.get("nodes", []) if n.get("source_file")]
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
        items.append(
            f"""    <button type="button" class="folder-row" data-track="{r["id"]}"
            title="Show {r["label"]} + linked pages ({r["count"]} nodes)">
      <div class="folder-head">
        <span class="folder-dot" style="background:{r["color"]}"></span>
        <span class="folder-label">{r["label"]}</span>
        <span class="folder-pct">{r["percent"]}%</span>
      </div>
      <div class="folder-bar"><div class="folder-fill" style="width:{r["percent"]}%;background:{r["color"]}"></div></div>
    </button>"""
        )
    body = "\n".join(items)
    return f"""{MARK_PANEL_START}
  <div id="folder-stats-wrap">
    <h3>Top folders</h3>
    <div class="folder-meta">{total} nodes · click a folder to show it and linked pages</div>
    <button type="button" id="folder-show-all" class="folder-show-all">Show all</button>
    <div id="folder-stats">
{body}
    </div>
  </div>
{MARK_PANEL_END}
"""


CSS = f"""
  {MARK_CSS_START}
  #folder-stats-wrap {{ padding: 12px 14px; border-bottom: 1px solid #2a2a4e; max-height: 42vh; overflow-y: auto; }}
  #folder-stats-wrap h3 {{ font-size: 13px; color: #aaa; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em; }}
  .folder-meta {{ font-size: 11px; color: #666; margin-bottom: 8px; line-height: 1.35; }}
  .folder-show-all {{
    display: none; width: 100%; margin-bottom: 10px; padding: 6px 8px;
    background: #0f0f1a; border: 1px solid #3a3a5e; color: #ccc;
    border-radius: 6px; cursor: pointer; font-size: 12px;
  }}
  .folder-show-all:hover {{ border-color: #4E79A7; color: #fff; }}
  .folder-show-all.visible {{ display: block; }}
  button.folder-row {{
    display: block; width: 100%; margin: 0 0 8px; padding: 6px 6px 8px;
    background: transparent; border: 1px solid transparent; border-radius: 6px;
    color: inherit; text-align: left; cursor: pointer; font: inherit;
  }}
  button.folder-row:hover {{ background: #2a2a4e; }}
  button.folder-row.active {{ background: #243044; border-color: #3a5a7a; }}
  button.folder-row.dimmed {{ opacity: 0.35; }}
  .folder-head {{ display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 3px; }}
  .folder-dot {{ width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }}
  .folder-label {{ flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .folder-pct {{ color: #9aa; font-variant-numeric: tabular-nums; font-size: 11px; }}
  .folder-bar {{ height: 6px; background: #0f0f1a; border-radius: 3px; overflow: hidden; }}
  .folder-fill {{ height: 100%; border-radius: 3px; opacity: 0.85; }}
  {MARK_CSS_END}
"""

# JS uses only double-quoted strings for path normalize to avoid regex escape bugs.
FOLDER_FILTER_JS = f"""
{MARK_JS_START}
<script>
(function () {{
  function trackOf(sf) {{
    if (!sf) return "misc";
    var s = String(sf).split("\\\\").join("/");
    var parts = s.split("/").filter(Boolean);
    var known = {{
      ai101:1, swe101:1, sre101:1, cs101:1, cybersecurity:1,
      "digital-marketing":1, cryptocurrency101:1, startups:1, food:1,
      languages:1, "getting-started":1
    }};
    for (var i = 0; i < parts.length; i++) {{
      var pl = parts[i].toLowerCase();
      if (known[pl]) return pl;
      if ((pl === "en" || pl === "jp") && i + 1 < parts.length) {{
        var nxt = parts[i + 1].toLowerCase();
        if (known[nxt]) return nxt;
      }}
      if (pl === ".obsidian") return ".obsidian";
    }}
    for (var j = 0; j < parts.length; j++) {{
      var p = parts[j].toLowerCase();
      if (p !== "src" && p !== "content" && p.charAt(0) !== ".") return p;
    }}
    return "misc";
  }}

  function titleOf(t) {{
    var map = {{
      ai101:"AI101", swe101:"SWE101", sre101:"SRE101", cs101:"CS101",
      cybersecurity:"Cybersecurity", "digital-marketing":"Digital marketing",
      cryptocurrency101:"Cryptocurrency101", startups:"Startups", food:"Food",
      languages:"Languages", "getting-started":"Getting started",
      ".obsidian":"Obsidian config", misc:"Other"
    }};
    return map[t] || t;
  }}

  if (typeof RAW_NODES === "undefined" || typeof nodesDS === "undefined") {{
    console.error("[folder-stats] graphify datasets not ready");
    return;
  }}

  var adj = {{}};
  function link(a, b) {{
    if (!adj[a]) adj[a] = [];
    if (!adj[b]) adj[b] = [];
    adj[a].push(b);
    adj[b].push(a);
  }}
  for (var ei = 0; ei < RAW_EDGES.length; ei++) {{
    link(RAW_EDGES[ei].from, RAW_EDGES[ei].to);
  }}

  var activeTrack = null;
  var wrap = document.getElementById("folder-stats-wrap");
  var showAllBtn = document.getElementById("folder-show-all");

  function setInfo(html) {{
    var el = document.getElementById("info-content");
    if (el) el.innerHTML = html;
  }}

  function nodeUpdates(predicateVisible) {{
    var out = [];
    for (var i = 0; i < RAW_NODES.length; i++) {{
      var n = RAW_NODES[i];
      var hide = !predicateVisible(n);
      if (typeof hiddenCommunities !== "undefined" && hiddenCommunities.has(n.community)) {{
        hide = true;
      }}
      out.push({{ id: n.id, hidden: hide }});
    }}
    return out;
  }}

  function edgeUpdates(visibleIds) {{
    var out = [];
    for (var i = 0; i < RAW_EDGES.length; i++) {{
      var e = RAW_EDGES[i];
      var show = visibleIds[e.from] && visibleIds[e.to];
      out.push({{ id: i, hidden: !show }});
    }}
    return out;
  }}

  function clearFolderFilter() {{
    activeTrack = null;
    var rows = wrap ? wrap.querySelectorAll(".folder-row") : [];
    for (var i = 0; i < rows.length; i++) {{
      rows[i].classList.remove("active", "dimmed");
    }}
    if (showAllBtn) showAllBtn.classList.remove("visible");

    nodesDS.update(nodeUpdates(function () {{ return true; }}));
    if (typeof edgesDS !== "undefined") {{
      var all = {{}};
      for (var i = 0; i < RAW_NODES.length; i++) all[RAW_NODES[i].id] = true;
      edgesDS.update(edgeUpdates(all));
    }}
    if (typeof network !== "undefined") network.fit({{ animation: true }});
    setInfo('<span class="empty">Click a node to inspect it</span>');
  }}

  function focusFolder(track) {{
    if (activeTrack === track) {{
      clearFolderFilter();
      return;
    }}
    activeTrack = track;

    var inFolder = {{}};
    var inCount = 0;
    for (var i = 0; i < RAW_NODES.length; i++) {{
      var n = RAW_NODES[i];
      if (trackOf(n.source_file) === track) {{
        inFolder[n.id] = true;
        inCount++;
      }}
    }}

    var visible = {{}};
    for (var id in inFolder) {{
      if (!Object.prototype.hasOwnProperty.call(inFolder, id)) continue;
      visible[id] = true;
      var nbs = adj[id] || [];
      for (var k = 0; k < nbs.length; k++) visible[nbs[k]] = true;
    }}

    var linkedOnly = 0;
    for (var vid in visible) {{
      if (!Object.prototype.hasOwnProperty.call(visible, vid)) continue;
      if (!inFolder[vid]) linkedOnly++;
    }}

    var rows = wrap ? wrap.querySelectorAll(".folder-row") : [];
    for (var r = 0; r < rows.length; r++) {{
      var t = rows[r].getAttribute("data-track");
      rows[r].classList.toggle("active", t === track);
      rows[r].classList.toggle("dimmed", t !== track);
    }}
    if (showAllBtn) showAllBtn.classList.add("visible");

    nodesDS.update(nodeUpdates(function (n) {{ return !!visible[n.id]; }}));
    if (typeof edgesDS !== "undefined") edgesDS.update(edgeUpdates(visible));

    var fitIds = [];
    for (var fid in visible) {{
      if (!Object.prototype.hasOwnProperty.call(visible, fid)) continue;
      var node = nodesDS.get(fid);
      if (node && !node.hidden) fitIds.push(fid);
    }}
    if (fitIds.length && typeof network !== "undefined") {{
      network.fit({{ nodes: fitIds, animation: true }});
    }}

    setInfo(
      "<div class=\\"field\\"><b>" + titleOf(track) + "</b></div>" +
      "<div class=\\"field\\">" + inCount + " nodes in folder</div>" +
      "<div class=\\"field\\">" + linkedOnly + " linked pages outside folder</div>" +
      "<div class=\\"field\\" style=\\"color:#888;margin-top:6px;font-size:11px\\">Click again or Show all to reset</div>"
    );
  }}

  if (wrap) {{
    wrap.addEventListener("click", function (ev) {{
      var btn = ev.target.closest ? ev.target.closest(".folder-row") : null;
      if (!btn || !wrap.contains(btn)) return;
      var track = btn.getAttribute("data-track");
      if (track) focusFolder(track);
    }});
  }}
  if (showAllBtn) {{
    showAllBtn.addEventListener("click", function (ev) {{
      ev.stopPropagation();
      clearFolderFilter();
    }});
  }}

  window.focusGraphifyFolder = focusFolder;
  window.clearGraphifyFolderFilter = clearFolderFilter;
  console.info("[folder-stats] ready — click a Top folders row to filter");
}})();
</script>
{MARK_JS_END}
"""


def strip_previous(html: str) -> str:
    html = re.sub(
        re.escape(MARK_CSS_START) + r".*?" + re.escape(MARK_CSS_END),
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        re.escape(MARK_PANEL_START) + r".*?" + re.escape(MARK_PANEL_END),
        "",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        re.escape(MARK_JS_START) + r".*?" + re.escape(MARK_JS_END),
        "",
        html,
        count=1,
        flags=re.S,
    )
    # Legacy leftovers from earlier broken patches
    html = re.sub(
        r"\s*/\* folder-stats-css \*/.*?/\* /folder-stats-css \*/\s*",
        "\n",
        html,
        flags=re.S,
    )
    html = re.sub(
        r'\s*<script id="folder-filter-js">[\s\S]*?</script>\s*',
        "\n",
        html,
        count=1,
    )
    return html


def patch_html(html: str, panel: str) -> str:
    html = strip_previous(html)

    if "</style>" not in html:
        raise SystemExit("error: no </style> in HTML")
    html = html.replace("</style>", CSS + "\n</style>", 1)

    needle = '<div id="legend-wrap">'
    if needle not in html:
        raise SystemExit("error: #legend-wrap not found — refusing to patch broken HTML")
    html = html.replace(needle, panel + "\n  " + needle, 1)

    if "</body>" not in html:
        raise SystemExit("error: no </body>")
    html = html.replace("</body>", FOLDER_FILTER_JS + "\n</body>", 1)

    # Sanity: sidebar must still contain legend-wrap
    side = re.search(r'<div id="sidebar">([\s\S]*?)</div>\s*<script>', html)
    if not side or 'id="legend-wrap"' not in side.group(1):
        raise SystemExit("error: patch would break sidebar structure — aborted write")
    if 'id="folder-stats-wrap"' not in side.group(1):
        raise SystemExit("error: folder panel not inside sidebar — aborted write")

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

    # Verify structure after write
    check = args.html.read_text(encoding="utf-8")
    side = re.search(r'<div id="sidebar">([\s\S]*?)</div>\s*<script>', check)
    ok = bool(side and "folder-stats-wrap" in side.group(1) and "legend-wrap" in side.group(1))
    print(f"Patched {args.html.relative_to(REPO_ROOT)} — sidebar OK={ok}")
    print("Click a Top folders button to filter that track + linked pages.")
    for r in rows[:8]:
        print(f"  {r['percent']:5.1f}%  {r['label']} ({r['count']})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
