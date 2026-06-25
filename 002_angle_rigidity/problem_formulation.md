# Problem Formulation

Consider `N` planar agents with positions

```text
p_i in R^2,    i = 1, ..., N.
```

The formation shape is not prescribed by absolute positions. Instead, it is prescribed by a set of angle constraints. For every ordered triplet `(i, j, k)`, the constraint is the angle at vertex `j` from ray `j -> i` to ray `j -> k`.

The questions studied in the paper are:

1. When do the selected angle constraints determine the local formation shape up to translation, rotation, and scaling?
2. How can this be checked from a rigidity matrix?
3. Can a formation be stabilized using only local angle measurements?
4. What happens when each agent's local coordinate frame is not aligned with the global frame?

For reproduction, the main target is the five-agent formation in Section V. The desired angle set is:

```text
alpha_213 = pi / 4
alpha_132 = pi / 4
alpha_321 = pi / 2
alpha_342 = arctan(0.5)
alpha_241 = arctan(0.5)
alpha_254 = arctan(0.5)
alpha_152 = arctan(3 / sqrt(10))
```

The initial positions are:

```text
p1(0) = [ 0.8, 0.2]^T
p2(0) = [ 0.1, 1.4]^T
p3(0) = [-1.4, 0.3]^T
p4(0) = [ 0.1, 2.3]^T
p5(0) = [-1.7, 1.6]^T
```
