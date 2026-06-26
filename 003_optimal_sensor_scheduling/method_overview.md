# Method Overview

The reproduction follows the paper in three layers.

First, compute the local steady-state Kalman covariance `P_i` and the open-loop operator `h_i(X) = A_i X A_i^T + Q_i`. This gives the remote estimation error trace as a function of holding time.

Second, formulate the small-dimensional scheduling problem as an MDP over holding times. For `n = 2`, we solve a truncated version using relative value iteration and visualize the optimal policy on the `(tau_1, tau_2)` plane.

Third, implement the Whittle-index heuristic from the paper. The hard transmission constraint is relaxed into decoupled single-sensor problems, and the analytic index expression is evaluated for each sensor state. This lets us compare:

- max-error-first;
- max-delay-first;
- original Whittle index;
- revised Whittle index that also respects positive net utility.
