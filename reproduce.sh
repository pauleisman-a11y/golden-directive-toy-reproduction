#!/bin/sh
# One-command reproduction. Invoke as: bash reproduce.sh
# (Do not rely on the executable bit: GitHub file uploads store this
# script as 100644, so ./reproduce.sh fails for a stranger. bash works.)
# Runs every toy, its benchmarks and tests, the pre-registration check,
# then verifies the regenerated tables against expected-outputs.sha256.
# Exits non-zero if any step fails or any checksum mismatches.
set -e
cd "$(dirname "$0")"
python3 --version
bash run_all.sh
sha256sum -c expected-outputs.sha256
echo "REPRODUCTION CHECK: outputs match expected-outputs.sha256"
