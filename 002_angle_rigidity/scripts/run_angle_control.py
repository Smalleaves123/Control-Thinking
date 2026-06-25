#!/usr/bin/env python3
"""Run the five-agent angle-rigidity formation-control example."""

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

from src.control import angle_control_input, angle_simulation_metrics, current_angles, paper_five_agent_spec, simulate
from src.rigidity import expected_full_rank, rigidity_rank
from src.visualization import plot_error_series, plot_formation_trajectory, plot_rank_bar


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "five_agent_angle_control.yaml")
    args = parser.parse_args()

    with args.config.open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    spec = paper_five_agent_spec()
    misaligned_agent = int(config["misaligned_agent"]) - 1
    theta = np.deg2rad(float(config["misalignment_degrees"]))
    rotations = {misaligned_agent: theta}

    def controller(positions: np.ndarray) -> np.ndarray:
        return angle_control_input(
            positions,
            spec.angle_triplets,
            spec.desired_angles,
            gain=float(config["gain"]),
            local_frame_rotations=rotations,
        )

    trajectory = simulate(spec.initial_positions, controller, dt=float(config["dt"]), steps=int(config["steps"]))
    times = np.arange(trajectory.shape[0]) * float(config["dt"])
    angle_errors = np.vstack([current_angles(frame, spec.angle_triplets) - spec.desired_angles for frame in trajectory])
    metrics = angle_simulation_metrics(trajectory, spec.angle_triplets, spec.desired_angles)

    figures_dir = ROOT / "results" / "figures"
    logs_dir = ROOT / "results" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    plot_formation_trajectory(
        trajectory,
        figures_dir / "angle_control_trajectory.png",
        title="Angle Rigidity-Based Control With Local-Frame Misalignment",
    )
    plot_error_series(
        times,
        angle_errors,
        figures_dir / "angle_control_errors.png",
        title="Angle Errors Under Angle Rigidity-Based Control",
        ylabel="angle error [rad]",
    )
    plot_rank_bar(
        rigidity_rank(trajectory[-1], spec.angle_triplets),
        expected_full_rank(spec.initial_positions.shape[0]),
        figures_dir / "angle_rigidity_rank.png",
    )
    with (logs_dir / "angle_control_metrics.json").open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
