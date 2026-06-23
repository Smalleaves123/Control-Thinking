"""Geometry primitives used by the localization algorithms."""

from __future__ import annotations

import math
from typing import Iterable

import numpy as np

EPSILON = 1e-9


def wrap_to_pi(angle: float | np.ndarray) -> float | np.ndarray:
    """Wrap an angle to [-pi, pi)."""
    return (angle + np.pi) % (2.0 * np.pi) - np.pi


def rotation_matrix(theta: float) -> np.ndarray:
    """Return the 2D counterclockwise rotation matrix."""
    c = math.cos(theta)
    s = math.sin(theta)
    return np.array([[c, -s], [s, c]], dtype=float)


def rotation_vector(theta: float) -> np.ndarray:
    """Return [cos(theta), sin(theta)]^T."""
    return np.array([math.cos(theta), math.sin(theta)], dtype=float)


def as_vector(values: Iterable[float]) -> np.ndarray:
    """Convert an iterable to a 2D float vector."""
    array = np.asarray(list(values), dtype=float)
    if array.shape != (2,):
        raise ValueError(f"Expected a 2D vector, got shape {array.shape}.")
    return array


def safe_norm(vector: np.ndarray) -> float:
    """Compute a stable vector norm."""
    return float(np.linalg.norm(vector))


def normalize(vector: np.ndarray, *, eps: float = EPSILON) -> np.ndarray:
    """Return a normalized vector."""
    norm = safe_norm(vector)
    if norm <= eps:
        raise ValueError("Cannot normalize a near-zero vector.")
    return vector / norm


def cross_2d(a: np.ndarray, b: np.ndarray) -> float:
    """Return the scalar 2D cross product."""
    return float(a[0] * b[1] - a[1] * b[0])


def complex_operator(vector: np.ndarray) -> np.ndarray:
    """
    Return the matrix M(v) such that M(v) [cos(theta), sin(theta)]^T = R(theta) v.
    """
    x, y = as_vector(vector)
    return np.array([[x, -y], [y, x]], dtype=float)


def signed_angle(vector_from: np.ndarray, vector_to: np.ndarray) -> float:
    """Return the signed angle from vector_from to vector_to."""
    v_from = normalize(np.asarray(vector_from, dtype=float))
    v_to = normalize(np.asarray(vector_to, dtype=float))
    return float(math.atan2(cross_2d(v_from, v_to), float(np.dot(v_from, v_to))))


def triangle_signed_angles(p_i: np.ndarray, p_j: np.ndarray, p_m: np.ndarray) -> dict[str, float]:
    """
    Compute the signed interior angles used by the paper notation.

    alpha_mij: angle at i from i->m to i->j
    alpha_ijm: angle at j from j->i to j->m
    alpha_jmi: angle at m from m->j to m->i
    """
    return {
        "mij": signed_angle(p_m - p_i, p_j - p_i),
        "ijm": signed_angle(p_i - p_j, p_m - p_j),
        "jmi": signed_angle(p_j - p_m, p_i - p_m),
    }


def angle_sum_correction(angles: np.ndarray) -> np.ndarray:
    """
    Enforce the triangle constraint |alpha_1| + |alpha_2| + |alpha_3| = pi.
    """
    corrected = np.asarray(angles, dtype=float).copy()
    magnitudes = np.abs(corrected)
    magnitudes += (np.pi - magnitudes.sum()) / 3.0
    magnitudes = np.clip(magnitudes, EPSILON, np.pi - EPSILON)
    return np.sign(corrected) * magnitudes


def orientation_error(estimate: np.ndarray, truth: np.ndarray) -> float:
    """Angular error between two orientation vectors."""
    est = normalize(estimate)
    ref = normalize(truth)
    return abs(float(math.atan2(cross_2d(ref, est), float(np.dot(ref, est)))))
