#!/usr/bin/env python3
"""Build JSON graph exports from src/content markdown notes.

Formats:
  graph     — flat nodes + contains/link edges (original)
  clusters  — radial layout, cluster metadata, proximity edges for spatial viz
  both      — write both files (default)

Usage:
  python scripts/build-content-graph.py
  python scripts/build-content-graph.py --format clusters --locale en
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_ROOT = REPO_ROOT / "src" / "content"
DEFAULT_GRAPH_OUTPUT = REPO_ROOT / "scripts" / "output" / "content-graph.json"
DEFAULT_CLUSTER_OUTPUT = REPO_ROOT / "scripts" / "output" / "content-clusters.json"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
FM_FIELD_RE = re.compile(
    r"^(label|subtitle|group|order|groupOrder):\s*[\"']?(.+?)[\"']?\s*$",
    re.MULTILINE,
)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^```[\w.-]*\s*$", re.MULTILINE)

# Radial layout tuning
LAYOUT_RADIUS_STEP = 72
LAYOUT_LOCALE_GAP = 900


def split_fences(text: str) -> list[tuple[bool, str]]:
    parts: list[tuple[bool, str]] = []
    pos = 0
    in_fence = False
    fence_start = 0
    for m in FENCE_RE.finditer(text):
        if not in_fence:
            if m.start() > pos:
                parts.append((False, text[pos : m.start()]))
            in_fence = True
            fence_start = m.start()
        else:
            end_pos = m.end()
            parts.append((True, text[fence_start:end_pos]))
            pos = end_pos
            in_fence = False
    if pos < len(text):
        parts.append((False, text[pos:]))
    return parts


def parse_frontmatter(path: Path) -> dict[str, Any]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    meta: dict[str, Any] = {}
    for key, raw in FM_FIELD_RE.findall(m.group(1)):
        value: Any = raw.strip()
        if key in {"order", "groupOrder"}:
            try:
                value = int(value)
            except ValueError:
                pass
        meta[key] = value
    return meta


def read_meta_json(path: Path) -> dict[str, Any]:
    meta_path = path / "_meta.json"
    if not meta_path.is_file():
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def node_id(rel: Path) -> str:
    return rel.as_posix()


def build_path_index() -> dict[str, Any]:
    by_rel: dict[str, Path] = {}
    by_name: dict[str, list[Path]] = {}
    by_suffix: dict[str, list[Path]] = {}
    for path in CONTENT_ROOT.rglob("*.md"):
        rel = path.relative_to(CONTENT_ROOT).as_posix()
        key = rel.lower()
        by_rel[key] = path
        by_name.setdefault(path.name.lower(), []).append(path)
        parts = key.split("/")
        for i in range(len(parts)):
            suffix = "/".join(parts[i:])
            by_suffix.setdefault(suffix, []).append(path)
    return {"by_rel": by_rel, "by_name": by_name, "by_suffix": by_suffix}


def resolve_target(ref: str, source: Path, index: dict[str, Any]) -> Path | None:
    ref = ref.replace("\\", "/").strip()
    if not ref.lower().endswith(".md") and ".md#" not in ref.lower():
        return None
    if ref.startswith(("http://", "https://", "mailto:")):
        return None

    ref_path = ref.split("#", 1)[0].split("?", 1)[0]
    if ref_path.lower() == "readme.md":
        return None

    candidate = (source.parent / ref_path).resolve()
    try:
        candidate.relative_to(CONTENT_ROOT.resolve())
        if candidate.is_file():
            return candidate
    except ValueError:
        pass

    rel_key = ref_path.lstrip("./").lower()
    if rel_key in index["by_rel"]:
        return index["by_rel"][rel_key]

    suffix_matches = index["by_suffix"].get(rel_key, [])
    if len(suffix_matches) == 1:
        return suffix_matches[0]
    if len(suffix_matches) > 1:
        source_top = source.relative_to(CONTENT_ROOT).parts[0].lower()
        same_locale = [
            m
            for m in suffix_matches
            if m.relative_to(CONTENT_ROOT).parts[0].lower() == source_top
        ]
        pool = same_locale or suffix_matches
        return min(pool, key=lambda p: len(os.path.relpath(p, start=source.parent)))

    name = Path(ref_path).name.lower()
    matches = index["by_name"].get(name, [])
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        source_top = source.relative_to(CONTENT_ROOT).parts[0].lower()
        for m in matches:
            if m.relative_to(CONTENT_ROOT).parts[0].lower() == source_top:
                return m
    return None


def extract_links(path: Path, index: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []

    m = FRONTMATTER_RE.match(text)
    body = text[m.end() :] if m else text

    links: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for in_fence, chunk in split_fences(body):
        if in_fence:
            continue
        for match in MARKDOWN_LINK_RE.finditer(chunk):
            label = match.group(1).strip()
            href = match.group(2).strip()
            if href.startswith("<") and href.endswith(">"):
                href = href[1:-1]
            target = resolve_target(href, path, index)
            if not target:
                continue
            source_id = node_id(path.relative_to(CONTENT_ROOT))
            target_id = node_id(target.relative_to(CONTENT_ROOT))
            key = (source_id, target_id)
            if key in seen:
                continue
            seen.add(key)
            links.append(
                {
                    "source": source_id,
                    "target": target_id,
                    "kind": "link",
                    "weight": 0.12,
                    "label": label,
                    "href": href,
                }
            )
    return links


def sort_key(meta: dict[str, Any], fallback_name: str) -> tuple[int, str]:
    order = meta.get("order")
    if isinstance(order, int):
        return (order, fallback_name.lower())
    return (10_000, fallback_name.lower())


def leaf_count(node: dict[str, Any]) -> int:
    if node.get("type") == "note":
        return 1
    children = node.get("children") or []
    total = sum(leaf_count(c) for c in children)
    return max(total, 1) if children else 1


def build_section_tree(
    section_dir: Path,
    rel_dir: Path,
    locale: str,
    nodes: list[dict[str, Any]],
    contains_edges: list[dict[str, Any]],
    parent_id: str | None,
) -> dict[str, Any]:
    meta = read_meta_json(section_dir)
    section_node_id = node_id(rel_dir)

    section_entry: dict[str, Any] = {
        "id": section_node_id,
        "type": "section",
        "locale": locale,
        "path": section_node_id,
        "label": meta.get("label", section_dir.name),
        "order": meta.get("order"),
        "parentId": parent_id,
        "children": [],
    }
    nodes.append(
        {
            "id": section_node_id,
            "type": "section",
            "locale": locale,
            "path": section_node_id,
            "label": section_entry["label"],
            "order": section_entry["order"],
            "parentId": parent_id,
        }
    )

    child_dirs = [
        p
        for p in section_dir.iterdir()
        if p.is_dir() and (p / "_meta.json").is_file()
    ]
    child_dirs.sort(key=lambda p: sort_key(read_meta_json(p), p.name))

    md_files = sorted(
        section_dir.glob("*.md"),
        key=lambda p: sort_key(parse_frontmatter(p), p.name),
    )

    ordered_children: list[dict[str, Any]] = []

    for sub in child_dirs:
        child_rel = rel_dir / sub.name
        child_tree = build_section_tree(
            sub, child_rel, locale, nodes, contains_edges, section_node_id
        )
        section_entry["children"].append(child_tree)
        ordered_children.append(child_tree)
        contains_edges.append(
            {
                "source": section_node_id,
                "target": child_tree["id"],
                "kind": "contains",
                "weight": 1.0,
            }
        )

    for md in md_files:
        note_rel = rel_dir / md.name
        note_id = node_id(note_rel)
        fm = parse_frontmatter(md)
        note_entry: dict[str, Any] = {
            "id": note_id,
            "type": "note",
            "locale": locale,
            "path": note_id,
            "file": md.name,
            "label": fm.get("label"),
            "subtitle": fm.get("subtitle"),
            "group": fm.get("group"),
            "order": fm.get("order"),
            "groupOrder": fm.get("groupOrder"),
            "parentId": section_node_id,
        }
        section_entry["children"].append(note_entry)
        ordered_children.append(note_entry)
        nodes.append(note_entry)
        contains_edges.append(
            {
                "source": section_node_id,
                "target": note_id,
                "kind": "contains",
                "weight": 1.0,
            }
        )

    section_entry["_orderedChildren"] = ordered_children
    return section_entry


def discover_locales() -> list[str]:
    locales: list[str] = []
    for path in sorted(CONTENT_ROOT.iterdir()):
        if path.is_dir() and (path / "_meta.json").is_file():
            locales.append(path.name)
    return locales


def build_graph(locales: list[str]) -> dict[str, Any]:
    index = build_path_index()
    nodes: list[dict[str, Any]] = []
    contains_edges: list[dict[str, Any]] = []
    link_edges: list[dict[str, Any]] = []
    trees: dict[str, Any] = {}

    for locale in locales:
        locale_dir = CONTENT_ROOT / locale
        if not locale_dir.is_dir():
            continue
        locale_rel = Path(locale)
        locale_meta = read_meta_json(locale_dir)
        locale_tree: dict[str, Any] = {
            "id": locale,
            "type": "locale",
            "locale": locale,
            "path": locale,
            "label": locale_meta.get("label", locale),
            "order": locale_meta.get("order"),
            "parentId": None,
            "children": [],
        }
        nodes.append(
            {
                "id": locale,
                "type": "locale",
                "locale": locale,
                "path": locale,
                "label": locale_tree["label"],
                "order": locale_tree["order"],
                "parentId": None,
            }
        )

        top_sections = [
            p
            for p in locale_dir.iterdir()
            if p.is_dir() and (p / "_meta.json").is_file()
        ]
        top_sections.sort(key=lambda p: sort_key(read_meta_json(p), p.name))

        ordered_top: list[dict[str, Any]] = []
        for section in top_sections:
            child_rel = locale_rel / section.name
            child_tree = build_section_tree(
                section, child_rel, locale, nodes, contains_edges, locale
            )
            locale_tree["children"].append(child_tree)
            ordered_top.append(child_tree)
            contains_edges.append(
                {
                    "source": locale,
                    "target": child_tree["id"],
                    "kind": "contains",
                    "weight": 1.0,
                }
            )

        locale_tree["_orderedChildren"] = ordered_top
        trees[locale] = locale_tree

    note_paths = [n["id"] for n in nodes if n["type"] == "note"]
    for rel in note_paths:
        path = CONTENT_ROOT / rel
        link_edges.extend(extract_links(path, index))

    unique_nodes: dict[str, dict[str, Any]] = {}
    for n in nodes:
        unique_nodes[n["id"]] = n

    all_edges = contains_edges + link_edges

    return {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "contentRoot": "src/content",
            "script": "scripts/build-content-graph.py",
            "format": "graph",
            "localeCount": len(trees),
            "nodeCount": len(unique_nodes),
            "edgeCount": len(all_edges),
            "linkEdgeCount": len(link_edges),
            "containsEdgeCount": len(contains_edges),
        },
        "locales": locales,
        "trees": trees,
        "nodes": sorted(unique_nodes.values(), key=lambda n: n["id"]),
        "edges": all_edges,
    }


def _cluster_path_parts(node_id_str: str) -> list[str]:
    return node_id_str.split("/")


def _note_cluster_id(note: dict[str, Any]) -> str:
    return note.get("parentId") or note["id"]


def _layout_radial(
    node: dict[str, Any],
    cx: float,
    cy: float,
    angle_start: float,
    angle_end: float,
    depth: int,
    positions: dict[str, dict[str, float]],
) -> None:
    children = node.get("_orderedChildren") or node.get("children") or []
    if not children:
        return

    total_leaves = sum(leaf_count(c) for c in children)
    angle = angle_start
    span_total = angle_end - angle_start

    for child in children:
        fraction = leaf_count(child) / total_leaves
        child_span = span_total * fraction
        child_end = angle + child_span
        mid = (angle + child_end) / 2
        radius = (depth + 1) * LAYOUT_RADIUS_STEP
        x = cx + radius * math.cos(mid)
        y = cy + radius * math.sin(mid)
        positions[child["id"]] = {"x": round(x, 2), "y": round(y, 2)}

        if child.get("type") in {"locale", "section"}:
            _layout_radial(child, cx, cy, angle, child_end, depth + 1, positions)

        angle = child_end


def _collect_cluster_members(
    trees: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Map section id -> cluster record with member note ids."""
    clusters: dict[str, dict[str, Any]] = {}

    def walk(node: dict[str, Any], ancestry: list[str]) -> None:
        nid = node["id"]
        path_labels = ancestry + [node.get("label") or nid.split("/")[-1]]
        if node.get("type") in {"locale", "section"}:
            clusters[nid] = {
                "id": nid,
                "label": node.get("label"),
                "type": node.get("type"),
                "locale": node.get("locale"),
                "depth": len(ancestry),
                "path": nid,
                "pathLabels": path_labels,
                "members": [],
                "noteCount": 0,
            }
        for child in node.get("_orderedChildren") or node.get("children") or []:
            walk(child, path_labels if node.get("type") in {"locale", "section"} else ancestry)
            if child.get("type") == "note" and node.get("type") in {"locale", "section"}:
                clusters[nid]["members"].append(child["id"])
                clusters[nid]["noteCount"] += 1

    for tree in trees.values():
        walk(tree, [])

    return clusters


