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
            f"""    <div class="folder-row" title="{r['count']} nodes">
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
    <div class="folder-meta">{total} nodes by curriculum track</div>
    <div id="folder-stats">
{body}
    </div>
  </div>
"""


CSS = """
  #folder-stats-wrap { padding: 12px 14px; border-bottom: 1px solid #2a2a4e; max-height: 42vh; overflow-y: auto; }
  #folder-stats-wrap h3 { font-size: 13px; color: #aaa; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.05em; }
  .folder-meta { font-size: 11px; color: #666; margin-bottom: 10px; }
  .folder-row { margin-bottom: 8px; }
  .folder-head { display: flex; align-items: center; gap: 8px; font-size: 12px; margin-bottom: 3px; }
  .folder-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
  .folder-label { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .folder-pct { color: #9aa; font-variant-numeric: tabular-nums; font-size: 11px; }
  .folder-bar { height: 6px; background: #0f0f1a; border-radius: 3px; overflow: hidden; }
  .folder-fill { height: 100%; border-radius: 3px; opacity: 0.85; }
"""


def patch_html(html: str, panel: str) -> str:
    # Remove a previous injection if re-run
    html = re.sub(
        r"\s*/\* folder-stats-css \*/.*?/\* /folder-stats-css \*/\s*",
        "\n",
        html,
        count=1,
        flags=re.S,
    )
    html = re.sub(
        r'\s*<div id="folder-stats-wrap">[\s\S]*?</div>\s*(?=<div id="legend-wrap">|<div id="stats">)',
        "\n",
        html,
        count=1,
    )

    if "/* folder-stats-css */" not in html:
        html = html.replace(
            "</style>",
            f"  /* folder-stats-css */{CSS}  /* /folder-stats-css */\n</style>",
            1,
        )

    # Prefer placing above communities legend
    if '<div id="legend-wrap">' in html:
        html = html.replace(
            '<div id="legend-wrap">',
            panel + '  <div id="legend-wrap">',
            1,
        )
    elif '<div id="stats">' in html:
        html = html.replace('<div id="stats">', panel + '  <div id="stats">', 1)
    else:
        raise SystemExit("error: could not find sidebar insertion point")

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

    print(f"Patched {args.html.relative_to(REPO_ROOT)} — {total} nodes across {len(rows)} top folders:")
    for r in rows[:12]:
        print(f"  {r['percent']:5.1f}%  {r['label']} ({r['count']})")
    if len(rows) > 12:
        print(f"  … +{len(rows) - 12} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
