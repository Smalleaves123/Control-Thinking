# Algorithm Summary

## 1. Aligned Three-Follower Relative Localization

This is the recommended first implementation target.

## 2. Inputs

The algorithm uses measurements from two consecutive time steps $k$ and $k+1$.

Required inputs:

- signed angles $\alpha_{mij}[k]$, $\alpha_{ijm}[k]$, $\alpha_{jmi}[k]$;
- signed angles $\alpha_{mij}[k+1]$, $\alpha_{ijm}[k+1]$, $\alpha_{jmi}[k+1]$;
- self-displacements $\Delta p_i[k]$, $\Delta p_j[k]$, $\Delta p_m[k]$.

## 3. Outputs

The outputs are

$$
p_{mi}[k],
\quad
p_{ji}[k].
$$

These are the relative positions from robot $i$ to robot $m$ and from robot $i$ to robot $j$.

## 4. Procedure

First, compute the relative self-displacements:

$$
\Delta p_{mi}[k] = \Delta p_m[k] - \Delta p_i[k],
$$

and

$$
\Delta p_{ji}[k] = \Delta p_j[k] - \Delta p_i[k].
$$

Second, construct the matrix $B_1(k,k+1)$ and vector $c_1(k,k+1)$.

Third, solve the linear system

$$
B_1(k,k+1)p_{mi}[k] = c_1(k,k+1).
$$

Fourth, recover $p_{ji}[k]$ using

$$
p_{ji}[k]
=
\frac{\sin(\alpha_{jmi}[k])}{\sin(\alpha_{ijm}[k])}
R(\alpha_{mij}[k])p_{mi}[k].
$$

Finally, compare the estimates with ground-truth relative positions.

## 5. Pseudocode

Use the following implementation logic:

- Generate or load three robot trajectories.
- Compute signed angle measurements.
- Compute self-displacements.
- For each valid time step $k$, construct $B_1(k,k+1)$ and $c_1(k,k+1)$.
- Check whether $B_1(k,k+1)$ is well-conditioned.
- Solve for $p_{mi}[k]$.
- Recover $p_{ji}[k]$.
- Compute localization errors.
- Plot trajectories and error curves.

## 6. Unaligned Case

For unaligned coordinate frames, the unknown vector becomes

$$
x
=
\begin{bmatrix}
p_{mi}^i[k] \\
r_{mi} \\
r_{ji}
\end{bmatrix}.
$$

The algorithm uses four time steps and solves

$$
B_4(k:k+3)x = c_4(k:k+3).
$$

This should be implemented after the aligned case is fully verified.

## 7. Recommended Implementation Order

1. Implement $R(\theta)$.
2. Implement signed angle computation.
3. Generate synthetic three-robot trajectories.
4. Compute self-displacements.
5. Implement aligned linear localization.
6. Plot estimated relative positions and errors.
7. Add condition-number checks.
8. Add noise experiments.
9. Implement the unaligned case.
