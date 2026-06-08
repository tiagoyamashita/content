#!/usr/bin/env python3
"""One-off: create ai-applied submenu structure from using-ai flat files."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

GROUP = "AI Applied"

SUBMENUS: list[tuple[str, str, int, list[tuple[str, str, str]]]] = [
    # (folder, label, order, [(filename, subtitle, source_section_keys or 'all')])
    (
        "effective-prompting",
        "Effective prompting",
        2,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-minimum-prompt-and-techniques.md", "Minimum prompt & techniques", "1-2"),
            ("iii-iteration-and-templates.md", "Iteration & templates", "3-4"),
            ("iv-system-instructions-and-mistakes.md", "System instructions & mistakes", "5-7"),
        ],
    ),
    (
        "agents-and-agentic-workflows",
        "Agents & agentic workflows",
        3,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-chat-assistant-agent.md", "Chat, assistant & agent", "1-2"),
            ("iii-directing-agents.md", "Directing agents", "3-4"),
            ("iv-products-and-human-in-the-loop.md", "Products & human-in-the-loop", "5-7"),
        ],
    ),
    (
        "tools-and-orchestration",
        "Tools & orchestration",
        4,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-tool-map-and-patterns.md", "Tool map", "1"),
            ("iii-orchestration-patterns.md", "Orchestration patterns", "2"),
            ("iv-connectors-models-and-teams.md", "Connectors, models & teams", "3-4"),
            ("v-antipatterns-and-rehearsal.md", "Anti-patterns & rehearsal", "5-6"),
        ],
    ),
    (
        "custom-assistants-and-knowledge",
        "Custom assistants & knowledge",
        5,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-products-and-building-assistants.md", "Products & building assistants", "1-3"),
            ("iii-rag-and-knowledge-libraries.md", "RAG & knowledge libraries", "4-5"),
            ("iv-memory-and-governance.md", "Memory & governance", "6-7"),
        ],
    ),
    (
        "multimodal-and-files",
        "Multimodal & files",
        6,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-pdfs-and-documents.md", "PDFs & documents", "2"),
            ("iii-images-spreadsheets-data.md", "Images, spreadsheets & data", "3-4"),
            ("iv-voice-code-and-limits.md", "Voice, code & limits", "5-7"),
        ],
    ),
    (
        "trust-privacy-and-verify",
        "Trust, privacy & verify",
        7,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-hallucinations-and-verification.md", "Hallucinations & verification", "1,4"),
            ("iii-privacy-enterprise-data.md", "Privacy & enterprise data", "2-3"),
            ("iv-agents-injection-limits.md", "Agents, injection & limits", "5-9"),
        ],
    ),
    (
        "skills-and-agent-instructions",
        "Skills & agent instructions",
        8,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-artifacts-why-and-what.md", "Artifacts & why bother", "1-2"),
            ("iii-cross-tool-portable-setup.md", "Cross-tool portable setup", "3"),
            ("iv-cursor-skills-rules-agents-md.md", "Cursor skills, rules & AGENTS.md", "4-6"),
            ("v-writing-and-maintaining-skills.md", "Writing & maintaining skills", "7-12"),
        ],
    ),
    (
        "how-mcp-works",
        "How MCP works",
        9,
        [
            ("i-overview.md", "Overview", "map"),
            ("ii-json-rpc-and-transports.md", "JSON-RPC & transports", "1-4"),
            ("iii-end-to-end-flow-and-llm.md", "End-to-end flow & LLM", "5-7"),
            ("iv-mcp-vs-connectors-and-security.md", "MCP vs connectors & security", "8-9"),
            ("v-vector-db-skills-and-reference.md", "Vector DB, skills & reference", "10-12"),
        ],
    ),
]

OLD_FILES = {
    "effective-prompting": "ii-effective-prompting.md",
    "agents-and-agentic-workflows": "iii-agents-and-agentic-workflows.md",
    "tools-and-orchestration": "iv-tools-and-orchestration.md",
    "custom-assistants-and-knowledge": "v-custom-assistants-and-knowledge.md",
    "multimodal-and-files": "vi-multimodal-and-files.md",
    "trust-privacy-and-verify": "vii-trust-privacy-and-verify.md",
    "skills-and-agent-instructions": "viii-skills-and-agent-instructions.md",
    "how-mcp-works": "ix-how-mcp-works.md",
}

SECTION_RE = re.compile(r"^## (.+)$", re.MULTILINE)


def parse_sections(text: str) -> dict[int, str]:
    """Split body by numbered ## N. headers."""
    body = text.split("---", 2)[2] if text.count("---") >= 2 else text
    matches = list(SECTION_RE.finditer(body))
    sections: dict[int, str] = {}
    for i, m in enumerate(matches):
        num_m = re.match(r"(\d+)\.", m.group(1))
        if not num_m:
            continue
        num = int(num_m.group(1))
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sections[num] = body[start:end].strip()
    return sections


