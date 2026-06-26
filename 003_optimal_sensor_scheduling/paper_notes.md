# Paper Notes

This paper studies centralized scheduling of multiple sensors that monitor independent linear systems and send local state estimates to a remote estimator over lossy and bandwidth-limited channels.

Each process has a local Kalman filter, so the remote estimation error depends only on the holding time: the number of steps since the last successful packet reception. This converts the scheduling problem from a matrix-valued remote estimation problem into an MDP over integer states.

The main technical results are:

- a sufficient condition for existence of an optimal deterministic stationary policy;
- monotonicity of optimal policies with respect to holding time;
- indexability of the decoupled problem;
- an analytic Whittle index formula that avoids iterative per-state index computation.

The numerical examples in the paper have two roles:

- show the switching-boundary structure of optimal policies in small dimensions;
- compare Whittle-index scheduling against max-error-first and max-delay-first heuristics in larger systems.
