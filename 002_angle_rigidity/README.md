# Angle Rigidity and Its Usage to Stabilize Multiagent Formations in 2-D

## Paper Information

- Title: Angle Rigidity and Its Usage to Stabilize Multiagent Formations in 2-D
- Authors: Liangming Chen, Ming Cao, Chuanjiang Li
- Venue: IEEE Transactions on Automatic Control
- Volume/issue: vol. 66, no. 8
- Pages: 3667-3681
- Year: 2021
- DOI: `10.1109/TAC.2020.3025539`
- Topic: angle rigidity, angularity, angle-only multiagent formation control

## Citation

Use the published paper citation below when referencing this project:

L. Chen, M. Cao and C. Li, "Angle Rigidity and Its Usage to Stabilize Multiagent Formations in 2-D," IEEE Transactions on Automatic Control, vol. 66, no. 8, pp. 3667-3681, Aug. 2021, doi: 10.1109/TAC.2020.3025539.

The repository keeps notes and reproduction code only. The original paper PDF is not pushed.

## Environment Setup

Install MATLAB R2020b or newer, or use a recent Octave version. The current scripts use base MATLAB-style functions only and are compatible with Octave after the repository-side fixes in this project.

```bash
git clone https://github.com/Smalleaves123/Control-Thinking.git
cd Control-Thinking/002_angle_rigidity
```

See `requirements.md` for the environment note.

## How To Run

Run all commands from the project directory:

```bash
cd Control-Thinking/002_angle_rigidity
```

### 1. Five-Agent Angle Rigidity-Based Control

This reproduces the main five-agent angle-only control example in Section V-A. The script uses the initial positions and desired angles listed in the paper and includes a 5 degree local-frame misalignment for agent 1.

```bash
matlab -batch "run('scripts/run_angle_control.m')"
octave --quiet --eval "run('scripts/run_angle_control.m')"
```

In the MATLAB desktop, run:

```matlab
run('scripts/run_angle_control.m')
```

### 2. Bearing-Based Comparison

This compares the bearing-rigidity controller without and with the same local-frame misalignment.

```bash
matlab -batch "run('scripts/run_bearing_comparison.m')"
octave --quiet --eval "run('scripts/run_bearing_comparison.m')"
```

In the MATLAB desktop, run:

```matlab
run('scripts/run_bearing_comparison.m')
```

## Output Locations

- figures: `results/figures`
- metrics logs: `results/logs`
- optional tables: `results/tables`

Generated result files are ignored by git. Keep the figures and logs locally for analysis, or copy them from the server after running the scripts.

## What Is Implemented

The current code follows the paper at two levels:

- It builds the angle rigidity matrix `R_a(p)` from ordered angle triplets and checks the rank condition `rank(R_a(p)) = 2N - 4`.
- It implements the unified angle-only control law in equation (58) for the five-agent example in Section V-A.
- It implements the bearing-based comparison controller in equation (61), including the coordinate-frame misalignment case used to show why angle-only control is frame independent.
- It writes PNG figures and JSON metrics from MATLAB or Octave scripts.

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

This reproduction targets the paper's main 2-D simulation story rather than every theorem proof. The focus is:

- angularity and ordered triplet constraints;
- infinitesimal angle rigidity via the rank of `R_a(p)`;
- local angle-only formation stabilization;
- comparison with bearing-based control under local-frame misalignment.
