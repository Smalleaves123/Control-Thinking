# Algorithm Summary

## Core Covariance Computation

1. Solve the local steady-state Kalman covariance for each process.
2. Repeatedly apply `h_i(X) = A_i X A_i^T + Q_i` to get remote error traces.
3. Store `c_e^(i)(tau) = Tr(h_i^tau(P_i))`.

## Small MDP Example

1. Enumerate the truncated holding-time state grid.
2. Enumerate feasible scheduling actions under `sum_i a_i <= m`.
3. Run relative value iteration until the policy stabilizes.
4. Plot the optimal decision regions.

## Whittle-Index Scheduling

1. Evaluate each sensor's current holding time `tau_i`.
2. Compute `w_i(tau_i)` using the analytic expression from Theorem 3.
3. Sort indices and schedule the top `m` sensors.
4. In the revised version, only schedule sensors with positive indices.

## Heuristic Comparison

1. Generate random first-order LTI systems.
2. Run the four policies on the same scenarios.
3. Average total cost and active-sensor ratio over Monte Carlo trials.
