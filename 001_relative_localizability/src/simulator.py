"""Scenario generation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .geometry import rotation_matrix


@dataclass(frozen=True)
class TrajectoryScenario:
    """Trajectories and local-frame metadata for a simulated experiment."""

    times: np.ndarray
    positions_global: Mapping[str, np.ndarray]
    frame_orientations: Mapping[str, float]
    landmarks_global: Mapping[str, np.ndarray]
    leaders_global: Mapping[str, np.ndarray]


def _smooth_trajectory(times: np.ndarray, parameters: tuple[float, ...]) -> np.ndarray:
    a1, a2, b1, b2, drift_x, drift_y, phase = parameters
    t = times
    x = a1 * np.cos(0.75 * t + phase) + a2 * np.sin(1.30 * t - 0.4 * phase) + drift_x * t
    y = b1 * np.sin(0.95 * t - 0.2 * phase) + b2 * np.cos(1.15 * t + phase) + drift_y * t
    return np.column_stack([x, y])


def build_default_scenario(
    num_steps: int = 90,
    dt: float = 0.1,
    seed: int = 7,
    frame_orientations: Mapping[str, float] | None = None,
) -> TrajectoryScenario:
    """Build a smooth three-robot scenario with non-degenerate motion."""
    rng = np.random.default_rng(seed)
    times = np.arange(num_steps, dtype=float) * dt

    base_i = _smooth_trajectory(times, (0.7, 0.2, 0.5, 0.15, 0.08, 0.05, 0.1))
    base_j = _smooth_trajectory(times, (0.6, 0.25, 0.55, 0.18, -0.04, 0.06, 0.9)) + np.array([1.8, 0.9])
    base_m = _smooth_trajectory(times, (0.55, 0.18, 0.7, 0.20, -0.06, -0.03, -0.6)) + np.array([-1.1, 1.6])

    jitter = 0.015 * rng.standard_normal((3, num_steps, 2))
    positions_global = {
        "i": base_i + jitter[0],
        "j": base_j + jitter[1],
        "m": base_m + jitter[2],
    }

    if frame_orientations is None:
        frame_orientations = {"i": 0.0, "j": 0.55, "m": -0.82}

    return TrajectoryScenario(
        times=times,
        positions_global=positions_global,
        frame_orientations=frame_orientations,
        landmarks_global={},
        leaders_global={},
    )


def build_mixed_topology_scenario(
    num_steps: int = 90,
    dt: float = 0.1,
    seed: int = 11,
) -> TrajectoryScenario:
    """Build a small mixed follower-leader-landmark scenario."""
    scenario = build_default_scenario(num_steps=num_steps, dt=dt, seed=seed)
    times = scenario.times

    leader = np.column_stack(
        [
            2.3 + 0.4 * np.cos(0.6 * times + 0.2) + 0.05 * times,
            -0.3 + 0.7 * np.sin(0.5 * times + 0.7),
        ]
    )
    landmark = np.array([2.9, 2.2], dtype=float)

    return TrajectoryScenario(
        times=times,
        positions_global=dict(scenario.positions_global),
        frame_orientations=dict(scenario.frame_orientations),
        landmarks_global={"A": np.repeat(landmark[None, :], num_steps, axis=0)},
        leaders_global={"L": leader},
    )


def compute_local_displacements(positions_global: np.ndarray, frame_orientation: float) -> np.ndarray:
    """Express self-displacements in the robot's local frame."""
    displacements_global = np.diff(positions_global, axis=0)
    return displacements_global @ rotation_matrix(-frame_orientation).T
