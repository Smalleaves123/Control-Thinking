# Experiment Report

This file is reserved for local or server-run results.

The scripts write figures to `results/figures` and JSON metrics to `results/logs`. Those generated files are ignored by git by default, so this report can be updated after stable runs are collected.

Recommended run order:

```bash
octave --quiet --eval "run('scripts/run_two_sensor_policy_example.m')"
octave --quiet --eval "run('scripts/run_heuristic_comparison.m')"
```

Expected checks:

- The `n = 2, m = 1` optimal policy should show a monotone switching boundary.
- Positive transmission costs should create a region where scheduling no sensor is optimal.
- The revised Whittle-index policy should beat max-error-first and max-delay-first on average in the large random benchmark.

For quick local verification, the benchmark script uses lighter default Monte Carlo settings than the paper. The heavier paper-scale settings are kept as comments in the script for server runs.
