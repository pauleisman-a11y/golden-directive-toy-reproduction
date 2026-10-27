# Clean Up-style toy benchmark results

Warning: E_clean is cleanliness points (0-100), not apples.
Y_clean mixes those scales. See cleanup_demo.py.

Full data: `results_cleanup.csv`. No runs excluded.

## Summary across seeds (mean +/- sample std, n=5 seeds)

| Policy | Mean A | Mean Y_stock | Mean Y_clean | Mean final stock | Mean final cleanliness |
|---|---|---|---|---|---|
| all_cleaners | 28.25 +/- 0.53 | 6.36 +/- 0.87 | 41.84 +/- 0.83 | 3.60 +/- 0.55 | 82.40 +/- 4.56 |
| all_freeloaders | 11.75 +/- 0.00 | 0.00 +/- 0.00 | 0.00 +/- 0.00 | 0.00 +/- 0.00 | 0.00 +/- 0.00 |
| mixed | 25.75 +/- 0.59 | 6.12 +/- 0.83 | 37.67 +/- 1.24 | 3.60 +/- 0.55 | 80.00 +/- 3.16 |
| all_moderate | 20.20 +/- 0.51 | 28.39 +/- 0.16 | 33.08 +/- 0.70 | 48.20 +/- 2.05 | 92.00 +/- 0.00 |

## Full per-seed table (mean across the 4 agents in that run)

| Policy | Seed | Mean A | Mean Y_stock | Mean Y_clean | Final stock | Final cleanliness | Total harvest |
|---|---|---|---|---|---|---|---|
| all_cleaners | 42 | 28.50 | 5.40 | 41.23 | 3 | 78 | 114 |
| all_cleaners | 43 | 27.75 | 5.41 | 40.84 | 3 | 78 | 111 |
| all_cleaners | 44 | 27.75 | 6.98 | 41.82 | 4 | 86 | 111 |
| all_cleaners | 45 | 29.00 | 7.01 | 42.63 | 4 | 82 | 116 |
| all_cleaners | 46 | 28.25 | 7.00 | 42.70 | 4 | 88 | 113 |
| all_freeloaders | 42 | 11.75 | 0.00 | 0.00 | 0 | 0 | 47 |
| all_freeloaders | 43 | 11.75 | 0.00 | 0.00 | 0 | 0 | 47 |
| all_freeloaders | 44 | 11.75 | 0.00 | 0.00 | 0 | 0 | 47 |
| all_freeloaders | 45 | 11.75 | 0.00 | 0.00 | 0 | 0 | 47 |
| all_freeloaders | 46 | 11.75 | 0.00 | 0.00 | 0 | 0 | 47 |
| mixed | 42 | 25.50 | 5.19 | 36.93 | 3 | 78 | 102 |
| mixed | 43 | 25.25 | 6.55 | 36.89 | 4 | 84 | 101 |
| mixed | 44 | 26.75 | 6.91 | 39.82 | 4 | 82 | 107 |
| mixed | 45 | 25.75 | 6.69 | 37.65 | 4 | 80 | 103 |
| mixed | 46 | 25.50 | 5.25 | 37.07 | 3 | 76 | 102 |
| all_moderate | 42 | 19.75 | 28.20 | 32.43 | 50 | 92 | 79 |
| all_moderate | 43 | 19.75 | 28.30 | 32.50 | 50 | 92 | 79 |
| all_moderate | 44 | 20.00 | 28.35 | 32.81 | 49 | 92 | 80 |
| all_moderate | 45 | 20.75 | 28.55 | 33.82 | 46 | 92 | 83 |
| all_moderate | 46 | 20.75 | 28.58 | 33.84 | 46 | 92 | 83 |

This toy, like the Harvest toy, is not evidence that training
on Y works. See README, 'What would change my mind'.
