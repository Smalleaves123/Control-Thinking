# Math Derivation

For a triplet `(i, j, k)`, the angle derivative can be written as

```text
d beta / dt = N_kji p_dot_i - (N_kji + N_ijk) p_dot_j + N_ijk p_dot_k.
```

The row of the angle rigidity matrix is formed by placing these three vector blocks in the columns for vertices `i`, `j`, and `k`.

The terms are:

```text
N_kji = - z_jk^T P_zji / (l_ji sin(beta))
N_ijk = - z_ji^T P_zjk / (l_jk sin(beta))
P_z   = I - z z^T
```

The full matrix has one row per angle constraint and `2N` columns. Four infinitesimal motions always preserve all angles:

- translation in x;
- translation in y;
- rotation;
- scaling.

Therefore,

```text
rank(R_a(p)) <= 2N - 4.
```

The paper's infinitesimal angle-rigidity condition is:

```text
rank(R_a(p)) = 2N - 4.
```

In the five-agent example, `N = 5`, so the maximum rank is `6`. The chosen angle constraints are expected to reach this rank.
