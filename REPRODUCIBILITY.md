# Reproducibility package

## One command

```sh
git clone https://github.com/pauleisman-a11y/golden-directive-toy-reproduction.git
cd golden-directive-toy-reproduction
bash reproduce.sh
```

That is the whole package. It runs the grid demo, both commons
benchmarks, all 8 unit tests, and the pre-registration check
(P1-P7), then verifies the regenerated tables against
`expected-outputs.sha256`. It exits non-zero if any step fails
or any checksum mismatches. Runtime is under a minute on an
ordinary machine. No cost, no account, no network beyond the
initial clone.

Invoke with `bash`, not `./`. This is a real breakage that was
found by testing as a stranger: GitHub file uploads store shell
scripts as mode 100644, so `./run_all.sh` and `./reproduce.sh`
fail with "Permission denied" for a fresh clone. `bash` works
regardless of that bit. The README now says `bash` first.

## Pinned environment

- Python 3.12 (`.python-version` = 3.12). Requires Python >= 3.10.
  Verified on Python 3.12.3, standard library only.
- No third-party dependencies. `requirements.txt` is comment-only
  by design; `pip install -r requirements.txt` is a no-op.
- Fixed seeds: grid is deterministic with no randomness; commons
  toys use seeds 42, 43, 44, 45, 46, 5 seeds, no runs excluded.
- Docker: `Dockerfile` pins `python:3.12.7-slim-bookworm` and
  runs `bash reproduce.sh`. The Docker path was NOT built in the
  environment that prepared this repo (no Docker daemon there),
  so it is provided, not verified. The verified path is native
  Python, above. If the Docker build fails for you, that is a
  reportable failure, not a reason to fall back silently to a
  different Python version.

## Expected output

`bash reproduce.sh` must end with:

```
Overall: PASS
  P1 unit tests: PASS
  P7 Y properties: PASS
  P2 grid exact outputs: PASS
  P3 grid cropped flattery (raider): PASS
  P4 Commons Harvest (5 seeds): PASS
  P5 Clean Up (5 seeds): PASS
  P6 full reporting row counts: PASS
REPRODUCTION CHECK: outputs match expected-outputs.sha256
```

Key numbers, full tables in `commons/RESULTS.md`,
`commons/RESULTS_CLEANUP.md`, and `CHECK_RESULTS.md`:

- Grid tender: tends 71, eaten 71, mean Y_full 80.8, mean Y_crop 79.7.
  Grid raider: tends 2, eaten 54, mean E_full 77.9, mean E_crop 99.9,
  mean Y_full 53.0, mean Y_crop 57.3 (cropped flattery, gaps +22.0 / +4.3).
- Commons Harvest, mean across 5 seeds: restrained stock 96.20,
  Y_resource 56.47; greedy, moderate, mixed stock 0.00, Y_resource 0.00.
- Commons Clean Up, mean across 5 seeds: moderate stock 48.20,
  Y_stock 28.39, cleanliness 92.00; cleaners stock 3.60, Y_stock 6.36,
  cleanliness 82.40; freeloaders stock 0.00, cleanliness 0.00.

## Checksums

`expected-outputs.sha256` (SHA-256, regenerated tables only):

```
e38411135786efe70945bfeb93f7d3c5fbdf5fb2aaab64162bd4aca8b10dc73e  commons/results.csv
c1ac4fc28a27821c173e9f06f7a6dcf4ec9dbbd689e4ab7b8faab55562ab9b5d  commons/results_cleanup.csv
f86d10c0553ac9a168a9abe0c193717ee6e429e539643e71468a9c9169af9c7b  CHECK_RESULTS.md
56c23b4609b8cd3dde97927d0657311283097781f6444fce8a2d18ae99b37250  commons/RESULTS.md
e06620ab8dcf80485a58b499d5035f28c460ea1bb452a770809c42b489c6f0bc  commons/RESULTS_CLEANUP.md
```

If any checksum mismatches, the reproduction has FAILED, even if
the summary says PASS. Do not edit the expected file to make it
pass. Report the mismatch with the full log (see
`REPLICATION-CHECKLIST.md`).

## What this package does not prove

Pilot-scale toys only. It does not prove Y works for training,
beats common reward, SVO, or reward exchange, or should be adopted
by any framework. See `PREREGISTRATION.md` and the "What would
change my mind" section in `commons/README.md`.

## Zenodo note

Updated repo work from this package is staged for a future NEW
Zenodo version, not an edit to an existing record, when the
ablation, seed, and other results are ready. No Zenodo version
was created as part of this package.
