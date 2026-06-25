# Critical Analysis

The paper's main strength is that it separates shape information from coordinate-frame alignment. Angles are invariant under local frame rotations, so the angle-error feedback can be implemented by agents with different local frames.

There are also practical limits:

- Angle rigidity is local in general. A formation can be locally rigid but still have globally ambiguous realizations.
- The stability result for adding agents is local and depends on the initial formation being close enough to the desired shape.
- The control laws assume nondegenerate angles. Collinear or near-collision configurations can make the angle derivative and feedback ill-conditioned.
- The simulation is planar and single-integrator. Real robot dynamics would need an additional tracking or low-level control layer.

For this repository, the most important check is whether the implemented `R_a(p)` and controller reproduce the qualitative result: angle control remains robust to frame misalignment, while bearing control does not.
