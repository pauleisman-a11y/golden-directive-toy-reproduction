#!/bin/sh
# Run every toy, its benchmarks and tests, then the preregistration check.
# No dependencies, no cost. Run from this directory: bash run_all.sh
# (bash, not ./ — GitHub stores this as 100644, see REPRODUCIBILITY.md.)
set -e
cd "$(dirname "$0")"
python3 grid/golden_demo.py
cd commons && python3 benchmark.py && python3 benchmark_cleanup.py && python3 -m unittest -v; cd ..
python3 check_preregistration.py
