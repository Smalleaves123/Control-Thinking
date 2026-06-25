"""Geometry helpers for planar angle-rigidity simulations."""

from __future__ import annotations

import math

import numpy as np

EPSILON = 1e-9


def rotation_matrix(theta: float) -> np.ndarray:
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def perpendicular_matrix() -> np.ndarray:
    return np.array([[0.0, -1.0], [1.0, 0.0]], dtype=float)


def normalize(vector: np.ndarray, *, eps: float = EPSILON) -> np.ndarray:
    norm = float(np.linalg.norm(vector))
    if norm <= eps:
        raise ValueError("Cannot normalize a near-zero vector.")
    return vector / norm


def bearing(positions: np.ndarray, i: int, j: int) -> np.ndarray:
    """Return z_ij = (p_j - p_i) / ||p_j - p_i|| using zero-based indices."""
    return normalize(positions[j] - positions[i])


def wrap_to_pi(angle: float | np.ndarray) -> float | np.ndarray:
    return (angle + np.pi) % (2.0 * np.pi) - np.pi


def unsigned_angle_at(positions: np.ndarray, j: int, i: int, k: int) -> float:
    """Return alpha_jik in (0, pi), the interior angle at vertex i."""
    z_ij = bearing(positions, i, j)
    z_ik = bearing(positions, i, k)
    dot = float(np.clip(np.dot(z_ij, z_ik), -1.0, 1.0))
    return float(math.acos(dot))


def signed_angle_at(positions: np.ndarray, i: int, j: int, k: int) -> float:
    """Return the paper's signed alpha_ijk from ray j->i to ray j->k."""
    z_ji = bearing(positions, j, i)
    z_jk = bearing(positions, j, k)
    return float(math.atan2(np.cross(z_ji, z_jk), np.dot(z_ji, z_jk)) % (2.0 * math.pi))


def projection(vector: np.ndarray) -> np.ndarray:
    z = normalize(vector)
    return np.eye(2) - np.outer(z, z)
