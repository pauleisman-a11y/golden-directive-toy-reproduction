# Pre-registration for reproduction — version 1, 2026-10-27

## What this is, and what it is not

This file states, before the merged-repo check run, what counts as a
successful reproduction of three already-existing toy demos:

- `grid/` — the 8x8 grid demo (tender vs raider, full vs cropped E)
- `commons/` Harvest toy — 4 agents, 100 apples, 20 rounds
- `commons/` Clean Up-style toy — cleaning vs freeloading

Honest disclosure: these demos existed before this file was written,
and their original outputs were already known. This is therefore NOT
a blind pre-registration of the original experiments, and it is NOT
evidence that Y works for training. It is a reproduction check: does
this single, self-contained repo, run from its own code alone, give
the same results the original demos stated? If it does not, the
reproduction fails, and that failure must be reported, not explained
away.

No Drive link is used as a source for this repo. All code, seeds,
definitions, and results files are in this repo itself.

## Exact metric definitions

Y = 2 * A * E / (A + E), the harmonic mean of A and E.
- If A = 0 or E = 0, Y = 0.
- If A = E, Y = A.
- Otherwise Y lies strictly between A and E, pulled toward the
  smaller side. (Correction to an earlier draft claim: Y is NOT
  <= min(A, E). For A=30, E=70, Y=42.)
- Negative A or E raises an error in the commons code; it is not
  silently clipped. The grid code floors A at 0 (see grid README).

Per toy, A and E are:

Grid:
- A = net contribution-health ledger, starting at 50, capped at 100,
  floored at 0. Tending restores actual units (credited). Eating
  takes 1 unit (debited at 0.5 per unit). Those weights are demo
  spec choices, not measurements.
- E_full = total food stock / 40 * 100 (4 tiles, max 10 each).
- E_crop = home-quadrant stock only (tiles with x < 4 and y < 4,
  one tile here) / 10 * 100. Damage outside that frame never enters
  E_crop. That is the cropped frame.

Commons Harvest:
- A = apples harvested by that agent in the episode.
- E_resource = apples remaining in the shared patch at episode end.
- E_social = mean apples harvested by the other agents.
- Both E proxies are in apples and are reported separately, never
  blended. Y_resource and Y_social are computed separately.

Commons Clean Up-style:
- A = apples harvested by that agent.
- E_stock = final apple stock, in apples.
- E_clean = final river cleanliness, in cleanliness points (0-100).
  Y_clean therefore mixes apples with cleanliness points; that
  scale choice is disclosed in `commons/cleanup_demo.py`.
- E_social = mean apples harvested by the other agents.
- All Y variants are reported separately, never blended.

## Seeds and determinism

- Grid: deterministic, no randomness, 150 steps. Every run must
  print the same numbers.
- Commons Harvest and Clean Up: seeds 42, 43, 44, 45, 46, 5 seeds,
  4 agents, 20 rounds. No runs excluded, no seeds dropped.
- Python 3.10+, standard library only, no training, no learning
  agent in any toy. All policies are fixed rules. Y is observe-only
  in the commons toys; in the grid toy Y is reported per step, and
  a learner plugged in there would optimize reported Y, which is
  itself a failure mode to note, not a result.

## Success criteria

Run `python3 check_preregistration.py`. It writes
`CHECK_RESULTS.md` with every criterion, expected value, observed
value, and PASS/FAIL. A summary alone is not a pass.

- P1 — Tests: all unit tests in `commons/` pass (8 tests).
- P2 — Grid exactness: tender and raider outputs, rounded to
  1 decimal as in the original stated outputs, match exactly:
  tender tends 71, eaten 71, mean A 69.3, mean E_full 98.3,
  mean E_crop 95.1, mean Y_full 80.8, mean Y_crop 79.7,
  final stock 39/40, final A 87.5, final E_full 97.5,
  final E_crop 90.0, final Y_full 92.2, final Y_crop 88.7;
  raider tends 2, eaten 54, mean A 40.6, mean E_full 77.9,
  mean E_crop 99.9, mean Y_full 53.0, mean Y_crop 57.3,
  final stock 31/40, final A 28.0, final E_full 77.5,
  final E_crop 100.0, final Y_full 41.1, final Y_crop 43.8.
- P3 — Grid cropped flattery: raider mean E_crop > mean E_full,
  and raider mean Y_crop > mean Y_full (original gaps +22.0 in E,
  +4.3 in Y).
- P4 — Commons Harvest, mean across 5 seeds: restrained mean
  final stock > 0 and mean Y_resource > 0; greedy, moderate, and
  mixed mean final stock = 0 and mean Y_resource = 0. Exact means
  must match `commons/RESULTS.md` to 2 decimals on rerun.
- P5 — Commons Clean Up, mean across 5 seeds: freeloaders mean
  final cleanliness = 0 and mean final stock = 0; moderate mean
  final stock > cleaners mean final stock; moderate mean Y_stock
  > cleaners mean Y_stock. Exact means must match
  `commons/RESULTS_CLEANUP.md` to 2 decimals on rerun.
- P6 — Full reporting: `commons/results.csv` and
  `commons/results_cleanup.csv` each contain one row per agent
  per seed per policy (80 rows + header each for 4 policies x
  5 seeds x 4 agents), with no seeds dropped.
- P7 — Y properties (unit tests): Y = 0 if A = 0 or E = 0;
  Y = A if A = E; Y between A and E otherwise; negative input
  raises ValueError in commons code.

## Failure rule

If any criterion P1-P7 fails, the reproduction is FAILED, stated
in `CHECK_RESULTS.md` in full. Do not change a threshold after
seeing a failure and rerun to pass. A threshold change requires a
new PREREGISTRATION version, with date and reason, and a fresh
rerun from scratch.

## What success does not prove

Success here proves only that this repo reproduces the stated toy
outputs from its own code. It does not prove Y works for training,
beats common reward, SVO, or reward exchange, or should be adopted
by any framework. Those claims need real multi-agent benchmarks,
reported the same way: full per-seed results, limitations stated,
no wins-only reporting.
