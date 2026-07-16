#!/usr/bin/env python3
"""Build note-link graph exports from src/content markdown notes.

One node per note (labels from frontmatter subtitle/group), edges from
markdown links and [[wikilinks]] — Obsidian-style knowledge graph.

Formats:
  graph     — flat nodes + contains/link edges
  clusters  — radial layout, cluster metadata, proximity edges for spatial viz
  both      — write both JSON files (default)
  html      — interactive force-directed note graph (also written with --html)

Usage:
  python scripts/build-content-graph.py
  python scripts/build-content-graph.py --format both --html --locale en
  python scripts/build-content-graph.py --format html --locale en
"""

from __future__ import annotations

import argparse
import html as html_lib
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
DEFAULT_HTML_OUTPUT = REPO_ROOT / "scripts" / "output" / "note-links-graph.html"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
FM_FIELD_RE = re.compile(
    r"^(label|subtitle|group|order|groupOrder):\s*[\"']?(.+?)[\"']?\s*$",
    re.MULTILINE,
)
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
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


def note_display_title(fm: dict[str, Any], filename: str) -> str:
    """Human label for graph UI — prefer frontmatter subtitle over path."""
    subtitle = fm.get("subtitle")
    if isinstance(subtitle, str) and subtitle.strip():
        return subtitle.strip()
    label = fm.get("label")
    if isinstance(label, str) and label.strip() and label.strip().lower() != filename.lower():
        return label.strip()
    return Path(filename).stem.replace("-", " ")


def resolve_target(ref: str, source: Path, index: dict[str, Any]) -> Path | None:
    ref = ref.replace("\\", "/").strip()
    if ref.startswith(("http://", "https://", "mailto:")):
        return None

    ref_path = ref.split("#", 1)[0].split("?", 1)[0].strip()
    if not ref_path:
        return None

    # Wikilinks often omit .md
    if not ref_path.lower().endswith(".md") and ".md#" not in ref.lower():
        if "/" in ref_path or Path(ref_path).suffix == "":
            candidate_md = ref_path + ".md"
        else:
            return None
    else:
        candidate_md = ref_path

    if Path(candidate_md).name.lower() == "readme.md":
        return None

    for attempt in (candidate_md, ref_path):
        candidate = (source.parent / attempt).resolve()
        try:
            candidate.relative_to(CONTENT_ROOT.resolve())
            if candidate.is_file():
                return candidate
            if candidate.suffix == "" and candidate.with_suffix(".md").is_file():
                return candidate.with_suffix(".md")
        except ValueError:
            pass

    for attempt in (candidate_md, ref_path):
        rel_key = attempt.lstrip("./").lower()
        if not rel_key.endswith(".md"):
            rel_key_md = rel_key + ".md"
        else:
            rel_key_md = rel_key

        if rel_key_md in index["by_rel"]:
            return index["by_rel"][rel_key_md]
        if rel_key in index["by_rel"]:
            return index["by_rel"][rel_key]

        for key in (rel_key_md, rel_key):
            suffix_matches = index["by_suffix"].get(key, [])
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
                return min(
                    pool, key=lambda p: len(os.path.relpath(p, start=source.parent))
                )

        name = Path(rel_key_md).name.lower()
        if not name.endswith(".md"):
            name = name + ".md"
        matches = index["by_name"].get(name, [])
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1:
            source_top = source.relative_to(CONTENT_ROOT).parts[0].lower()
            for m in matches:
                if m.relative_to(CONTENT_ROOT).parts[0].lower() == source_top:
                    return m
    return None


