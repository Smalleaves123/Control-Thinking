# Reproduction Plan

The reproduction is organized around the simulation examples in Section V.

## Stage 1: Core Geometry

- Implement 2-D bearings, angles, and projection matrices.
- Implement ordered triplet angle evaluation.
- Add the paper's five-agent initial condition and desired angle set.

## Stage 2: Rigidity Check

- Build `R_a(p)` from the seven angle constraints.
- Verify that the final or desired formation reaches `rank(R_a) = 2N - 4`.
- Save a small rank summary plot and JSON metrics.

## Stage 3: Angle-Only Formation Control

- Run equation (58) on the five-agent system.
- Include a 5 degree local-frame misalignment for agent 1.
- Save trajectory and angle-error figures.

## Stage 4: Bearing Comparison

- Run the bearing-based controller without frame misalignment.
- Run the same controller with agent 1's frame misaligned.
- Compare final bearing errors and trajectory deformation.

## Stage 5: Result Write-Up

- After server runs, copy the generated figures and JSON logs into `results/`.
- Summarize final angle errors, rank, and bearing comparison metrics in `experiment_report.md`.
- Do not commit generated result files unless a report specifically needs selected figures.
