#!/usr/bin/env python3
"""Run a simplified mixed follower-leader-landmark stage-5 experiment."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.measurements import build_measurements
from src.simulator import build_mixed_topology_scenario
from src.solver import run_mixed_topology_experiment, write_metrics
from src.visualization import plot_error_curve, plot_trajectories

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency at runtime
    yaml = None


DEFAULT_CONFIG = {
    "num_steps": 90,
    "dt": 0.1,
    "seed": 31,
    "angle_noise_std": 0.001,
    "displacement_noise_std": 0.001,
    "condition_number_max": 1.0e8,
}


def load_config(path: Path) -> dict:
    if yaml is None:
        raise RuntimeError("PyYAML is required to read the YAML config files.")
    with path.open("r", encoding="utf-8") as handle:
        loaded = yaml.safe_load(handle) or {}
    merged = DEFAULT_CONFIG.copy()
    merged.update(loaded)
    return merged


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "general_topology_case.yaml",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    scenario = build_mixed_topology_scenario(
        num_steps=config["num_steps"],
        dt=config["dt"],
        seed=config["seed"],
    )
    measurements = build_measurements(
        scenario,
        angle_noise_std=config["angle_noise_std"],
        displacement_noise_std=config["displacement_noise_std"],
        seed=config["seed"] + 1,
    )
    result = run_mixed_topology_experiment(
        measurements,
        condition_number_max=config["condition_number_max"],
    )

    figures_dir = ROOT / "results" / "figures"
    logs_dir = ROOT / "results" / "logs"

    all_positions = dict(measurements.positions_global)
    all_positions.update(measurements.landmarks_global)
    all_positions.update(measurements.leaders_global)
    plot_trajectories(all_positions, figures_dir / "mixed_agent_topology.png")

    error_curve = np.column_stack(
        [
            np.linalg.norm(result.estimated_pAi - result.ground_truth_pAi, axis=1),
            np.linalg.norm(result.estimated_pLi - result.ground_truth_pLi, axis=1),
        ]
    )
    plot_error_curve(
        result.times,
        error_curve,
        figures_dir / "general_topology_localization_error.png",
        title="General Topology Localization Error",
        ylabel="error norm",
        legend_labels=["landmark", "leader"],
    )

    metrics = {
        "rmse_landmark": result.rmse_landmark,
        "rmse_leader": result.rmse_leader,
        "localizability_flags": result.localizability_flags,
    }
    write_metrics(logs_dir / "general_topology_metrics.json", metrics)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
