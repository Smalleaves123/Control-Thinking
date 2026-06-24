"""Plotting helpers for the reproduction scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import matplotlib.pyplot as plt
import numpy as np


def _prepare_path(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def plot_trajectories(
    positions: Mapping[str, np.ndarray],
    save_path: Path,
    extra_positions: Mapping[str, np.ndarray] | None = None,
) -> None:
    _prepare_path(save_path)
    fig, ax = plt.subplots(figsize=(8, 6))
    colors = {"i": "#0b6e4f", "j": "#c44536", "m": "#345995", "A": "#8f754f", "L": "#6d597a"}

    for label, series in positions.items():
        ax.plot(series[:, 0], series[:, 1], label=label, linewidth=2.0, color=colors.get(label))
        ax.scatter(series[0, 0], series[0, 1], s=35, color=colors.get(label), marker="o")
        ax.scatter(series[-1, 0], series[-1, 1], s=45, color=colors.get(label), marker="x")

    if extra_positions:
        for label, series in extra_positions.items():
            ax.plot(series[:, 0], series[:, 1], label=label, linewidth=2.0, linestyle="--", color=colors.get(label))

    ax.set_title("Robot Trajectories")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.axis("equal")
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def plot_relative_position_estimation(
    times: np.ndarray,
    ground_truth: np.ndarray,
    estimate: np.ndarray,
    save_path: Path,
    *,
    title: str,
) -> None:
    _prepare_path(save_path)
    fig, axes = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
    labels = ("x", "y")
    for axis_index, axis in enumerate(axes):
        axis.plot(times, ground_truth[:, axis_index], label="ground truth", linewidth=2.0)
        axis.plot(times, estimate[:, axis_index], label="estimate", linewidth=1.7, linestyle="--")
        axis.set_ylabel(labels[axis_index])
        axis.grid(alpha=0.25)
    axes[0].set_title(title)
    axes[0].legend()
    axes[-1].set_xlabel("time [s]")
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def plot_error_curve(
    times: np.ndarray,
    errors: np.ndarray,
    save_path: Path,
    *,
    title: str,
    ylabel: str,
    xlabel: str = "time [s]",
    legend_labels: list[str] | None = None,
) -> None:
    _prepare_path(save_path)
    fig, ax = plt.subplots(figsize=(9, 4.8))
    if errors.ndim == 1:
        ax.plot(times, errors, linewidth=2.0)
    else:
        if legend_labels is None:
            legend_labels = [f"series_{idx}" for idx in range(errors.shape[1])]
        for index in range(errors.shape[1]):
            ax.plot(times, errors[:, index], linewidth=2.0, label=legend_labels[index])
        ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def plot_rmse_vs_noise(
    noise_levels: np.ndarray,
    series: Mapping[str, np.ndarray],
    save_path: Path,
    *,
    title: str,
    ylabel: str,
) -> None:
    _prepare_path(save_path)
    fig, ax = plt.subplots(figsize=(8.5, 5))
    for label, values in series.items():
        ax.plot(noise_levels, values, marker="o", linewidth=2.0, label=label)
    ax.set_title(title)
    ax.set_xlabel("angle noise std [rad]")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def plot_condition_numbers(times: np.ndarray, values: np.ndarray, save_path: Path) -> None:
    _prepare_path(save_path)
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.semilogy(times, values, linewidth=2.0)
    ax.set_title("Condition Number of the Linear System")
    ax.set_xlabel("time [s]")
    ax.set_ylabel("cond")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)
