# Method Overview

## 1. Core Idea

This paper studies relative localization in multi-robot systems. The goal is to recover inter-agent relative positions from partial inter-agent measurements and robot self-displacements.

The key idea is to convert geometric constraints induced by signed angles, distances, or bearings into algebraic equations involving relative positions.

For the first reproduction, the most important case is the three-follower case with aligned coordinate frames.

## 2. Three-Follower Case With Aligned Coordinate Frames

Consider three followers $i$, $j$, and $m$ in the plane. Their coordinate frames are assumed to be aligned.

Let

$$
p_{ji}[k] = p_j[k] - p_i[k],
$$

and

$$
p_{mi}[k] = p_m[k] - p_i[k].
$$

Here, $p_{ji}[k]$ is the relative position from robot $i$ to robot $j$, and $p_{mi}[k]$ is the relative position from robot $i$ to robot $m$ at time step $k$.

The signed interior angles of triangle $\triangle ijm$ are denoted by

$$
\alpha_{mij}[k], \quad \alpha_{ijm}[k], \quad \alpha_{jmi}[k].
$$

Using the law of sines and the signed angle relation, the paper derives the following angle-induced linear equation:

$$
\sin(\alpha_{ijm}[k])p_{ji}[k]
=
\sin(\alpha_{jmi}[k])R(\alpha_{mij}[k])p_{mi}[k].
$$

This equation is valid when the three robots are not collinear.

## 3. Using Self-Displacement

Each robot measures its self-displacement between two consecutive time steps.

Define

$$
\Delta p_{mi}[k] = \Delta p_m[k] - \Delta p_i[k],
$$

and

$$
\Delta p_{ji}[k] = \Delta p_j[k] - \Delta p_i[k].
$$

Then the relative positions satisfy

$$
p_{mi}[k+1] = p_{mi}[k] + \Delta p_{mi}[k],
$$

and

$$
p_{ji}[k+1] = p_{ji}[k] + \Delta p_{ji}[k].
$$

By substituting these relations into the angle-induced equation at time $k+1$, the paper obtains a linear system:

$$
B_1(k,k+1)p_{mi}[k] = c_1(k,k+1).
$$

If $B_1(k,k+1)$ is invertible, then

$$
p_{mi}[k] = B_1^{-1}(k,k+1)c_1(k,k+1).
$$

After $p_{mi}[k]$ is recovered, $p_{ji}[k]$ can be obtained from the angle-induced linear equation.

## 4. Three-Follower Case With Unaligned Coordinate Frames

When coordinate frames are not aligned, the self-displacement measured by robot $m$ is expressed in robot $m$'s local frame, not in robot $i$'s local frame.

The transformation is written as

$$
\Delta p_m^i[k] = R_m^i \Delta p_m^m[k],
$$

where $R_m^i$ is the rotation matrix from frame $m$ to frame $i$.

The paper parameterizes this unknown relative orientation by

$$
r_{mi}
=
\begin{bmatrix}
\cos \theta_{mi} \\
\sin \theta_{mi}
\end{bmatrix}.
$$

In this case, the unknown variables include both relative positions and relative orientations:

$$
x
=
\begin{bmatrix}
p_{mi}^i[k] \\
r_{mi} \\
r_{ji}
\end{bmatrix}.
$$

Using measurements from four time steps, the paper constructs a larger linear system:

$$
B_4(k:k+3)
\begin{bmatrix}
p_{mi}^i[k] \\
r_{mi} \\
r_{ji}
\end{bmatrix}
=
c_4(k:k+3).
$$

If $B_4(k:k+3)$ is invertible, then the relative position and relative orientations can be recovered.

## 5. Relative Localizability

The paper introduces the concept of relative localizability.

A multi-robot system is called $d$-step relatively localizable if its inter-agent relative positions can be uniquely determined from measurements collected over $d$ sampling instants.

The key idea is that relative localizability depends on both the measurement topology and the number of sampling instants.

For the aligned coordinate-frame case, the basic three-follower setting can be solved using two sampling instants.

For the unaligned coordinate-frame case, the paper uses four sampling instants to estimate both relative positions and relative orientations.
