#!/usr/bin/env python3
"""Run the unaligned three-follower simulation and robust refinement experiment."""

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
from src.simulator import build_default_scenario
from src.solver import run_unaligned_experiment, write_metrics
from src.visualization import (
    plot_condition_numbers,
    plot_error_curve,
    plot_relative_position_estimation,
    plot_trajectories,
)

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency at runtime
    yaml = None


DEFAULT_CONFIG = {
    "num_steps": 90,
    "dt": 0.1,
    "seed": 13,
    "angle_noise_std": 0.003,
    "displacement_noise_std": 0.002,
    "direct_window_instants": 4,
    "robust_window_instants": 6,
    "frame_orientations": {"i": 0.0, "j": 0.55, "m": -0.82},
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
        default=ROOT / "configs" / "unaligned_three_robot_case.yaml",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    scenario = build_default_scenario(
        num_steps=config["num_steps"],
        dt=config["dt"],
        seed=config["seed"],
        frame_orientations=config["frame_orientations"],
    )
    measurements = build_measurements(
        scenario,
        angle_noise_std=config["angle_noise_std"],
        displacement_noise_std=config["displacement_noise_std"],
        seed=config["seed"] + 1,
    )
    result = run_unaligned_experiment(
        measurements,
        direct_window_instants=config["direct_window_instants"],
        robust_window_instants=config["robust_window_instants"],
    )

    figures_dir = ROOT / "results" / "figures"
    logs_dir = ROOT / "results" / "logs"

    plot_trajectories(measurements.positions_global, figures_dir / "three_robot_trajectories_unaligned.png")
    plot_relative_position_estimation(
        result.times,
        result.ground_truth_pmi,
        result.robust_estimated_pmi,
        figures_dir / "relative_position_estimation_unaligned.png",
        title="Estimated Relative Position p_mi (Unaligned, Robust)",
    )
    position_error = np.column_stack(
        [
            np.linalg.norm(result.estimated_pmi - result.ground_truth_pmi, axis=1),
            np.linalg.norm(result.robust_estimated_pmi - result.ground_truth_pmi, axis=1),
        ]
    )
    plot_error_curve(
        result.times,
        position_error,
        figures_dir / "relative_position_error_unaligned.png",
        title="Linear vs Robust Position Error",
        ylabel="error norm",
        legend_labels=["linear", "robust"],
    )
    orientation_error = np.column_stack(
        [
            [np.linalg.norm(result.estimated_rmi[idx] - result.ground_truth_rmi[idx]) for idx in range(len(result.times))],
            [np.linalg.norm(result.robust_estimated_rmi[idx] - result.ground_truth_rmi[idx]) for idx in range(len(result.times))],
        ]
    )
    plot_error_curve(
        result.times,
        orientation_error,
        figures_dir / "relative_orientation_error.png",
        title="Relative Orientation Error r_mi",
        ylabel="vector error",
        legend_labels=["linear", "robust"],
    )
    plot_condition_numbers(result.times, result.condition_numbers, figures_dir / "condition_number_b4.png")

    metrics = {
        "linear_position_rmse": result.linear_position_rmse,
        "robust_position_rmse": result.robust_position_rmse,
        "linear_orientation_rmse": result.linear_orientation_rmse,
        "robust_orientation_rmse": result.robust_orientation_rmse,
    }
    write_metrics(logs_dir / "unaligned_metrics.json", metrics)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
