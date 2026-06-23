# Relative Localizability and Localization for Multirobot Systems

## Paper Information

- Title: Relative Localizability and Localization for Multirobot Systems
- Authors: Liangming Chen, Chenyang Liang, Shenghai Yuan, Muqing Cao, Lihua Xie
- Venue: IEEE Transactions on Robotics
- Year: 2025
- DOI: `10.1109/TRO.2025.3544103`
- Topic: Multi-robot relative localization
- Main keywords: relative localization, relative localizability, multi-robot systems, signed angle measurements, self-displacement, algebraic localization

## Citation

Use the published paper citation below when referencing this project:

L. Chen, C. Liang, S. Yuan, M. Cao and L. Xie, "Relative Localizability and Localization for Multirobot Systems," in IEEE Transactions on Robotics, vol. 41, pp. 2931-2949, 2025, doi: 10.1109/TRO.2025.3544103.

The repository keeps the reproduction code and notes. The original paper PDF is not intended to be pushed with the project.

## Environment Setup

Create a local Python environment and install dependencies:

```bash
git clone https://github.com/Smalleaves123/Control-Thinking.git
cd Control-Thinking/001_relative_localizability
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Dependencies used by the code:

- `numpy`
- `matplotlib`
- `PyYAML`
- `scipy`

## How To Run

Run the scripts from the project directory:

```bash
cd Control-Thinking/001_relative_localizability
```

### 1. Aligned Three-Follower Case

```bash
python3 scripts/run_aligned_three_robot_case.py
```

Or explicitly pass the config:

```bash
python3 scripts/run_aligned_three_robot_case.py --config configs/aligned_three_robot_case.yaml
```

### 2. Unaligned Three-Follower Case

```bash
python3 scripts/run_unaligned_three_robot_case.py
```

Or:

```bash
python3 scripts/run_unaligned_three_robot_case.py --config configs/unaligned_three_robot_case.yaml
```

### 3. Noise Robustness Experiment

```bash
python3 scripts/run_noise_robustness_test.py
```

Or:

```bash
python3 scripts/run_noise_robustness_test.py --config configs/noise_robustness_test.yaml
```

### 4. Simplified Mixed Topology Example

```bash
python3 scripts/run_general_topology_case.py
```

Or:

```bash
python3 scripts/run_general_topology_case.py --config configs/general_topology_case.yaml
```

### 5. Aggregate Saved Metrics

```bash
python3 scripts/evaluate_results.py
```

## Output Locations

- figures: `results/figures`
- metrics logs: `results/logs`
- optional tables: `results/tables`

## Notes For Local And Server Runs

- The aligned and unaligned scripts finish quickly on a normal local machine.
- The noise robustness script is the most computationally expensive because the robust part solves the paper objective with constrained trust-region optimization.
- If you want to run on a server later, copy the repository, create a fresh virtual environment, install `requirements.txt`, and run the same commands there.
- Generated result files are ignored by git, so local experiments will not be pushed by default.

## Short Summary

This paper studies the problem of relative localization in multi-robot systems when robots cannot directly measure full relative position vectors. Instead, each robot may only have partial inter-robot measurements, such as distances, bearings, or angles, together with its own self-displacement obtained from odometry.

The main idea is to determine whether the available measurements are sufficient to uniquely recover inter-agent relative positions. The paper introduces the concept of relative localizability and proposes algebraic, distributed relative localization algorithms for multi-robot systems consisting of followers, leaders, and landmarks.

A key contribution is that the method can also handle unaligned local coordinate frames. In this case, the algorithm can simultaneously estimate inter-robot relative positions and relative orientations between local coordinate frames.

## Why This Paper Is Relevant

This paper is a good starting point for a multi-agent paper reproduction repository because:

- It is directly related to multi-robot localization.
- It does not require ROS2, Isaac Sim, or heavy 3D simulation.
- The core algorithms can be reproduced with Python, NumPy, and Matplotlib.
- The first reproduction target can be reduced to a clean three-robot 2D simulation.
- The paper naturally connects to later topics such as formation control, angle rigidity, SLAM, and sensor-based estimation.

## Main Problem

In a multi-robot system, relative positions are essential for tasks such as formation control, collaborative inspection, and coordinated navigation. However, practical sensors often provide only partial relative information.

The paper asks:

1. Can self-displacement and partial inter-robot measurements uniquely determine relative positions?
2. How can one check whether a general multi-robot system is relatively localizable?
3. Can relative localization still be achieved when robots have unaligned coordinate frames?
4. Can relative orientations between local coordinate frames be recovered from local measurements?

## Repository Files

Suggested reading order:

1. `paper_notes.md`
2. `problem_formulation.md`
3. `method_overview.md`
4. `algorithm_summary.md`
5. `reproduction_plan.md`
6. `critical_analysis.md`
7. `future_improvements.md`

## Suggested First Reproduction Target

The recommended first target is the aligned three-follower case.

In this setting:

- There are three followers: robot i, robot j, and robot m.
- Their coordinate frames are aligned.
- Each robot can measure its self-displacement.
- The robots can measure signed interior angles within the triangle formed by them.
- The goal is to recover relative positions using a linear algebraic equation.

Expected outputs:

- `three_robot_trajectories.png`
- `relative_position_estimation.png`
- `relative_position_error.png`
- `rmse_vs_noise_level.png`
