# Verification note — minimal demo training environment

## Clean-room check (done Oct 25, 2026, by the builder)

Method: copied `golden_demo.py`, `run_demo.sh`, and `README.md` to a
fresh directory, followed ONLY the README (one command:
`./run_demo.sh`), and diffed the policy output against the stated
outputs block in the README.

Result:

- Exit code 0, no errors, no extra steps, no fixes from memory.
- Policy output matches the README's stated outputs EXACTLY
  (tender and raider blocks, every number, byte-for-byte).
- Interventions needed: ZERO.
- Determinism check: two consecutive runs produce identical output.

## What this does and does not prove

- It proves the README is sufficient: a runner with python3 who
  follows the README gets the stated numbers with no help.
- It does NOT prove an outside runner has done it — this check was
  run by the builder, not an independent outsider. The true
  outside-runner check happens after hosting, when someone with no
  connection to the build follows the README cold. If that runner
  needs any intervention, the success bar is not met and the build
  or README must be fixed, not explained away.

## Freshness

Written from the spec in README.md. No code was copied from the
project's toy harness (VM meters directory or the Mac's
golden-directive directory). The only shared content is the spec
itself: the Y formula, the ledger idea, and the cropping idea.
