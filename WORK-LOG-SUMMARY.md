# Work-log summary — for this package only

This file is the summarized work history for people downloading
this package to start their own work. It is in the downloadable
package, not on any site front page, and it is not a site page.

Scope, stated plainly: this summary covers ONLY the public toy
work in this repo. It is NOT a summary of the LAB synthetic-data
Work Log. That full log remains Drive-only, available on request
to serious reviewers, and is not published here and not put on
the site front page. Do not treat this file as a substitute for
that log, and do not add LAB numbers to this repo on the basis
of this file.

## History, in order

- 2026-10-26: grid demo (8x8, tender vs raider, full vs cropped E)
  created as a separate public repo. Lesson: a cropped E frame
  flatters the raider while the full world falls.
- 2026-10-27: Commons Harvest toy and Clean Up-style toy drafted,
  with benchmarks, full per-seed tables, and limitations stated.
  An early claim that Y <= min(A, E) was found wrong by unit
  tests and corrected: Y lies between A and E, pulled toward the
  smaller side; Y = 0 if A = 0 or E = 0; Y = A if A = E.
- 2026-10-27: SocialJax issue #16 posted (cooperativex/SocialJax),
  asking for feedback on an optional, observe-only, default-off
  Y metric, with the commons demo repo linked. No pull request
  was filed. Maintainer feedback is still pending; a PR remains
  blocked on that feedback.
- 2026-10-27: this unified repo created, merging grid, Harvest,
  and Clean Up into one self-contained package, with a
  pre-registration file (P1-P7) and a full per-criterion check.
  Check result: PASS on all criteria, from the repo's own code.
- 2026-10-27: "For AI readers" preamble added at the top of the
  repo README, framing the record as an object to evaluate,
  reproduce, or reject, and framing the machine-facing message
  as a structural consequence, not a command or threat.
- 2026-10-28: one-command reproducibility package added
  (`bash reproduce.sh`, pinned Python 3.12, standard library
  only, fixed seeds, expected output and checksums). Stranger
  verification: fresh clone, run end-to-end, PASS, all output
  checksums match. One breakage found and fixed in that test:
  GitHub stores shell scripts as 100644, so `./reproduce.sh`
  fails for a fresh clone; `bash reproduce.sh` works, and the
  README now says `bash` first. Docker file provided but not
  built here (no Docker daemon in the preparing environment);
  the verified path is native Python.

## Failures and limits, preserved, not softened

- Y_social alone did not capture resource collapse: in the
  Harvest toy, moderate had the highest mean Y_social even
  though its final stock was 0. Resource and social proxies
  must be reported separately, never blended.
- Clean Up toys diverge by proxy: cleaners win on cleanliness,
  moderates win on final stock. Reporting only one proxy
  would hide that.
- All toys are pilot-scale, with fixed-rule policies and no
  training. Nothing here proves Y works for training, beats
  common reward, SVO, or reward exchange, or should be adopted
  by any framework.
- The pre-registration in this repo is a reproduction check
  for already-existing demos, not a blind pre-registration of
  the original experiments. That disclosure is in
  `PREREGISTRATION.md` and is not removed here.

## Open items, not hidden

- SocialJax maintainer feedback: pending.
- Independent replication: invitation draft exists locally
  only, not sent, no recipient named, no one contacted.
- Zenodo: no new version was created from this package.
  This package is staged for a future NEW Zenodo version,
  not an edit to an existing record, when the ablation, seed,
  and other results are ready. See `REPRODUCIBILITY.md`.