def section_range(sections: dict[int, str], spec: str, title: str) -> str:
    if spec == "map":
        return ""
    nums: list[int] = []
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-", 1)
            nums.extend(range(int(a), int(b) + 1))
        elif "," in part:
            nums.extend(int(x.strip()) for x in part.split(","))
        else:
            nums.append(int(part))
    chunks = [sections[n] for n in sorted(nums) if n in sections]
    return "\n\n".join(chunks)


def make_frontmatter(label: str, subtitle: str, order: int) -> str:
    return f"""---
label: "{label}"
subtitle: "{subtitle}"
group: "{GROUP}"
order: {order}
---
"""


def rel_link(old_name: str, new_folder: str, new_file: str) -> str:
    """Map old sibling links to new paths."""
    mapping = {
        "ii-effective-prompting.md": "effective-prompting/i-overview.md",
        "iii-agents-and-agentic-workflows.md": "agents-and-agentic-workflows/i-overview.md",
        "iv-tools-and-orchestration.md": "tools-and-orchestration/i-overview.md",
        "v-custom-assistants-and-knowledge.md": "custom-assistants-and-knowledge/i-overview.md",
        "vi-multimodal-and-files.md": "multimodal-and-files/i-overview.md",
        "vii-trust-privacy-and-verify.md": "trust-privacy-and-verify/i-overview.md",
        "viii-skills-and-agent-instructions.md": "skills-and-agent-instructions/i-overview.md",
        "ix-how-mcp-works.md": "how-mcp-works/i-overview.md",
    }
    for old, new_path in mapping.items():
        old_name = old_name.replace(old, new_path)
    return old_name


def fix_links(content: str, current_folder: str) -> str:
    for old, new_path in {
        "ii-effective-prompting.md": "../effective-prompting/i-overview.md",
        "iii-agents-and-agentic-workflows.md": "../agents-and-agentic-workflows/i-overview.md",
        "iv-tools-and-orchestration.md": "../tools-and-orchestration/i-overview.md",
        "v-custom-assistants-and-knowledge.md": "../custom-assistants-and-knowledge/i-overview.md",
        "vi-multimodal-and-files.md": "../multimodal-and-files/i-overview.md",
        "vii-trust-privacy-and-verify.md": "../trust-privacy-and-verify/i-overview.md",
        "viii-skills-and-agent-instructions.md": "../skills-and-agent-instructions/i-overview.md",
        "ix-how-mcp-works.md": "../how-mcp-works/i-overview.md",
    }.items():
        content = content.replace(f"]({old})", f"]({new_path})")
        content = content.replace(f"](../using-ai/{old})", f"]({new_path})")
    content = content.replace('group: "Using AI"', f'group: "{GROUP}"')
    return content


def overview_for_submenu(folder: str, label: str, files: list[tuple[str, str, str]], source: str) -> str:
    lines = [
        make_frontmatter("I", "Overview", 1).strip(),
        f"{label} — overview",
        f"Deep dive on **{label.lower()}** — split into focused notes below.",
        "",
        "## Map of this submenu",
        "",
        "| Note | Focus |",
        "|------|--------|",
    ]
    for fn, sub, _ in files:
        if fn == "i-overview.md":
            continue
        slug = fn.replace(".md", "")
        lines.append(f"| [{sub}]({fn}) | Part of {label.lower()} track |")
    lines.append("")
    # intro paragraph from source first section before ## 1
    body = source.split("---", 2)[2] if source.count("---") >= 2 else source
    title_line, _, rest = body.partition("\n")
    intro = rest.split("## 1.")[0].strip()
    if intro:
        lines.append(intro)
        lines.append("")
    lines.append("## Study order")
    lines.append("")
    order_parts = [f"[{sub}]({fn})" for fn, sub, _ in files if fn != "i-overview.md"]
    lines.append(" → ".join(order_parts))
    return "\n".join(lines) + "\n"