def _proximity_edges_from_tree(trees: dict[str, Any]) -> list[dict[str, Any]]:
    """Sibling + curriculum-order edges keep nested notes physically close."""
    edges: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()

    def add_edge(source: str, target: str, kind: str, weight: float) -> None:
        key = (source, target, kind)
        if key in seen or source == target:
            return
        seen.add(key)
        edges.append(
            {"source": source, "target": target, "kind": kind, "weight": weight}
        )

    def walk(node: dict[str, Any]) -> None:
        children = node.get("_orderedChildren") or node.get("children") or []
        child_ids = [c["id"] for c in children]

        for i, cid in enumerate(child_ids):
            if i > 0:
                add_edge(child_ids[i - 1], cid, "sibling", 0.55)
            if i > 0 and i < len(child_ids):
                add_edge(child_ids[i - 1], cid, "adjacent", 0.7)

        notes = [c for c in children if c.get("type") == "note"]
        for i in range(len(notes) - 1):
            a, b = notes[i]["id"], notes[i + 1]["id"]
            add_edge(a, b, "sequence", 0.85)

        for child in children:
            if child.get("type") in {"locale", "section"}:
                walk(child)

    for tree in trees.values():
        walk(tree)

    return edges


def build_cluster_graph(graph: dict[str, Any]) -> dict[str, Any]:
    trees = graph["trees"]
    nodes_by_id = {n["id"]: dict(n) for n in graph["nodes"]}
    positions: dict[str, dict[str, float]] = {}

    locale_list = graph["locales"]
    n_locales = len(locale_list)
    for i, locale in enumerate(locale_list):
        if locale not in trees:
            continue
        offset_x = (i - (n_locales - 1) / 2) * LAYOUT_LOCALE_GAP
        positions[locale] = {"x": round(offset_x, 2), "y": 0.0}
        _layout_radial(trees[locale], offset_x, 0.0, 0.0, 2 * math.pi, 0, positions)

    clusters = _collect_cluster_members(trees)

    for cid, cluster in clusters.items():
        member_positions = [positions[m] for m in cluster["members"] if m in positions]
        if member_positions:
            cluster["centroid"] = {
                "x": round(sum(p["x"] for p in member_positions) / len(member_positions), 2),
                "y": round(sum(p["y"] for p in member_positions) / len(member_positions), 2),
            }
        elif cid in positions:
            cluster["centroid"] = dict(positions[cid])

    cluster_nodes: list[dict[str, Any]] = []
    for nid, base in nodes_by_id.items():
        pos = positions.get(nid, {"x": 0.0, "y": 0.0})
        parts = _cluster_path_parts(nid)
        depth = len(parts) - (1 if base["type"] == "note" else 0)

        entry: dict[str, Any] = {
            **base,
            "x": pos["x"],
            "y": pos["y"],
            "depth": depth,
            "clusterId": _note_cluster_id(base) if base["type"] == "note" else nid,
            "clusterPath": parts[:-1] if base["type"] == "note" else parts,
        }
        if base["type"] == "note":
            parent = base.get("parentId")
            if parent and parent in clusters:
                entry["clusterLabel"] = clusters[parent].get("label")
                entry["topicPath"] = clusters[parent].get("pathLabels", [])
        elif nid in clusters:
            entry["clusterLabel"] = clusters[nid].get("label")
            entry["topicPath"] = clusters[nid].get("pathLabels", [])
            entry["noteCount"] = clusters[nid].get("noteCount", 0)

        cluster_nodes.append(entry)

    proximity = _proximity_edges_from_tree(trees)
    link_edges = [
        {**e, "weight": e.get("weight", 0.12)}
        for e in graph["edges"]
        if e.get("kind") == "link"
    ]

    # Boost cross-links inside the same leaf cluster
    note_cluster_map = {
        n["id"]: n.get("clusterId")
        for n in cluster_nodes
        if n["type"] == "note"
    }
    for edge in link_edges:
        sc = note_cluster_map.get(edge["source"])
        tc = note_cluster_map.get(edge["target"])
        if sc and sc == tc:
            edge["weight"] = 0.45
            edge["kind"] = "link-intra-cluster"

    contains_edges = [
        {**e, "weight": e.get("weight", 1.0)}
        for e in graph["edges"]
        if e.get("kind") == "contains"
    ]

    all_edges = contains_edges + proximity + link_edges

    cluster_list = sorted(
        clusters.values(),
        key=lambda c: (c.get("locale", ""), c.get("path", "")),
    )

    note_count = sum(1 for n in cluster_nodes if n["type"] == "note")
    leaf_clusters = [c for c in cluster_list if c["noteCount"] > 0]

    return {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "contentRoot": "src/content",
            "script": "scripts/build-content-graph.py",
            "format": "clusters",
            "description": (
                "Radial cluster layout — nested topics share space; "
                "use sequence/sibling edges for cohesion, link edges for cross-refs"
            ),
            "localeCount": len(trees),
            "nodeCount": len(cluster_nodes),
            "noteCount": note_count,
            "clusterCount": len(leaf_clusters),
            "edgeCount": len(all_edges),
            "layout": {
                "type": "radial",
                "radiusStep": LAYOUT_RADIUS_STEP,
                "localeGap": LAYOUT_LOCALE_GAP,
            },
            "edgeKinds": {
                "contains": "parent → child in folder tree (weight 1.0)",
                "sequence": "curriculum order within same folder (weight 0.85)",
                "adjacent": "immediate neighbor in sidebar order (weight 0.7)",
                "sibling": "same parent section (weight 0.55)",
                "link": "markdown cross-reference (weight 0.12)",
                "link-intra-cluster": "cross-ref within same cluster (weight 0.45)",
            },
        },
        "locales": graph["locales"],
        "clusters": cluster_list,
        "nodes": sorted(cluster_nodes, key=lambda n: n["id"]),
        "edges": all_edges,
    }


