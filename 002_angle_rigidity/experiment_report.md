# Experiment Report

This file is reserved for server-run results.

The scripts write figures to `results/figures` and JSON metrics to `results/logs`. Those generated files are ignored by git by default, so this report can be updated after stable runs are collected.

Recommended run order:

```bash
python3 scripts/run_angle_control.py
python3 scripts/run_bearing_comparison.py
```

Expected checks:

- The angle-based controller should reduce all seven angle errors.
- The final angle rigidity matrix should reach rank `2N - 4 = 6` for the five-agent example.
- Bearing control should behave better without frame misalignment than with the 5 degree misalignment.
