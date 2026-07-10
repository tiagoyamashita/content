"""Scan staged files for .env and obvious secrets."""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field


SECRET_RE = re.compile(
    r"(api[_-]?key|secret|password|private[_-]?key)\s*[:=]\s*['\"][a-zA-Z0-9_\-]{8,}",
    re.IGNORECASE,
)


@dataclass
class ScanResult:
    findings: list[str] = field(default_factory=list)

    @property
    def blocked(self) -> bool:
        return bool(self.findings)

    def add(self, message: str) -> None:
        self.findings.append(message)


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    ).stdout


def scan_staged() -> ScanResult:
    result = ScanResult()
    names = _git("diff", "--cached", "--name-only").splitlines()

    for name in names:
        if re.search(r"\.env(\.|$)", name):
            result.add(f"STAGED_ENV_FILE: {name}")
        if name == ".env":
            result.add("DOT_ENV_IN_COMMIT")

    diff = _git("diff", "--cached", "-U0")
    if SECRET_RE.search(diff):
        result.add("POSSIBLE_SECRET_IN_STAGED_DIFF")

    return result
