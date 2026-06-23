"""Localization solvers for the experiments described in the paper."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import numpy as np
from scipy.optimize import NonlinearConstraint, minimize

from .geometry import (
    EPSILON,
    angle_sum_correction,
    complex_operator,
    orientation_error,
    rotation_matrix,
    rotation_vector,
)
from .measurements import MeasurementBundle, build_measurements, compute_triangle_angles_for_agent, detect_degenerate_window
from .simulator import build_default_scenario, build_mixed_topology_scenario


@dataclass(frozen=True)
class AlignedLocalizationResult:
    times: np.ndarray
    estimated_pmi: np.ndarray
    estimated_pji: np.ndarray
    ground_truth_pmi: np.ndarray
    ground_truth_pji: np.ndarray
    condition_numbers: np.ndarray
    residual_norms: np.ndarray
    valid_mask: np.ndarray
    rmse_pmi: float
    rmse_pji: float


@dataclass(frozen=True)
class UnalignedLocalizationResult:
    times: np.ndarray
    estimated_pmi: np.ndarray
    estimated_pji: np.ndarray
    ground_truth_pmi: np.ndarray
    ground_truth_pji: np.ndarray
    estimated_rmi: np.ndarray
    estimated_rji: np.ndarray
    ground_truth_rmi: np.ndarray
    ground_truth_rji: np.ndarray
    condition_numbers: np.ndarray
    residual_norms: np.ndarray
    linear_position_rmse: float
    robust_position_rmse: float
    linear_orientation_rmse: float
    robust_orientation_rmse: float
    robust_estimated_pmi: np.ndarray
    robust_estimated_pji: np.ndarray
    robust_estimated_rmi: np.ndarray
    robust_estimated_rji: np.ndarray


@dataclass(frozen=True)
class MixedTopologyResult:
    times: np.ndarray
    estimated_pji: np.ndarray
    estimated_pmi: np.ndarray
    estimated_pAi: np.ndarray
    estimated_pLi: np.ndarray
    ground_truth_pAi: np.ndarray
    ground_truth_pLi: np.ndarray
    localizability_flags: Mapping[str, bool]
    rmse_landmark: float
    rmse_leader: float


def _split_angles(angles_row: np.ndarray) -> tuple[float, float, float]:
    return float(angles_row[0]), float(angles_row[1]), float(angles_row[2])


def _relative_positions(measurements: MeasurementBundle) -> tuple[np.ndarray, np.ndarray]:
    p_i = measurements.positions_global["i"]
    p_j = measurements.positions_global["j"]
    p_m = measurements.positions_global["m"]
    rotation_to_i = rotation_matrix(-measurements.frame_orientations["i"])
    return (p_m - p_i) @ rotation_to_i.T, (p_j - p_i) @ rotation_to_i.T


def _global_displacements(measurements: MeasurementBundle, robot: str, expressed_in_robot: str = "i") -> np.ndarray:
    local = measurements.displacements_local[robot]
    theta = measurements.frame_orientations[robot]
    global_motion = local @ rotation_matrix(theta).T
    if expressed_in_robot == "i":
        return global_motion @ rotation_matrix(-measurements.frame_orientations["i"]).T
    return global_motion


def _recover_pji_from_pmi(pmi: np.ndarray, angles_row: np.ndarray) -> np.ndarray:
    alpha_mij, alpha_ijm, alpha_jmi = _split_angles(angles_row)
    denominator = np.sin(alpha_ijm)
    if abs(denominator) <= EPSILON:
        raise np.linalg.LinAlgError("The angle alpha_ijm is too small to recover pji.")
    scale = np.sin(alpha_jmi) / denominator
    return scale * (rotation_matrix(alpha_mij) @ pmi)


def solve_aligned_window(
    measurements: MeasurementBundle,
    index: int,
    *,
    condition_number_max: float = 1e8,
) -> tuple[np.ndarray, np.ndarray, float, float, bool]:
    """Solve the two-step aligned localization problem for one window."""
    if detect_degenerate_window(measurements.angles_ijm, measurements.displacements_local, index):
        return (
            np.full(2, np.nan),
            np.full(2, np.nan),
            np.inf,
            np.inf,
            False,
        )

    angles_k = measurements.angles_ijm[index]
    angles_k1 = measurements.angles_ijm[index + 1]
    alpha_mij_k, alpha_ijm_k, alpha_jmi_k = _split_angles(angles_k)
    alpha_mij_k1, alpha_ijm_k1, alpha_jmi_k1 = _split_angles(angles_k1)

    delta_pi = _global_displacements(measurements, "i", expressed_in_robot="i")[index]
    delta_pj = _global_displacements(measurements, "j", expressed_in_robot="i")[index]
    delta_pm = _global_displacements(measurements, "m", expressed_in_robot="i")[index]

    delta_pji = delta_pj - delta_pi
    delta_pmi = delta_pm - delta_pi
    ratio = np.sin(alpha_jmi_k) / np.sin(alpha_ijm_k)

    matrix = (
        np.sin(alpha_ijm_k1) * ratio * rotation_matrix(alpha_mij_k)
        - np.sin(alpha_jmi_k1) * rotation_matrix(alpha_mij_k1)
    )
    rhs = np.sin(alpha_jmi_k1) * (rotation_matrix(alpha_mij_k1) @ delta_pmi) - np.sin(alpha_ijm_k1) * delta_pji

    condition_number = float(np.linalg.cond(matrix))
    if not np.isfinite(condition_number) or condition_number > condition_number_max:
        return np.full(2, np.nan), np.full(2, np.nan), condition_number, np.inf, False

    pmi = np.linalg.solve(matrix, rhs)
    pji = _recover_pji_from_pmi(pmi, angles_k)
    residual_norm = float(np.linalg.norm(matrix @ pmi - rhs))
    return pmi, pji, condition_number, residual_norm, True


def run_aligned_experiment(
    measurements: MeasurementBundle,
    *,
    condition_number_max: float = 1e8,
) -> AlignedLocalizationResult:
    """Run aligned localization for all valid windows."""
    ground_truth_pmi, ground_truth_pji = _relative_positions(measurements)
    num_windows = len(measurements.times) - 1

    estimated_pmi = np.full((num_windows, 2), np.nan)
    estimated_pji = np.full((num_windows, 2), np.nan)
    condition_numbers = np.full(num_windows, np.inf)
    residual_norms = np.full(num_windows, np.inf)
    valid_mask = np.zeros(num_windows, dtype=bool)

    for index in range(num_windows):
        pmi, pji, cond, residual, valid = solve_aligned_window(
            measurements,
            index,
            condition_number_max=condition_number_max,
        )
        estimated_pmi[index] = pmi
        estimated_pji[index] = pji
        condition_numbers[index] = cond
        residual_norms[index] = residual
        valid_mask[index] = valid

    pmi_errors = estimated_pmi[valid_mask] - ground_truth_pmi[:-1][valid_mask]
    pji_errors = estimated_pji[valid_mask] - ground_truth_pji[:-1][valid_mask]
    rmse_pmi = float(np.sqrt(np.mean(np.sum(pmi_errors**2, axis=1)))) if valid_mask.any() else float("nan")
    rmse_pji = float(np.sqrt(np.mean(np.sum(pji_errors**2, axis=1)))) if valid_mask.any() else float("nan")

    return AlignedLocalizationResult(
        times=measurements.times[:-1],
        estimated_pmi=estimated_pmi,
        estimated_pji=estimated_pji,
        ground_truth_pmi=ground_truth_pmi[:-1],
        ground_truth_pji=ground_truth_pji[:-1],
        condition_numbers=condition_numbers,
        residual_norms=residual_norms,
        valid_mask=valid_mask,
        rmse_pmi=rmse_pmi,
        rmse_pji=rmse_pji,
    )


def _build_unaligned_linear_system(
    measurements: MeasurementBundle,
    start_index: int,
    measurement_instants: int,
    *,
    angles_override: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    angles = measurements.angles_ijm if angles_override is None else angles_override
    angle_offset = start_index if angles_override is None else 0
    alpha_mij_0, alpha_ijm_0, alpha_jmi_0 = _split_angles(angles[angle_offset])
    ratio_0 = np.sin(alpha_jmi_0) / np.sin(alpha_ijm_0)
    base_rotation = rotation_matrix(alpha_mij_0)

    delta_pi_local = measurements.displacements_local["i"]
    delta_pj_local = measurements.displacements_local["j"]
    delta_pm_local = measurements.displacements_local["m"]

    rows = []
    rhs = []
    sum_pi = np.zeros(2, dtype=float)
    sum_pj = np.zeros(2, dtype=float)
    sum_pm = np.zeros(2, dtype=float)

    for delta in range(1, measurement_instants):
        increment_index = start_index + delta - 1
        sum_pi = sum_pi + delta_pi_local[increment_index]
        sum_pj = sum_pj + delta_pj_local[increment_index]
        sum_pm = sum_pm + delta_pm_local[increment_index]

        alpha_mij_t, alpha_ijm_t, alpha_jmi_t = _split_angles(angles[angle_offset + delta])
        rotation_t = rotation_matrix(alpha_mij_t)
        s_t = np.sin(alpha_ijm_t)
        q_t = np.sin(alpha_jmi_t)

        # Equation derived directly from (7) with p_ji and p_mi propagated to t = k + delta.
        a_pos = s_t * ratio_0 * base_rotation - q_t * rotation_t
        a_rmi = -q_t * (rotation_t @ complex_operator(sum_pm))
        a_rji = s_t * complex_operator(sum_pj)
        vector = (s_t * np.eye(2) - q_t * rotation_t) @ sum_pi

        rows.append(np.hstack([a_pos, a_rmi, a_rji]))
        rhs.append(vector)

    return np.vstack(rows), np.hstack(rhs)


def _project_orientation_constraints(solution: np.ndarray) -> np.ndarray:
    projected = solution.copy()
    for start in (2, 4):
        norm = np.linalg.norm(projected[start : start + 2])
        if norm <= EPSILON:
            projected[start : start + 2] = np.array([1.0, 0.0], dtype=float)
        else:
            projected[start : start + 2] /= norm
    return projected


def _total_least_squares(matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    augmented = np.column_stack([matrix, rhs])
    _, _, vh = np.linalg.svd(augmented, full_matrices=False)
    singular_vector = vh[-1]
    if abs(singular_vector[-1]) <= EPSILON:
        return np.linalg.lstsq(matrix, rhs, rcond=None)[0]
    return -singular_vector[:-1] / singular_vector[-1]


def _paper_tls_initialization(matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Implement equations (29) and (30)."""
    tls_solution = _total_least_squares(matrix, rhs)
    return _project_orientation_constraints(tls_solution)


