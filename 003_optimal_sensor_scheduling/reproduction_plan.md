# Reproduction Plan

## Stage 1: Single-Sensor Building Blocks

- Implement local steady-state Kalman covariance.
- Implement remote error trace as a function of holding time.
- Implement threshold-policy average error and Whittle index.

## Stage 2: Small Optimal Policy Example

- Implement finite-grid relative value iteration for `n = 2, m = 1`.
- Reproduce the two policy plots with and without communication costs.

## Stage 3: Large-Scale Heuristic Comparison

- Implement max-error-first, max-delay-first, original index, and revised index policies.
- Generate the paper's random first-order systems and compare average total costs.
- Plot the ratio of active sensors under the revised index policy.

## Stage 4: Reporting

- Save figures to `results/figures`.
- Save JSON metrics to `results/logs`.
- Summarize observations in `experiment_report.md`.
