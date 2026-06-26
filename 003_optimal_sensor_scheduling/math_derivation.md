# Math Derivation

For each sensor `i`, the remote estimator error under holding time `tau` is

```text
P^{(i)}(tau) = h_i^tau(P_i)
```

with

```text
h_i(X) = A_i X A_i^T + Q_i.
```

The MDP state is the stacked holding-time vector

```text
s = [tau^(1), ..., tau^(n)]^T in N^n.
```

If sensor `i` is scheduled, the next holding time resets to `0` with probability `lambda_i` and increases by one otherwise. If it is not scheduled, the holding time always increases by one.

The single-sensor relaxed problem leads to a threshold policy and the paper derives the Whittle index

```text
w_i(tau) = lambda_i (lambda_i tau + 1) / (1 - lambda_i)
           * ((tau + 1) J_e^(i)(tau) - sum_{t=0}^tau c_e^(i)(t))
           - c_c^(i)
```

where `J_e^(i)(tau)` is the time-averaged estimation error under the threshold policy with threshold `tau`.

This closed form is the key practical contribution because it avoids solving a Bellman equation for every index value.