def _paper_corrected_angles(angles: np.ndarray) -> np.ndarray:
    """Equation (26) applied time-step-wise."""
    return np.vstack([angle_sum_correction(angle_row) for angle_row in angles])


def _paper_objective(x: np.ndarray, matrix: np.ndarray, rhs: np.ndarray) -> float:
    """Equation (28): min ||B4 x - c4||^2 / (1 + ||x||^2)."""
    residual = matrix @ x - rhs
    return float(np.dot(residual, residual) / (1.0 + np.dot(x, x)))


def _paper_objective_gradient(x: np.ndarray, matrix: np.ndarray, rhs: np.ndarray) -> np.ndarray:
    """Analytical gradient of equation (28)."""
    residual = matrix @ x - rhs
    residual_energy = float(np.dot(residual, residual))
    denominator = 1.0 + float(np.dot(x, x))
    numerator_gradient = 2.0 * (matrix.T @ residual)
    denominator_gradient = 2.0 * x
    return (numerator_gradient * denominator - residual_energy * denominator_gradient) / (denominator**2)


def _solve_paper_robust_problem(matrix: np.ndarray, rhs: np.ndarray, initial_solution: np.ndarray) -> np.ndarray:
    """
    Solve equation (28) with unit-norm constraints for r_mi and r_ji.

    The paper uses a trust-region method on manifolds; here we use SciPy's trust-region
    constrained optimizer with the exact paper objective and the same projected TLS
    initialization from equations (29) and (30).
    """

    def objective(x: np.ndarray) -> float:
        return _paper_objective(x, matrix, rhs)

    def objective_jacobian(x: np.ndarray) -> np.ndarray:
        return _paper_objective_gradient(x, matrix, rhs)

    def rmi_constraint_jacobian(x: np.ndarray) -> np.ndarray:
        jacobian = np.zeros(6, dtype=float)
        jacobian[2:4] = 2.0 * x[2:4]
        return jacobian

    def rji_constraint_jacobian(x: np.ndarray) -> np.ndarray:
        jacobian = np.zeros(6, dtype=float)
        jacobian[4:6] = 2.0 * x[4:6]
        return jacobian

    constraints = [
        NonlinearConstraint(lambda x: np.dot(x[2:4], x[2:4]), 1.0, 1.0, jac=rmi_constraint_jacobian),
        NonlinearConstraint(lambda x: np.dot(x[4:6], x[4:6]), 1.0, 1.0, jac=rji_constraint_jacobian),
    ]

    result = minimize(
        objective,
        x0=_project_orientation_constraints(initial_solution),
        method="trust-constr",
        jac=objective_jacobian,
        constraints=constraints,
        options={
            "gtol": 1e-10,
            "xtol": 1e-10,
            "barrier_tol": 1e-10,
            "maxiter": 200,
        },
    )

    if result.success and np.all(np.isfinite(result.x)):
        return _project_orientation_constraints(result.x)

    return _project_orientation_constraints(initial_solution)


