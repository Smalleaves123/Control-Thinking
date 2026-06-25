# Algorithm Summary

## Angle Rigidity Matrix

1. Read positions `p`.
2. For each ordered triplet `(i, j, k)`, compute the two bearings from center vertex `j`.
3. Compute the angle derivative blocks `N_kji` and `N_ijk`.
4. Insert the three blocks into one row of `R_a(p)`.
5. Check whether `rank(R_a(p))` equals `2N - 4`.

## Angle-Based Formation Control

1. For each angle constraint centered at agent `i`, measure `alpha_jik`.
2. Compute the scalar angle error `alpha_jik - alpha_jik*`.
3. Compute the local direction `z_ij + z_ik`.
4. Add `-(alpha_jik - alpha_jik*) (z_ij + z_ik)` to agent `i`'s control input.
5. Integrate the single-integrator dynamics with Euler integration.

## Bearing-Based Comparison

1. For each directed bearing constraint `(i, j)`, compute current bearing `z_ij`.
2. Project the desired bearing through `P_zij = I - z_ij z_ij^T`.
3. Apply the bearing controller from the paper.
4. Repeat once with aligned frames and once with a 5 degree frame misalignment.
