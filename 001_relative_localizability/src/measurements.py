"""Measurement generation and perturbation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .geometry import angle_sum_correction, triangle_signed_angles
from .simulator import TrajectoryScenario, compute_local_displacements


@dataclass(frozen=True)
class MeasurementBundle:
    """All measurements required by the simulation scripts."""

    times: np.ndarray
    angles_ijm: np.ndarray
    displacements_local: Mapping[str, np.ndarray]
    positions_global: Mapping[str, np.ndarray]
    frame_orientations: Mapping[str, float]
    landmarks_global: Mapping[str, np.ndarray]
    leaders_global: Mapping[str, np.ndarray]


def build_measurements(
    scenario: TrajectoryScenario,
    *,
    angle_noise_std: float = 0.0,
    displacement_noise_std: float = 0.0,
    seed: int = 0,
    enforce_triangle_constraint: bool = False,
) -> MeasurementBundle:
    """Generate angle and self-displacement measurements from a scenario."""
    rng = np.random.default_rng(seed)
    positions = scenario.positions_global
    num_steps = len(scenario.times)

    angles = np.zeros((num_steps, 3), dtype=float)
    for index in range(num_steps):
        signed = triangle_signed_angles(
            positions["i"][index],
            positions["j"][index],
            positions["m"][index],
        )
        angles[index] = np.array([signed["mij"], signed["ijm"], signed["jmi"]], dtype=float)

    if angle_noise_std > 0.0:
        angles = angles + rng.normal(scale=angle_noise_std, size=angles.shape)

    if enforce_triangle_constraint:
        angles = np.vstack([angle_sum_correction(angle_row) for angle_row in angles])

    displacements_local = {}
    for robot, position_series in positions.items():
        local = compute_local_displacements(position_series, scenario.frame_orientations[robot])
        if displacement_noise_std > 0.0:
            local = local + rng.normal(scale=displacement_noise_std, size=local.shape)
        displacements_local[robot] = local

    return MeasurementBundle(
        times=scenario.times,
        angles_ijm=angles,
        displacements_local=displacements_local,
        positions_global=positions,
        frame_orientations=scenario.frame_orientations,
        landmarks_global=scenario.landmarks_global,
        leaders_global=scenario.leaders_global,
    )


def detect_degenerate_window(
    angles: np.ndarray,
    displacements_local: Mapping[str, np.ndarray],
    index: int,
    *,
    angle_delta_threshold: float = 1e-3,
    motion_threshold: float = 1e-3,
) -> bool:
    """Detect the nearly strongly-similar motion pattern discussed in the paper."""
    if index >= len(angles) - 1:
        return True

    angle_delta = float(np.sum(np.abs(angles[index + 1] - angles[index])))
    motion_scale = (
        np.linalg.norm(displacements_local["i"][index])
        + np.linalg.norm(displacements_local["j"][index])
        + np.linalg.norm(displacements_local["m"][index])
    )
    return angle_delta <= angle_delta_threshold and motion_scale <= motion_threshold


def compute_triangle_angles_for_agent(
    vertex_positions: Mapping[str, np.ndarray],
    triangle: tuple[str, str, str],
) -> np.ndarray:
    """Compute the three signed interior angles for an arbitrary triangle over time."""
    a, b, c = triangle
    num_steps = len(vertex_positions[a])
    angles = np.zeros((num_steps, 3), dtype=float)
    for index in range(num_steps):
        values = triangle_signed_angles(
            vertex_positions[a][index],
            vertex_positions[b][index],
            vertex_positions[c][index],
        )
        angles[index] = np.array([values["mij"], values["ijm"], values["jmi"]], dtype=float)
    return angles
