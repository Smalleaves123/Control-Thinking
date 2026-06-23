# Reproduction Plan

## 1. Overall Goal

The goal is to reproduce the core ideas of the paper using lightweight 2D simulation.

The first reproduction should focus on clarity, correctness, and visualization rather than full coverage of all cases.

## 2. Stage 1: Aligned Three-Follower Case

This is the minimal reproduction target.

### Tasks

- Generate trajectories for three robots in 2D.
- Compute ground-truth relative positions.
- Compute signed interior angles.
- Compute self-displacements.
- Construct the linear system for the aligned case.
- Estimate relative positions.
- Compare estimates with ground truth.

### Expected Figures

- `three_robot_trajectories.png`
- `relative_position_estimation.png`
- `relative_position_error.png`

### Evaluation Metrics

- relative position error,
- RMSE over time,
- matrix condition number of B1.

## 3. Stage 2: Noise Robustness for the Aligned Case

### Tasks

- Add Gaussian noise to angle measurements.
- Add Gaussian noise to self-displacements.
- Run multiple random trials.
- Plot localization error under different noise levels.

### Expected Figures

- `rmse_vs_noise_level.png`
- `error_curve_under_noise.png`

## 4. Stage 3: Unaligned Three-Follower Case

### Tasks

- Assign different fixed coordinate-frame orientations to each robot.
- Express self-displacements in each robot's local frame.
- Construct the larger linear system for the unaligned case.
- Estimate relative positions and relative orientations.

### Expected Figures

- `relative_position_error_unaligned.png`
- `relative_orientation_error.png`

## 5. Stage 4: Robust Algorithm

### Tasks

- Use the linear solution as initialization.
- Implement or approximate the robust refinement step.
- Compare the linear method and robust method under increasing noise levels.

### Expected Figures

- `linear_vs_robust_rmse.png`
- `rmse_vs_number_of_time_instants.png`

## 6. Stage 5: Extension to General Topology

### Tasks

- Create a small system with followers, leaders, and landmarks.
- Define effective triangles.
- Implement a simplified version of the general relative localization logic.
- Analyze which parts of the system are relatively localizable.

### Expected Figures

- `mixed_agent_topology.png`
- `general_topology_localization_error.png`

## 7. Minimal Deliverable

The minimal deliverable for the first version is:

- aligned three-follower simulation,
- clean plots,
- error metrics,
- a short experiment report,
- a failure case showing when the method becomes ill-conditioned.
