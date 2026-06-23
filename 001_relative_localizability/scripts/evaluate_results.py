#!/usr/bin/env python3
"""Aggregate saved metrics into a compact experiment summary."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOGS_DIR = ROOT / "results" / "logs"


def load_metrics(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> None:
    summary = {
        "aligned": load_metrics(LOGS_DIR / "aligned_metrics.json"),
        "unaligned": load_metrics(LOGS_DIR / "unaligned_metrics.json"),
        "noise_robustness": load_metrics(LOGS_DIR / "noise_robustness_metrics.json"),
        "general_topology": load_metrics(LOGS_DIR / "general_topology_metrics.json"),
    }
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