def _strip_internal_keys(obj: Any) -> Any:
    """Remove _orderedChildren from tree output."""
    if isinstance(obj, dict):
        return {
            k: _strip_internal_keys(v)
            for k, v in obj.items()
            if not k.startswith("_")
        }
    if isinstance(obj, list):
        return [_strip_internal_keys(v) for v in obj]
    return obj


def write_json(path: Path, data: dict[str, Any], indent: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _strip_internal_keys(data)
    path.write_text(
        json.dumps(payload, indent=indent if indent > 0 else None, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build content graph JSON (flat graph and/or cluster layout).",
    )
    parser.add_argument(
        "--format",
        choices=("graph", "clusters", "both"),
        default="both",
        help="Output format (default: both)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_GRAPH_OUTPUT,
        help="Graph output path (--format graph or both)",
    )
    parser.add_argument(
        "--clusters-output",
        type=Path,
        default=DEFAULT_CLUSTER_OUTPUT,
        help="Cluster layout output path (--format clusters or both)",
    )
    parser.add_argument(
        "--locale",
        action="append",
        dest="locales",
        help="Limit to locale folder(s), e.g. en or jp (repeatable)",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indent (default: 2; use 0 for compact)",
    )
    args = parser.parse_args()

    available = discover_locales()
    if args.locales:
        locales = [loc for loc in args.locales if loc in available]
        missing = set(args.locales) - set(locales)
        for loc in sorted(missing):
            print(f"warning: unknown locale '{loc}', skipping", file=sys.stderr)
    else:
        locales = available

    if not locales:
        print("error: no locales found under src/content", file=sys.stderr)
        return 1

    graph = build_graph(locales)

    if args.format in ("graph", "both"):
        write_json(args.output, graph, args.indent)
        m = graph["meta"]
        print(
            f"Wrote {args.output.relative_to(REPO_ROOT)} — "
            f"{m['nodeCount']} nodes, {m['edgeCount']} edges"
        )

    if args.format in ("clusters", "both"):
        clusters = build_cluster_graph(graph)
        write_json(args.clusters_output, clusters, args.indent)
        m = clusters["meta"]
        print(
            f"Wrote {args.clusters_output.relative_to(REPO_ROOT)} — "
            f"{m['noteCount']} notes in {m['clusterCount']} clusters, "
            f"{m['edgeCount']} edges, radial layout"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
