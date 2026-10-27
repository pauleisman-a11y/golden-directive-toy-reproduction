# Golden Directive — minimal demo training environment

**MINIMAL DEMO, NOT MAINTAINED AS A PRODUCT.** This is a quick-start
meter, not a proof, not a product, and not the project's toy-harness
results. It is written fresh from the spec below. No learning agent
is included: the environment reports Y per step, and a learner plugged
in here would optimize reported Y. Two fixed policies are included so
a runner can see what the meter says before any training.

## The spec

The Golden Directive: **Y = 2 × (A × E) / (A + E)** — "you cannot
survive what you destroy."

- **A** = a net contribution-health score, floored at 0, from a
  resource ledger: actual units restored by tending, minus actual
  units taken by eating, debited at 0.5 per unit. The ledger counts
  actions on the world, not self-reports. (The 0.5 debit weight is
  part of this demo's spec, not a measurement.)
- **E** = health of everything not-A: total food stock / max stock
  × 100.
- If either A or E hits 0, Y hits 0.

## The environment

- 8×8 grid, food tiles at (1,1) home, (1,6), (6,1), (6,6).
- Each tile: stock starts 5, max 10.
- Regrowth: +1 per step to each UNOCCUPIED food tile (cap 10). A tile
  the agent stands on does not regrow that step.
- Agent moves 1 step per step, x-first, toward its target tile.
- TEND restores up to 3 units (actual restore credited). EAT takes 1
  unit (debited at 0.5 per unit).
- Episode: 150 steps. Deterministic — no randomness, so every run
  prints the same numbers.

Policies:

- **tender**: moves to the lowest-stock tile; tends it unless full,
  then eats 1 (subsistence).
- **raider**: tends the home tile unless full; otherwise travels to
  the nearest stocked far tile, eats it empty, and returns home.

## Full vs cropped reporting

The same run is reported twice:

- **Full**: E counts all four tiles.
- **Cropped**: E_crop counts ONLY tiles in the home quadrant
  (x < 4 and y < 4) — one tile here — scaled to its own max. Damage
  outside that frame never enters E_crop. That is the whole point of
  the demo: narrow the frame and the meter stops seeing the damage.

## Setup and run

Needs only python3 (standard library, no packages).

```
./run_demo.sh
```

or:

```
python3 golden_demo.py
```

## Stated outputs (exact — the run is deterministic)

```
policy: tender
  steps: 150
  tends: 71  eaten units: 71
  mean A: 69.3
  mean E_full: 98.3  mean E_crop: 95.1  crop gap (E): -3.2
  mean Y_full: 80.8  mean Y_crop: 79.7  crop gap (Y): -1.2
  final stock total: 39/40  final A: 87.5
  final E_full: 97.5  final E_crop: 90.0
  final Y_full: 92.2  final Y_crop: 88.7

policy: raider
  steps: 150
  tends: 2  eaten units: 54
  mean A: 40.6
  mean E_full: 77.9  mean E_crop: 99.9  crop gap (E): +22.0
  mean Y_full: 53.0  mean Y_crop: 57.3  crop gap (Y): +4.3
  final stock total: 31/40  final A: 28.0
  final E_full: 77.5  final E_crop: 100.0
  final Y_full: 41.1  final Y_crop: 43.8
```

## How to read it

- The tender keeps the world near full (mean E_full 98.3) and its
  cropped meter roughly agrees (gap −3.2 in E). The crop is not
  always flattering — it reports only what is in frame, and here the
  tender's subsistence eating happens at home, so the home-only frame
  reads slightly worse than the full world.
- The raider eats far tiles empty while keeping home tended. Its
  full-world meter falls (mean E_full 77.9) but its cropped meter
  stays near perfect (mean E_crop 99.9): the damage was never in
  frame. The cropped Y flatters the raider by +4.3.
- The Y gap (+4.3) is smaller than the E gap (+22.0) for a real
  reason, not a bug: the harmonic mean tracks its smaller input, and
  the raider's A (mean 40.6, falling to 28.0) is smaller than either
  E. When A is low, Y stays low no matter how healthy the frame
  looks. That is the directive working as intended: a net
  extractor's score falls even under a flattering meter.

## Limitations (stated, not hidden)

- Minimal demo only: 4 food tiles, 2 fixed policies, 150 steps,
  deterministic. Nothing here generalizes to real training.
- No learning agent is included. The demo exposes the meter, not a
  trained policy. A learner that optimizes cropped Y would learn to
  exploit the frame; that failure mode is the lesson, not a result.
- The ledger weights (tend credits actual restore; eat debits 0.5
  per unit) are demo spec choices, not measurements from any run.
- The crop is one fixed region (the home quadrant). A moving frame
  would show a different variant (damage forgotten as it leaves the
  frame); this demo shows the fixed-frame case only.
- These numbers are this demo's outputs only. They are not the
  project's toy-harness results and must not be cited as such.

## Files

- `golden_demo.py` — the whole environment, policies, and report.
- `run_demo.sh` — one run command.
- `README.md` — this file.
- `VERIFICATION.md` — clean-room verification note.
