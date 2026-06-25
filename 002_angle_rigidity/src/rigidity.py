"""Angle rigidity matrix construction and rank tests."""

from __future__ import annotations

import numpy as np

from .geometry import EPSILON, bearing, projection, unsigned_angle_at

Triplet = tuple[int, int, int]


def angle_rigidity_row(positions: np.ndarray, triplet: Triplet) -> np.ndarray:
    """
    Build one row of R_a(p) for alpha_ijk.

    The implementation follows the paper's differential expression
    d beta / dt = N_kji p_dot_i - (N_kji + N_ijk) p_dot_j + N_ijk p_dot_k.
    Indices are zero-based in code.
    """
    i, j, k = triplet
    count = positions.shape[0]
    row = np.zeros(2 * count, dtype=float)

    z_jk = bearing(positions, j, k)
    z_ji = bearing(positions, j, i)
    length_ji = float(np.linalg.norm(positions[i] - positions[j]))
    length_jk = float(np.linalg.norm(positions[k] - positions[j]))
    beta = unsigned_angle_at(positions, i, j, k)
    sin_beta = np.sin(beta)
    if abs(sin_beta) <= EPSILON:
        raise ValueError(f"Degenerate triplet {triplet}: sin(beta) is near zero.")

    n_kji = -(z_jk @ projection(z_ji)) / (length_ji * sin_beta)
    n_ijk = -(z_ji @ projection(z_jk)) / (length_jk * sin_beta)

    row[2 * i : 2 * i + 2] = n_kji
    row[2 * j : 2 * j + 2] = -(n_kji + n_ijk)
    row[2 * k : 2 * k + 2] = n_ijk
    return row


def angle_rigidity_matrix(positions: np.ndarray, triplets: list[Triplet]) -> np.ndarray:
    return np.vstack([angle_rigidity_row(positions, triplet) for triplet in triplets])


def rigidity_rank(positions: np.ndarray, triplets: list[Triplet], *, tol: float = 1e-8) -> int:
    matrix = angle_rigidity_matrix(positions, triplets)
    return int(np.linalg.matrix_rank(matrix, tol=tol))


def expected_full_rank(agent_count: int) -> int:
    return 2 * agent_count - 4
