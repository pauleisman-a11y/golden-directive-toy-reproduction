"""Check PREREGISTRATION.md P1-P7 and write CHECK_RESULTS.md.

Usage: python3 check_preregistration.py
Reads no Drive files. Runs grid and commons code from this repo,
compares to PREREGISTRATION.md, and writes a full per-criterion
table. If any criterion fails, the overall verdict is FAILED.
"""

from __future__ import annotations

import csv
import statistics
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "grid"))
sys.path.insert(0, str(HERE / "commons"))

import cleanup_demo  # noqa: E402
import golden_demo  # noqa: E402
import golden_directive  # noqa: E402

SEEDS = [42, 43, 44, 45, 46]
results = []  # (criterion, expected, observed, verdict)


def check(name: str, expected: str, observed: str, ok: bool) -> None:
    results.append((name, expected, observed, "PASS" if ok else "FAIL"))


def mean(xs):
    return statistics.mean(xs)


def stdev(xs):
    return statistics.stdev(xs) if len(xs) > 1 else 0.0


def main() -> None:
    # P1 + P7: unit tests in commons/
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "-v"],
        cwd=HERE / "commons",
        capture_output=True,
        text=True,
    )
    tail = (proc.stderr + proc.stdout).strip().splitlines()[-1] if (proc.stderr + proc.stdout).strip() else ""
    check("P1 unit tests", "8 tests, OK", tail, proc.returncode == 0 and "OK" in tail)

    # P7 direct Y properties (also covered by unit tests)
    y = golden_directive.harmonic_mean
    try:
        y(-1, 10)
        neg_ok = False
    except ValueError:
        neg_ok = True
    check(
        "P7 Y properties",
        "Y(0,10)=0; Y(7,7)=7; 30<Y(30,70)<70; negative raises",
        f"Y(0,10)={y(0,10)}; Y(7,7)={y(7,7)}; Y(30,70)={y(30,70)}; negative raises={neg_ok}",
        y(0, 10) == 0 and y(7, 7) == 7 and 30 < y(30, 70) < 70 and neg_ok,
    )

    # P2 + P3: grid
    expected_grid = {
        "tender": {"tends": 71, "eaten": 71, "mean_A": 69.3, "mean_E_full": 98.3,
                   "mean_E_crop": 95.1, "mean_Y_full": 80.8, "mean_Y_crop": 79.7,
                   "final_stock": 39, "final_A": 87.5, "final_E_full": 97.5,
                   "final_E_crop": 90.0, "final_Y_full": 92.2, "final_Y_crop": 88.7},
        "raider": {"tends": 2, "eaten": 54, "mean_A": 40.6, "mean_E_full": 77.9,
                   "mean_E_crop": 99.9, "mean_Y_full": 53.0, "mean_Y_crop": 57.3,
                   "final_stock": 31, "final_A": 28.0, "final_E_full": 77.5,
                   "final_E_crop": 100.0, "final_Y_full": 41.1, "final_Y_crop": 43.8},
    }
    grid_ok = True
    grid_obs = []
    for policy in ("tender", "raider"):
        rows, env = golden_demo.run_policy(policy)
        n = len(rows)
        m = lambda i: sum(r[i] for r in rows) / n
        obs = {
            "tends": env.tends, "eaten": env.eaten, "mean_A": round(m(0), 1),
            "mean_E_full": round(m(1), 1), "mean_E_crop": round(m(2), 1),
            "mean_Y_full": round(m(3), 1), "mean_Y_crop": round(m(4), 1),
            "final_stock": sum(env.stock.values()), "final_A": round(rows[-1][0], 1),
            "final_E_full": round(rows[-1][1], 1), "final_E_crop": round(rows[-1][2], 1),
            "final_Y_full": round(rows[-1][3], 1), "final_Y_crop": round(rows[-1][4], 1),
        }
        grid_obs.append(f"{policy}: {obs}")
        if obs != expected_grid[policy]:
            grid_ok = False
    check("P2 grid exact outputs", "tender + raider match stated outputs to 1 decimal", "; ".join(grid_obs), grid_ok)

    # P3 from the same runs
    rows_r, _ = golden_demo.run_policy("raider")
    n = len(rows_r)
    e_full = sum(r[1] for r in rows_r) / n
    e_crop = sum(r[2] for r in rows_r) / n
    y_full = sum(r[3] for r in rows_r) / n
    y_crop = sum(r[4] for r in rows_r) / n
    check("P3 grid cropped flattery (raider)",
          "mean E_crop > mean E_full and mean Y_crop > mean Y_full",
          f"E_crop {e_crop:.1f} vs E_full {e_full:.1f}; Y_crop {y_crop:.1f} vs Y_full {y_full:.1f}",
          e_crop > e_full and y_crop > y_full)

    # P4: Commons Harvest
    harvest = {}
    for policy in golden_directive.POLICIES:
        per_seed_stock, per_seed_y = [], []
        for seed in SEEDS:
            r = golden_directive.run_episode(policy, seed)
            per_seed_stock.append(r["final_stock"])
            per_seed_y.append(mean([a["Y_resource"] for a in r["agents"]]))
        harvest[policy] = (mean(per_seed_stock), mean(per_seed_y))
    p4_ok = (
        harvest["restrained"][0] > 0 and harvest["restrained"][1] > 0
        and harvest["greedy"][0] == 0 and harvest["greedy"][1] == 0
        and harvest["moderate"][0] == 0 and harvest["moderate"][1] == 0
        and harvest["mixed"][0] == 0 and harvest["mixed"][1] == 0
    )
    check("P4 Commons Harvest (5 seeds)",
          "restrained stock>0, Y>0; greedy/moderate/mixed stock=0, Y=0",
          "; ".join(f"{k}: stock {v[0]:.2f}, Y_resource {v[1]:.2f}" for k, v in harvest.items()),
          p4_ok)

    # P5: Clean Up
    cleanup = {}
    for policy in cleanup_demo.POLICIES_CLEANUP:
        per_seed_stock, per_seed_clean, per_seed_y = [], [], []
        for seed in SEEDS:
            r = cleanup_demo.run_cleanup_episode(policy, seed)
            per_seed_stock.append(r["final_stock"])
            per_seed_clean.append(r["final_cleanliness"])
            per_seed_y.append(mean([a["Y_stock"] for a in r["agents"]]))
        cleanup[policy] = (mean(per_seed_stock), mean(per_seed_clean), mean(per_seed_y))
    p5_ok = (
        cleanup["all_freeloaders"][0] == 0 and cleanup["all_freeloaders"][1] == 0
        and cleanup["all_moderate"][0] > cleanup["all_cleaners"][0]
        and cleanup["all_moderate"][2] > cleanup["all_cleaners"][2]
    )
    check("P5 Clean Up (5 seeds)",
          "freeloaders stock=0, clean=0; moderate stock and Y_stock > cleaners",
          "; ".join(f"{k}: stock {v[0]:.2f}, clean {v[1]:.2f}, Y_stock {v[2]:.2f}" for k, v in cleanup.items()),
          p5_ok)

    # P6: full reporting row counts
    p6_ok = True
    p6_obs = []
    for fname in ("results.csv", "results_cleanup.csv"):
        with open(HERE / "commons" / fname, newline="") as f:
            rows = list(csv.reader(f))
        p6_obs.append(f"{fname}: {len(rows)-1} data rows + header")
        if len(rows) - 1 != 80:
            p6_ok = False
    check("P6 full reporting row counts", "80 data rows in each CSV", "; ".join(p6_obs), p6_ok)

    overall = "PASS" if all(v == "PASS" for _, _, _, v in results) else "FAILED"
    lines = ["# Pre-registration check results", "",
             f"Overall reproduction verdict: **{overall}**", "",
             "| Criterion | Expected | Observed | Verdict |",
             "|---|---|---|---|"]
    for name, exp, obs, verdict in results:
        lines.append(f"| {name} | {exp} | {obs} | {verdict} |")
    lines += ["", "If any criterion is FAIL, the reproduction is FAILED. "
              "Do not change a threshold after seeing a failure; see "
              "PREREGISTRATION.md failure rule.", ""]
    (HERE / "CHECK_RESULTS.md").write_text("\n".join(lines) + "\n")
    print(f"Overall: {overall}")
    for name, _, _, verdict in results:
        print(f"  {name}: {verdict}")


if __name__ == "__main__":
    main()
