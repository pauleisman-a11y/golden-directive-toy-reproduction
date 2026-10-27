# Demo benchmark results

Warning: E in this demo is a bounded proxy (apples remaining,
mean other agents' harvest), not true E. See README.

Full data: `results.csv` (one row per agent per seed per policy).
No runs excluded. No seeds dropped.

## Summary across seeds (mean +/- sample std, n=5 seeds)

| Policy | Mean A | Mean Y_resource | Mean Y_social | Mean final stock |
|---|---|---|---|---|
| greedy | 31.20 +/- 0.57 | 0.00 +/- 0.00 | 31.10 +/- 0.54 | 0.00 +/- 0.00 |
| moderate | 41.90 +/- 1.50 | 0.00 +/- 0.00 | 41.81 +/- 1.54 | 0.00 +/- 0.00 |
| restrained | 40.05 +/- 1.08 | 56.47 +/- 1.04 | 39.96 +/- 1.06 | 96.20 +/- 3.77 |
| mixed | 37.20 +/- 1.16 | 0.00 +/- 0.00 | 33.99 +/- 0.65 | 0.00 +/- 0.00 |

## Full per-seed table (mean across the 4 agents in that run)

| Policy | Seed | Mean A | Mean Y_resource | Mean Y_social | Final stock | Total harvest |
|---|---|---|---|---|---|---|
| greedy | 42 | 31.50 | 0.00 | 31.36 | 0 | 126 |
| greedy | 43 | 30.50 | 0.00 | 30.44 | 0 | 122 |
| greedy | 44 | 31.00 | 0.00 | 30.88 | 0 | 124 |
| greedy | 45 | 32.00 | 0.00 | 31.86 | 0 | 128 |
| greedy | 46 | 31.00 | 0.00 | 30.95 | 0 | 124 |
| moderate | 42 | 42.25 | 0.00 | 42.23 | 0 | 169 |
| moderate | 43 | 40.75 | 0.00 | 40.49 | 0 | 163 |
| moderate | 44 | 41.75 | 0.00 | 41.66 | 0 | 167 |
| moderate | 45 | 44.25 | 0.00 | 44.20 | 0 | 177 |
| moderate | 46 | 40.50 | 0.00 | 40.45 | 0 | 162 |
| restrained | 42 | 38.50 | 55.58 | 38.47 | 100 | 154 |
| restrained | 43 | 40.25 | 57.22 | 39.98 | 100 | 161 |
| restrained | 44 | 40.75 | 56.63 | 40.69 | 93 | 163 |
| restrained | 45 | 39.50 | 55.25 | 39.46 | 92 | 158 |
| restrained | 46 | 41.25 | 57.66 | 41.18 | 96 | 165 |
| mixed | 42 | 37.25 | 0.00 | 33.55 | 0 | 149 |
| mixed | 43 | 35.50 | 0.00 | 33.29 | 0 | 142 |
| mixed | 44 | 37.50 | 0.00 | 33.77 | 0 | 150 |
| mixed | 45 | 38.75 | 0.00 | 34.77 | 0 | 155 |
| mixed | 46 | 37.00 | 0.00 | 34.57 | 0 | 148 |

## How to read this honestly

- Y_resource rewards a policy only if it both harvests and leaves stock.
- Y_social rewards a policy only if it both harvests and others harvest.
- A toy with fixed rules is not evidence that training on Y works.
  That claim would need a real multi-agent benchmark (see README).
