# Experiment Report

## Overview

This report summarizes the current reproduction results for the paper
*Relative Localizability and Localization for Multirobot Systems*.
The reported figures and metrics are generated from the server-side run
stored in `results/figures` and `results/logs`.

The main goals of this reproduction stage are:

- verify the aligned three-follower linear localization result;
- verify the unaligned three-follower linear and robust results;
- evaluate the effect of measurement noise;
- check whether increasing the number of time instants improves the robust estimator.

## Experiment Outputs

Key generated figures:

- `results/figures/three_robot_trajectories.png`
- `results/figures/relative_position_estimation.png`
- `results/figures/relative_position_error.png`
- `results/figures/relative_position_error_unaligned.png`
- `results/figures/relative_orientation_error.png`
- `results/figures/rmse_vs_noise_level.png`
- `results/figures/linear_vs_robust_rmse.png`
- `results/figures/rmse_vs_number_of_time_instants.png`

## 1. Aligned Three-Follower Case

Metrics from `results/logs/aligned_metrics.json`:

- `rmse_pmi = 1.0497720048033503e-13`
- `rmse_pji = 6.907105711100133e-14`
- `valid_windows = 89 / 89`

These numbers are effectively at machine precision. The aligned case
therefore behaves exactly as expected in the noise-free setting, and all
89 windows remain numerically valid.

Related figures:

![Aligned trajectories](results/figures/three_robot_trajectories.png)

![Aligned relative position estimation](results/figures/relative_position_estimation.png)

![Aligned relative position error](results/figures/relative_position_error.png)

## 2. Unaligned Three-Follower Case

Metrics from `results/logs/unaligned_metrics.json`:

- `linear_position_rmse = 1.5547470428508907`
- `robust_position_rmse = 0.4077039609333382`
- `linear_orientation_rmse = 0.8108389629949352 rad`
- `robust_orientation_rmse = 0.2537805177739717 rad`

The robust stage improves both outputs substantially. Position RMSE drops
from about `1.55` to `0.41`, and orientation RMSE drops from about
`0.81 rad` to `0.25 rad`. In relative terms, this is roughly a `73.8%`
reduction in position error and a `68.7%` reduction in orientation error.
This is consistent with the role of the optimization stage in the paper.

Related figures:

![Unaligned position error](results/figures/relative_position_error_unaligned.png)

![Unaligned orientation error](results/figures/relative_orientation_error.png)

## 3. Noise Robustness

Metrics from `results/logs/noise_robustness_metrics.json` give the
following mean position RMSE values:

| Angle noise std (rad) | Aligned linear | Unaligned linear | Unaligned robust |
| --- | ---: | ---: | ---: |
| 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| 0.0015 | 0.6590 | 1.3296 | 0.2445 |
| 0.0030 | 1.9218 | 2.0935 | 0.5386 |
| 0.0050 | 1.9891 | 2.4713 | 0.8970 |
| 0.0075 | 2.9897 | 3.1405 | 1.4270 |
| 0.0100 | 3.6774 | 3.2714 | 1.8660 |
| 0.0125 | 3.1129 | 3.1297 | 2.7164 |
| 0.0150 | 3.3865 | 4.0382 | 2.8330 |

Several patterns stand out:

- At zero noise, all methods recover the relative states almost exactly.
- As noise increases, the robust unaligned solver stays consistently below
  the direct unaligned linear solver.
- The gap is already large at mild noise levels. At `0.0015 rad`, the
  robust mean RMSE is `0.2445`, while the direct unaligned solver is
  `1.3296`. At `0.0030 rad`, the gap is `0.5386` versus `2.0935`.
- At higher noise levels, the robust method still has the better mean
  result, although the spread across trials grows noticeably.

Related figures:

![RMSE vs noise](results/figures/rmse_vs_noise_level.png)

![Linear vs robust RMSE](results/figures/linear_vs_robust_rmse.png)

![Orientation error under noise](results/figures/error_curve_under_noise.png)

## 4. Effect of Increasing the Number of Time Instants

For the robust estimator at noise level `0.0030 rad`, the server run produced:

| Number of time instants d | Mean robust RMSE |
| --- | ---: |
| 4 | 1.8236 |
| 5 | 1.1803 |
| 6 | 0.5386 |
| 7 | 0.4014 |
| 8 | 0.3283 |

The trend is clean: using more time instants improves the robust estimate.
The most noticeable improvement appears between `d = 5` and `d = 6`, and
the error continues to fall through `d = 8`. This agrees with the paper's
discussion that a larger measurement window provides a better-constrained
optimization problem.

Related figure:

![Robust RMSE vs number of time instants](results/figures/rmse_vs_number_of_time_instants.png)

## 5. Mixed Topology Example

Metrics from `results/logs/general_topology_metrics.json`:

- `rmse_landmark = 0.5002624109389123`
- `rmse_leader = 0.3592559194169054`

This part of the repository is still best viewed as a constrained
demonstration rather than a full reproduction of the paper's general
topology pipeline. It is useful as a qualitative extension, but not yet as
the final word on Algorithm 4.

Related figures:

![Mixed topology](results/figures/mixed_agent_topology.png)

![Mixed topology error](results/figures/general_topology_localization_error.png)

## Final Summary

The current results support four main conclusions:

- The aligned three-follower method reproduces the exact recovery behavior
  expected from the paper in the noise-free case.
- The unaligned three-follower formulation works in both its direct linear
  form and its optimization-refined form.
- The robust stage consistently outperforms the direct linear stage once
  noise is present.
- Increasing the number of measurement instants improves the robust result,
  in line with the analysis in the paper.

The remaining limitation is that the mixed-topology script is still a simplified demonstration rather than a full general-topology implementation from the paper.
