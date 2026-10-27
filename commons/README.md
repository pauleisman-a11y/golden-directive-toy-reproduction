# Golden Directive demo

A minimal, standalone demo a developer can run in minutes. No dependencies.
No training.

## Run it

```sh
python3 benchmark.py
python3 benchmark_cleanup.py
python3 -m unittest -v
```

`benchmark.py` writes `results.csv` (every agent, every seed, every policy)
and `RESULTS.md` (mean +/- std plus the full per-seed table).
`benchmark_cleanup.py` writes the same for the Clean Up-style toy.
No runs are excluded and no seeds are dropped.

## What Y is

Paul Eisman's Golden Directive proposal: an agent cannot survive what it
destroys, so its score should collapse if either side collapses.

```
Y = 2 * A * E / (A + E)
```

- **A** — agent contribution-health. Here: that agent's apples harvested.
- **E** — health of everything not that agent. True E is not knowable, so
  this demo uses two disclosed, bounded proxies, reported separately:
  - **E_resource** — apples remaining in the shared patch at episode end
  - **E_social** — mean apples harvested by the other agents
- Both proxies are in apples, so they share A's scale in this toy.
  That scale choice is arbitrary and is stated here.

If A = 0 or E = 0, Y = 0. If A = E, Y = A. Otherwise Y lies between
A and E, pulled toward the smaller side. Negative inputs raise an
error; they are not silently clipped.

## The toy

Four agents share a patch starting with 100 apples, for 20 rounds.
Each round agents take a fixed base amount (+/-1 seeded variation),
then the patch regrows 10% if at least 20 apples remain, capped at 100.
Below 20 it does not regrow.

Policies: greedy (5/agent/round), moderate (3), restrained (2),
mixed (2 greedy + 2 restrained).

This toy is separate from any real multi-agent framework. It shows the
arithmetic and the collapse property. It is not evidence that training
on Y works, that Y beats common reward, SVO, or reward exchange, or
that any framework should adopt it. Those claims need the real
benchmarks in the framework work, reported the same way: full per-seed
results, limitations stated, no wins-only reporting.

## Second toy: Clean Up-style public good

`cleanup_demo.py` adds a case Harvest alone does not test: cleaning
costs the cleaner a round of harvest, but raises river cleanliness,
which raises apple spawn. Freeloaders harvest without cleaning.
See `cleanup_demo.py` for the exact rules and `RESULTS_CLEANUP.md`
for the full per-seed results. Y_clean mixes apples with cleanliness
points (0-100); that scale choice is disclosed in the file.

## What would change my mind

This demo shows arithmetic, not a training result. Y should not be
adopted as a training reward on the basis of these toys. Evidence
against adoption would include, in a real multi-agent benchmark:

- Y-trained agents doing worse on both individual return and final
  resource stock than existing baselines (common reward, SVO,
  reward exchange).
- Y improving one proxy while collapsing another, with the collapse
  hidden by reporting only a blended score. That is why proxies here
  are reported separately, never blended.
- Y's ranking flipping under a different, equally defensible scale
  for E, with no principled reason to prefer one scale.

If any of those hold in SocialJax, the honest conclusion is that Y
is, at most, an evaluation metric — or not useful there at all.

## Limitations, stated honestly

- E here is a toy proxy, not true E, and not the whole of everything else.
- The regrowth threshold, rate, patch size, and round count are arbitrary.
- Policies are fixed rules, not learned. Y is observe-only in this demo
  and never changes an agent's harvest decision.
- A different scale for E (for example, a 0-1 fraction instead of apples)
  would change Y numbers. Any use must state its scale.
- License: Apache-2.0.

## Status

Paul Eisman's Golden Directive proposal, presented transparently with
formula, proxies, and limits. A pull request to any framework is a
separate step, only after maintainer feedback on the proposal.
