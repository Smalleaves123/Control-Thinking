# Problem Formulation

There are `n` independent linear dynamic processes

```text
x_{k+1}^{(i)} = A_i x_k^{(i)} + w_k^{(i)}
y_k^{(i)} = C_i x_k^{(i)} + v_k^{(i)}.
```

Each sensor runs a local Kalman filter and sends its local estimate to a remote estimator when scheduled. At each time step, at most `m` sensors may transmit, and each scheduled transmission succeeds with probability `lambda_i`.

The remote estimator keeps track of the holding time

```text
tau_k^{(i)} = time elapsed since the last successful packet from sensor i.
```

Because the local estimator is in steady state, the remote estimation covariance for process `i` becomes a deterministic function of `tau_k^{(i)}`:

```text
P_k^{(i)} = h_i^{tau_k^{(i)}}(P_i).
```

The paper minimizes the infinite-horizon average cost

```text
sum_i Tr(P_k^{(i)}) + c_c^{(i)} a_k^{(i)}
```

subject to the hard bandwidth constraint

```text
sum_i a_k^{(i)} <= m.
```
