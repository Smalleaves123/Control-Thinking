"""Formation control laws used in the angle-rigidity paper."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .geometry import bearing, rotation_matrix, unsigned_angle_at
from .rigidity import Triplet, angle_rigidity_matrix, expected_full_rank, rigidity_rank


@dataclass(frozen=True)
class FormationSpec:
    initial_positions: np.ndarray
    angle_triplets: list[Triplet]
    desired_angles: np.ndarray
    bearing_edges: list[tuple[int, int]]
    desired_bearings: dict[tuple[int, int], np.ndarray]


def paper_five_agent_spec() -> FormationSpec:
    """Return the five-agent example from Section V of the paper."""
    initial_positions = np.array(
        [
            [0.8, 0.2],
            [0.1, 1.4],
            [-1.4, 0.3],
            [0.1, 2.3],
            [-1.7, 1.6],
        ],
        dtype=float,
    )

    angle_triplets = [
        (1, 0, 2),  # alpha_213
        (0, 2, 1),  # alpha_132
        (2, 1, 0),  # alpha_321
        (2, 3, 1),  # alpha_342
        (1, 3, 0),  # alpha_241
        (1, 4, 3),  # alpha_254
        (0, 4, 1),  # alpha_152
    ]
    desired_angles = np.array(
        [
            np.pi / 4.0,
            np.pi / 4.0,
            np.pi / 2.0,
            np.arctan(0.5),
            np.arctan(0.5),
            np.arctan(0.5),
            np.arctan(3.0 / np.sqrt(10.0)),
        ],
        dtype=float,
    )

    s2 = np.sqrt(2.0)
    s5 = np.sqrt(5.0)
    desired_bearings = {
        (2, 0): np.array([1.0, 0.0]),
        (1, 0): np.array([s2 / 2.0, -s2 / 2.0]),
        (2, 1): np.array([s2 / 2.0, s2 / 2.0]),
        (3, 1): np.array([0.0, -1.0]),
        (3, 0): np.array([s5 / 5.0, -2.0 * s5 / 5.0]),
        (3, 2): np.array([-s5 / 5.0, -2.0 * s5 / 5.0]),
        (4, 3): np.array([2.0 * s5 / 5.0, -s5 / 5.0]),
        (4, 1): np.array([-s5 / 5.0, -2.0 * s5 / 5.0]),
        (4, 0): np.array([3.0 / np.sqrt(10.0), -1.0 / np.sqrt(10.0)]),
    }
    return FormationSpec(
        initial_positions=initial_positions,
        angle_triplets=angle_triplets,
        desired_angles=desired_angles,
        bearing_edges=list(desired_bearings.keys()),
        desired_bearings=desired_bearings,
    )


def current_angles(positions: np.ndarray, triplets: list[Triplet]) -> np.ndarray:
    return np.array([unsigned_angle_at(positions, j, i, k) for j, i, k in triplets], dtype=float)


def angle_control_input(
    positions: np.ndarray,
    triplets: list[Triplet],
    desired_angles: np.ndarray,
    *,
    gain: float = 1.0,
    local_frame_rotations: dict[int, float] | None = None,
) -> np.ndarray:
    """
    Compute the unified angle-only controller in (58).

    local_frame_rotations optionally applies R_gb and R_bg around the local
    computation to verify the coordinate-frame invariance noted in Remark 6.
    """
    controls = np.zeros_like(positions, dtype=float)
    for (j, i, k), desired in zip(triplets, desired_angles):
        alpha = unsigned_angle_at(positions, j, i, k)
        term = bearing(positions, i, j) + bearing(positions, i, k)
        if local_frame_rotations and i in local_frame_rotations:
            theta = local_frame_rotations[i]
            local_term = rotation_matrix(theta) @ term
            term = rotation_matrix(-theta) @ local_term
        controls[i] -= gain * (alpha - desired) * term
    return controls


def bearing_control_input(
    positions: np.ndarray,
    edges: list[tuple[int, int]],
    desired_bearings: dict[tuple[int, int], np.ndarray],
    *,
    gain: float = 1.0,
    local_frame_rotations: dict[int, float] | None = None,
) -> np.ndarray:
    """Compute the bearing-based comparison controller in (61)."""
    controls = np.zeros_like(positions, dtype=float)
    for i, j in edges:
        z_ij = bearing(positions, i, j)
        desired = desired_bearings[(i, j)]
        if local_frame_rotations and i in local_frame_rotations:
            theta = local_frame_rotations[i]
            desired = rotation_matrix(theta) @ desired
        projection = np.eye(2) - np.outer(z_ij, z_ij)
        controls[i] -= gain * projection @ desired
    return controls


def simulate(
    initial_positions: np.ndarray,
    controller,
    *,
    dt: float,
    steps: int,
) -> np.ndarray:
    positions = np.zeros((steps + 1, *initial_positions.shape), dtype=float)
    positions[0] = initial_positions
    for index in range(steps):
        positions[index + 1] = positions[index] + dt * controller(positions[index])
    return positions


def angle_simulation_metrics(
    trajectory: np.ndarray,
    triplets: list[Triplet],
    desired_angles: np.ndarray,
) -> dict[str, float | int]:
    final_angles = current_angles(trajectory[-1], triplets)
    final_errors = final_angles - desired_angles
    matrix = angle_rigidity_matrix(trajectory[-1], triplets)
    return {
        "final_angle_rmse": float(np.sqrt(np.mean(final_errors**2))),
        "final_max_abs_angle_error": float(np.max(np.abs(final_errors))),
        "final_rank": rigidity_rank(trajectory[-1], triplets),
        "expected_rank": expected_full_rank(trajectory.shape[1]),
        "condition_number": float(np.linalg.cond(matrix @ matrix.T)),
    }