def _append_link(
    links: list[dict[str, Any]],
    seen: set[tuple[str, str]],
    source: Path,
    target: Path,
    label: str,
    href: str,
) -> None:
    source_id = node_id(source.relative_to(CONTENT_ROOT))
    target_id = node_id(target.relative_to(CONTENT_ROOT))
    key = (source_id, target_id)
    if key in seen or source_id == target_id:
        return
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
            if target:
                _append_link(links, seen, path, target, label or href, href)
        for match in WIKILINK_RE.finditer(chunk):
            target_ref = match.group(1).strip()
            alias = (match.group(2) or "").strip()
            target = resolve_target(target_ref, path, index)
            if target:
                _append_link(
                    links,
                    seen,
                    path,
                    target,
                    alias or target_ref,
                    f"[[{target_ref}]]",
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
        track = rel_dir.parts[1] if len(rel_dir.parts) > 1 else rel_dir.parts[0]
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
            "displayTitle": note_display_title(fm, md.name),
            "track": track,
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


def build_note_links_payload(graph: dict[str, Any]) -> dict[str, Any]:
    """Obsidian-style payload: notes + link edges only, titled from frontmatter."""
    notes = [n for n in graph["nodes"] if n.get("type") == "note"]
    link_edges = [e for e in graph["edges"] if e.get("kind") == "link"]
    note_ids = {n["id"] for n in notes}
    edges = [
        e
        for e in link_edges
        if e.get("source") in note_ids and e.get("target") in note_ids
    ]

    degree: dict[str, int] = {n["id"]: 0 for n in notes}
    for e in edges:
        degree[e["source"]] = degree.get(e["source"], 0) + 1
        degree[e["target"]] = degree.get(e["target"], 0) + 1

    out_nodes = []
    for n in notes:
        title = n.get("displayTitle") or n.get("subtitle") or n.get("file") or n["id"]
        out_nodes.append(
            {
                "id": n["id"],
                "title": title,
                "subtitle": n.get("subtitle"),
                "label": n.get("label"),
                "group": n.get("group") or n.get("track") or "other",
                "track": n.get("track") or "",
                "path": n.get("path") or n["id"],
                "locale": n.get("locale"),
                "order": n.get("order"),
                "degree": degree.get(n["id"], 0),
            }
        )

    return {
        "meta": {
            "generatedAt": datetime.now(timezone.utc).isoformat(),
            "kind": "note-links",
            "description": (
                "One node per note; labels from frontmatter subtitle; "
                "edges from markdown links and wikilinks"
            ),
            "noteCount": len(out_nodes),
            "linkCount": len(edges),
            "orphanCount": sum(1 for n in out_nodes if n["degree"] == 0),
        },
        "nodes": out_nodes,
        "edges": [
            {
                "source": e["source"],
                "target": e["target"],
                "label": e.get("label"),
            }
            for e in edges
        ],
    }


def write_note_links_html(path: Path, payload: dict[str, Any]) -> None:
    """Self-contained interactive force graph (Obsidian-like)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    data_json = json.dumps(payload, ensure_ascii=False)
    # Escape </script> in JSON so it cannot break out of the script tag
    data_json = data_json.replace("<", "\\u003c")
    meta = payload["meta"]
    title = "Note links graph"
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>{html_lib.escape(title)}</title>
<style>
  :root {{
    --bg: #f3efe6;
    --panel: #fffdf8;
    --ink: #1c1917;
    --muted: #78716c;
    --line: #d6d3d1;
    --accent: #0f766e;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; height: 100%; background: var(--bg); color: var(--ink);
    font-family: "IBM Plex Sans", "Segoe UI", sans-serif; }}
  #app {{ display: grid; grid-template-columns: 280px 1fr; height: 100%; }}
  aside {{
    background: var(--panel); border-right: 1px solid var(--line);
    padding: 1rem; overflow: auto; display: flex; flex-direction: column; gap: .75rem;
  }}
  h1 {{ font-size: 1.05rem; margin: 0; font-weight: 650; letter-spacing: -.01em; }}
  .meta {{ color: var(--muted); font-size: .8rem; line-height: 1.4; }}
  label {{ font-size: .75rem; color: var(--muted); display: block; margin-bottom: .25rem; }}
  input[type=search], select {{
    width: 100%; padding: .45rem .55rem; border: 1px solid var(--line);
    border-radius: 6px; background: #fff; color: var(--ink); font: inherit;
  }}
  .row {{ display: flex; gap: .5rem; align-items: center; font-size: .85rem; }}
  button {{
    border: 1px solid var(--line); background: #fff; border-radius: 6px;
    padding: .4rem .65rem; cursor: pointer; font: inherit; color: var(--ink);
  }}
  button:hover {{ border-color: var(--accent); color: var(--accent); }}
  #detail {{
    margin-top: auto; padding-top: .75rem; border-top: 1px solid var(--line);
    font-size: .85rem; line-height: 1.45; min-height: 7rem;
  }}
  #detail strong {{ display: block; font-size: .95rem; margin-bottom: .25rem; }}
  #detail code {{ font-size: .72rem; color: var(--muted); word-break: break-all; }}
  main {{ position: relative; overflow: hidden; }}
  canvas {{ display: block; width: 100%; height: 100%; cursor: grab; }}
  canvas.dragging {{ cursor: grabbing; }}
  .hint {{
    position: absolute; left: 1rem; bottom: 1rem; color: var(--muted);
    font-size: .75rem; pointer-events: none; background: rgba(243,239,230,.85);
    padding: .35rem .55rem; border-radius: 6px;
  }}
  @media (max-width: 800px) {{
    #app {{ grid-template-columns: 1fr; grid-template-rows: auto 1fr; }}
    aside {{ border-right: none; border-bottom: 1px solid var(--line); max-height: 40vh; }}
  }}
</style>
</head>
<body>
<div id="app">
  <aside>
    <h1>Note links</h1>
    <div class="meta">{meta.get("noteCount", 0)} notes · {meta.get("linkCount", 0)} links · {meta.get("orphanCount", 0)} orphans<br/>
      Labels from frontmatter <code>subtitle</code>; edges from markdown / wikilinks.
    </div>
    <div>
      <label for="q">Search</label>
      <input id="q" type="search" placeholder="subtitle, group, path…"/>
    </div>
    <div>
      <label for="track">Track filter</label>
      <select id="track"><option value="">All tracks</option></select>
    </div>
    <div class="row"><input type="checkbox" id="orphans" checked/><label for="orphans" style="margin:0">Show orphans</label></div>
    <div class="row"><input type="checkbox" id="labels" checked/><label for="labels" style="margin:0">Show labels</label></div>
    <div class="row">
      <button type="button" id="reset">Reset view</button>
      <button type="button" id="reheat">Reheat</button>
    </div>
    <div id="detail"><em>Click a note</em></div>
  </aside>
  <main>
    <canvas id="c"></canvas>
    <div class="hint">Drag canvas · scroll zoom · click node · drag node</div>
  </main>
</div>
<script id="graph-data" type="application/json">{data_json}</script>
<script>
(() => {{
  const DATA = JSON.parse(document.getElementById("graph-data").textContent);
  const canvas = document.getElementById("c");
  const ctx = canvas.getContext("2d");
  const detail = document.getElementById("detail");
  const q = document.getElementById("q");
  const trackSel = document.getElementById("track");
  const orphans = document.getElementById("orphans");
  const labels = document.getElementById("labels");

  const tracks = [...new Set(DATA.nodes.map(n => n.track).filter(Boolean))].sort();
  for (const t of tracks) {{
    const o = document.createElement("option");
    o.value = t; o.textContent = t;
    trackSel.appendChild(o);
  }}

  const palette = [
    "#0f766e","#b45309","#1d4ed8","#be123c","#7c3aed",
    "#047857","#c2410c","#0369a1","#a16207","#4f46e5",
    "#0e7490","#9f1239","#15803d","#854d0e","#6d28d9"
  ];
  const trackColor = {{}};
  tracks.forEach((t,i) => trackColor[t] = palette[i % palette.length]);

  let width = 0, height = 0, dpr = 1;
  let transform = {{ x: 0, y: 0, k: 1 }};
  let nodes = [], links = [];
  let simNodes = [], simLinks = [];
  let selected = null;
  let hover = null;
  let dragging = null;
  let panning = false;
  let lastPan = null;

  function resize() {{
    dpr = window.devicePixelRatio || 1;
    const rect = canvas.parentElement.getBoundingClientRect();
    width = rect.width; height = rect.height;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }}

  function matchesFilter(n) {{
    if (!orphans.checked && n.degree === 0) return false;
    if (trackSel.value && n.track !== trackSel.value) return false;
    const s = q.value.trim().toLowerCase();
    if (!s) return true;
    return [n.title, n.group, n.path, n.subtitle, n.label].filter(Boolean)
      .some(v => String(v).toLowerCase().includes(s));
  }}

  function rebuild() {{
    const visible = new Set(DATA.nodes.filter(matchesFilter).map(n => n.id));
    nodes = DATA.nodes.filter(n => visible.has(n.id));
    links = DATA.edges.filter(e => visible.has(e.source) && visible.has(e.target));
    const byId = Object.fromEntries(nodes.map(n => [n.id, n]));
    simNodes = nodes.map(n => ({{
      ...n,
      x: n.x ?? (Math.random() - .5) * 400,
      y: n.y ?? (Math.random() - .5) * 400,
      vx: 0, vy: 0,
      r: 4 + Math.min(10, Math.sqrt(n.degree || 0) * 1.8),
    }}));
    const simById = Object.fromEntries(simNodes.map(n => [n.id, n]));
    simLinks = links.map(e => ({{
      source: simById[e.source],
      target: simById[e.target],
      label: e.label,
    }})).filter(e => e.source && e.target);
    void byId;
  }}

  function tick() {{
    const alpha = 0.08;
    // repulsion
    for (let i = 0; i < simNodes.length; i++) {{
      for (let j = i + 1; j < simNodes.length; j++) {{
        const a = simNodes[i], b = simNodes[j];
        let dx = a.x - b.x, dy = a.y - b.y;
        let dist2 = dx*dx + dy*dy || 0.01;
        let dist = Math.sqrt(dist2);
        let force = 900 / dist2;
        let fx = dx / dist * force, fy = dy / dist * force;
        a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
      }}
    }}
    // springs
    for (const e of simLinks) {{
      const a = e.source, b = e.target;
      let dx = b.x - a.x, dy = b.y - a.y;
      let dist = Math.sqrt(dx*dx + dy*dy) || 0.01;
      let desired = 90;
      let force = (dist - desired) * 0.02;
      let fx = dx / dist * force, fy = dy / dist * force;
      a.vx += fx; a.vy += fy; b.vx -= fx; b.vy -= fy;
    }}
    // center gravity
    for (const n of simNodes) {{
      if (n === dragging) continue;
      n.vx += -n.x * 0.002;
      n.vy += -n.y * 0.002;
      n.vx *= 0.85; n.vy *= 0.85;
      n.x += n.vx * alpha * 12;
      n.y += n.vy * alpha * 12;
    }}
  }}

  function screenToWorld(sx, sy) {{
    return {{
      x: (sx - transform.x) / transform.k,
      y: (sy - transform.y) / transform.k,
    }};
  }}

  function findNode(sx, sy) {{
    const w = screenToWorld(sx, sy);
    let best = null, bestD = Infinity;
    for (const n of simNodes) {{
      const dx = n.x - w.x, dy = n.y - w.y;
      const d = Math.sqrt(dx*dx + dy*dy);
      if (d < n.r + 6 / transform.k && d < bestD) {{ best = n; bestD = d; }}
    }}
    return best;
  }}

  function draw() {{
    ctx.clearRect(0, 0, width, height);
    ctx.save();
    ctx.translate(transform.x, transform.y);
    ctx.scale(transform.k, transform.k);

    const neighbor = new Set();
    if (selected) {{
      neighbor.add(selected.id);
      for (const e of simLinks) {{
        if (e.source.id === selected.id) neighbor.add(e.target.id);
        if (e.target.id === selected.id) neighbor.add(e.source.id);
      }}
    }}

    for (const e of simLinks) {{
      const dim = selected && !(neighbor.has(e.source.id) && neighbor.has(e.target.id));
      ctx.beginPath();
      ctx.moveTo(e.source.x, e.source.y);
      ctx.lineTo(e.target.x, e.target.y);
      ctx.strokeStyle = dim ? "rgba(120,113,108,.12)" : "rgba(68,64,60,.35)";
      ctx.lineWidth = (selected && !dim ? 1.6 : 1) / transform.k;
      ctx.stroke();
    }}

    for (const n of simNodes) {{
      const dim = selected && !neighbor.has(n.id);
      const isSel = selected && selected.id === n.id;
      const isHover = hover && hover.id === n.id;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = dim ? "rgba(168,162,158,.35)" : (trackColor[n.track] || "#57534e");
      ctx.fill();
      if (isSel || isHover) {{
        ctx.strokeStyle = "#1c1917";
        ctx.lineWidth = 2 / transform.k;
        ctx.stroke();
      }}
      if (labels.checked && (transform.k > 0.7 || isSel || isHover || n.degree >= 4)) {{
        ctx.fillStyle = dim ? "rgba(120,113,108,.5)" : "#1c1917";
        ctx.font = `${{12 / transform.k}}px "IBM Plex Sans", sans-serif`;
        ctx.fillText(n.title, n.x + n.r + 4 / transform.k, n.y + 4 / transform.k);
      }}
    }}
    ctx.restore();
  }}

  function showDetail(n) {{
    if (!n) {{ detail.innerHTML = "<em>Click a note</em>"; return; }}
    detail.innerHTML = `<strong>${{escapeHtml(n.title)}}</strong>
      <div>${{escapeHtml(n.group || "")}} · track <code>${{escapeHtml(n.track || "")}}</code></div>
      <div>degree ${{n.degree}} · order ${{n.order ?? "—"}}</div>
      <code>${{escapeHtml(n.path)}}</code>`;
  }}
  function escapeHtml(s) {{
    return String(s).replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;","\\"":"&quot;","'":"&#39;"}}[c]));
  }}

  function loop() {{
    tick();
    draw();
    requestAnimationFrame(loop);
  }}

  canvas.addEventListener("wheel", (ev) => {{
    ev.preventDefault();
    const rect = canvas.getBoundingClientRect();
    const sx = ev.clientX - rect.left, sy = ev.clientY - rect.top;
    const before = screenToWorld(sx, sy);
    const factor = Math.exp(-ev.deltaY * 0.0015);
    transform.k = Math.min(4, Math.max(0.15, transform.k * factor));
    transform.x = sx - before.x * transform.k;
    transform.y = sy - before.y * transform.k;
  }}, {{ passive: false }});

  canvas.addEventListener("pointerdown", (ev) => {{
    const rect = canvas.getBoundingClientRect();
    const sx = ev.clientX - rect.left, sy = ev.clientY - rect.top;
    const hit = findNode(sx, sy);
    if (hit) {{
      dragging = hit;
      selected = hit;
      showDetail(hit);
      canvas.setPointerCapture(ev.pointerId);
    }} else {{
      panning = true;
      lastPan = {{ x: ev.clientX, y: ev.clientY }};
      canvas.classList.add("dragging");
      canvas.setPointerCapture(ev.pointerId);
    }}
  }});
  canvas.addEventListener("pointermove", (ev) => {{
    const rect = canvas.getBoundingClientRect();
    const sx = ev.clientX - rect.left, sy = ev.clientY - rect.top;
    if (dragging) {{
      const w = screenToWorld(sx, sy);
      dragging.x = w.x; dragging.y = w.y;
      dragging.vx = 0; dragging.vy = 0;
    }} else if (panning && lastPan) {{
      transform.x += ev.clientX - lastPan.x;
      transform.y += ev.clientY - lastPan.y;
      lastPan = {{ x: ev.clientX, y: ev.clientY }};
    }} else {{
      hover = findNode(sx, sy);
    }}
  }});
  canvas.addEventListener("pointerup", () => {{
    dragging = null; panning = false; lastPan = null;
    canvas.classList.remove("dragging");
  }});

  function resetView() {{
    transform = {{ x: width / 2, y: height / 2, k: 0.85 }};
  }}

  document.getElementById("reset").onclick = resetView;
  document.getElementById("reheat").onclick = () => {{
    for (const n of simNodes) {{ n.vx += (Math.random()-.5)*8; n.vy += (Math.random()-.5)*8; }}
  }};
  for (const el of [q, trackSel, orphans, labels]) {{
    el.addEventListener("input", () => {{ rebuild(); }});
    el.addEventListener("change", () => {{ rebuild(); }});
  }}

  window.addEventListener("resize", () => {{ resize(); }});
  resize();
  rebuild();
  resetView();
  loop();
}})();
</script>
</body>
</html>
"""
    path.write_text(doc, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Build content note-link graph JSON / Obsidian-style HTML "
            "(nodes use frontmatter subtitle; edges from markdown + wikilinks)."
        ),
    )
    parser.add_argument(
        "--format",
        choices=("graph", "clusters", "both", "html"),
        default="both",
        help="Output format (default: both JSON formats)",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Also write interactive note-links HTML (implied by --format html)",
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
        "--html-output",
        type=Path,
        default=DEFAULT_HTML_OUTPUT,
        help="HTML graph output path",
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
    want_html = args.html or args.format == "html"

    if args.format in ("graph", "both"):
        write_json(args.output, graph, args.indent)
        m = graph["meta"]
        print(
            f"Wrote {args.output.relative_to(REPO_ROOT)} — "
            f"{m['nodeCount']} nodes, {m['edgeCount']} edges "
            f"({m['linkEdgeCount']} note links)"
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

    if want_html:
        payload = build_note_links_payload(graph)
        write_note_links_html(args.html_output, payload)
        note_json = args.html_output.with_suffix(".json")
        write_json(note_json, payload, args.indent)
        m = payload["meta"]
        print(
            f"Wrote {args.html_output.relative_to(REPO_ROOT)} — "
            f"{m['noteCount']} notes, {m['linkCount']} links "
            f"({m['orphanCount']} orphans)"
        )
        print(f"Wrote {note_json.relative_to(REPO_ROOT)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
