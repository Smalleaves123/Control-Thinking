# Control-Thinking

This repository collects paper-reading notes and code reproductions around multi-agent control, localization, and related estimation problems.

## Projects

- [001_relative_localizability](001_relative_localizability/README.md): reproduction of the paper *Relative Localizability and Localization for Multirobot Systems*.
- [002_angle_rigidity](002_angle_rigidity/README.md): reproduction of the paper *Angle Rigidity and Its Usage to Stabilize Multiagent Formations in 2-D*.
- [003_optimal_sensor_scheduling](003_optimal_sensor_scheduling/README.md): reproduction of the paper *Optimal Scheduling of Multiple Sensors Over Lossy and Bandwidth Limited Channels*.

## Quick Start

The current runnable projects are `001_relative_localizability`, `002_angle_rigidity`, and `003_optimal_sensor_scheduling`.

```bash
git clone https://github.com/Smalleaves123/Control-Thinking.git
cd Control-Thinking/001_relative_localizability
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the main scripts:

```bash
python3 scripts/run_aligned_three_robot_case.py
python3 scripts/run_unaligned_three_robot_case.py
python3 scripts/run_noise_robustness_test.py
python3 scripts/run_general_topology_case.py
python3 scripts/evaluate_results.py
```

For the angle-rigidity project:

```bash
cd ../002_angle_rigidity
matlab -batch "run('scripts/run_angle_control.m')"
matlab -batch "run('scripts/run_bearing_comparison.m')"
```

For the optimal-scheduling project:

```bash
cd ../003_optimal_sensor_scheduling
octave --quiet --eval "run('scripts/run_two_sensor_policy_example.m')"
octave --quiet --eval "run('scripts/run_heuristic_comparison.m')"
```

Generated outputs:

- figures: `001_relative_localizability/results/figures`
- metrics logs: `001_relative_localizability/results/logs`
- angle-rigidity figures: `002_angle_rigidity/results/figures`
- angle-rigidity metrics logs: `002_angle_rigidity/results/logs`
- optimal-scheduling figures: `003_optimal_sensor_scheduling/results/figures`
- optimal-scheduling metrics logs: `003_optimal_sensor_scheduling/results/logs`

The repository is configured not to push generated result files or the original paper PDF.
