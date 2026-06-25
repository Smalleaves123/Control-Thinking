"""Plotting utilities for the reproduction scripts."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def _prepare(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def plot_formation_trajectory(trajectory: np.ndarray, save_path: Path, *, title: str) -> None:
    _prepare(save_path)
    fig, ax = plt.subplots(figsize=(7.5, 6.0))
    colors = ["#0f5c4a", "#bb4430", "#345995", "#7f557d", "#d0951b"]
    for idx in range(trajectory.shape[1]):
        series = trajectory[:, idx, :]
        ax.plot(series[:, 0], series[:, 1], linewidth=2.0, color=colors[idx], label=f"agent {idx + 1}")
        ax.scatter(series[0, 0], series[0, 1], marker="o", s=35, color=colors[idx])
        ax.scatter(series[-1, 0], series[-1, 1], marker="x", s=50, color=colors[idx])
    ax.set_title(title)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.axis("equal")
    ax.grid(alpha=0.25)
    ax.legend(ncol=2)
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def plot_error_series(times: np.ndarray, errors: np.ndarray, save_path: Path, *, title: str, ylabel: str) -> None:
    _prepare(save_path)
    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    for idx in range(errors.shape[1]):
        ax.plot(times, errors[:, idx], linewidth=1.8, label=f"constraint {idx + 1}")
    ax.set_title(title)
    ax.set_xlabel("time [s]")
    ax.set_ylabel(ylabel)
    ax.grid(alpha=0.25)
    ax.legend(ncol=2)
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)


def plot_rank_bar(rank: int, expected_rank: int, save_path: Path) -> None:
    _prepare(save_path)
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.bar(["rank(Ra)", "2N-4"], [rank, expected_rank], color=["#0f5c4a", "#d0951b"])
    ax.set_ylim(0, max(rank, expected_rank) + 1)
    ax.set_title("Angle Rigidity Rank Check")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(save_path, dpi=180)
    plt.close(fig)
