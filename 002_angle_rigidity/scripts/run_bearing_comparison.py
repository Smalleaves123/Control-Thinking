#!/usr/bin/env python3
"""Run the bearing-control comparison used in the simulation section."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.control import bearing_control_input, paper_five_agent_spec, simulate
from src.geometry import bearing
from src.visualization import plot_error_series, plot_formation_trajectory


def bearing_errors(trajectory: np.ndarray, edges: list[tuple[int, int]], desired: dict[tuple[int, int], np.ndarray]) -> np.ndarray:
    rows = []
    for frame in trajectory:
        rows.append([np.linalg.norm(bearing(frame, i, j) - desired[(i, j)]) for i, j in edges])
    return np.asarray(rows, dtype=float)


def run_case(config: dict, *, misaligned: bool) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    spec = paper_five_agent_spec()
    rotations = None
    if misaligned:
        rotations = {int(config["misaligned_agent"]) - 1: np.deg2rad(float(config["misalignment_degrees"]))}

    def controller(positions: np.ndarray) -> np.ndarray:
        return bearing_control_input(
            positions,
            spec.bearing_edges,
            spec.desired_bearings,
            gain=float(config["gain"]),
            local_frame_rotations=rotations,
        )

    trajectory = simulate(spec.initial_positions, controller, dt=float(config["dt"]), steps=int(config["steps"]))
    errors = bearing_errors(trajectory, spec.bearing_edges, spec.desired_bearings)
    metrics = {
        "final_bearing_rmse": float(np.sqrt(np.mean(errors[-1] ** 2))),
        "final_max_bearing_error": float(np.max(errors[-1])),
    }
    return trajectory, errors, metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "bearing_comparison.yaml")
    args = parser.parse_args()

    with args.config.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    figures_dir = ROOT / "results" / "figures"
    logs_dir = ROOT / "results" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    times = np.arange(int(config["steps"]) + 1) * float(config["dt"])

    outputs = {}
    for label, misaligned in [("no_misalignment", False), ("with_misalignment", True)]:
        trajectory, errors, metrics = run_case(config, misaligned=misaligned)
        outputs[label] = metrics
        plot_formation_trajectory(
            trajectory,
            figures_dir / f"bearing_control_{label}_trajectory.png",
            title=f"Bearing-Based Control ({label.replace('_', ' ')})",
        )
        plot_error_series(
            times,
            errors,
            figures_dir / f"bearing_control_{label}_errors.png",
            title=f"Bearing Errors ({label.replace('_', ' ')})",
            ylabel="bearing error norm",
        )

    with (logs_dir / "bearing_comparison_metrics.json").open("w", encoding="utf-8") as handle:
        json.dump(outputs, handle, indent=2)
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
