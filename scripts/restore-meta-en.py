#!/usr/bin/env python3
"""Restore English labels in _meta.json from a pre-translation git commit."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

CONTENT_ROOT = Path(__file__).resolve().parent.parent / "src" / "content"
SOURCE_COMMIT = "77294ec^"
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u9fff]")

# Labels for paths added after SOURCE_COMMIT or renamed folders.
FALLBACK_LABELS: dict[str, str] = {
    "_meta.json": "Notes",
    "ai101/_meta.json": "AI",
    "ai101/machine-learning/_meta.json": "Machine learning",
    "CS101/_meta.json": "CS101",
    "CS101/algorithms/_meta.json": "Algorithms",
    "CS101/data-structures/_meta.json": "Data structures",
    "CS101/databases/_meta.json": "Databases",
    "CS101/networking/_meta.json": "Networking",
    "getting-started/_meta.json": "Getting started",
    "getting-started/intro/_meta.json": "Intro",
    "sre101/_meta.json": "SRE",
    "sre101/cicd/_meta.json": "CI/CD",
    "sre101/cicd/ansible-and-jenkins/_meta.json": "Ansible and Jenkins",
    "sre101/cicd/security-and-best-practices/_meta.json": "Security and best practices",
    "sre101/cicd/terraform/_meta.json": "Terraform",
    "sre101/cicd/tools-and-platforms/_meta.json": "Tools and platforms",
    "sre101/cloud-architecture/_meta.json": "Cloud architecture",
    "sre101/cloud-architecture/foundations/_meta.json": "Foundations",
    "sre101/cloud-architecture/patterns-and-design/_meta.json": "Patterns and design",
    "sre101/tooling/_meta.json": "Tooling",
    "sre101/tooling/alertmanager/_meta.json": "Alertmanager",
    "sre101/tooling/grafana/_meta.json": "Grafana",
    "sre101/tooling/kubernetes/_meta.json": "Kubernetes",
    "sre101/tooling/prometheus/_meta.json": "Prometheus",
    "sre101/tooling/terraform/_meta.json": "Terraform",
    "startups/_meta.json": "Startups",
    "startups/free-services/_meta.json": "Free services",
    "swe101/_meta.json": "SWE101",
    "swe101/api-gateway/_meta.json": "API Gateway",
    "swe101/cdn/_meta.json": "CDN",
    "swe101/git/_meta.json": "Git",
    "swe101/git/essentials/_meta.json": "Essentials",
    "swe101/git/github/_meta.json": "GitHub",
    "swe101/java/_meta.json": "Java",
    "swe101/java/intro/_meta.json": "Intro",
    "swe101/java/springboot/_meta.json": "Spring Boot",
    "swe101/mongodb/_meta.json": "MongoDB",
    "swe101/plsql/_meta.json": "PL/SQL",
    "swe101/plantuml/_meta.json": "PlantUML",
    "swe101/postgres/_meta.json": "Postgres",
    "swe101/python/_meta.json": "Python",
    "swe101/redis/_meta.json": "Redis",
    "swe101/rust/_meta.json": "Rust",
    "swe101/sysdesign/_meta.json": "System design",
    "swe101/sysdesign/bottleneck-analysis/_meta.json": "Bottleneck analysis",
    "swe101/sysdesign/classic-designs/_meta.json": "Classic designs",
    "swe101/sysdesign/scalable-patterns/_meta.json": "Scalable patterns",
}


def git_show(commit: str, path: str) -> str | None:
    for candidate in (path, path.replace("CS101/", "cs101/")):
        try:
            return subprocess.check_output(
                ["git", "show", f"{commit}:{candidate}"],
                stderr=subprocess.DEVNULL,
                text=True,
                encoding="utf-8",
            )
        except subprocess.CalledProcessError:
            continue
    return None


def label_from_path(rel_posix: str) -> str:
    name = Path(rel_posix).parent.name
    words = name.replace("-", " ").split()
    acronyms = {"cdn", "sql", "api", "sre", "ci", "cd", "jpa"}
    parts: list[str] = []
    for word in words:
        lower = word.lower()
        if lower in acronyms or word.isupper():
            parts.append(word.upper() if lower == "cdn" else word.title())
        else:
            parts.append(word.title())
    return " ".join(parts)


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    updated = 0

    for path in sorted(CONTENT_ROOT.rglob("_meta.json")):
        rel = path.relative_to(CONTENT_ROOT).as_posix()
        git_path = f"src/content/{rel}"
        data = json.loads(path.read_text(encoding="utf-8"))
        label = data.get("label", "")
        if not isinstance(label, str) or not CJK_RE.search(label):
            continue

        new_label: str | None = None
        raw = git_show(SOURCE_COMMIT, git_path)
        if raw:
            old = json.loads(raw)
            candidate = old.get("label", "")
            if isinstance(candidate, str) and candidate and not CJK_RE.search(candidate):
                new_label = candidate

        if not new_label:
            new_label = FALLBACK_LABELS.get(rel) or label_from_path(rel)

        if new_label == label:
            continue

        data["label"] = new_label
        new_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        print(f"{rel}: {label!r} -> {new_label!r}")
        updated += 1
        if not dry_run:
            path.write_text(new_text, encoding="utf-8")

    print(f"Done. Updated {updated} file(s). dry_run={dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
