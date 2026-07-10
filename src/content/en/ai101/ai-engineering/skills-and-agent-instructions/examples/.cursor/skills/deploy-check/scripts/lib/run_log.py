from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_path(log_dir: Path, prefix: str = "run") -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    return log_dir / f"{prefix}-{stamp}.json"


def write_log(
    log_file: Path,
    *,
    script: str,
    started_at: str,
    duration_ms: int,
    exit_code: int,
    parameters: dict[str, Any],
    results: dict[str, Any],
    messages: list[str],
) -> Path:
    payload = {
        "script": script,
        "started_at": started_at,
        "finished_at": utc_now(),
        "duration_ms": duration_ms,
        "exit_code": exit_code,
        "parameters": parameters,
        "results": results,
        "messages": messages,
        "log_file": str(log_file),
    }
    log_file.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Log written: {log_file}")
    print(json.dumps(payload, indent=2))
    return log_file


class Timer:
    def __init__(self) -> None:
        self.started_at = utc_now()
        self._t0 = perf_counter()

    @property
    def duration_ms(self) -> int:
        return int((perf_counter() - self._t0) * 1000)
