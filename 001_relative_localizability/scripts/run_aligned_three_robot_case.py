#!/usr/bin/env python3
"""Run the aligned three-follower simulation described in the repository docs."""

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
from src.solver import run_aligned_experiment, write_metrics
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
    "seed": 7,
    "condition_number_max": 1.0e8,
    "frame_orientations": {"i": 0.0, "j": 0.0, "m": 0.0},
    "angle_noise_std": 0.0,
    "displacement_noise_std": 0.0,
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
        default=ROOT / "configs" / "aligned_three_robot_case.yaml",
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
    result = run_aligned_experiment(
        measurements,
        condition_number_max=config["condition_number_max"],
    )

    figures_dir = ROOT / "results" / "figures"
    logs_dir = ROOT / "results" / "logs"

    plot_trajectories(measurements.positions_global, figures_dir / "three_robot_trajectories.png")
    plot_relative_position_estimation(
        result.times,
        result.ground_truth_pmi,
        result.estimated_pmi,
        figures_dir / "relative_position_estimation.png",
        title="Estimated Relative Position p_mi",
    )
    error_series = np.column_stack(
        [
            np.linalg.norm(result.estimated_pmi - result.ground_truth_pmi, axis=1),
            np.linalg.norm(result.estimated_pji - result.ground_truth_pji, axis=1),
        ]
    )
    plot_error_curve(
        result.times,
        error_series,
        figures_dir / "relative_position_error.png",
        title="Relative Position Error",
        ylabel="error norm",
        legend_labels=["p_mi error", "p_ji error"],
    )
    plot_condition_numbers(result.times, result.condition_numbers, figures_dir / "condition_number_b1.png")

    metrics = {
        "rmse_pmi": result.rmse_pmi,
        "rmse_pji": result.rmse_pji,
        "valid_windows": int(result.valid_mask.sum()),
        "total_windows": int(result.valid_mask.size),
    }
    write_metrics(logs_dir / "aligned_metrics.json", metrics)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
