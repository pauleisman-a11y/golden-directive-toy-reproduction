# Golden Directive — toy reproduction repo (draft)

A single, self-contained public repo reproducing three existing toy
demos, with code, seeds, exact metric definitions, pre-registered
success criteria, and full-versus-cropped reporting. No Drive link
is used as a source. Everything needed to reproduce the results is
in this repo itself.

No training. No learning agent is included in any toy. Policies are
fixed rules. Y is observe-only in the commons toys.

## Run it all

```sh
./run_all.sh
```

That runs the grid demo, both commons benchmarks, all unit tests,
and the pre-registration check. Or run pieces:

```sh
python3 grid/golden_demo.py
python3 commons/benchmark.py
python3 commons/benchmark_cleanup.py
python3 -m unittest discover -s commons -v
python3 check_preregistration.py
```

Python 3.10+, standard library only. No dependencies, no cost.

## The three toys

### 1. Grid — `grid/` (original files preserved)

8x8 grid, 4 food tiles, 150 steps, deterministic, no randomness.
Policies: tender (tends lowest-stock tile, eats for subsistence)
and raider (tends home, eats far tiles empty).

This toy is the full-versus-cropped lesson:
- E_full counts all 4 tiles.
- E_crop counts ONLY the home quadrant (x < 4, y < 4), one tile.
  Damage outside that frame never enters E_crop.
- The raider's cropped meter stays near perfect while its full
  meter falls. See `grid/README-original.md` and
  `PREREGISTRATION.md` P2-P3 for the exact stated outputs.

### 2. Commons Harvest — `commons/`

4 agents share 100 apples for 20 rounds, seeds 42-46.
Policies: greedy, moderate, restrained, mixed.
A = apples harvested. E_resource = apples remaining at end.
E_social = mean harvest of other agents. Both reported separately.

### 3. Clean Up-style — `commons/`

Cleaning costs a round of harvest but raises cleanliness, which
raises apple spawn. Policies: all cleaners, all freeloaders,
mixed, all moderate. A = apples harvested. E_stock = final stock.
E_clean = final cleanliness (0-100 points, mixed scale disclosed).
E_social = mean harvest of others. All reported separately.

## What Y is

Paul Eisman's Golden Directive proposal: Y = 2 * A * E / (A + E),
the harmonic mean of A and E. "You cannot survive what you destroy."

- If A = 0 or E = 0, Y = 0.
- If A = E, Y = A.
- Otherwise Y lies between A and E, pulled toward the smaller side.
- True E is not knowable. Every E here is a disclosed, bounded
  proxy, never the whole of everything else, and never silently
  blended with another proxy. See `PREREGISTRATION.md` for the exact
  A and E definition for each toy, including the grid ledger weights
  (tend credits actual restore; eat debits 0.5 per unit) and the
  Clean Up cleanliness scale.

## Full versus cropped reporting

Two meanings, kept distinct:

1. Cropped E: the grid toy's home-quadrant frame, which hides
   damage outside it. Reported side by side with full E, with the
   gap stated, never as a replacement for full E.
2. Full reporting: every summary in this repo is accompanied by
   full data — per-agent, per-seed tables in `commons/results.csv`
   and `commons/results_cleanup.csv`, and a per-criterion table in
   `CHECK_RESULTS.md`. No runs excluded, no seeds dropped, no
   wins-only reporting. A cropped summary (mean alone) is never
   presented without the full table it came from.

## Pre-registration

`PREREGISTRATION.md` (version 1, 2026-10-27) states success
criteria P1-P7 before the merged-repo check run. Disclosure: the
original demos existed before that file, so this is a reproduction
check, not a blind pre-registration of the original experiments.
It does not prove Y works for training. If any criterion fails,
the reproduction is FAILED in `CHECK_RESULTS.md`, with no
post-hoc threshold change.

## What would change my mind

See `commons/README.md`: if, in a real benchmark, Y-trained agents
do worse on both individual return and final resource stock than
existing baselines, or if Y's ranking flips under an equally
defensible scale for E with no principled reason to prefer one
scale, then Y should not be adopted as a training reward.

## License

Apache-2.0. See `LICENSE`.

## Status

Draft prepared locally for Grok review, for consideration. This
draft is self-contained and does not depend on any Drive file.
A pull request to any framework is a separate step, only after
maintainer feedback on the SocialJax issue, and is not part of
this repo.
