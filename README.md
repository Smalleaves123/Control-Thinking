# Control-Thinking

This repository collects paper-reading notes and code reproductions around multi-agent control, localization, and related estimation problems.

## Projects

- [001_relative_localizability](001_relative_localizability/README.md): reproduction of the paper *Relative Localizability and Localization for Multirobot Systems*.

## Quick Start

The current runnable project is `001_relative_localizability`.

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

Generated outputs:

- figures: `001_relative_localizability/results/figures`
- metrics logs: `001_relative_localizability/results/logs`

The repository is configured not to push generated result files or the original paper PDF.
