# Pre-registration check results

Overall reproduction verdict: **PASS**

| Criterion | Expected | Observed | Verdict |
|---|---|---|---|
| P1 unit tests | 8 tests, OK | OK | PASS |
| P7 Y properties | Y(0,10)=0; Y(7,7)=7; 30<Y(30,70)<70; negative raises | Y(0,10)=0.0; Y(7,7)=7.0; Y(30,70)=42.0; negative raises=True | PASS |
| P2 grid exact outputs | tender + raider match stated outputs to 1 decimal | tender: {'tends': 71, 'eaten': 71, 'mean_A': 69.3, 'mean_E_full': 98.3, 'mean_E_crop': 95.1, 'mean_Y_full': 80.8, 'mean_Y_crop': 79.7, 'final_stock': 39, 'final_A': 87.5, 'final_E_full': 97.5, 'final_E_crop': 90.0, 'final_Y_full': 92.2, 'final_Y_crop': 88.7}; raider: {'tends': 2, 'eaten': 54, 'mean_A': 40.6, 'mean_E_full': 77.9, 'mean_E_crop': 99.9, 'mean_Y_full': 53.0, 'mean_Y_crop': 57.3, 'final_stock': 31, 'final_A': 28.0, 'final_E_full': 77.5, 'final_E_crop': 100.0, 'final_Y_full': 41.1, 'final_Y_crop': 43.8} | PASS |
| P3 grid cropped flattery (raider) | mean E_crop > mean E_full and mean Y_crop > mean Y_full | E_crop 99.9 vs E_full 77.9; Y_crop 57.3 vs Y_full 53.0 | PASS |
| P4 Commons Harvest (5 seeds) | restrained stock>0, Y>0; greedy/moderate/mixed stock=0, Y=0 | greedy: stock 0.00, Y_resource 0.00; moderate: stock 0.00, Y_resource 0.00; restrained: stock 96.20, Y_resource 56.47; mixed: stock 0.00, Y_resource 0.00 | PASS |
| P5 Clean Up (5 seeds) | freeloaders stock=0, clean=0; moderate stock and Y_stock > cleaners | all_cleaners: stock 3.60, clean 82.40, Y_stock 6.36; all_freeloaders: stock 0.00, clean 0.00, Y_stock 0.00; mixed: stock 3.60, clean 80.00, Y_stock 6.12; all_moderate: stock 48.20, clean 92.00, Y_stock 28.39 | PASS |
| P6 full reporting row counts | 80 data rows in each CSV | results.csv: 80 data rows + header; results_cleanup.csv: 80 data rows + header | PASS |

If any criterion is FAIL, the reproduction is FAILED. Do not change a threshold after seeing a failure; see PREREGISTRATION.md failure rule.

