# Mathematical Derivation Overview

This file summarizes the main mathematical structure needed for the first reproduction. The goal is not to reproduce every proof in the paper, but to connect the paper's equations with implementation variables.

## 1. Rotation Matrix

In 2D, the rotation matrix is

$$
R(\theta)
=
\begin{bmatrix}
\cos\theta & -\sin\theta \\
\sin\theta & \cos\theta
\end{bmatrix}.
$$

This matrix rotates a 2D vector counterclockwise by angle $\theta$.

## 2. Relative Position Vectors

For robots $i$, $j$, and $m$, define

$$
p_{ji}[k] = p_j[k] - p_i[k],
$$

and

$$
p_{mi}[k] = p_m[k] - p_i[k].
$$

These are the relative positions from robot $i$ to robot $j$ and from robot $i$ to robot $m$.

## 3. Signed Interior Angle

The signed interior angle at robot $i$ with respect to robots $j$ and $m$ is denoted by

$$
\alpha_{jim}[k].
$$

It is measured from vector $i \rightarrow j$ to vector $i \rightarrow m$ in the counterclockwise direction.

For implementation, define

$$
b_{ij} = \frac{p_j - p_i}{\|p_j - p_i\|},
\quad
b_{im} = \frac{p_m - p_i}{\|p_m - p_i\|}.
$$

Then the signed angle can be computed as

$$
\alpha_{jim}
=
\operatorname{atan2}
\left(
b_{ij,x}b_{im,y} - b_{ij,y}b_{im,x},
b_{ij}^{T}b_{im}
\right).
$$

## 4. Angle-Induced Linear Equation

For the aligned three-follower case, the paper derives

$$
\sin(\alpha_{ijm}[k])p_{ji}[k]
=
\sin(\alpha_{jmi}[k])R(\alpha_{mij}[k])p_{mi}[k].
$$

This is the core geometric relation. It converts angle measurements into a linear relation between relative position vectors.

## 5. Relative Motion Between Two Time Steps

The relative positions evolve as

$$
p_{mi}[k+1] = p_{mi}[k] + \Delta p_{mi}[k],
$$

and

$$
p_{ji}[k+1] = p_{ji}[k] + \Delta p_{ji}[k],
$$

where

$$
\Delta p_{mi}[k] = \Delta p_m[k] - \Delta p_i[k],
$$

and

$$
\Delta p_{ji}[k] = \Delta p_j[k] - \Delta p_i[k].
$$

## 6. Linear System for the Aligned Case

By combining the angle-induced linear equations at time $k$ and $k+1$, the paper obtains

$$
B_1(k,k+1)p_{mi}[k] = c_1(k,k+1).
$$

The solution is

$$
p_{mi}[k] = B_1^{-1}(k,k+1)c_1(k,k+1),
$$

when $B_1(k,k+1)$ is nonsingular.

In code, it is better to solve the system using `numpy.linalg.solve` instead of explicitly computing the inverse.

## 7. Recovering the Remaining Relative Position

After $p_{mi}[k]$ is estimated, $p_{ji}[k]$ can be obtained from

$$
p_{ji}[k]
=
\frac{\sin(\alpha_{jmi}[k])}{\sin(\alpha_{ijm}[k])}
R(\alpha_{mij}[k])p_{mi}[k].
$$

This gives both relative vectors needed for the three-robot case.

## 8. Degenerate Cases

The method can fail or become numerically unstable when:

1. the three robots are collinear;
2. the triangle at time $k$ and time $k+1$ is strongly similar;
3. the motion between two time steps is too small;
4. $B_1(k,k+1)$ is singular or ill-conditioned.

In implementation, check the condition number:

$$
\kappa(B_1) = \|B_1\| \|B_1^{-1}\|.
$$

A large value of $\kappa(B_1)$ indicates an ill-conditioned localization problem.
