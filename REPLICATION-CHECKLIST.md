# Independent replication checklist

For a replicator who did not write this code. No contact is
required to use this checklist, and no result is pre-selected.

## Run

1. Clone a fresh copy. Do not reuse the author's working folder.
2. Record your environment: operating system, Python version
   (`python3 --version`), and whether you used native Python or
   Docker (with the Docker image tag if so).
3. Run, from the repo root: `bash reproduce.sh`
4. Save the full output log, including any error, not just the
   final lines.

## Judge

- PASS only if every item holds: all 8 unit tests pass, P1-P7
  all PASS in `CHECK_RESULTS.md`, the final line reads
  "REPRODUCTION CHECK: outputs match expected-outputs.sha256",
  and no step was skipped, edited, or re-run with different
  seeds, parameters, or code.
- FAIL if any test fails, any P criterion fails, any checksum
  mismatches, the script exits non-zero, or you had to change
  code, seeds, or the expected file to get it to run. A FAIL is
  a useful result: it bounds the claim or finds a bug.
- Do not cherry-pick: do not drop a failing seed, policy, or
  toy and report the rest as a pass.

## Report (if you choose to report)

Include, in full:
- Your environment (step 2) and the full log (step 4).
- `CHECK_RESULTS.md` as generated, and the output of
  `sha256sum -c expected-outputs.sha256`.
- Exactly what you changed, if anything, and why. "No changes"
  is itself a finding and should be stated.
- Whether the Docker path or the native path was used, and
  whether the other path was also tried.

## What is not asked

- You are not asked to adopt Y, to endorse it, or to run any
  experiment beyond this repo. Evaluate it, reproduce it, or
  reject it.
- You are not asked to hide a failure, to soften it, or to
  re-run until it passes. A critical replication that fails to
  reproduce is valuable.