def migrate_lang(lang: str) -> None:
    base = REPO / "src" / "content" / lang / "ai101"
    EN = base / "ai-applied"
    OLD = base / "using-ai"
    en_old = REPO / "src" / "content" / "en" / "ai101" / "using-ai"

    EN.mkdir(parents=True, exist_ok=True)
    (EN / "_meta.json").write_text(
        json.dumps({"label": "AI Applied", "order": 4}, indent=2) + "\n",
        encoding="utf-8",
    )

    for folder, label, order, files in SUBMENUS:
        sf = EN / folder
        sf.mkdir(parents=True, exist_ok=True)
        (sf / "_meta.json").write_text(
            json.dumps({"label": label, "order": order}, indent=2) + "\n",
            encoding="utf-8",
        )
        src_path = OLD / OLD_FILES[folder]
        if not src_path.exists() and folder == "how-mcp-works":
            src_path = en_old / OLD_FILES[folder]
        if not src_path.exists():
            src_path = REPO / "src" / "content" / "en" / "ai101" / "ai-applied" / folder / "i-overview.md"
            # fallback: copy en subtree
            en_sub = REPO / "src" / "content" / "en" / "ai101" / "ai-applied" / folder
            if en_sub.exists():
                import shutil
                if sf.exists():
                    shutil.rmtree(sf)
                shutil.copytree(en_sub, sf)
                continue
        source = src_path.read_text(encoding="utf-8")
        sections = parse_sections(source)

        for idx, (fn, subtitle, spec) in enumerate(files):
            roman = ["I", "II", "III", "IV", "V", "VI"][idx] if idx < 6 else str(idx + 1)
            if fn == "i-overview.md":
                content = overview_for_submenu(folder, label, files, source)
            else:
                body = section_range(sections, spec, subtitle)
                title = source.split("---", 2)[2].strip().split("\n")[0]
                content = make_frontmatter(roman, subtitle, idx + 1) + f"{subtitle}\n\n" + body
                content = fix_links(content, folder)
            (sf / fn).write_text(content, encoding="utf-8")

    # Root overview
    root_src = OLD / "i-overview.md"
    if not root_src.exists():
        root_src = REPO / "src" / "content" / "en" / "ai101" / "ai-applied" / "i-overview.md"
    root_overview = root_src.read_text(encoding="utf-8")
    root_overview = root_overview.replace('group: "Using AI"', f'group: "{GROUP}"')
    root_overview = root_overview.replace("Using AI — overview", "AI Applied — overview")
    root_overview = root_overview.replace("Using AI — 概要", "AI Applied — 概要")
    root_overview = fix_links(root_overview, "")
    # Update map table
    map_block = """## Map of this submenu

| Part | Topic |
|------|--------|
| **I — Overview** | Who this is for, mental model, pick your path |
| **[Effective prompting](effective-prompting/i-overview.md)** | Prompt structure, techniques, templates |
| **[Agents & agentic workflows](agents-and-agentic-workflows/i-overview.md)** | Multi-step AI, tools, guardrails |
| **[Tools & orchestration](tools-and-orchestration/i-overview.md)** | Chat apps, IDE agents, automations, MCP intro |
| **[Custom assistants & knowledge](custom-assistants-and-knowledge/i-overview.md)** | Projects, custom GPTs, RAG for users |
| **[Multimodal & files](multimodal-and-files/i-overview.md)** | PDFs, images, spreadsheets, voice |
| **[Trust, privacy & verify](trust-privacy-and-verify/i-overview.md)** | Hallucinations, sensitive data, fact-checking |
| **[Skills & agent instructions](skills-and-agent-instructions/i-overview.md)** | `SKILL.md`, rules, `AGENTS.md` |
| **[How MCP works](how-mcp-works/i-overview.md)** | JSON-RPC, stdio vs HTTP, vector DB vs MCP |
"""
    root_overview = re.sub(
        r"## Map of this submenu\n\n.*?(?=\n## Mental model)",
        map_block + "\n",
        root_overview,
        flags=re.DOTALL,
    )
    (EN / "i-overview.md").write_text(root_overview, encoding="utf-8")
    print("Created", EN)


def main() -> None:
    for lang in ("en", "jp"):
        migrate_lang(lang)


if __name__ == "__main__":
    main()