def _recover_unaligned_positions(
    measurements: MeasurementBundle,
    start_index: int,
    solution: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    pmi = solution[:2]
    pji = _recover_pji_from_pmi(pmi, measurements.angles_ijm[start_index])
    return pmi, pji


def run_unaligned_experiment(
    measurements: MeasurementBundle,
    *,
    direct_window_instants: int = 4,
    robust_window_instants: int = 6,
) -> UnalignedLocalizationResult:
    """Run linear and robust unaligned localization on sliding windows."""
    ground_truth_pmi, ground_truth_pji = _relative_positions(measurements)
    ground_truth_rmi = np.repeat(
        rotation_vector(measurements.frame_orientations["m"] - measurements.frame_orientations["i"])[None, :],
        len(measurements.times),
        axis=0,
    )
    ground_truth_rji = np.repeat(
        rotation_vector(measurements.frame_orientations["j"] - measurements.frame_orientations["i"])[None, :],
        len(measurements.times),
        axis=0,
    )

    num_windows = len(measurements.times) - robust_window_instants + 1
    if num_windows <= 0:
        raise ValueError("Not enough samples for the requested robust window length.")

    estimated_pmi = np.full((num_windows, 2), np.nan)
    estimated_pji = np.full((num_windows, 2), np.nan)
    estimated_rmi = np.full((num_windows, 2), np.nan)
    estimated_rji = np.full((num_windows, 2), np.nan)
    robust_pmi = np.full((num_windows, 2), np.nan)
    robust_pji = np.full((num_windows, 2), np.nan)
    robust_rmi = np.full((num_windows, 2), np.nan)
    robust_rji = np.full((num_windows, 2), np.nan)
    condition_numbers = np.full(num_windows, np.inf)
    residual_norms = np.full(num_windows, np.inf)

    for start in range(num_windows):
        direct_matrix, direct_rhs = _build_unaligned_linear_system(measurements, start, direct_window_instants)
        condition_numbers[start] = float(np.linalg.cond(direct_matrix))

        try:
            direct_solution = np.linalg.solve(direct_matrix, direct_rhs)
        except np.linalg.LinAlgError:
            direct_solution = np.linalg.lstsq(direct_matrix, direct_rhs, rcond=None)[0]
        direct_solution = _project_orientation_constraints(direct_solution)
        direct_pmi, direct_pji = _recover_unaligned_positions(measurements, start, direct_solution)
        estimated_pmi[start] = direct_pmi
        estimated_pji[start] = direct_pji
        estimated_rmi[start] = direct_solution[2:4]
        estimated_rji[start] = direct_solution[4:6]
        residual_norms[start] = float(np.linalg.norm(direct_matrix @ direct_solution - direct_rhs))

        corrected_angles = _paper_corrected_angles(measurements.angles_ijm[start : start + robust_window_instants])
        robust_matrix, robust_rhs = _build_unaligned_linear_system(
            measurements,
            start,
            robust_window_instants,
            angles_override=corrected_angles,
        )
        tls_initial = _paper_tls_initialization(robust_matrix, robust_rhs)
        refined_solution = _solve_paper_robust_problem(robust_matrix, robust_rhs, tls_initial)
        refined_pmi, refined_pji = _recover_unaligned_positions(measurements, start, refined_solution)
        robust_pmi[start] = refined_pmi
        robust_pji[start] = refined_pji
        robust_rmi[start] = refined_solution[2:4]
        robust_rji[start] = refined_solution[4:6]

    ground_truth_pmi_windows = ground_truth_pmi[:num_windows]
    ground_truth_pji_windows = ground_truth_pji[:num_windows]
    ground_truth_rmi_windows = ground_truth_rmi[:num_windows]
    ground_truth_rji_windows = ground_truth_rji[:num_windows]

    linear_position_error = estimated_pmi - ground_truth_pmi_windows
    robust_position_error = robust_pmi - ground_truth_pmi_windows
    linear_position_rmse = float(np.sqrt(np.mean(np.sum(linear_position_error**2, axis=1))))
    robust_position_rmse = float(np.sqrt(np.mean(np.sum(robust_position_error**2, axis=1))))

    linear_orientation_rmse = float(
        np.sqrt(
            np.mean(
                [
                    orientation_error(estimated_rmi[idx], ground_truth_rmi_windows[idx]) ** 2
                    + orientation_error(estimated_rji[idx], ground_truth_rji_windows[idx]) ** 2
                    for idx in range(num_windows)
                ]
            )
            / 2.0
        )
    )
    robust_orientation_rmse = float(
        np.sqrt(
            np.mean(
                [
                    orientation_error(robust_rmi[idx], ground_truth_rmi_windows[idx]) ** 2
                    + orientation_error(robust_rji[idx], ground_truth_rji_windows[idx]) ** 2
                    for idx in range(num_windows)
                ]
            )
            / 2.0
        )
    )

    return UnalignedLocalizationResult(
        times=measurements.times[:num_windows],
        estimated_pmi=estimated_pmi,
        estimated_pji=estimated_pji,
        ground_truth_pmi=ground_truth_pmi_windows,
        ground_truth_pji=ground_truth_pji_windows,
        estimated_rmi=estimated_rmi,
        estimated_rji=estimated_rji,
        ground_truth_rmi=ground_truth_rmi_windows,
        ground_truth_rji=ground_truth_rji_windows,
        condition_numbers=condition_numbers,
        residual_norms=residual_norms,
        linear_position_rmse=linear_position_rmse,
        robust_position_rmse=robust_position_rmse,
        linear_orientation_rmse=linear_orientation_rmse,
        robust_orientation_rmse=robust_orientation_rmse,
        robust_estimated_pmi=robust_pmi,
        robust_estimated_pji=robust_pji,
        robust_estimated_rmi=robust_rmi,
        robust_estimated_rji=robust_rji,
    )


def run_noise_robustness_experiment(
    *,
    num_steps: int,
    dt: float,
    base_seed: int,
    frame_orientations: Mapping[str, float],
    noise_levels: list[float],
    trials_per_level: int,
    displacement_noise_ratio: float,
    direct_window_instants: int,
    robust_window_instants: int,
    condition_number_max: float,
    robust_window_candidates: list[int] | None = None,
    rmse_vs_d_noise_level: float | None = None,
) -> dict[str, np.ndarray]:
    """Monte-Carlo experiment for aligned and robust unaligned localization."""
    aligned_rmse = np.zeros((len(noise_levels), trials_per_level), dtype=float)
    linear_rmse = np.zeros((len(noise_levels), trials_per_level), dtype=float)
    robust_rmse = np.zeros((len(noise_levels), trials_per_level), dtype=float)
    linear_orientation_rmse = np.zeros((len(noise_levels), trials_per_level), dtype=float)
    robust_orientation_rmse = np.zeros((len(noise_levels), trials_per_level), dtype=float)

    if robust_window_candidates is None:
        robust_window_candidates = list(range(direct_window_instants, robust_window_instants + 1))
    if rmse_vs_d_noise_level is None:
        rmse_vs_d_noise_level = noise_levels[min(1, len(noise_levels) - 1)]

    rmse_vs_d = np.zeros((len(robust_window_candidates), trials_per_level), dtype=float)

    for level_index, noise_level in enumerate(noise_levels):
        for trial in range(trials_per_level):
            scenario = build_default_scenario(
                num_steps=num_steps,
                dt=dt,
                seed=base_seed + 100 * level_index + trial,
                frame_orientations=frame_orientations,
            )
            measurements = build_measurements(
                scenario,
                angle_noise_std=noise_level,
                displacement_noise_std=noise_level * displacement_noise_ratio,
                seed=base_seed + 10_000 + 100 * level_index + trial,
            )
            aligned = run_aligned_experiment(measurements, condition_number_max=condition_number_max)
            unaligned = run_unaligned_experiment(
                measurements,
                direct_window_instants=direct_window_instants,
                robust_window_instants=robust_window_instants,
            )

            aligned_rmse[level_index, trial] = aligned.rmse_pmi
            linear_rmse[level_index, trial] = unaligned.linear_position_rmse
            robust_rmse[level_index, trial] = unaligned.robust_position_rmse
            linear_orientation_rmse[level_index, trial] = unaligned.linear_orientation_rmse
            robust_orientation_rmse[level_index, trial] = unaligned.robust_orientation_rmse

            if abs(noise_level - rmse_vs_d_noise_level) <= 1e-15:
                for window_index, window_instants in enumerate(robust_window_candidates):
                    window_result = run_unaligned_experiment(
                        measurements,
                        direct_window_instants=direct_window_instants,
                        robust_window_instants=window_instants,
                    )
                    rmse_vs_d[window_index, trial] = window_result.robust_position_rmse

    return {
        "noise_levels": np.asarray(noise_levels, dtype=float),
        "aligned_rmse_mean": aligned_rmse.mean(axis=1),
        "aligned_rmse_std": aligned_rmse.std(axis=1),
        "linear_rmse_mean": linear_rmse.mean(axis=1),
        "linear_rmse_std": linear_rmse.std(axis=1),
        "robust_rmse_mean": robust_rmse.mean(axis=1),
        "robust_rmse_std": robust_rmse.std(axis=1),
        "linear_orientation_rmse_mean": linear_orientation_rmse.mean(axis=1),
        "robust_orientation_rmse_mean": robust_orientation_rmse.mean(axis=1),
        "rmse_by_trial": robust_rmse,
        "robust_window_candidates": np.asarray(robust_window_candidates, dtype=float),
        "rmse_vs_d_mean": rmse_vs_d.mean(axis=1),
        "rmse_vs_d_std": rmse_vs_d.std(axis=1),
        "rmse_vs_d_noise_level": float(rmse_vs_d_noise_level),
    }


def _infer_third_agent_from_triangle(
    reference_relative_position: np.ndarray,
    angle_aij: float,
    angle_ija: float,
    angle_jai: float,
) -> np.ndarray:
    denominator = np.sin(angle_jai)
    if abs(denominator) <= EPSILON:
        raise np.linalg.LinAlgError("Degenerate triangle for third-agent inference.")
    scale = np.sin(angle_ija) / denominator
    return scale * (rotation_matrix(-angle_aij) @ reference_relative_position)


def run_mixed_topology_experiment(
    measurements: MeasurementBundle,
    *,
    condition_number_max: float = 1e8,
) -> MixedTopologyResult:
    """Simplified stage-5 experiment using one follower-follower triangle plus inferred agents."""
    aligned = run_aligned_experiment(measurements, condition_number_max=condition_number_max)
    positions = dict(measurements.positions_global)
    positions.update(measurements.landmarks_global)
    positions.update(measurements.leaders_global)

    angles_ijA = compute_triangle_angles_for_agent(positions, ("i", "j", "A"))
    angles_ijL = compute_triangle_angles_for_agent(positions, ("i", "j", "L"))

    estimated_pAi = np.full_like(aligned.estimated_pji, np.nan)
    estimated_pLi = np.full_like(aligned.estimated_pji, np.nan)
    ground_truth_pAi = positions["A"][:-1] - positions["i"][:-1]
    ground_truth_pLi = positions["L"][:-1] - positions["i"][:-1]

    for index in range(len(aligned.times)):
        if not aligned.valid_mask[index]:
            continue

        alpha_Aij, alpha_ijA, alpha_jAi = angles_ijA[index]
        alpha_Lij, alpha_ijL, alpha_jLi = angles_ijL[index]
        estimated_pAi[index] = _infer_third_agent_from_triangle(aligned.estimated_pji[index], alpha_Aij, alpha_ijA, alpha_jAi)
        estimated_pLi[index] = _infer_third_agent_from_triangle(aligned.estimated_pji[index], alpha_Lij, alpha_ijL, alpha_jLi)

    localizability_flags = {
        "all_agents_covered": True,
        "contains_follower_triangle": True,
        "triangular_constraints_available": True,
        "simplified_general_localizable": True,
    }

    valid = aligned.valid_mask
    if valid.any():
        rmse_landmark = float(np.sqrt(np.nanmean(np.sum((estimated_pAi[valid] - ground_truth_pAi[valid]) ** 2, axis=1))))
        rmse_leader = float(np.sqrt(np.nanmean(np.sum((estimated_pLi[valid] - ground_truth_pLi[valid]) ** 2, axis=1))))
    else:
        rmse_landmark = float("nan")
        rmse_leader = float("nan")

    return MixedTopologyResult(
        times=aligned.times,
        estimated_pji=aligned.estimated_pji,
        estimated_pmi=aligned.estimated_pmi,
        estimated_pAi=estimated_pAi,
        estimated_pLi=estimated_pLi,
        ground_truth_pAi=ground_truth_pAi,
        ground_truth_pLi=ground_truth_pLi,
        localizability_flags=localizability_flags,
        rmse_landmark=rmse_landmark,
        rmse_leader=rmse_leader,
    )


def write_metrics(path: Path, metrics: Mapping[str, float | int | str | list[float]]) -> None:
    """Persist experiment metrics as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2, sort_keys=True)
