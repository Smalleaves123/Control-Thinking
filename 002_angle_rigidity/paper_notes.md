# Paper Notes

This paper introduces angle rigidity for planar multiagent formations. Instead of distance constraints or bearing constraints, the shape is described by ordered angle constraints on triples of vertices.

The basic object is an angularity `A(V, A, p)`, where `V` is the vertex set, `A` is a set of ordered triplets, and `p` is the stacked configuration. A triplet `(i, j, k)` describes the signed angle from ray `j -> i` to ray `j -> k`.

The paper separates several related ideas:

- Equivalent angularities preserve the specified triplet angles.
- Congruent angularities preserve all inter-vertex angles.
- Global angle rigidity requires every equivalent angularity to be congruent.
- Local angle rigidity only requires this in a neighborhood of the current configuration.
- Infinitesimal angle rigidity is checked through the rank of the angle rigidity matrix.

The most useful computational result for reproduction is:

```text
rank(R_a(p)) = 2N - 4
```

When this rank condition holds, the only infinitesimal motions preserving all specified angles are translation, rotation, and scaling. These four degrees of freedom are unavoidable because angles do not change under those transformations.

For formation control, the paper uses angle-only feedback. The important point is that the measured angle error is a scalar and is independent of the local coordinate frame. This is why the angle-based controller can tolerate misaligned agent frames while a bearing-based controller generally cannot.
