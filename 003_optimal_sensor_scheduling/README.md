# Optimal Scheduling of Multiple Sensors Over Lossy and Bandwidth Limited Channels

## Paper Information

- Title: Optimal Scheduling of Multiple Sensors Over Lossy and Bandwidth Limited Channels
- Authors: Shuang Wu, Kemi Ding, Peng Cheng, Ling Shi
- Venue: IEEE Transactions on Control of Network Systems
- Volume/issue: vol. 7, no. 3
- Pages: 1188-1197
- Year: 2020
- DOI: `10.1109/TCNS.2020.2966671`
- Topic: sensor scheduling, remote estimation, Whittle index, lossy communication, MDP

## Citation

Use the published paper citation below when referencing this project:

S. Wu, K. Ding, P. Cheng and L. Shi, "Optimal Scheduling of Multiple Sensors Over Lossy and Bandwidth Limited Channels," IEEE Transactions on Control of Network Systems, vol. 7, no. 3, pp. 1188-1197, Sept. 2020, doi: 10.1109/TCNS.2020.2966671.

The repository keeps notes and reproduction code only. The original paper PDF is not pushed.

## Environment Setup

Install MATLAB R2020b or newer, or use a recent Octave version. The current scripts use base MATLAB-style functions only and are intended to run in Octave as well.

```bash
git clone https://github.com/Smalleaves123/Control-Thinking.git
cd Control-Thinking/003_optimal_sensor_scheduling
```

See `requirements.md` for the environment note.

## How To Run

Run all commands from the project directory:

```bash
cd Control-Thinking/003_optimal_sensor_scheduling
```

### 1. Two-Sensor Optimal Policy Visualization

This reproduces the `n = 2, m = 1` numerical example used in the paper to show the monotone structure of the optimal policy.

```bash
octave --quiet --eval "run('scripts/run_two_sensor_policy_example.m')"
matlab -batch "run('scripts/run_two_sensor_policy_example.m')"
```

### 2. Heuristic Performance Comparison

This reproduces the large-scale comparison among max-error-first, max-delay-first, original Whittle index, and revised Whittle index policies.

```bash
octave --quiet --eval "run('scripts/run_heuristic_comparison.m')"
matlab -batch "run('scripts/run_heuristic_comparison.m')"
```

The benchmark script uses local-friendly default settings by default. The paper-scale `horizon = 1000` and `trials = 100` are noted inside the script for later server runs.

## Output Locations

- figures: `results/figures`
- metrics logs: `results/logs`
- optional tables: `results/tables`

Generated result files are ignored by git. Keep the figures and logs locally for analysis, or copy them from the server after running the scripts.

## What Is Implemented

- Kalman steady-state local estimator covariance for each process.
- Remote estimation error as a function of holding time.
- Feasibility grouping check from Algorithm 1.
- Relative value iteration on a truncated state grid for the `n = 2` policy plots.
- Closed-form Whittle index evaluation from Theorem 3.
- Four scheduling heuristics used in the paper's performance comparison.

## Reading Order

Suggested reading order for the notes:

1. `paper_notes.md`
2. `problem_formulation.md`
3. `method_overview.md`
4. `math_derivation.md`
5. `algorithm_summary.md`
6. `reproduction_plan.md`
7. `critical_analysis.md`
8. `future_improvements.md`

## Reproduction Scope

This reproduction focuses on the computational core of the paper:

- holding-time-based MDP formulation;
- monotone optimal policies for the small example;
- Whittle index heuristic for large-scale scheduling;
- empirical comparison against common heuristics.
