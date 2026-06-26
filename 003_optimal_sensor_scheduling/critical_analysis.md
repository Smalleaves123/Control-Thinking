# Critical Analysis

The paper's main advantage is the modeling simplification from covariance matrices to holding times. Once each sensor maintains a local Kalman filter, the remote scheduling state becomes scalar per process, which makes structural results feasible.

The main practical limitation is that the exact optimal MDP still suffers from the curse of dimensionality. The paper addresses this by proving monotonicity and by using a Whittle-index heuristic, but the asymptotic optimality claim is not the same as exact finite-size optimality.

Another limitation is that the channel success probabilities are assumed known and stationary. In practice, if channel quality drifts over time, the scheduling logic would need online learning or adaptive estimation.

For this repository, the clearest validation target is not proving every theorem, but reproducing the numerical behavior:

- monotone switching boundaries in the small example;
- revised Whittle index outperforming simple heuristics in larger random systems.
