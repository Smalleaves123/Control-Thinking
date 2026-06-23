#!/usr/bin/env python3
"""Run the noise-robustness experiments from stages 2 and 4."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.solver import run_noise_robustness_experiment, write_metrics
from src.visualization import plot_error_curve, plot_rmse_vs_noise

try:
    import yaml
except ImportError:  # pragma: no cover - optional dependency at runtime
    yaml = None


DEFAULT_CONFIG = {
    "num_steps": 90,
    "dt": 0.1,
    "base_seed": 23,
    "frame_orientations": {"i": 0.0, "j": 0.55, "m": -0.82},
    "noise_levels": [0.0, 0.0015, 0.003, 0.005, 0.0075, 0.01, 0.0125, 0.015],
    "trials_per_level": 20,
    "displacement_noise_ratio": 0.6,
    "direct_window_instants": 4,
    "robust_window_instants": 6,
    "condition_number_max": 1.0e8,
    "robust_window_candidates": [4, 5, 6, 7, 8],
    "rmse_vs_d_noise_level": 0.003,
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
        default=ROOT / "configs" / "noise_robustness_test.yaml",
    )
    args = parser.parse_args()

    config = load_config(args.config)
    stats = run_noise_robustness_experiment(**config)

    figures_dir = ROOT / "results" / "figures"
    logs_dir = ROOT / "results" / "logs"

    plot_rmse_vs_noise(
        stats["noise_levels"],
        {
            "aligned linear": stats["aligned_rmse_mean"],
            "unaligned linear": stats["linear_rmse_mean"],
            "unaligned robust": stats["robust_rmse_mean"],
        },
        figures_dir / "rmse_vs_noise_level.png",
        title="RMSE vs Noise Level",
        ylabel="position RMSE",
    )
    plot_rmse_vs_noise(
        stats["noise_levels"],
        {
            "linear": stats["linear_rmse_mean"],
            "robust": stats["robust_rmse_mean"],
        },
        figures_dir / "linear_vs_robust_rmse.png",
        title="Linear vs Robust RMSE",
        ylabel="position RMSE",
    )
    plot_error_curve(
        stats["noise_levels"],
        np.column_stack([stats["linear_orientation_rmse_mean"], stats["robust_orientation_rmse_mean"]]),
        figures_dir / "error_curve_under_noise.png",
        title="Orientation Error Under Noise",
        ylabel="orientation RMSE [rad]",
        legend_labels=["linear", "robust"],
    )

    plot_error_curve(
        stats["robust_window_candidates"],
        stats["rmse_vs_d_mean"],
        figures_dir / "rmse_vs_number_of_time_instants.png",
        title=f"Robust RMSE vs Number of Time Instants (noise={stats['rmse_vs_d_noise_level']:.4f} rad)",
        ylabel="position RMSE",
    )

    serializable = {key: value.tolist() if hasattr(value, "tolist") else value for key, value in stats.items()}
    write_metrics(logs_dir / "noise_robustness_metrics.json", serializable)
    print(json.dumps(serializable, indent=2))


if __name__ == "__main__":
    main()
