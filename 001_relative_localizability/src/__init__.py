"""Simulation toolkit for relative localizability experiments."""

from .geometry import rotation_matrix, signed_angle, triangle_signed_angles, wrap_to_pi
from .measurements import MeasurementBundle
from .simulator import TrajectoryScenario, build_default_scenario, build_mixed_topology_scenario
from .solver import (
    AlignedLocalizationResult,
    MixedTopologyResult,
    UnalignedLocalizationResult,
    run_aligned_experiment,
    run_mixed_topology_experiment,
    run_noise_robustness_experiment,
    run_unaligned_experiment,
)

__all__ = [
    "AlignedLocalizationResult",
    "MeasurementBundle",
    "MixedTopologyResult",
    "TrajectoryScenario",
    "UnalignedLocalizationResult",
    "build_default_scenario",
    "build_mixed_topology_scenario",
    "rotation_matrix",
    "run_aligned_experiment",
    "run_mixed_topology_experiment",
    "run_noise_robustness_experiment",
    "run_unaligned_experiment",
    "signed_angle",
    "triangle_signed_angles",
    "wrap_to_pi",
]
